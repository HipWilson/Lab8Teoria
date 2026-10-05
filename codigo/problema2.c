// Problema 2: O(n)  (el printf se cuenta con un contador para no medir la E/S)
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
long long function_p2(long long n) {
    long long i, j, counter = 0;
    if (n <= 1) return 0;
    for (i = 1; i <= n; i++)
        for (j = 1; j <= n; j++) {
            counter++;   /* equivale a printf("Sequence\n") */
            break;
        }
    return counter;
}
int main(int argc, char **argv) {
    long long n = atoll(argv[1]);
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    long long c = function_p2(n);
    clock_gettime(CLOCK_MONOTONIC, &b);
    double t = (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9;
    printf("%lld,%lld,%.9f\n", n, c, t);
    return 0;
}
