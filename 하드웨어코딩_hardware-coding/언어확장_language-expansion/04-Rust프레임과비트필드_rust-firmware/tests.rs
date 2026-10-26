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
