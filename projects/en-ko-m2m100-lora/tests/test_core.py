import csv
import contextlib
import io
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from cpu_app import CPUTranslator
from editable_app import validate_checkpoint

ROOT=Path(__file__).resolve().parents[1]

class CoreTests(unittest.TestCase):
    def test_tiny_synthetic_training_cli(self):
        """Random tiny model, five invented pairs, CPU only; no downloads."""
        import torch
        import train_extended
        import transformers
        from transformers import M2M100Config, M2M100ForConditionalGeneration
        torch.set_num_threads(1)

        class ToyTokenizer:
            pad_token_id = 0
            def __call__(self, texts=None, *, text_target=None, truncation=False,
                         padding=False, max_length=None, return_tensors=None):
                values = text_target if text_target is not None else texts
                if isinstance(values, str): values = [values]
                sequences = [[1] + [4 + ord(c) % 24 for c in text] + [2] for text in values]
                if truncation: sequences = [s[:max_length] for s in sequences]
                if return_tensors is None: return {"input_ids": sequences}
                width = max(map(len, sequences))
                ids = torch.tensor([s + [0] * (width-len(s)) for s in sequences])
                return {"input_ids": ids, "attention_mask": ids.ne(0).long()}
            def save_pretrained(self, path):
                (Path(path)/"toy_tokenizer.json").write_text("{}", encoding="utf-8")

        with tempfile.TemporaryDirectory() as d:
            root = Path(d); data = root/"data"; data.mkdir(); run=root/"run"
            for name, texts in [("train", ["aa", "ab", "ac", "ad", "ae"]),
                                ("validation", ["ba"]), ("test", ["ca"])]:
                with (data/f"{name}.tsv").open("w", encoding="utf-8", newline="") as f:
                    writer=csv.DictWriter(f,fieldnames=["source", "target"],delimiter="\t")
                    writer.writeheader(); writer.writerows({"source":t,"target":"합성"+t} for t in texts)
            (data/"split_manifest.json").write_text('{"normalized_overlap": {}}',encoding="utf-8")
            config=json.loads((ROOT/"configs/train.json").read_text(encoding="utf-8"))
            config.update(require_cuda=False, epochs=1, batch_size=2, grad_accum=2,
                          max_length=16, lora_rank=2, lora_alpha=4)
            config_path=root/"config.json"; config_path.write_text(json.dumps(config),encoding="utf-8")
            tiny=M2M100ForConditionalGeneration(M2M100Config(vocab_size=32,d_model=16,
                encoder_layers=1,decoder_layers=1,encoder_attention_heads=2,decoder_attention_heads=2,
                encoder_ffn_dim=32,decoder_ffn_dim=32,max_position_embeddings=32,
                encoder_layerdrop=0.0,decoder_layerdrop=0.0,
                pad_token_id=0,bos_token_id=1,eos_token_id=2,decoder_start_token_id=2))
            argv=["train_extended.py","--config",str(config_path),"--data-dir",str(data),"--run-dir",str(run)]
            with patch.object(sys,"argv",argv), patch("torch.cuda.is_available",return_value=False), \
                 patch.object(transformers.AutoTokenizer,"from_pretrained",return_value=ToyTokenizer()), \
                 patch.object(transformers.AutoModelForSeq2SeqLM,"from_pretrained",return_value=tiny), \
                 contextlib.redirect_stdout(io.StringIO()):
                train_extended.main()
            experiment=json.loads((run/"experiment.json").read_text(encoding="utf-8"))
            history=json.loads((run/"history.json").read_text(encoding="utf-8"))
            self.assertEqual(experiment["status"],"completed")
            self.assertEqual(history[0]["optimizer_windows"],2)
            self.assertEqual(experiment["best_epoch"],1)
            self.assertTrue((run/"adapter/adapter_model.safetensors").is_file())
            self.assertTrue((run/"loss.png").is_file())

    def test_missing_training_data_before_heavy_imports(self):
        import train_extended
        with tempfile.TemporaryDirectory() as d:
            with patch.object(sys, "argv", ["train_extended.py", "--data-dir", d]):
                with self.assertRaises(FileNotFoundError): train_extended.main()

    def test_training_import_does_not_load_models(self):
        code="import sys; import train_extended; assert 'torch' not in sys.modules; assert 'transformers' not in sys.modules"
        result=subprocess.run([sys.executable,"-c",code],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_missing_adapter_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError): validate_checkpoint(Path(d))
            with self.assertRaises(FileNotFoundError): CPUTranslator(Path(d),"unused").load()

    def test_input_rejected_before_tokenization(self):
        translator=CPUTranslator(Path("unused"),"unused")
        for text in ["", " ", "x"*6001]:
            with self.assertRaises(ValueError): translator.translate(text)

    def test_group_split_blocks_text_and_id_overlap(self):
        from prepare_grouped_split import normalize
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"source"; dest=Path(d)/"grouped"; source.mkdir()
            rows=[{"source_id":str(i),"target_id":str(i+1000),"source":f"synthetic source {i}","target":f"합성 문자열 {i}"} for i in range(40)]
            rows += [{"source_id":"same-text","target_id":"new-id","source":"SYNTHETIC SOURCE 0", "target":"합성 연결"}, {"source_id":"0","target_id":"new-id-2","source":"synthetic id connection", "target":"합성 다른 연결"}]
            for name,part in [("train",rows[:30]),("validation",rows[30:36]),("test",rows[36:])]:
                with (source/f"{name}.tsv").open("w",encoding="utf-8",newline="") as f:
                    writer=csv.DictWriter(f,fieldnames=["source_id","target_id","source","target"],delimiter="\t")
                    writer.writeheader(); writer.writerows(part)
            cmd=[sys.executable,"prepare_grouped_split.py","--source",str(source),"--dest",str(dest)]
            result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,encoding="utf-8")
            self.assertEqual(result.returncode,0,result.stderr)
            manifest=json.loads((dest/"split_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["total"],42)
            self.assertFalse(any(manifest["normalized_overlap"].values()))
            self.assertEqual(subprocess.run(cmd,cwd=ROOT,capture_output=True).returncode,1)
            seen={}
            for name in ("train","validation","test"):
                with (dest/f"{name}.tsv").open(encoding="utf-8",newline="") as f:
                    for row in csv.DictReader(f,delimiter="\t"):
                        for kind in ("source","target","source_id","target_id"):
                            value=normalize(row[kind]) if kind in ("source","target") else row[kind]
                            key=(kind,value)
                            self.assertIn(seen.setdefault(key,name),(name,))

if __name__ == "__main__": unittest.main()
