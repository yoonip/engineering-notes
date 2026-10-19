#include <stddef.h>
// freestanding 컴파일러도 구조체/배열 초기화를 memset/memcpy로 낮출 수 있다.
// libc 없는 이미지이므로 필요한 runtime 함수를 제공한다. -fno-builtin과 함께 사용.
void *memset(void *dest, int value, size_t n)
{
    unsigned char *p=dest;
    for (size_t i=0;i<n;i++) p[i]=(unsigned char)value;
    return dest;
}
void *memcpy(void *dest, const void *src, size_t n)
{
    unsigned char *d=dest; const unsigned char *s=src;
    for (size_t i=0;i<n;i++) d[i]=s[i];
    return dest; // 겹치는 영역에는 memcpy 대신 memmove가 필요하지만 여기엔 사용 안 함.
}
