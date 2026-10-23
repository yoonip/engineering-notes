#include <string>
#include <vector>

using namespace std;

string solution(vector<string> storage, vector<int> num) {
    int num_item = 0;
    vector<string> clean_storage(storage.size());
    vector<int> clean_num(num.size());
    
    for(int i=0; i<storage.size(); i++){
        int clean_idx = -1;
        for(int j=0; j<num_item; j++){
            if(storage[i] == clean_storage[j]){
                clean_idx = j;
                break;
            }
        }
        if(clean_idx == -1){
            clean_storage[num_item] = storage[i];
            clean_num[num_item] = num[i];
            num_item += 1;
        }
        else{
            clean_num[clean_idx] += num[i];
        }
    }
    
    // 아래 코드에는 틀린 부분이 없습니다.
    
    int num_max = -1;
    string answer = "";
    for(int i=0; i<num_item; i++){
        if(clean_num[i] > num_max){
            num_max = clean_num[i];
            answer = clean_storage[i];
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(vector<string> storage, vector<int> num) {  // [PCCE 기출문제] 8번 / 창고 정리 풀이 시작
//     int num_item = 0;  // 지금까지 합쳐 둔 서로 다른 물건 종류 수
//     vector<string> clean_storage(storage.size());  // clean_storage를 보관할 컨테이너 준비
//     vector<int> clean_num(num.size());  // clean_num를 보관할 컨테이너 준비
//
//     for(int i=0; i<storage.size(); i++){  // 원래 창고 기록을 하나씩 합치기
//         int clean_idx = -1;  // 같은 물건을 아직 찾지 못했다는 표시
//         for(int j=0; j<num_item; j++){  // 이미 합친 물건 이름 중 같은 이름 찾기
//             if(storage[i] == clean_storage[j]){  // 현재 물건이 이미 기록된 종류인 경우
//                 clean_idx = j;  // clean_idx에 j 저장
//                 break;  // break로 가장 가까운 반복문이나 switch를 끝
//             }  // 블록 끝
//         }  // 블록 끝
//         if(clean_idx == -1){  // clean_idx == -1이면 이 분기에서 처리
//             clean_storage[num_item] = storage[i];  // 처음 발견한 물건의 이름을 새 정리 위치에 저장
//             clean_num[num_item] = num[i];  // clean_num[num_item]에 num[i] 저장
//             num_item += 1;  // 처음 본 물건을 등록했으니 종류 수 추가
//         }  // 블록 끝
//         else{  // 같은 이름의 물건이 이미 있는 경우
//             clean_num[clean_idx] += num[i];  // 기존 물건의 합계에 이번 수량 추가
//         }  // 블록 끝
//     }  // 블록 끝
//
//     // 아래 코드에는 틀린 부분이 없습니다.  // 아래는 합쳐진 수량 중 최댓값을 고르는 구간
//
//     int num_max = -1;  // 지금까지 찾은 가장 많은 수량
//     string answer = "";  // 수량이 가장 많은 물건의 이름
//     for(int i=0; i<num_item; i++){  // 합친 물건 종류별 수량 비교
//         if(clean_num[i] > num_max){  // 기존 최댓값보다 많은 물건 발견
//             num_max = clean_num[i];  // num_max에 clean_num[i] 저장
//             answer = clean_storage[i];  // 최대 수량에 해당하는 물건 이름 갱신
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 이미 기록한 물건이면 수량을 더하기. 처음 보는 물건이면 이름과 수량을 새 위치에 저장한 뒤 가장 많은 이름을 선택
