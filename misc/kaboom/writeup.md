### brief writeup:
- Need to overflow a 20_000_000 byte buffer with a zip file of at most 1994 bytes (all files in the zip get concatenated)
- Use repeated central directory headers for the same file contents to increase the unzipped size
- These params
```py
MAX_UNCOMPRESSED_SIZE = 1000001
NUM_FILES = 20
```
give us 20000020 bytes total, so a 20 byte overflow.

Since we have
```c
struct zip_action {
    char unzipped[MAX_UNZIPPED_SIZE];
    char *(*fn)(const char *, size_t);
    size_t fn_arg;
};
```
we want to overwrite `fn` with `system`, so we need the unzipped data to end with `p64(system)` + 12 padding bytes
- Make the unzipped data start with "sh\x00" since it's passed to `fn`

### running
```sh
python3 ./soln/makezip.py
python3 ./soln/exploit.py
```

`makezip.py` is based on https://www.bamsoftware.com/hacks/zipbomb/ and https://www.bamsoftware.com/git/zipbomb.git