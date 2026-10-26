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
