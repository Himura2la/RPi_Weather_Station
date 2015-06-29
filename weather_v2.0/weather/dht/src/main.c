#include "pi_dht_read.h"
#include <stdio.h>

float t, h;
int result;
int testrun() {
    result = pi_dht_read(22, 23, &h, &t);
    printf("Result: %d\n", result);
    printf("t:%6.3f\tH:%6.3f\n", t, h);
}


int main() {
    testrun();
    return 0;
}