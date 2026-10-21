"""고정 extended Hamming(13,8) 교육용 SECDED 부호기와 복호기입니다."""
from dataclasses import dataclass  # 반환 필드를 이름으로 구분하는 자료형을 만듭니다.

DATA_POSITIONS = (3, 5, 6, 7, 9, 10, 11, 12)
PARITY_POSITIONS = (1, 2, 4, 8)
MUTATIONS = ("none", "omit-overall", "reject-overall-bit", "correct-double", "leak-double-data")


def checked_integer(value, maximum):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError("expected a bounded integer; bool is not accepted")


def encode(data: int, mutation: str = "none") -> int:
    checked_integer(data, 255)
    if mutation not in MUTATIONS:
        raise ValueError("unknown mutation")
    word = 0
    for bit, position in enumerate(DATA_POSITIONS):
        word |= ((data >> bit) & 1) << (position-1)  # 자료 bit를 1부터 세는 코드워드 위치에 둡니다.
    for parity in PARITY_POSITIONS:
        value = 0
        for position in range(1, 13):
            if position & parity:
                value ^= (word >> (position-1)) & 1
        word |= value << (parity-1)  # 각 검사 집합의 1 개수를 짝수로 맞춥니다.
    if mutation != "omit-overall":
        word |= (word.bit_count() & 1) << 12  # 위치13은 전체 13비트의 짝수 parity를 만듭니다.
    return word


def extract_data(word: int) -> int:
    data = 0
    for bit, position in enumerate(DATA_POSITIONS):
        data |= ((word >> (position-1)) & 1) << bit
    return data


@dataclass(frozen=True)
class Decoded:
    status: str
    data: int | None
    corrected_word: int | None
    corrected_position: int | None
    syndrome: int
    overall_bad: bool


def decode(word: int, mutation: str = "none") -> Decoded:
    checked_integer(word, 8191)
    if mutation not in MUTATIONS:
        raise ValueError("unknown mutation")
    syndrome = 0
    for position in range(1, 13):
        if (word >> (position-1)) & 1:
            syndrome ^= position  # 켜진 위치 번호의 XOR가 네 Hamming 검사 결과를 묶습니다.
    overall_bad = bool(word.bit_count() & 1)
    if syndrome == 0 and not overall_bad:
        return Decoded("clean", extract_data(word), word, None, syndrome, overall_bad)
    if overall_bad and syndrome <= 12:
        # syndrome=0이어도 전체 parity가 홀수이면 위치13의 단일 오류로 처리합니다.
        if syndrome == 0 and mutation == "reject-overall-bit":
            return Decoded("uncorrectable", None, None, None, syndrome, overall_bad)
        position = syndrome if syndrome else 13
        corrected = word ^ (1 << (position-1))
        return Decoded("corrected", extract_data(corrected), corrected, position, syndrome, overall_bad)
    if mutation == "correct-double" and 1 <= syndrome <= 12:
        corrected = word ^ (1 << (syndrome-1))  # 의도한 결함: 짝수 parity의 이중 오류까지 고칩니다.
        return Decoded("corrected", extract_data(corrected), corrected, syndrome, syndrome, overall_bad)
    data = extract_data(word) if mutation == "leak-double-data" else None
    return Decoded("uncorrectable", data, None, None, syndrome, overall_bad)
