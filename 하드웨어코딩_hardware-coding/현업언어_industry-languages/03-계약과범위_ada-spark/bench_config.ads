package Bench_Config with SPARK_Mode is -- 범위와 계약을 공개하는 부작용 없는 벤치 계산
   subtype Sample_Count is Positive range 1 .. 64; -- 한 배치의 표본 개수 제한
   subtype Sample_Width is Positive range 1 .. 16; -- 표본 하나의 바이트 수 제한
   subtype Byte_Total is Natural range 0 .. 1024; -- 벤치 메모리 예산의 유효 범위
   function Required_Bytes -- 표본 배치가 차지할 바이트 수 계산
     (Count : Sample_Count; Width : Sample_Width; Budget : Byte_Total) -- 서로 다른 역할의 입력 이름
      return Byte_Total -- 반환값에도 예산 자료형의 범위 적용
     with Global => null, -- 전역 상태를 읽거나 바꾸지 않는 함수
       Pre => Count * Width <= Budget, -- 이 벤치에서 배치가 예산 안에 들어와야 호출 가능
       Post => Required_Bytes'Result = Count * Width -- 반환값은 정확한 배치 크기
         and then Required_Bytes'Result <= Budget; -- 반환 뒤에도 요청 예산 조건 확인
   function Add_Used -- 기존 사용량과 새 사용량을 합산
     (Used, Added : Byte_Total) return Byte_Total -- 입력 두 개와 결과의 공통 단위는 바이트
     with Global => null, -- 누적 상태는 호출자가 보관하고 함수는 값만 반환
       Pre => Used <= Byte_Total'Last - Added, -- 합산 전에 남은 범위가 충분한지 확인
       Post => Add_Used'Result = Used + Added; -- 허용된 입력의 정확한 합을 약속
end Bench_Config; -- 공개 자료형과 계약 정의 끝
