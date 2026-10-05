// Problema 1: O(n^2 log n)
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
long long function_p1(long long n) {
    long long i, j, k, counter = 0;
    for (i = n/2; i <= n; i++)
        for (j = 1; j + n/2 <= n; j++)
            for (k = 1; k <= n; k = k*2)
                counter++;
    return counter;
}
int main(int argc, char **argv) {
    long long n = atoll(argv[1]);
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    long long c = function_p1(n);
    clock_gettime(CLOCK_MONOTONIC, &b);
    double t = (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9;
    printf("%lld,%lld,%.9f\n", n, c, t);
    return 0;
}
