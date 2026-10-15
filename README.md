# Hello World

A minimal Python + PBS project for GAAS onboarding pilot tests.

## Files

- `hello_world.py` — prints a greeting and the hostname.
- `hello_world.pbs` — submits the Python program as a small PBS job.
- `output/output1.txt` and `output2.txt` — synthetic example output files.

## Run locally

```bash
python3 hello_world.py
```

## Run through PBS on GAAS

After placing this project in an approved GAAS working directory and checking
site-specific queue/account requirements:

```bash
qsub hello_world.pbs
```

This project uses only Python's standard library.
