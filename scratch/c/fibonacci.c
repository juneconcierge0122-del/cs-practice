// gcc -std=c99 -Wall -o fib fibonacci.c

#include <stdio.h>
#include <stdlib.h>

void fibonacci(int n){
    unsigned long long first=0, second=1;

    for(int i=0;i<n;i++){
        printf("%llu\n", first);
        long long next = first +second;
        if (next < second){ //wrapped
            printf("overflow after F(%d)\n", i);
            return;
        }

        first = second;
        second = next;
    }

}

int main(){
    int number;
    printf("Choose a Number for Fibonacci:");
    scanf("%d", &number);
    fibonacci(number);
    return 0;
}
