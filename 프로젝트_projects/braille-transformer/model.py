"""점자 → 한국어: 사전 학습 가중치 없이 시작하는 작은 Transformer.

이 파일을 먼저 읽으세요. `train.py`는 아래 모델의 숫자(가중치)를 실제로
수정하고, `inference.py`는 저장된 숫자를 불러와 다음 글자를 하나씩 예측합니다.
TensorFlow는 필요 없습니다. PyTorch 하나가 미분, GPU 계산, 저장을 담당합니다.

초보자용 기호 사전
------------------
B: 한 번에 처리하는 문장 수(batch), S: 점자 길이, T: 출력 자모 길이,
D: 한 토큰을 표현하는 벡터의 차원(d_model), V: 출력 어휘 수입니다.
문자열 → 정수 토큰 [B,S] → 실수 embedding [B,S,D] → Transformer 순서입니다.
embedding은 사전의 뜻을 넣은 표가 아니라 학습으로 바뀌는 숫자 표입니다.

한글 '각'을 NFD 정규화하면 초성 ᄀ + 중성 ᅡ + 종성 ᆨ입니다. 호환 자모
'ㄱㅏㄱ'와는 다른 Unicode 코드입니다. 이렇게 하면 학습에서 못 본 음절도
이미 본 자모를 조합해 만들 수 있습니다. 마지막에 NFC로 다시 '각'을 만듭니다.
이것은 한글 점자 규칙을 하드코딩한 변환기가 아니라 말뭉치로 학습하는 모델입니다.
정확한 규칙 변환이 항상 보장되는 것은 아니므로 실제 오류 평가가 필요합니다.

원리 자료: https://arxiv.org/abs/1706.03762 (Attention Is All You Need)
https://docs.pytorch.org/docs/stable/generated/torch.nn.Transformer.html
https://unicode.org/reports/tr15/ (Unicode 정규화)
"""
from __future__ import annotations

import hashlib
import json
import math
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import torch
from torch import Tensor, nn
from torch.utils.data import Dataset

PAD, BOS, EOS, UNK = 0, 1, 2, 3
SPECIAL = ["<pad>", "<bos>", "<eos>", "<unk>"]


def sha256_file(path: str | Path) -> str:
    """파일의 내용을 대표하는 SHA-256. 이름이 같아도 내용 변경을 찾습니다."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: str | Path) -> list[dict]:
    """JSONL = 한 줄에 JSON 객체 하나. 원문 공백을 strip하지 않습니다."""
    rows = []
    with Path(path).open(encoding="utf-8-sig") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row.get("braille"), str) or not isinstance(row.get("korean"), str):
                raise ValueError(f"{path}:{line_no}: braille, korean 문자열 필드가 필요합니다.")
            if not row["braille"] or not row["korean"]:
                raise ValueError(f"{path}:{line_no}: 빈 문장은 학습할 수 없습니다.")
            rows.append(row)
    if not rows:
        raise ValueError(f"빈 데이터 파일: {path}")
    return rows


class Vocabulary:
    """문자 ↔ 정수 대응표. 반드시 train split에서만 만들고 그대로 저장합니다.

    validation/test까지 보고 사전을 만들면 시험 데이터의 정보를 미리 본 셈입니다.
    모르는 문자는 UNK가 됩니다. UNK 비율도 모델의 적용 범위를 보여주는 지표입니다.
    PAD는 길이를 맞추기 위한 자리이고 정답 글자가 아닙니다. BOS는 출력 시작,
    EOS는 출력 끝입니다. 띄어쓰기 ' ' 역시 의미가 있는 일반 문자 토큰입니다.
    """
    def __init__(self, source_tokens: list[str], target_tokens: list[str]):
        if source_tokens[:4] != SPECIAL or target_tokens[:4] != SPECIAL:
            raise ValueError("특수 토큰 순서는 PAD/BOS/EOS/UNK = 0/1/2/3이어야 합니다.")
        if len(source_tokens) != len(set(source_tokens)) or len(target_tokens) != len(set(target_tokens)):
            raise ValueError("어휘에 중복 토큰이 있습니다.")
        self.source_tokens = source_tokens
        self.target_tokens = target_tokens
        self.source_to_id = {char: index for index, char in enumerate(source_tokens)}
        self.target_to_id = {char: index for index, char in enumerate(target_tokens)}

    @classmethod
    def from_training_rows(cls, rows: Iterable[dict]) -> "Vocabulary":
        source, target = set(), set()
        for row in rows:
            source.update(row["braille"])
            target.update(unicodedata.normalize("NFD", row["korean"]))
        return cls(SPECIAL + sorted(source), SPECIAL + sorted(target))

    def encode_source(self, text: str) -> list[int]:
        return [BOS] + [self.source_to_id.get(char, UNK) for char in text] + [EOS]

    def encode_target(self, text: str) -> list[int]:
        return [BOS] + [self.target_to_id.get(char, UNK) for char in unicodedata.normalize("NFD", text)] + [EOS]

    def decode_target(self, ids: Iterable[int]) -> str:
        chars = []
        for token in ids:
            token = int(token)
            if token == EOS:
                break
            if token in (PAD, BOS):
                continue
            # UNK를 조용히 지우지 않습니다. 대체 문자 �가 보이고 경고가 기록됩니다.
            chars.append("\ufffd" if token == UNK else self.target_tokens[token])
        return unicodedata.normalize("NFC", "".join(chars))

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps({"format_version": 1,
            "target_normalization": "NFD", "decoded_normalization": "NFC",
            "special_tokens": {"pad": PAD, "bos": BOS, "eos": EOS, "unk": UNK},
            "source_tokens": self.source_tokens, "target_tokens": self.target_tokens},
            ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "Vocabulary":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if data.get("target_normalization") != "NFD":
            raise ValueError("이 코드는 NFD target 어휘만 지원합니다.")
        return cls(data["source_tokens"], data["target_tokens"])


@dataclass
class ModelConfig:
    source_vocab_size: int
    target_vocab_size: int
    d_model: int = 256
    heads: int = 8
    encoder_layers: int = 3
    decoder_layers: int = 3
    ffn_dim: int = 1024
    dropout: float = 0.1
    max_source_length: int = 560
    max_target_length: int = 560

    def to_dict(self) -> dict:
        return asdict(self)


class SinusoidalPosition(nn.Module):
    """문자 순서 신호. sin/cos 표는 학습 가중치가 아니라 고정된 공식입니다.

    attention만으로는 순서를 알 수 없으므로 embedding에 위치 벡터를 더합니다.
    position과 embedding의 shape는 각각 [1,L,D], [B,L,D]입니다.
    broadcasting은 앞의 1차원 표를 B개 문장에 동일하게 적용하는 기능입니다.
    """
    def __init__(self, d_model: int, max_length: int, dropout: float):
        super().__init__()
        if d_model % 2:
            raise ValueError("이 위치 인코딩은 짝수 d_model을 사용합니다.")
        position = torch.arange(max_length, dtype=torch.float32).unsqueeze(1)
        frequency = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        table = torch.zeros(max_length, d_model)
        table[:, 0::2] = torch.sin(position * frequency)
        table[:, 1::2] = torch.cos(position * frequency)
        self.register_buffer("table", table.unsqueeze(0), persistent=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: Tensor) -> Tensor:
        if x.size(1) > self.table.size(1):
            raise ValueError("위치 인코딩 범위를 넘었습니다. 입력을 자르지 않고 중단합니다.")
        return self.dropout(x + self.table[:, :x.size(1)].to(dtype=x.dtype))


class BrailleTransformer(nn.Module):
    """Encoder가 점자를 읽고 Decoder가 한국어 자모를 생성합니다.

    Q(query: 찾는 정보), K(key: 비교할 특징), V(value: 가져올 정보)는 입력을
    각각 학습되는 선형변환에 통과시킨 벡터입니다. attention(Q,K,V)는
    softmax(QKᵀ/sqrt(d_head))V이며 관련 위치에 더 큰 가중치를 둡니다.
    Encoder self-attention: Q/K/V 모두 점자.
    Decoder self-attention: Q/K/V 모두 지금까지의 한국어 정답/생성 접두사.
    Decoder cross-attention: Q는 한국어, K/V는 encoder의 점자 표현입니다.
    causal mask는 decoder가 미래 정답을 훔쳐보는 것을 막습니다.
    padding mask는 문장 길이를 맞춘 PAD 자리의 영향을 막습니다.
    head 8개는 서로 다른 관계를 동시에 배울 수 있는 8개 attention 공간입니다.

    이 모델은 전체 가중치를 처음부터 학습합니다. LoRA나 외부 언어모델을 쓰지
    않습니다. 소규모 말뭉치에서 일반 한국어 지식까지 자동으로 보장되지는 않습니다.
    """
    def __init__(self, config: ModelConfig):
        super().__init__()
        if config.d_model % config.heads:
            raise ValueError("d_model은 heads로 나누어떨어져야 합니다.")
        self.config = config
        self.source_embedding = nn.Embedding(config.source_vocab_size, config.d_model, padding_idx=PAD)
        self.target_embedding = nn.Embedding(config.target_vocab_size, config.d_model, padding_idx=PAD)
        self.position = SinusoidalPosition(config.d_model,
            max(config.max_source_length, config.max_target_length) + 1, config.dropout)
        encoder_layer = nn.TransformerEncoderLayer(config.d_model, config.heads,
            config.ffn_dim, config.dropout, activation="gelu", batch_first=True, norm_first=True)
        decoder_layer = nn.TransformerDecoderLayer(config.d_model, config.heads,
            config.ffn_dim, config.dropout, activation="gelu", batch_first=True, norm_first=True)
        self.encoder = nn.TransformerEncoder(encoder_layer, config.encoder_layers,
            norm=nn.LayerNorm(config.d_model), enable_nested_tensor=False)
        self.decoder = nn.TransformerDecoder(decoder_layer, config.decoder_layers,
            norm=nn.LayerNorm(config.d_model))
        self.output_projection = nn.Linear(config.d_model, config.target_vocab_size)
        # Transformer clones initially have equal values; independent Xavier draws below
        # give each layer its own starting point while keeping seed reproducibility.
        for parameter in self.parameters():
            if parameter.dim() > 1:
                nn.init.xavier_uniform_(parameter)
        with torch.no_grad():
            self.source_embedding.weight[PAD].zero_()
            self.target_embedding.weight[PAD].zero_()

    def encode(self, source: Tensor) -> tuple[Tensor, Tensor]:
        source_padding = source.eq(PAD)
        x = self.position(self.source_embedding(source) * math.sqrt(self.config.d_model))
        return self.encoder(x, src_key_padding_mask=source_padding), source_padding

    def decode(self, target_prefix: Tensor, memory: Tensor, source_padding: Tensor) -> Tensor:
        length = target_prefix.size(1)
        causal = torch.ones(length, length, dtype=torch.bool, device=target_prefix.device).triu(1)
        y = self.position(self.target_embedding(target_prefix) * math.sqrt(self.config.d_model))
        hidden = self.decoder(y, memory, tgt_mask=causal,
            tgt_key_padding_mask=target_prefix.eq(PAD), memory_key_padding_mask=source_padding)
        return self.output_projection(hidden)

    def forward(self, source: Tensor, target_prefix: Tensor) -> Tensor:
        memory, source_padding = self.encode(source)
        return self.decode(target_prefix, memory, source_padding)


class PairDataset(Dataset):
    """문장을 한 번만 토큰화해 CPU RAM에 저장합니다. GPU에는 batch만 보냅니다."""
    def __init__(self, rows: list[dict], vocab: Vocabulary, max_source: int,
                 max_target: int, length_policy: str = "error"):
        self.items = []
        self.stats = {"input_rows": len(rows), "kept_rows": 0, "excluded_rows": 0,
            "too_long_source": 0, "too_long_target": 0, "source_tokens": 0,
            "target_tokens": 0, "unknown_source_tokens": 0, "unknown_target_tokens": 0,
            "max_source_observed": 0, "max_target_observed": 0,
            "excluded_ids": []}
        for index, row in enumerate(rows):
            source, target = vocab.encode_source(row["braille"]), vocab.encode_target(row["korean"])
            self.stats["max_source_observed"] = max(self.stats["max_source_observed"], len(source))
            self.stats["max_target_observed"] = max(self.stats["max_target_observed"], len(target))
            long_source, long_target = len(source) > max_source, len(target) > max_target
            if long_source or long_target:
                self.stats["excluded_rows"] += 1
                self.stats["too_long_source"] += int(long_source)
                self.stats["too_long_target"] += int(long_target)
                self.stats["excluded_ids"].append(str(row.get("id", index)))
                continue
            self.items.append({"source": source, "target": target, "row": row, "index": index})
            self.stats["source_tokens"] += len(source) - 2
            self.stats["target_tokens"] += len(target) - 2
            self.stats["unknown_source_tokens"] += source.count(UNK)
            self.stats["unknown_target_tokens"] += target.count(UNK)
        self.stats["kept_rows"] = len(self.items)
        if self.stats["excluded_rows"] and length_policy != "filter":
            raise ValueError("길이 제한을 넘었습니다. 기본 정책은 자르지 않고 중단합니다. "
                "길이를 늘리거나 --length-policy filter로 제외를 명시하세요. " + json.dumps(self.stats, ensure_ascii=False))
        if not self.items:
            raise ValueError("사용할 문장이 없습니다.")

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> dict:
        return self.items[index]


def collate_pairs(items: list[dict]) -> dict:
    """Dynamic padding: 전체 최대 길이 대신 이번 batch의 최대 길이에만 맞춥니다.

    label의 PAD는 loss에서 ignore_index=PAD로 무시합니다. HuggingFace의 -100과
    같은 목적이지만 이 순수 PyTorch 구현은 PAD=0을 명시적으로 제외합니다.
    """
    source = nn.utils.rnn.pad_sequence([torch.tensor(x["source"]) for x in items],
        batch_first=True, padding_value=PAD)
    target = nn.utils.rnn.pad_sequence([torch.tensor(x["target"]) for x in items],
        batch_first=True, padding_value=PAD)
    return {"source": source, "target": target, "indices": [x["index"] for x in items]}


@torch.inference_mode()
def greedy_generate(model: BrailleTransformer, source: Tensor, max_new_tokens: int) -> tuple[Tensor, Tensor]:
    """정답을 보지 않는 실제 추론. 한 batch에서 여러 문장을 동시에 생성합니다.

    teacher forcing 검증 loss와 다릅니다. 앞서 잘못 만든 글자도 다음 입력이
    되므로 실제 번역은 오류가 누적될 수 있습니다. EOS가 없으면 길이 한계에서
    멈춘 것이며 정상적으로 완료했다고 표시하지 않습니다.
    """
    if max_new_tokens < 1 or max_new_tokens > model.config.max_target_length - 1:
        raise ValueError("max_new_tokens는 1 .. max_target_length-1 범위여야 합니다.")
    memory, source_padding = model.encode(source)
    batch = source.size(0)
    prefix = torch.full((batch, 1), BOS, dtype=torch.long, device=source.device)
    finished = torch.zeros(batch, dtype=torch.bool, device=source.device)
    for _ in range(max_new_tokens):
        logits = model.decode(prefix, memory, source_padding)[:, -1, :]
        logits[:, PAD] = -torch.inf
        logits[:, BOS] = -torch.inf
        next_token = logits.argmax(dim=-1)
        next_token = torch.where(finished, torch.full_like(next_token, PAD), next_token)
        prefix = torch.cat([prefix, next_token.unsqueeze(1)], dim=1)
        finished |= next_token.eq(EOS)
        if bool(finished.all()):
            break
    return prefix[:, 1:], finished


def uncombined_jamo_count(text: str) -> int:
    """NFC 후 남은 자모 수. 유효한 Unicode지만 음절 조합 실패의 후보입니다.

    원래 고립 자모를 뜻한 정답일 수도 있어 이를 전부 '불법 문자'라고 하지는 않습니다.
    """
    return sum(0x1100 <= ord(c) <= 0x11FF or 0x3130 <= ord(c) <= 0x318F
        or 0xA960 <= ord(c) <= 0xA97F or 0xD7B0 <= ord(c) <= 0xD7FF for c in text)
