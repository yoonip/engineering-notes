// 경계 타일까지 처리하는 FP32 행렬곱과 독립적인 CPU 기준해를 실행한다.
#include <cuda_runtime.h>
#include <algorithm>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

static void check(cudaError_t status) {
    if (status != cudaSuccess) throw std::runtime_error(cudaGetErrorString(status));
}

struct DeviceBuffer {
    float* data = nullptr;
    explicit DeviceBuffer(size_t count) { check(cudaMalloc(&data, count * sizeof(float))); }
    ~DeviceBuffer() { if (data) cudaFree(data); }
    DeviceBuffer(const DeviceBuffer&) = delete;
    DeviceBuffer& operator=(const DeviceBuffer&) = delete;
};

struct Event {
    cudaEvent_t value;
    Event() { check(cudaEventCreate(&value)); }
    ~Event() { cudaEventDestroy(value); }
};

template<int T>
__global__ void multiply(const float* a, const float* b, float* c, int m, int n, int k) {
    __shared__ float left[T][T];
    __shared__ float right[T][T];
    const int x = threadIdx.x, y = threadIdx.y;
    const int row = blockIdx.y * T + y, column = blockIdx.x * T + x;
    float total = 0;
    for (int start = 0; start < k; start += T) {
        // 경계 밖의 lane도 동기화에 참여하며 값만 0으로 채운다.
        left[y][x] = row < m && start + x < k ? a[row*k + start + x] : 0;
        right[y][x] = start + y < k && column < n ? b[(start+y)*n + column] : 0;
        __syncthreads();
        for (int inner = 0; inner < T; ++inner) total += left[y][inner] * right[inner][x];
        // 다음 타일이 현재 공유 값을 덮기 전에 모든 읽기를 끝낸다.
        __syncthreads();
    }
    if (row < m && column < n) c[row*n + column] = total;
}

static int dimension(const char* text) {
    std::string source(text);
    size_t consumed = 0;
    int value = std::stoi(source, &consumed);
    if (consumed != source.size() || value < 1 || value > 2048)
        throw std::invalid_argument("행렬 차원은 1~2048이어야 합니다");
    return value;
}

int main(int argc, char** argv) {
    try {
        if (argc != 1 && argc != 4) throw std::invalid_argument("실행 형식: tiled_matmul [M N K]");
        const int m = argc == 4 ? dimension(argv[1]) : 37;
        const int n = argc == 4 ? dimension(argv[2]) : 45;
        const int k = argc == 4 ? dimension(argv[3]) : 29;
        std::vector<float> a(size_t(m)*k), b(size_t(k)*n), result(size_t(m)*n);
        for (int i = 0; i < m; ++i) for (int p = 0; p < k; ++p)
            a[size_t(i)*k+p] = float((i*3+p)%11-5)/7;
        for (int p = 0; p < k; ++p) for (int j = 0; j < n; ++j)
            b[size_t(p)*n+j] = float((p+2*j)%7-3)/5;
        DeviceBuffer da(a.size()), db(b.size()), dc(result.size());
        check(cudaMemcpy(da.data,a.data(),a.size()*sizeof(float),cudaMemcpyHostToDevice));
        check(cudaMemcpy(db.data,b.data(),b.size()*sizeof(float),cudaMemcpyHostToDevice));
        const dim3 block(16,16), grid((n+15)/16,(m+15)/16);
        multiply<16><<<grid,block>>>(da.data,db.data,dc.data,m,n,k);
        check(cudaGetLastError());
        check(cudaDeviceSynchronize());
        Event start,stop;
        const int repetitions = 5;
        check(cudaEventRecord(start.value));
        for (int repeat = 0; repeat < repetitions; ++repeat)
            multiply<16><<<grid,block>>>(da.data,db.data,dc.data,m,n,k);
        check(cudaGetLastError());
        check(cudaEventRecord(stop.value));
        check(cudaEventSynchronize(stop.value));
        float milliseconds = 0;
        check(cudaEventElapsedTime(&milliseconds,start.value,stop.value));
        check(cudaMemcpy(result.data(),dc.data,result.size()*sizeof(float),cudaMemcpyDeviceToHost));
        double max_error = 0;
        int failures = 0;
        for (int i = 0; i < m; ++i) for (int j = 0; j < n; ++j) {
            double expected = 0;
            for (int p = 0; p < k; ++p) expected += double(a[size_t(i)*k+p])*double(b[size_t(p)*n+j]);
            const double error = std::abs(double(result[size_t(i)*n+j])-expected);
            max_error = std::max(max_error,error);
            if (!std::isfinite(result[size_t(i)*n+j]) || error > 2e-4 + 2e-4*std::abs(expected)) ++failures;
        }
        std::cout << "{\"m\":" << m << ",\"n\":" << n << ",\"k\":" << k
                  << ",\"max_absolute_error\":" << max_error
                  << ",\"failed_elements\":" << failures
                  << ",\"kernel_ms_per_run\":" << milliseconds/repetitions
                  << ",\"transfer_in_timing\":false}\n";
        return failures ? 1 : 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << "\n";
        return 2;
    }
}
