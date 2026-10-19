# Mobile & Cross-Platform

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

모바일 애플리케이션은 화면뿐 아니라 센서·카메라·무선 연결·전원·백그라운드 실행 정책을 함께 다룬다. Embedded 장치와 연결하면 휴대용 제어·계측·추론 인터페이스가 된다.

## 플랫폼과 연결

Android는 Kotlin·Java, iOS는 Swift 중심의 개발 생태계를 갖는다. Flutter·Dart·React Native·Kotlin Multiplatform은 코드 공유 범위와 UI 구성 방식이 다르다. BLE에서는 광고·연결·service·characteristic 같은 구조로 장치의 데이터를 주고받는다.

## 자원과 사용자 경험

카메라 영상과 센서 stream은 timestamp·좌표계·전처리·권한 처리가 중요하다. Offline 동작에는 로컬 저장과 나중의 동기화가 필요하다. 네트워크가 복구되었을 때 중복 전송과 충돌을 어떻게 다루는지가 데이터 무결성과 연결된다.

Core ML·LiteRT 같은 runtime은 장치 추론에 사용된다. 지속적인 추론은 battery·발열·메모리 조건에 영향을 받으며 짧은 benchmark와 장시간 실행의 성능이 다를 수 있다. 접근성·화면 크기·기기별 OS 지원은 동작 범위를 결정한다.

## 관련 기술

Kotlin, Java, Android, Swift, iOS, Flutter, Dart, React Native, Kotlin Multiplatform, Core ML

## 참고 자료

- [Android Developers](https://developer.android.com/guide)
