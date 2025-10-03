## safe exam browser
Description:
```
i love academic misconduct
```

## solution
`decode_flag()` calls `op()`, which checks `/proc` and exits if any other processes are running.
This can be bypassed by patching `op()` to just immediately return `1`. Alternatively, you could run the program in a chroot jail with a fake `/proc` directory.

The flag can then be obtained by inspecting the register values in GDB after `decode_flag()` is called in `main()`.

`decode_flag()` is heavily obfuscated, so reversing it direcly is unlikely to be fruitful.

## flag
<details>
    <summary>Click to reveal</summary>

    K17{i_heard_that_it's_impossible_to_re_c++!}
</details>