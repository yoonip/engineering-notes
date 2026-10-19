# Software-backed misc character device

`valdemo.c`는 외부 장치 없이 kernel의 `write`/`read` callback을 연결하는 모듈이다. 입력은 1~256 byte이며 각 byte의 unsigned 합, 길이, 증가하는 sequence를 저장한다. `client.py`는 `[1, 2, 3, 250]`을 쓰고 길이 4와 합 256을 확인한다.

이 버전은 `.llseek = NULL`을 사용한다. 입력의 `copy_from_user`, 결과 갱신 mutex, `simple_read_from_buffer`의 offset 처리를 포함한다. `.mode = 0600`이므로 device 접근에는 해당 권한이 필요하다.

## 빌드와 실행

모듈은 실제 실행할 kernel과 맞는 release/configuration의 build tree에서 만든다. 일반 Linux 배포판의 headers를 사용해 만든 모듈을 다른 WSL kernel에 삽입하는 방식은 호환성을 보장하지 않는다.

```sh
cd linux
make KDIR=/lib/modules/$(uname -r)/build
# 다음은 kernel에 모듈을 삽입하는 실제 실행 단계다.
sudo insmod ./valdemo.ko
sudo python3 -B client.py
sudo rmmod valdemo
```

기대 출력은 `PASS sequence=... length=4 sum=256`이다. Sequence는 실행 이력에 따라 달라진다. Module signing·kernel ABI·device 권한은 별도로 맞아야 한다. 이번 배포 검증은 위 명령을 실행하지 않고 client의 I/O 경로를 mock으로 검사한다.

## 동시성 범위

결과는 전역의 마지막 write 하나를 나타낸다. Client가 write한 뒤 다른 process가 write하면 첫 client가 다른 결과를 읽을 수 있다. Mutex는 한 결과의 필드 갱신을 보호하지만 여러 호출을 한 transaction으로 묶지 않는다. 작은 read 사이에 동시 write가 발생한 경우에도 열린 file별 snapshot을 유지하지 않는다. 예제 실행 계약은 writer 하나, client 하나다.

실제 DMA·IRQ·MMIO·하드웨어 completion은 이 모듈에 구현되어 있지 않다. Kernel 내부 접근 실패와 일반 process 오류를 분리해 다루는 I/O 예제다.
