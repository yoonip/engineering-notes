# Ada 부분 자료형과 계약으로 확인하는 벤치 메모리 예산

이 예제는 벤치에서 사용할 표본 개수, 표본당 바이트 수, 메모리 예산을 정수 범위와 함수 계약으로 표현합니다. 배치 크기를 계산하는 `Required_Bytes`와 사용량을 더하는 `Add_Used`를 직접 작성하고, Windows용 GNAT 16.1.0으로 컴파일·실행했습니다. 장치 I/O나 제어 명령 없이 숫자로 주어진 벤치 설정만 확인합니다.

Ada 컴파일, 런타임 계약 검사, SPARK 형식 증명은 서로 다른 확인 단계입니다. 이 폴더에서는 앞의 두 단계만 실행했습니다. `SPARK_Mode`를 붙였지만 GNATprove를 설치하거나 실행하지 않았으므로, 정적 증명이나 모든 실행 경로의 안전성을 주장하지 않습니다. 임시 저장공간 제약으로 증명 도구의 추가 설치를 보류했습니다.

## 파일과 실제 실행 범위

| 파일 | 역할 |
| --- | --- |
| [bench_config.ads](bench_config.ads) | 입력 범위와 `Pre`·`Post` 계약을 공개하는 패키지 명세입니다. |
| [bench_config.adb](bench_config.adb) | 두 계산 함수의 구현입니다. |
| [bench_demo.adb](bench_demo.adb) | 일반 Ada I/O, 독립 기대값 비교, 실제 예외 확인을 담당하는 실행기입니다. |
| [bench.gpr](bench.gpr) | 같은 소스·옵션을 적은 프로젝트 파일입니다. 이번 실행은 이 파일을 사용하는 `gprbuild`가 아닌 `gnatmake` 명령으로 수행했습니다. |
| [example.json](example.json) | 소스 SHA-256, 도구 판본, 실제 명령·출력·종료 코드와 미실행 증명 상태를 기록합니다. |

`bench_config`는 SPARK 대상으로 표시한 계산 패키지이고 `bench_demo`는 명령행·텍스트 출력·예외 처리를 하는 일반 Ada 실행기입니다. `Global => null`은 함수가 전역 상태를 읽거나 바꾸지 않는다는 계약을 나타냅니다. 이 선언을 붙이고 GNAT로 컴파일했다는 사실만으로 해당 성질을 GNATprove가 증명했다고 볼 수는 없습니다.

## 범위와 계약을 나누어 읽기

| 이름 | 허용 범위·의미 | 확인할 점 |
| --- | --- | --- |
| `Sample_Count` | `1 .. 64`의 `Positive` 부분 자료형입니다. | 개수 `0`이나 `65`를 변환하면 `Constraint_Error`가 발생합니다. |
| `Sample_Width` | `1 .. 16`의 `Positive` 부분 자료형입니다. | 표본당 바이트 수를 제한합니다. |
| `Byte_Total` | `0 .. 1024`의 `Natural` 부분 자료형입니다. | 예산·기존 사용량·추가 사용량·반환값의 바이트 범위를 제한합니다. |
| `Required_Bytes` | `Count * Width <= Budget`일 때 호출합니다. | 각 입력의 범위가 맞아도 조합이 예산을 넘으면 사전조건 위반입니다. |
| `Add_Used` | `Used <= 1024 - Added`일 때 호출합니다. | 먼저 남은 범위를 비교하여 허용 범위를 넘는 합산을 거절합니다. |

부분 자료형은 기존 자료형의 값 범위를 좁힙니다. 이 예제의 `Sample_Count`와 `Sample_Width`가 서로 다른 이름이라고 해서 독립적인 새 정수 자료형이 되는 것은 아닙니다. 역할을 타입 수준에서 완전히 분리하려면 새 자료형 선언 등 추가 설계를 검토해야 합니다. [AdaCore의 강한 자료형 입문](https://learn.adacore.com/courses/intro-to-ada/chapters/strongly_typed_language.html)에서 부분 자료형과 자료형의 차이를 읽을 수 있습니다.

`Pre`는 호출 전에 만족해야 할 관계이고, `Post`는 정상 반환 때 결과가 만족해야 할 관계입니다. `'Result`는 해당 함수의 반환값, `'Last`는 부분 자료형의 상한을 뜻합니다. `and then`은 왼쪽이 참일 때만 오른쪽을 평가하는 단락 논리 연산자입니다. [AdaCore 계약 입문](https://learn.adacore.com/courses/intro-to-ada/chapters/contracts.html)에서 문법과 호출자·피호출자의 약속을 설명합니다.

`Count * Width` 자체가 안전한지도 별도로 살펴야 합니다. 여기서는 두 범위의 최대 곱이 `64 * 16 = 1024`이므로 기본 정수 연산 범위 안에 있습니다. 임의의 큰 정수에 같은 곱셈 사전조건을 복사하면, 비교하기 전에 곱셈이 넘칠 수 있으므로 일반적인 오버플로 방지식으로 사용할 수는 없습니다. 합산 함수는 `1024 - Added`를 먼저 구하며, `Added`의 범위가 `0 .. 1024`이므로 이 뺄셈도 범위 안에 있습니다.

## 입력과 예외의 흐름

| 단계 | 구체적인 값·실행 | 의미 |
| --- | --- | --- |
| 1 | 인수 `4 8 32`를 정수로 읽습니다. | 정수 형식과 각 부분 자료형의 범위를 먼저 확인합니다. |
| 2 | `4 * 8 <= 32`를 검사합니다. | 입력별 범위를 통과한 뒤 배치와 예산의 관계를 확인합니다. |
| 3 | `Required_Bytes`가 `32`를 반환합니다. | 반환 부분 자료형의 범위와 사후조건을 확인합니다. |
| 4 | 같은 배치를 예산 `31`로 요청합니다. | 실제 사전조건 예외 `Assertion_Error`를 잡고 종료 코드 `1`로 거절합니다. |
| 5 | 개수 `65`를 요청합니다. | 함수에 도달하기 전 부분 자료형 변환에서 `Constraint_Error`를 잡고 종료 코드 `1`로 거절합니다. |

`Add_Used (1023, 1)`은 `1024`를 반환하지만 `Add_Used (1024, 1)`은 사전조건을 어깁니다. 두 함수는 설정을 저장하지 않고 계산한 값만 반환합니다. 실제 시스템에서 설정을 반영한다면, 모든 입력을 확인한 뒤 상태를 바꾸는 별도 단계가 필요합니다.

계약 검사는 `-gnata`로 켰고, 범위 검사를 끄는 `-gnatp`는 사용하지 않았습니다. GNAT의 [`-gnata` 문서](https://gcc.gnu.org/onlinedocs/gnat_ugn/Debugging-and-Assertion-Control.html)는 이 옵션이 `Assertion_Policy(Check)`에 해당하며 사전·사후조건 등을 활성화한다고 설명합니다. 계약을 끈 실행 파일에서도 이 검사기가 통과한다고 가정하면 안 됩니다.

## 실제 실행 기록과 독립 기대값

인수 없이 실행하면 `Count` 64개와 `Width` 16개의 `1,024`개 조합을 순회합니다. 곱셈 함수의 기대값은 표본 폭을 `Count`번 더해서 구합니다. 각 조합에서 최대 예산과 정확히 맞는 예산의 정상 결과를 비교하고, 한 바이트 부족한 예산은 실제 `Assertion_Error`로 거절되는지 확인합니다.

합산 함수는 경계값 `(0, 1, 512, 1023, 1024)`의 `25`개 조합을 검사합니다. 기대 합은 더 넓은 `Long_Long_Integer`로 계산합니다. 그중 정상 합은 `15`개이고 사전조건 거절은 `10`개입니다. 이 검사는 모든 `Byte_Total` 쌍을 열거하는 검사가 아닙니다.

| 확인 항목 | 실제 결과 |
| --- | --- |
| GNAT 컴파일·바인드·링크 | 종료 코드 `0`이며 경고를 오류로 처리했습니다. |
| 내부 비교 | 총 `3,098`개입니다. 정상 결과 `2,063`개, 실제 사전조건 거절 `1,034`개, 마지막 집계 비교 `1`개입니다. |
| 명령행 경계·오류 | 최소·일반·최대 배치, 부족 예산, 범위·형식·인수 개수 오류를 포함한 `11`건의 출력과 종료 코드가 기대값과 일치했습니다. |
| 소스 대응 | 게시한 네 파일과 실제 빌드 디렉터리의 네 파일 SHA-256이 일치합니다. |
| GNATprove | 설치·실행하지 않았습니다. 증명 의무나 증명 개수는 기록하지 않습니다. |

정상 완료 출력은 다음과 같습니다. 양의 정수 앞의 공백은 Ada의 `'Image` 출력에 포함됩니다.

```text
PASS ada checks= 3098 accepted= 2063 precondition_rejections= 1034
```

검사 함수 `Verify`는 기대값이 다르면 `Program_Error`를 발생시킵니다. 계약 거절 검사에서는 `Assertion_Error`만 잡으므로 검사기 자체의 실패를 정상 거절로 잘못 집계하지 않습니다. 검사에 통과했다는 사실은 실제 실행한 입력에 대한 결과이며, 일반 Ada I/O 코드 전체의 형식 증명이나 제품 인증을 대신하지 않습니다.

## GNAT로 다시 실행하기

이번 도구는 Alire가 제공하는 [GNAT-FSF-builds `16.1.0-1` Windows x86_64 배포](https://github.com/alire-project/GNAT-FSF-builds/releases/tag/gnat-16.1.0-1)이며, 실행한 `gnatmake --version`과 `gcc --version`은 `16.1.0`을 보고했습니다. Alire CLI나 GNAT Studio는 실행에 사용하지 않았습니다.

도구를 설치한 `bin` 경로와 이 폴더 경로를 지정하여 다음과 같이 실행할 수 있습니다. 생성 파일은 임시 빌드 디렉터리에 둡니다. Windows에서는 도구와 빌드 경로를 영문 경로에 두면 일부 하위 프로세스의 경로 처리 문제를 피하는 데 도움이 됩니다. 실제 실행에 사용한 영문 별칭 경로와 명령 인수는 `example.json`에 보존했습니다.

```powershell
$adaToolBin = 'C:\tools\gnat\bin'  # 사용할 GNAT의 bin 경로
$adaExample = (Get-Location).Path  # 이 README와 소스가 있는 폴더에서 실행
$adaBuild = Join-Path $env:TEMP 'ada-bench-example'  # 생성 파일용 임시 폴더
$adaSavedPath = $env:PATH  # 현재 프로세스의 경로를 복구할 값
New-Item -ItemType Directory -Path $adaBuild -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $adaExample 'bench_config.ads'), (Join-Path $adaExample 'bench_config.adb'), (Join-Path $adaExample 'bench_demo.adb') -Destination $adaBuild
try {
    $env:PATH = $adaToolBin + ';' + $adaSavedPath
    Push-Location -LiteralPath $adaBuild
    try {
        & (Join-Path $adaToolBin 'gnatmake.exe') -f -gnat2022 -gnata -gnatW8 -O0 -gnatwe bench_demo.adb
        if ($LASTEXITCODE -ne 0) { throw 'Ada build failed' }
        & .\bench_demo.exe
        if ($LASTEXITCODE -ne 0) { throw 'Ada checks failed' }
        & .\bench_demo.exe 4 8 32
        if ($LASTEXITCODE -ne 0) { throw 'Valid request failed' }
        & .\bench_demo.exe 64 16 1023
        if ($LASTEXITCODE -ne 1) { throw 'Short budget was not rejected' }
    } finally {
        Pop-Location
    }
} finally {
    $env:PATH = $adaSavedPath
}
```

`-f`는 기존 생성 파일이 있어도 지정한 옵션으로 다시 컴파일하게 합니다. `-gnat2022`는 Ada 2022 문법, `-gnatW8`은 UTF-8 소스 인코딩, `-gnatwe`는 컴파일 경고의 오류 처리를 지정합니다. `-O0`을 사용한 로컬 기능 검사이며 실행 성능을 측정하지 않았습니다.

## C와 비교할 때 기억할 점

| 항목 | C에서 자주 쓰는 방식 | 이 Ada 예제 |
| --- | --- | --- |
| 값 범위 | 정수 변수와 별도의 `if` 검사를 작성합니다. `typedef`만으로 값 범위 검사가 생기지는 않습니다. | 부분 자료형의 변환·대입·반환 범위 검사를 사용합니다. |
| 입력 간 관계 | 함수 안이나 호출부에서 수동으로 조건을 검사합니다. | 명세에 `Pre`를 적고 `-gnata`로 런타임 검사를 켭니다. |
| 결과 약속 | 반환 뒤 수동 검사나 테스트를 작성합니다. | 명세의 `Post`와 독립 테스트를 함께 사용합니다. |
| 선언과 구현 | 헤더와 구현 파일을 나누는 구성이 일반적입니다. | `.ads` 패키지 명세와 `.adb` 패키지 본문을 나눕니다. |
| 실패 전달 | 반환 코드나 별도 오류 채널을 설계합니다. | 범위·계약 예외를 실행기에서 구분해 종료 코드로 바꿉니다. |

Ada를 사용한다는 사실만으로 잘못된 요구사항이나 외부 장치의 동작까지 확인되지는 않습니다. 입력 범위, 검사 옵션, 예외 처리 경계, 상태를 바꾸는 순서를 함께 설계해야 합니다. 이 예제에는 동시성, 동적 메모리, 장치 드라이버, 실시간 스케줄링이 없습니다.

## 전체 코드와 줄별 복습 메모

각 소스의 비어 있지 않은 줄에 `--` 주석으로 문법이나 그 줄의 목적을 짧게 적었습니다. 아래 코드는 게시한 소스 파일과 같습니다.

### bench_config.ads

```ada
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

```

### bench_config.adb

```ada
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

```

### bench_demo.adb

```ada
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

```

### bench.gpr

```text
project Bench is -- 컴파일과 선택적 증명이 공유할 작은 프로젝트
   for Source_Dirs use ("."); -- 이 폴더의 직접 작성 소스만 검색
   for Object_Dir use "obj"; -- 생성 객체를 소스와 분리
   for Exec_Dir use "bin"; -- 실행 파일 위치를 별도로 지정
   for Main use ("bench_demo.adb"); -- 일반 Ada I/O 실행기의 진입점
   package Compiler is -- Ada 컴파일 옵션 묶음
      for Default_Switches ("Ada") use -- 모든 Ada 입력에 같은 조건 적용
        ("-gnat2022", "-gnata", "-gnatW8", "-O0", "-gnatwe"); -- Ada2022·계약 활성화·UTF-8·경고 오류 처리
   end Compiler; -- 컴파일 옵션 끝
end Bench; -- 프로젝트 정의 끝

```

## 풀이 요약과 다음 학습

입력 하나의 허용 범위는 부분 자료형으로, 입력 여러 개의 관계는 사전조건으로 나눕니다. 정상 반환값의 약속은 사후조건으로 적습니다. 계산 코드와 독립 기대값을 다른 방식으로 구성하고, 부족한 예산이 실제 계약 예외로 거절되는지도 확인합니다.

이후 형식 증명을 공부한다면 [SPARK Getting Started](https://docs.adacore.com/spark2014-docs/html/ug/en/getting_started.html)를 따라 GNATprove를 별도로 준비하고, 해당 도구 판본에 맞는 문서로 `bench_config`의 증명 결과를 새로 확인해야 합니다. 확인한 온라인 문서는 개발판 `28.0w`이므로 이번 GNAT `16.1.0`의 증명 결과나 동일한 도구 판본을 뜻하지 않습니다. 이 폴더에는 그 단계를 실행한 기록이 없습니다.

## 현업에서 연결되는 이유와 출처 범위

범위와 계약을 공개 명세로 옮기는 방식은 설정값의 유효성, 바이트 수·인덱스 산술, 호출자와 라이브러리 사이의 책임을 검토할 때 유용합니다. [AdaCore의 Welch Allyn 의료기기 사례](https://www.adacore.com/case-studies/ada-and-spark-at-welch-allyn)는 Hillrom의 Ada·SPARK 도입과 일부 속성의 형식 증명을 소개합니다. 이는 공급사가 공개한 산업 적용 사례이며, 여기의 간단한 메모리 예산 예제가 의료기기 구현이나 인증 요구사항을 재현했다는 뜻은 아닙니다.

코드는 이 벤치의 범위와 기대값 비교를 위해 직접 작성했습니다. 공식 문서에서는 언어·옵션·도구의 의미만 확인했으며 예제 원문을 복사하지 않았습니다. 공식 도구 배포물의 라이선스와 이 폴더의 직접 작성 코드의 출처를 구분합니다.

| 공식 자료 | 확인한 내용과 범위 |
| --- | --- |
| [AdaCore Strongly Typed Language](https://learn.adacore.com/courses/intro-to-ada/chapters/strongly_typed_language.html) | 자료형·부분 자료형·범위 검사의 학습 자료입니다. |
| [AdaCore Design by contracts](https://learn.adacore.com/courses/intro-to-ada/chapters/contracts.html) | 사전·사후조건 문법과 의미를 확인했습니다. |
| [GNAT Debugging and Assertion Control](https://gcc.gnu.org/onlinedocs/gnat_ugn/Debugging-and-Assertion-Control.html) | `-gnata`의 계약 검사 활성화 범위를 확인했습니다. |
| [SPARK Getting Started](https://docs.adacore.com/spark2014-docs/html/ug/en/getting_started.html) | GNATprove가 별도 도구임을 확인했습니다. 이 예제에서는 실행하지 않았습니다. |
| [Alire gnat_native](https://alire.ada.dev/crates/gnat_native)·[해당 16.1.0 메타데이터](https://raw.githubusercontent.com/alire-project/alire-index/stable-1.4.0/index/gn/gnat_native/gnat_native-16.1.0.toml) | 도구 배포의 판본·다운로드·해시·라이선스 범위를 확인했습니다. |

Alire 메타데이터의 도구 라이선스는 `GPL-3.0-or-later AND GPL-3.0-or-later WITH GCC-exception-3.1`입니다. GCC 런타임 예외가 붙은 구성요소와 도구 자체의 조건을 구분하여 확인해야 합니다. 이 표기는 이 폴더의 직접 작성 Ada 소스에 일괄 적용하는 라이선스 선언이 아닙니다. 저장소에는 컴파일러·런타임 바이너리나 다운로드 압축본을 넣지 않았습니다. 사용한 압축본의 SHA-256은 `example.json`에 기록했으며, 실제 도구 확인 뒤 해당 임시 압축본을 삭제했습니다.
