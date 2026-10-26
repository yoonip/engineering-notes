cmake_minimum_required(VERSION 3.16) # 예제에서 사용하는 CMake 기능의 하한
project(systemc_fifo_demo LANGUAGES CXX) # C++로 실행하는 SystemC 예제
find_package(SystemCLanguage CONFIG REQUIRED) # 별도 설치한 SystemC 패키지 검색
add_executable(fifo_demo example.cpp) # 실제 시뮬레이션 실행 파일 생성
target_link_libraries(fifo_demo PRIVATE SystemC::systemc) # 이벤트 커널과 채널 구현 연결
target_compile_features(fifo_demo PRIVATE cxx_std_17) # SystemC 3 계열과 맞춘 C++17
