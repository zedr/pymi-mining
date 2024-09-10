#!/usr/bin/env python3

import sys
import hashlib


def md5hash(s: str) -> str:
    """Get the md5 hash of the given string"""
    return hashlib.md5(s.encode()).hexdigest()


def verify(hashed: str, difficulty: int) -> bool:
    """Verify the nonce of a transaction message"""
    return hashed[:difficulty] == "0" * difficulty


def mine(text: str, difficulty: int, begin_nonce: int) -> int:
    """Attempt to mine a transaction message"""
    nonce = 0
    while True:
        print(f"Trying nonce: {nonce}...")
        to_hash = f"{nonce}{text}"
        hashed = md5hash(to_hash)
        if verify(hashed, difficulty):
            print(f"Mined! {nonce} {hashed}")
            return nonce
        else:
            nonce += 1


def main():
    text = sys.argv[1]
    difficulty = int(sys.argv[2])
    mine(text, difficulty, 0)


if __name__ == "__main__":
    main()
