with Ada.Assertions; -- 사전조건 위반의 실제 예외 이름
with Ada.Command_Line; -- 벤치 요청과 종료 코드 처리
with Ada.Text_IO; -- 검사 결과와 거절 사유 출력
with Bench_Config; use Bench_Config; -- 공개 범위 자료형과 두 계산 함수 사용
procedure Bench_Demo is -- I/O를 담당하는 일반 Ada 실행기
   Checks : Natural := 0; -- 실제 수행한 비교 개수
   Accepted : Natural := 0; -- 계약을 만족해 결과를 확인한 호출 수
   Rejected_Pre : Natural := 0; -- 사전조건 예외를 실제로 확인한 호출 수
   procedure Verify (Condition : Boolean; Message : String) is -- 빌드 최적화로 사라지지 않는 비교
   begin -- 비교 집계와 판정 시작
      Checks := Checks + 1; -- 실행한 비교만 집계
      if not Condition then -- 독립 기대값과 다를 때 실패
         raise Program_Error with Message; -- 계약 예외와 검사기 자체 오류를 구분
      end if; -- 실패 조건 끝
   end Verify; -- 비교 함수 끝
   procedure All_Tests is -- 작은 유효 범위와 경계를 직접 검사
      Expected : Natural; -- 반복 덧셈으로 구한 독립 배치 크기
      Actual : Byte_Total; -- 실제 계산 함수의 반환값
      Boundary : constant array (Positive range 1 .. 5) of Byte_Total := -- 사용량의 양끝과 중간 경계
        (0, 1, 512, 1023, 1024); -- 0·한 바이트·중간·상한 직전·상한
   begin -- 정상 호출과 잘못된 예산 호출의 대조 시작
      for Count in Sample_Count loop -- 허용한 표본 개수 64개
         for Width in Sample_Width loop -- 허용한 폭 16개
            Expected := 0; -- 현재 조합의 덧셈 기준 초기화
            for Index in 1 .. Count loop -- 곱셈 구현과 달리 표본별 폭을 반복 누적
               Expected := Expected + Width; -- 표본 하나의 바이트 수 추가
            end loop; -- 독립 덧셈 계산 끝
            Actual := Required_Bytes (Count, Width, Byte_Total'Last); -- 최대 예산 안의 정상 호출
            Verify (Actual = Expected, "repeated-add reference"); -- 곱셈과 독립 덧셈 비교
            Actual := Required_Bytes (Count, Width, Byte_Total (Expected)); -- 정확히 맞는 예산의 경계
            Verify (Actual = Expected, "exact budget boundary"); -- 예산과 같은 크기는 수락
            Accepted := Accepted + 2; -- 두 정상 결과 확인
            begin -- 한 바이트 부족한 예산을 독립적으로 시도
               Actual := Required_Bytes (Count, Width, Byte_Total (Expected - 1)); -- 실제 사전조건 위반 호출
               Verify (False, "missing precondition" & Byte_Total'Image (Actual)); -- 예외 없이 돌아오면 검사 실패
            exception -- 위 호출에서 발생한 지정 예외만 확인
               when Ada.Assertions.Assertion_Error => -- 실제 사전조건 예외
                  Rejected_Pre := Rejected_Pre + 1; -- 거절 건수 누적
                  Verify (True, "precondition rejected short budget"); -- 거절 확인도 실제 비교로 집계
            end; -- 부족한 예산 대조 끝
         end loop; -- 표본 폭 순회 끝
      end loop; -- 표본 개수 순회 끝
      for Used of Boundary loop -- 기존 사용량의 다섯 경계
         for Added of Boundary loop -- 추가 사용량의 다섯 경계
            declare -- 더 넓은 정수로 독립 기대값 생성
               Wide : constant Long_Long_Integer := -- 중간 합을 제한 자료형과 분리
                 Long_Long_Integer (Used) + Long_Long_Integer (Added); -- 넓힌 정수의 합
            begin -- 허용 가능한 합과 초과 합 구분
               if Wide <= Long_Long_Integer (Byte_Total'Last) then -- 예산 안의 조합
                  Actual := Add_Used (Used, Added); -- 실제 합산 함수 호출
                  Verify (Long_Long_Integer (Actual) = Wide, "wide sum reference"); -- 넓은 정수 기준과 비교
                  Accepted := Accepted + 1; -- 정상 결과 집계
               else -- 결과가 자료형 상한을 넘는 조합
                  begin -- 사전조건 예외를 확인할 별도 구간
                     Actual := Add_Used (Used, Added); -- 실제 계약 위반 시도
                     Verify (False, "missing sum precondition" & Byte_Total'Image (Actual)); -- 조용히 넘치면 실패
                  exception -- 예상한 계약 예외만 수락
                     when Ada.Assertions.Assertion_Error => -- 합산 전 사전조건 거절
                        Rejected_Pre := Rejected_Pre + 1; -- 거절 건수 집계
                        Verify (True, "precondition rejected oversized sum"); -- 초과 합 거절 확인
                  end; -- 초과 합 대조 끝
               end if; -- 합의 유효 범위 분기 끝
            end; -- 넓은 기대값의 범위 끝
         end loop; -- 추가 사용량 순회 끝
      end loop; -- 기존 사용량 순회 끝
      Verify (Accepted = 2063 and Rejected_Pre = 1034, "case accounting"); -- 실행한 정상·거절 조합 수 확인
      Ada.Text_IO.Put_Line -- 전체 경계 비교의 완료 표식
        ("PASS ada checks=" & Natural'Image (Checks) -- 실제 비교 수 출력
         & " accepted=" & Natural'Image (Accepted) -- 정상 호출 수 출력
         & " precondition_rejections=" & Natural'Image (Rejected_Pre)); -- 실제 계약 거절 수 출력
   end All_Tests; -- 선별 경계 검사 끝
begin -- 실행기의 명령행 처리 시작
   if Ada.Command_Line.Argument_Count = 0 then -- 인수가 없으면 경계 검사 전체 실행
      All_Tests; -- 직접 정의한 배치·합산 조합 대조
   elsif Ada.Command_Line.Argument_Count = 3 then -- 개수·폭·예산의 단일 벤치 요청
      declare -- 문자열 변환도 런타임 범위 검사의 대상
         Count : constant Sample_Count := -- 허용한 개수 자료형으로 변환
           Sample_Count (Integer'Value (Ada.Command_Line.Argument (1))); -- 0·65 등은 Constraint_Error
         Width : constant Sample_Width := -- 허용한 표본 폭으로 변환
           Sample_Width (Integer'Value (Ada.Command_Line.Argument (2))); -- 0·17 등은 Constraint_Error
         Budget : constant Byte_Total := -- 허용한 메모리 예산으로 변환
           Byte_Total (Integer'Value (Ada.Command_Line.Argument (3))); -- 음수·1025 등은 Constraint_Error
         Result : constant Byte_Total := Required_Bytes (Count, Width, Budget); -- 범위 뒤에 별도 사전조건 검사
      begin -- 정상 요청 결과 표시
         Ada.Text_IO.Put_Line ("OK required_bytes=" & Byte_Total'Image (Result)); -- 확인한 바이트 수 출력
      end; -- 단일 요청 처리 끝
   else -- 입력 개수가 맞지 않는 경우
      Ada.Text_IO.Put_Line ("usage: bench_demo [count width budget]"); -- 허용한 명령행 형식
      Ada.Command_Line.Set_Exit_Status (2); -- 사용법 오류를 계약 거절과 구분
   end if; -- 실행 모드 분기 끝
exception -- 실제 런타임 거절을 명시적인 종료 코드에 반영
   when Ada.Assertions.Assertion_Error => -- 범위는 맞지만 예산 계약을 어긴 요청
      Ada.Text_IO.Put_Line ("REJECT precondition Assertion_Error"); -- 실제 예외 종류 기록
      Ada.Command_Line.Set_Exit_Status (Ada.Command_Line.Failure); -- 계약 거절은 종료 코드 1
   when Constraint_Error => -- 정수 파싱 또는 부분 자료형 범위의 위반
      Ada.Text_IO.Put_Line ("REJECT range_or_integer Constraint_Error"); -- 입력 변환 거절 사유
      Ada.Command_Line.Set_Exit_Status (Ada.Command_Line.Failure); -- 범위 거절도 종료 코드 1
end Bench_Demo; -- 일반 Ada 실행기 끝
