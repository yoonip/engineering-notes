package body Bench_Config with SPARK_Mode is -- 공개 계약을 구현하는 SPARK 대상 본문
   function Required_Bytes -- 명세와 같은 함수 본문
     (Count : Sample_Count; Width : Sample_Width; Budget : Byte_Total) -- 호출자가 계약을 만족시킨 입력
      return Byte_Total is -- 반환 자료형의 범위 검사도 유지
   begin -- 배치 크기 계산 시작
      return Count * Width; -- 최대 64 곱하기 16이므로 기본 Integer 산술 범위 안
   end Required_Bytes; -- 배치 계산 끝
   function Add_Used -- 사용량 합산 함수 본문
     (Used, Added : Byte_Total) return Byte_Total is -- 명세의 사전조건이 합산 범위를 보장
   begin -- 합산 시작
      return Used + Added; -- 최대 반환값 1024를 사전조건으로 제한
   end Add_Used; -- 사용량 합산 끝
end Bench_Config; -- 계산 패키지 본문 끝
