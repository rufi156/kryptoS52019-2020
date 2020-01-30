#!/usr/bin/env python3
import os
from collections import OrderedDict
#not in bash cause it cant handle long bin/int

HASH_DICT = OrderedDict([(128,"md5sum"),
                         (160,"sha1sum"),
                         (224,"sha224sum"),
                         (256,"sha256sum"),
                         (384,"sha384sum"),
                         (512,"sha512sum")])
bash_setup = ("cat hash.pdf personal.txt | {} > hash1.txt\n"
              "cat hash.pdf personal_.txt | {} > hash2.txt")
bash_cleanup = "rm hash1.txt hash2.txt"
output_intro = "Wykonywane polecenia i wyniki:\n\n"
output_main = ("cat hash.pdf personal.txt | {}\n"
              "cat hash.pdf personal_.txt | {}\n"
              "{}\n"
              "{}\n"
              "Liczba bitow rozniaca wyniki: {} tj. {}% z {}\n\n")

def main():
    with open("diff.txt", "w+") as d:
        d.write(output_intro)
        for key, value in HASH_DICT.items():
            os.system(bash_setup.format(value, value))
            with open("hash1.txt", "a+") as h1, open("hash2.txt", "a+") as h2:
                h1.seek(0)
                h2.seek(0)
                h1 = h1.read()[:key//4]
                h2 = h2.read()[:key//4]
                int1 = int(h1, 16)
                int2 = int(h2, 16)
                diff = bin(int1^int2)[2:].count("1")
                d.write(output_main.format(value, value, h1, h2, diff, ((diff/key*100)//1), key))
            os.system(bash_cleanup)

if __name__ == "__main__":
    main()
