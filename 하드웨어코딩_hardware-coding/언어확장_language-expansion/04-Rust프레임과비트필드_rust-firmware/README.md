# Rust 비트필드와 빌린 프레임의 경계 검사

[하드웨어 코딩 목차](../../README.md)

32비트 값의 일부만 바꾸는 비트필드와, 바이트 배열에서 payload를 복사 없이 빌려 읽는 프레임 파서입니다. lib.rs는 core만 사용하는 no_std 라이브러리로 컴파일하고, tests.rs는 표준 라이브러리의 테스트 실행기로 실제 호스트에서 실행합니다. 펌웨어에서 사용할 수 있는 값 처리 예제이며 MCU·주변장치 레지스터에 접근한 실행 기록은 아닙니다.

## 라이브러리와 호스트 테스트의 구분

#![no_std]는 std의 자동 연결과 기본 prelude를 바꾸며 core 기반 코드를 작성하도록 합니다. 그 자체로 특정 보드에서 실행되거나 하드웨어 회로로 합성된다는 뜻은 아닙니다. 이 라이브러리는 Vec·파일·네트워크·할당을 사용하지 않습니다. [Rust Reference의 no_std 설명](https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute)이 언어 동작의 근거입니다.

tests.rs는 Vec·println!과 libtest를 사용합니다. 따라서 테스트 실행 파일은 no_std 프로그램이 아닙니다. [rustc --test 설명](https://doc.rust-lang.org/rustc/tests/index.html)에 따라 생성된 호스트 테스트 실행기가 no_std 라이브러리 함수를 호출합니다. 이 두 컴파일 단계와 실행 결과는 [example.json](example.json)에 따로 기록합니다.

## Field의 범위와 갱신

Field::new는 폭 0을 Empty로 거절하고, width>32·shift≥32·shift+width>32를 OutsideWord로 거절합니다. 두 u8의 합은 먼저 u16으로 넓혀 255+255도 중간 오버플로 없이 확인합니다. 필드의 두 멤버는 비공개이므로 외부의 일반적인 안전 Rust 코드는 생성자 검사를 건너뛴 명세를 직접 만들 수 없습니다.

낮은 비트의 마스크는 u32::MAX >> (32-width)입니다. width=32이면 0비트 이동이며 shift=0만 허용합니다. shift=31은 width=1일 때만 가능하므로 모든 실제 이동 수가 0~31 안에 있습니다. u32를 32칸 이동하지 않는 것이 핵심입니다. [Rust의 shift overflow 조건](https://doc.rust-lang.org/reference/expressions/operator-expr.html#overflow)은 피연산자 폭 이상의 이동 수를 오버플로로 다룹니다.

아래는 직접 계산한 추적 예입니다. 고정 테스트의 전체 입력 목록을 대신하는 표는 아닙니다.

| 순서 | 입력과 중간값 | 결과 |
| --- | --- | --- |
| 읽기 | word=0x12345678, shift=8,width=4 | (word>>8)&0xf=0x6입니다. |
| 마스크 | value_mask=0xf, positioned=0xf00 | 바꿀 위치는 8~11번입니다. |
| 갱신 | value=0xa | 결과는 0x12345a78입니다. |
| 범위 초과 | value=0x10 | ValueTooWide로 거절합니다. |
| 마지막 비트 | shift=31,width=1,value=1,word=0 | 결과는 0x80000000입니다. |
| 전체 폭 | shift=0,width=32 | 마스크는 0xffffffff이며 이동 수는 0입니다. |

replace는 새 값의 범위를 확인한 뒤 필드 자리만 지우고 새 값을 넣습니다. 단순 RAM 값의 계산입니다. 이 연산을 그대로 MMIO의 read-modify-write로 해석하면 장치의 read side effect·write-one-to-clear·경쟁 조건을 놓칠 수 있습니다. volatile 접근·원자적 갱신·장치 엔디언 변환은 구현하거나 실행하지 않았습니다.

## 프레임 길이와 borrowing

프레임 형식은 tag 1바이트, length 1바이트, payload length바이트, XOR checksum 1바이트입니다. payload는 0~255바이트이며 전체 길이는 3~258바이트입니다. 파서는 최소 3바이트를 확인하고, end=2+length를 구한 뒤 실제 길이가 end+1인지 확인합니다. 잘린 입력과 불필요한 뒷부분은 코드의 길이 조건에서 거절합니다. 이 확인을 통과한 뒤에만 bytes[..end]·bytes[end]·bytes[2..end]를 사용합니다.

| 순서 | 예제 바이트 a5 02 00 25 82 | 의미 |
| --- | --- | --- |
| 1 | tag=a5,length=02 | payload가 2바이트라는 선언입니다. |
| 2 | end=4,실제 길이=5 | header 2+payload 2+checksum 1과 맞습니다. |
| 3 | a5 XOR 02=a7 | 헤더 두 바이트부터 누적합니다. |
| 4 | a7 XOR 00 XOR 25=82 | payload까지의 검사합입니다. |
| 5 | 마지막 바이트=82 | 일치하면 payload 00 25를 빌려 반환합니다. |

Frame<'a>의 payload는 &'a [u8]입니다. 입력 배열을 새로 복사하거나 소유권을 가져가지 않습니다. 반환값이 가리키는 메모리는 호출자가 계속 소유하며, Rust의 대여 규칙이 그 참조의 유효 기간을 제한합니다. [공식 borrowing 설명](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)은 소유권 이전과 참조의 차이를 설명합니다. 이 예제의 테스트는 내용뿐 아니라 원래 payload 시작 주소를 가리키는지도 확인합니다.

## XOR 검사합의 검출 범위

정상 프레임에서 한 비트만 바뀌면, 길이 바이트 변화는 길이 조건에서 거절되고 다른 위치의 한 비트 변화는 XOR 불일치로 거절됩니다. 하지만 같은 비트 열의 두 반전은 상쇄할 수 있습니다. 원래 a5 02 00 25 82에서 payload를 01 24로 바꾸면 두 바이트의 최하위 비트가 함께 바뀌어 XOR 값은 여전히 82입니다. payload를 25 00으로 바꾸는 순서 교환도 XOR 값을 바꾸지 않습니다.

이 두 반례는 한계를 설명하는 직접 계산 예이며 추가로 수행한 호스트 테스트 수에 포함하지 않습니다. 이 검사합은 CRC·암호학적 해시·인증 코드가 아닙니다. 노이즈 모델이나 공격 상황에 적절한 보호 수단을 대체한다고 해석하지 않습니다.

## 독립 테스트와 실제 집계

필드는 가능한 유효 shift·width 528조합을 사용합니다. 각 조합에서 원래 word 5개와 새 값 4개를 비교하며, 기대값은 같은 마스크 식이 아니라 각 비트를 하나씩 선택해 구성합니다. 갱신 결과 비교와 다시 읽기 두 assert가 21,120회입니다. 폭 32를 제외한 527조합의 값 초과 검사, 폭 0 검사 1회, 잘못된 구성 4회를 합해 21,652회입니다. 모든 u32 입력값을 전수 검사한 것은 아닙니다.

프레임은 태그 4개와 payload 길이 0·1·2·8·255의 20개 정상 프레임을 사용합니다. 검사합 기대값은 같은 XOR 루프가 아니라 각 비트의 1 개수 패리티로 만듭니다. 정상 결과·원본 주소 60회, 모든 잘린 길이 1,124회, 프레임 각 위치의 단일 비트 반전 8,992회, 오류 종류 3회로 10,179회입니다. 임의 payload의 모든 조합이나 모든 다중 비트 오류를 전수 검사한 기록은 아닙니다.

2026-10-26에 실제 rustc 1.99.1, edition 2024로 rlib와 테스트를 -D warnings 조건에서 컴파일했습니다. 두 컴파일의 종료 코드는 0이고 stdout·stderr가 비어 있습니다. 호스트 테스트는 아래 결과로 종료 코드 0을 반환했습니다.

```text
running 2 tests
test fields ... PASS fields checks=21652
ok
test frames ... PASS frames checks=10179
ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
```

총 31,831개 비교와 테스트 2개의 완료를 확인했습니다. 실행 전후 lib.rs·tests.rs 바이트 SHA는 최초 확정값과 같으며, 임시 복사본도 원본과 일치했습니다. MCU cross-target 빌드·플래시·MMIO 접근·DMA·인터럽트·보드 측정은 수행하지 않았습니다.

## 복잡도와 펌웨어 연결

Field의 읽기와 갱신은 고정 u32 연산이므로 시간·추가 공간 O(1)입니다. 프레임은 payload 길이 L에서 헤더와 payload를 한 번 검사하여 시간 O(L), 추가 공간 O(1)입니다. 입력 저장 공간은 호출자가 갖고 있으며, tests.rs의 Vec 할당은 호스트 테스트용입니다.

통신 수신 버퍼를 해석하거나 설정값의 비트 범위를 검사하는 순수 함수에 연결할 수 있습니다. 실제 수신기에서는 프레임 경계 탐색·부분 수신·버퍼 소유 기간·동시 접근을 별도로 설계해야 합니다. 이 함수는 완성된 프레임 하나를 입력받는 계약입니다.

## 실행기와 Windows GNU 링커

run.py의 --rustc는 PATH 또는 명시한 컴파일러를 사용합니다. --build-dir 아래에 새 고유 폴더를 만들며 기존 폴더를 삭제하지 않습니다. --out은 실행 보고서 JSON이며 example.json을 덮어쓰지 않습니다. 각 도구 명령은 60초 상한을 가지며 종료 코드, 실제 PASS 집계, 테스트 완료 행을 확인합니다.

이 Windows GNU 환경의 기본 GCC 링크에서는 한글 경로가 깨지는 문제가 있어 같은 Rust 배포의 rust-lld.exe를 직접 사용했습니다. --linker auto는 x86_64-pc-windows-gnu에서 배포 LLD와 -C linker-flavor=ld.lld, -C link-self-contained=yes를 선택합니다. 이 선택은 모든 운영체제에서 필요한 일반 규칙이 아니라 이번 호스트의 재현 설정입니다. [공식 codegen 옵션](https://doc.rust-lang.org/rustc/codegen-options/index.html#linker)이 링커 선택 플래그의 근거입니다.

다른 호스트의 auto와 명시한 --linker default는 해당 타깃 기본 링커를 유지합니다. 필요한 경우 --linker에 실행 파일 경로를 줄 수 있습니다. 이 예제에서 다른 호스트까지 실제 실행했다는 뜻은 아닙니다.

저장소 루트의 PowerShell에서 다음처럼 실행합니다. $rustc는 설치한 해당 호스트의 rustc.exe 경로입니다.

```powershell
$py = 'C:/path/to/python.exe'
$rustc = 'C:/path/to/rust/toolchain/bin/rustc.exe'
& $py -B '하드웨어코딩_hardware-coding/언어확장_language-expansion/04-Rust프레임과비트필드_rust-firmware/run.py' --rustc $rustc --linker auto --build-dir 'tmp/rust-firmware-example' --out 'tmp/rust-firmware-validation.json'
```

## 전체 소스와 줄별 메모

### lib.rs

```rust
#![no_std] // OS나 힙 없이 쓸 수 있는 core 기반 라이브러리
#[derive(Debug, Clone, Copy, PartialEq, Eq)] // 검사 결과를 비교하고 짧은 오류를 출력할 준비
pub enum FieldError { // 비트필드 구성과 갱신에서 생기는 오류
    Empty, // 폭이 0인 필드는 허용하지 않기
    OutsideWord, // 시작 위치와 폭이 32비트 밖으로 나간 경우
    ValueTooWide, // 새 값이 필드에 들어가지 않는 경우
} // 필드 오류 종류 끝
#[derive(Debug, Clone, Copy)] // 작은 필드 명세를 값으로 전달
pub struct Field { shift: u8, width: u8 } // 외부에서 무효한 조합을 직접 만들 수 없는 필드
impl Field { // 생성 때 확인한 범위를 나머지 메서드에서 사용
    pub const fn new(shift: u8, width: u8) -> Result<Self, FieldError> { // 실행 전 상수로도 구성 가능한 검사
        if width == 0 { return Err(FieldError::Empty); } // 빈 범위를 먼저 구분
        if width > 32 || shift >= 32 || shift as u16 + width as u16 > 32 { // 더 넓은 정수에서 위치와 폭을 더하기
            return Err(FieldError::OutsideWord); // 32 이상 이동하거나 단어 밖의 비트를 쓰지 않기
        } // 범위 검사 끝
        Ok(Self { shift, width }) // 유효한 조합만 보관
    } // 생성자 끝
    pub const fn value_mask(self) -> u32 { u32::MAX >> (32 - self.width) } // 폭 32도 0비트 이동으로 처리
    pub const fn read(self, word: u32) -> u32 { (word >> self.shift) & self.value_mask() } // 필드를 낮은 자리로 옮겨 읽기
    pub fn replace(self, word: u32, value: u32) -> Result<u32, FieldError> { // 바깥 비트는 보존하는 일반 RAM 값 갱신
        let mask = self.value_mask(); // 새 값이 사용할 낮은 비트 범위
        if value & !mask != 0 { return Err(FieldError::ValueTooWide); } // 잘리는 값을 조용히 받아들이지 않기
        let positioned = mask << self.shift; // 원래 단어 안에서 필드가 차지하는 자리
        Ok((word & !positioned) | (value << self.shift)) // 필드만 비우고 새 비트를 채우기
    } // 갱신 끝
} // 비트필드 구현 끝
#[derive(Debug, Clone, Copy, PartialEq, Eq)] // 파싱 실패 원인을 구분해 테스트
pub enum FrameError { TooShort, Length, Checksum } // 최소 길이·선언 길이·검사합의 오류
#[derive(Debug, PartialEq, Eq)] // 파싱 결과의 값과 내용을 비교
pub struct Frame<'a> { pub tag: u8, pub payload: &'a [u8] } // 원본 버퍼를 빌려 보는 페이로드
pub fn parse_frame(bytes: &[u8]) -> Result<Frame<'_>, FrameError> { // 입력보다 오래 살 수 없는 뷰 반환
    if bytes.len() < 3 { return Err(FrameError::TooShort); } // tag·length·checksum이 있어야 인덱싱 가능
    let end = 2 + bytes[1] as usize; // 한 바이트 길이 뒤의 페이로드 끝
    if bytes.len() != end + 1 { return Err(FrameError::Length); } // 잘린 프레임과 불필요한 뒷부분 모두 거절
    let mut checksum = 0u8; // 헤더와 데이터의 XOR 검사합 시작
    for &byte in &bytes[..end] { checksum ^= byte; } // 마지막 검사합 바이트는 누적에서 제외
    if checksum != bytes[end] { return Err(FrameError::Checksum); } // 값이 다르면 결과 뷰를 만들지 않기
    Ok(Frame { tag: bytes[0], payload: &bytes[2..end] }) // 복사나 할당 없이 입력의 일부를 빌려주기
} // 길이 확인 뒤에만 슬라이스를 만드는 파서 끝
```

### tests.rs

```rust
use firmware_fields::{parse_frame, Field, FieldError, FrameError}; // 실제 no_std 라이브러리의 공개 API 검사
fn reference_replace(word: u32, value: u32, shift: u8, width: u8) -> u32 { // 마스크 식 대신 각 자리의 비트로 기대값 구성
    let mut result = 0u32; // 기대 단어를 빈 비트에서 시작
    for bit in 0..32u8 { // 모든 원래 비트 위치 열거
        let selected = bit >= shift && (bit as u16) < shift as u16 + width as u16; // 이 자리가 필드 내부인지 판정
        let source = if selected { (value >> (bit - shift)) & 1 } else { (word >> bit) & 1 }; // 필드 안은 새 값, 밖은 원래 값
        result |= source << bit; // 기대 단어의 한 자리를 확정
    } // 32비트 참조 계산 끝
    result // 독립 비트별 기대값 반환
} // 참조 함수 끝
#[test] // Rust 테스트 러너가 실행할 경계와 값 검사
fn fields() { // 가능한 유효 위치·폭과 대표 원래 값 비교
    let mut checks = 0usize; // 실제 assert 실행 수 기록
    for shift in 0..32u8 { // 유효한 시작 비트 위치
        for width in 1..=32 - shift { // 단어 안에 들어가는 모든 폭
            let field = Field::new(shift, width).unwrap(); // 이 범위에서는 생성에 성공해야 함
            let max = u32::MAX >> (32 - width); // 테스트 입력으로 사용할 최댓값
            for word in [0, u32::MAX, 0x12345678, 0xaaaaaaaa, 0x55555555] { // 비어 있음·모두 1·비대칭 패턴
                for value in [0, 1, max / 2, max] { // 비우기·작은 값·중간 값·최댓값
                    let actual = field.replace(word, value).unwrap(); // 검사할 갱신 실행
                    assert_eq!(actual, reference_replace(word, value, shift, width)); // 필드 밖 비트까지 비교
                    assert_eq!(field.read(actual), value); // 저장한 값을 다시 읽기
                    checks += 2; // 독립 계산과 읽기 검사의 두 비교
                } // 대표 새 값 검사 끝
            } // 원래 패턴 검사 끝
            if width < 32 { // 폭 32에는 u32 범위 밖의 새 값을 만들 수 없음
                assert_eq!(field.replace(0, max + 1), Err(FieldError::ValueTooWide)); // 잘리는 새 값을 거절
                checks += 1; // 범위를 넘는 값 검사 집계
            } // 폭 경계 검사 끝
        } // 폭 열거 끝
    } // 위치 열거 끝
    assert_eq!(Field::new(0, 0).unwrap_err(), FieldError::Empty); // 폭 0 확인
    checks += 1; // 빈 필드 검사 집계
    for (shift, width) in [(32, 1), (31, 2), (0, 33), (255, 255)] { // 단어 끝과 정수 덧셈 경계
        assert_eq!(Field::new(shift, width).unwrap_err(), FieldError::OutsideWord); // 구성 자체를 거절
        checks += 1; // 잘못된 구성 집계
    } // 무효한 구성 검사 끝
    println!("PASS fields checks={checks}"); // 실행한 비교 수를 결과에 남기기
} // 비트필드 테스트 끝
fn make_frame(tag: u8, length: usize) -> Vec<u8> { // 테스트용 직렬 바이트 배열 생성
    let mut bytes = vec![tag, length as u8]; // 태그와 한 바이트 선언 길이
    for index in 0..length { bytes.push((index as u8).wrapping_mul(37)); } // 0과 상위 비트가 섞인 페이로드
    let mut checksum = 0u8; // 검사합의 독립 비트별 기준 시작
    for bit in 0..8 { // 각 비트의 패리티를 따로 구하기
        let ones = bytes.iter().filter(|byte| (**byte >> bit) & 1 == 1).count(); // 해당 비트의 1 개수
        checksum |= ((ones % 2) as u8) << bit; // 홀수 개일 때만 결과 비트를 켜기
    } // 검사합 계산 끝
    bytes.push(checksum); // 마지막 바이트에 검사합 배치
    bytes // 완성한 외부 입력 반환
} // 테스트 프레임 생성 끝
#[test] // 올바른 입력과 잘린 입력·비트 오류를 함께 검사
fn frames() { // 입력 버퍼를 빌리는 파서의 경계 검사
    let mut checks = 0usize; // 실제 비교 수 기록
    for tag in [0u8, 0x42, 0xa5, 0xff] { // 태그의 서로 다른 비트 패턴
        for length in [0usize, 1, 2, 8, 255] { // 빈 페이로드부터 최대 길이까지
            let bytes = make_frame(tag, length); // 독립 기준으로 프레임 구성
            let frame = parse_frame(&bytes).unwrap(); // 입력 길이와 검사합이 맞아야 성공
            assert_eq!(frame.tag, tag); // 태그 보존 확인
            assert_eq!(frame.payload, &bytes[2..2 + length]); // 페이로드 내용 확인
            assert_eq!(frame.payload.as_ptr(), bytes[2..].as_ptr()); // 원본을 가리키는 뷰인지 확인
            checks += 3; // 값 두 개와 빌린 주소 비교
            for cut in 0..bytes.len() { // 모든 잘린 길이 검사
                assert!(parse_frame(&bytes[..cut]).is_err()); // 잘린 입력을 유효 프레임으로 읽지 않기
                checks += 1; // 잘림 검사 집계
            } // 잘린 입력 검사 끝
            for index in 0..bytes.len() { // 프레임의 모든 위치에서 단일 비트 반전
                for bit in 0..8 { // 한 바이트 안의 모든 비트
                    let mut damaged = bytes.clone(); // 정상 원본은 다음 검사에 보존
                    damaged[index] ^= 1 << bit; // 한 비트만 바꾸기
                    assert!(parse_frame(&damaged).is_err()); // 길이 또는 검사합 오류로 거절
                    checks += 1; // 단일 비트 오류 검사 집계
                } // 비트 오류 열거 끝
            } // 모든 위치 검사 끝
        } // 페이로드 길이 검사 끝
    } // 태그 검사 끝
    assert_eq!(parse_frame(&[1, 0]), Err(FrameError::TooShort)); // 최소 크기 미달의 정확한 오류
    assert_eq!(parse_frame(&[1, 1, 1]), Err(FrameError::Length)); // 선언 길이 불일치의 정확한 오류
    assert_eq!(parse_frame(&[1, 0, 0]), Err(FrameError::Checksum)); // 검사합 불일치의 정확한 오류
    checks += 3; // 오류 종류 확인 집계
    println!("PASS frames checks={checks}"); // 파서 비교 수를 결과에 남기기
} // 바이트 프레임 테스트 끝
```

### run.py

```python
import argparse  # 컴파일러·링커·생성물 위치 선택
from datetime import datetime, timezone  # 실제 실행 시각 기록
import hashlib  # 게시 소스와 컴파일 입력의 바이트 대조
import json  # 명령과 결과를 기계 판독용으로 저장
from pathlib import Path  # 원본과 임시 작업 경로 분리
import re  # 실제 테스트 수와 비교 수 판정
import shutil  # 도구 검색과 동일 바이트 복사
import subprocess  # 실제 rustc와 호스트 테스트 실행
import tempfile  # 기존 폴더를 지우지 않는 새 빌드 공간

def sha(path):  # 파일 원본의 정확한 바이트 식별
    return hashlib.sha256(path.read_bytes()).hexdigest()  # 줄바꿈을 정규화하지 않고 계산

def execute(argv, work, records):  # 셸 없이 실행하고 실패 로그도 남기기
    record = {"command": [str(value) for value in argv], "cwd": str(work)}  # 재현할 인자 목록
    records.append(record)  # 실행 실패도 보고서에서 빠지지 않기
    try:  # 도구가 멈추거나 시작하지 못한 경우 구분
        process = subprocess.run(record["command"], cwd=work, capture_output=True, timeout=60, check=False)  # 명령별 60초 상한
    except (subprocess.TimeoutExpired, OSError) as error:  # 컴파일·실행 환경 오류
        record["error"] = str(error)  # 실제 오류 보존
        raise RuntimeError(str(error)) from error  # 통과 판정 금지
    record.update(returncode=process.returncode, stdout=process.stdout.decode("utf-8", errors="replace"), stderr=process.stderr.decode("utf-8", errors="replace"))  # 출력과 종료 코드를 함께 저장
    if process.returncode != 0:  # 컴파일이나 테스트가 실패한 경우
        raise RuntimeError(f"command failed: {record['command'][0]} rc={process.returncode}")  # 다음 단계를 성공으로 세지 않기
    return record  # 성공한 단계의 실제 출력

def main():  # no_std 빌드와 표준 라이브러리 호스트 테스트 분리 실행
    parser = argparse.ArgumentParser()  # 실행 환경 인자 구성
    parser.add_argument("--rustc", default="rustc")  # 명시한 컴파일러 또는 PATH 이름
    parser.add_argument("--linker", default="auto", help="auto, default, or a linker executable path")  # 호스트 링커 정책 선택
    parser.add_argument("--out", type=Path)  # 보고서 위치를 지정하지 않으면 새 빌드 폴더 사용
    parser.add_argument("--build-dir", type=Path, required=True)  # 새 임시 작업 공간을 둘 부모 폴더
    args = parser.parse_args()  # 사용자 선택 읽기
    rustc = shutil.which(args.rustc)  # 실제 실행 가능한 컴파일러 검색
    if not rustc:  # 도구 부재를 완료로 표시하지 않기
        parser.error("rustc executable not found")  # 설치 경로 오류 알림
    rustc = str(Path(rustc).resolve())  # 작업 폴더를 바꿔도 같은 도구 사용
    source = Path(__file__).resolve().parent  # 확정된 소스의 위치
    original_hashes = {name: sha(source / name) for name in ("lib.rs", "tests.rs", "run.py")}  # 변경 전 세 파일의 식별값
    args.build_dir.mkdir(parents=True, exist_ok=True)  # 기존 파일 삭제 없이 빌드 부모 준비
    work = Path(tempfile.mkdtemp(prefix="rust-fw-", dir=args.build_dir)).resolve()  # 고유한 새 작업 폴더
    output = args.out.resolve() if args.out else work / "validation.json"  # 보고서는 명시한 위치 또는 생성물 옆에 저장
    if output.suffix.lower() != ".json" or output.name == "example.json":  # 예제 원본 메타데이터와 실행 결과 구분
        parser.error("--out must be a separate .json execution report")  # 원본 메타데이터 덮어쓰기 방지
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "status": "failed", "source_sha256": original_hashes, "build_directory": str(work), "commands": [], "scope": {"no_std_rlib_compile": True, "host_standard_library_tests": True, "mcu_execution": False, "mmio_execution": False, "cross_target_compile": False}}  # 실행 범위를 명확히 기록
    result_code = 1  # 모든 단계가 확인되기 전에는 실패가 기본
    try:  # 오류가 나도 실행 보고서를 남기는 범위
        for name in ("lib.rs", "tests.rs"):  # 확정한 Rust 소스만 임시 폴더에 복사
            shutil.copyfile(source / name, work / name)  # 원본 바이트를 그대로 사용
            if sha(work / name) != original_hashes[name]:  # 실제 컴파일 입력도 대조
                raise RuntimeError(f"staged copy mismatch: {name}")  # 손상된 복사본 거절
        version = execute([rustc, "--version", "--verbose"], work, report["commands"])  # 실제 도구 버전과 호스트 확인
        sysroot = execute([rustc, "--print", "sysroot"], work, report["commands"])["stdout"].strip()  # 배포 링커를 찾을 도구 루트
        host_match = re.search(r"^host: (\S+)$", version["stdout"], re.MULTILINE)  # 컴파일러가 대상으로 삼은 기본 호스트
        if not host_match:  # 호스트 확인이 안 된 상태로 GNU 옵션을 추측하지 않기
            raise RuntimeError("rustc verbose output has no host")  # 버전 출력 오류
        host = host_match.group(1)  # 실제 호스트 triple
        linker_options = []  # 다른 호스트에서는 기본 링커를 그대로 사용
        selected_linker = None  # 명시 또는 자동 선택된 링커
        if args.linker == "auto" and host == "x86_64-pc-windows-gnu":  # 확인한 Windows GNU의 경로 문제 우회
            selected_linker = Path(sysroot) / "lib" / "rustlib" / host / "bin" / "rust-lld.exe"  # 같은 Rust 배포에 포함된 LLD
            if not selected_linker.is_file():  # 자동 선택한 실행 파일 존재 확인
                raise RuntimeError("bundled rust-lld missing; choose --linker default or an explicit linker")  # 조용한 대체 금지
        elif args.linker not in ("auto", "default"):  # 사용자가 명시한 링커
            found = shutil.which(args.linker)  # 파일 경로 또는 PATH 검색
            if not found:  # 존재하지 않는 링커 경로
                raise RuntimeError("specified linker executable not found")  # 명확한 실패 기록
            selected_linker = Path(found).resolve()  # 작업 폴더와 무관한 절대 경로
        if selected_linker:  # 기본값 외의 링커를 선택한 경우
            linker_options += ["-C", f"linker={selected_linker}"]  # rustc가 실제로 사용할 실행 파일
            if host == "x86_64-pc-windows-gnu" and "lld" in selected_linker.stem:  # 이 호스트의 직접 LLD 호출 방식
                linker_options += ["-C", "linker-flavor=ld.lld", "-C", "link-self-contained=yes"]  # 배포본의 GNU 지원 파일과 함께 링크
        report["linker"] = {"requested": args.linker, "selected": str(selected_linker) if selected_linker else "target default", "codegen_options": linker_options}  # 다른 호스트와의 선택 차이 보관
        execute([rustc, "--edition", "2024", "--crate-name", "firmware_fields", "--crate-type", "rlib", "-D", "warnings", "lib.rs", "-o", "libfirmware_fields.rlib"], work, report["commands"])  # no_std 라이브러리 자체 컴파일
        test_binary = "tests.exe" if "windows" in host else "tests"  # 호스트의 실행 파일 이름
        execute([rustc, "--edition", "2024", "--test", "-D", "warnings", *linker_options, "tests.rs", "--extern", "firmware_fields=libfirmware_fields.rlib", "-o", test_binary], work, report["commands"])  # 표준 라이브러리 테스트 실행 파일 별도 빌드
        tested = execute([str(work / test_binary), "--test-threads=1", "--nocapture"], work, report["commands"])  # 정해진 순서로 실제 호스트 테스트 실행
        fields = re.search(r"PASS fields checks=(\d+)", tested["stdout"])  # 테스트가 실제 출력한 필드 비교 수
        frames = re.search(r"PASS frames checks=(\d+)", tested["stdout"])  # 테스트가 실제 출력한 프레임 비교 수
        if not fields or not frames or (int(fields.group(1)), int(frames.group(1))) != (21652, 10179):  # 예상 범위가 실제로 실행됨
            raise RuntimeError("expected assertion counts were not observed")  # 미완료나 축소된 실행 거절
        if not re.search(r"test result: ok\. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out", tested["stdout"]):  # 두 테스트 모두 실제 완료
            raise RuntimeError("host tests did not complete with the required result")  # 종료 코드만으로 완료 추정 금지
        report["checks"] = {"fields": int(fields.group(1)), "frames": int(frames.group(1)), "total": 31831, "tests_passed": 2}  # 실제 집계
        report["artifacts_sha256"] = {name: sha(work / name) for name in ("libfirmware_fields.rlib", test_binary)}  # 이번 컴파일 산출물의 식별값
        report["status"] = "passed_no_std_compile_and_host_tests"  # MCU 동작과 구분한 완료 상태
        result_code = 0  # 필요한 단계가 모두 확인됨
    except (OSError, RuntimeError) as error:  # 도구·파일·기능 실패를 보고서에 보존
        report["error"] = str(error)  # 실패 원인을 숨기지 않기
    after_hashes = {name: sha(source / name) for name in original_hashes}  # 실행 후 게시 소스 다시 읽기
    report["source_sha256_after"] = after_hashes  # 원본 보존 대조 근거
    report["source_bytes_unchanged"] = after_hashes == original_hashes  # 실행 전후 바이트 일치
    if not report["source_bytes_unchanged"]:  # 실행 중 외부 수정까지 구분
        report["status"] = "failed_source_changed"  # 옛 소스 근거로 통과를 기록하지 않기
        result_code = 1  # 실패 종료
    output.parent.mkdir(parents=True, exist_ok=True)  # 보고서 부모 위치 준비
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")  # 실제 실행 보고서 저장
    print(f"{report['status']} fields={report.get('checks', {}).get('fields', 0)} frames={report.get('checks', {}).get('frames', 0)} source_bytes_unchanged={report['source_bytes_unchanged']}")  # 간단한 실제 결과 표시
    return result_code  # 자동 실행에서도 실패를 전달

if __name__ == "__main__":  # import만으로 도구나 파일을 실행하지 않기
    raise SystemExit(main())  # 실제 결과를 프로세스 종료 코드로 연결
```

## 공식 근거와 라이선스

- [Rust Reference의 no_std](https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute)·[shift overflow](https://doc.rust-lang.org/reference/expressions/operator-expr.html#overflow)는 라이브러리 범위와 이동 수 조건의 근거입니다.
- [The Rust Programming Language의 borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)·[rustc 테스트](https://doc.rust-lang.org/rustc/tests/index.html)·[링커 옵션](https://doc.rust-lang.org/rustc/codegen-options/index.html#linker)은 참조와 호스트 실행 도구의 근거입니다.
- 회로 명세나 외부 예제 코드를 복사한 자료가 아니라 직접 구성한 값 처리·프레임 예제입니다. [Rust 저장소의 라이선스 안내](https://github.com/rust-lang/rust#license)는 컴파일러·표준 라이브러리의 MIT/Apache-2.0과 제삼자 구성요소를 구분합니다. 도구 바이너리와 표준 라이브러리 소스는 이 폴더에 재배포하지 않습니다.

공식 자료 열람과 실행 기준일은 2026-10-26입니다.
