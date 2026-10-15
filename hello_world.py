#!/usr/bin/env python3
"""Minimal, dependency-free hello-world example for GAAS pilot testing."""

import socket


def main():
    print("Hello, World!")
    print(f"Running on host: {socket.gethostname()}")


if __name__ == "__main__":
    main()
