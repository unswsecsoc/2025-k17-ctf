- The challenge involved a struct Person with fields for name and age, plus a function pointer used to "introduce" the person by printing their details.

- The struct was marked as packed, meaning the fields were laid out contiguously in memory without padding for alignment. 

- A vulnerability was introduced because scanf read a long long (%lld) into the char age field. This wrote 8 bytes instead of 1, overflowing into the adjacent func pointer.

- By providing the address of win left shifted by one byte, we could overwrite the func pointer with the address of win(), causing the program to call win() instead of print_greeting().

```c
struct person {
    char name[32];
    char age;
    void (*func)();
} __attribute__((packed));

...

scanf(" %lld", &c.age);

``` 

