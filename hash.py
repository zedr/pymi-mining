#!/usr/bin/env python3

import sys
import hashlib


def mine(text: str, difficulty: int, nonce: int = 0) -> None:
    while True:
        print(f"Trying nonce: {nonce}...")
        hsh = hashlib.md5(f"{nonce}{text}".encode()).hexdigest()
        if hsh[:difficulty] == "0" * difficulty:
            print(f"Mined! {nonce} {hsh}")
            break
        nonce += 1


def main():
    text = sys.argv[1]
    difficulty = int(sys.argv[2])
    mine(text, difficulty)    


if __name__ == "__main__":
    main()
