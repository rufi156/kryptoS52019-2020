#!/usr/bin/env python3
import argparse, sys, os, re, string
#TODO: pass file > pass file name; open as

def getKeySet(keyFile, mode="a"):
    keyFile.seek(0)
    keyList = keyFile.read().split()
    keyFile.seek(0)
    try:
        key1 = int(keyList[0])
        key2 = int(keyList[1])
    except IndexError:
        if mode == "c":
            key2 = 1
        else:
            key1 = -1
            key2 = -1
    if (key1 not in range(0, 27)) or (key2 not in [1,3,5,7,9,11,15,17,19,21,23,25]):
        sys.exit("ERROR: wrong key in key.txt\nkey.txt given: {}\nkey.txt expected format: '[number between 0-26]  [number coprime with 26: (1,3,5,7,9,11,15,17,19,21,23,25)]'".format(keyFile.read()))
    keySet = key1, key2
    return keySet

def getInverse(a):
    inverse = 0
    for i in range(0, 27):
        if (a*i)%26 == 1:
            inverse = i
    return inverse

def extractCezarKey(plain, crypto):
    plain.seek(0)
    crypto.seek(0)
    for line in plain:
        for symbol in line:
            if symbol.isalpha():
                plainSymbol = symbol
    for line in crypto:
        for symbol in line:
            if symbol.isalpha():
                cryptoSymbol = symbol
    key = ord(cryptoSymbol) - ord(plainSymbol)
    return key

def extractAffineKey(plain, crypto):
    plain.seek(0)
    crypto.seek(0)
    plainAlpha = re.sub(r'[^a-zA-Z]', "", plain.read()).upper()
    cryptoAlpha = re.sub(r'[^a-zA-Z]', "", crypto.read()).upper()
    i = 0
    m1 = ord(plainAlpha[i])-ord("A")
    m2 = ord(plainAlpha[i+1])-ord("A")
    while getInverse(m1 - m2) == 0:
        i += 1
        try:
            m1 = ord(plainAlpha[i])-ord("A")
            m2 = ord(plainAlpha[i+1])-ord("A")
            #print("m1={}\nm2={}".format(m1, m2))
        except IndexError:
            sys.exit("ERROR: More extra.txt text needed to calculate the key.")
    c1 = ord(cryptoAlpha[i])-ord("A")
    c2 = ord(cryptoAlpha[i+1])-ord("A")
    #a*m1 + b = c1
    #a*m2 + b = c2
    inverse = getInverse(m1 - m2)
    almosta = inverse * (c1 - c2)
    a = (inverse * (c1 - c2))%26
    b = (c1 - a * m1)%26
    #print("m1={}\nm2={}\nc1={}\nc2={}\n".format(m1, m2, c1, c2))
    #print("inverse = {} - {} ^-1 = {}".format(m1, m2, inverse))
    #print("a = {} * ({} - {}) mod26".format(inverse, c1, c2))
    #print("{} mod26 = {}".format(almosta, a))
    keySet = b, a
    #print(keySet)
    if inverse == 0:
        keySet = 0, 0
    if (b not in range(0, 27)) or (a not in [1,3,5,7,9,11,15,17,19,21,23,25]):
        keySet = 0, 0
    return keySet


def cezar(key, inFile, outFile):
    inFile.seek(0)
    for line in inFile:
        for symbol in line:
            translated = ""
            if symbol.isalpha():
                newSymbol = ord(symbol)+key
                if (symbol.isupper() and newSymbol > ord("Z")) or (symbol.islower() and newSymbol > ord("z")):
                    translated = chr(newSymbol-26)
                elif (symbol.isupper() and newSymbol < ord("A")) or (symbol.islower() and newSymbol < ord("a")):
                    translated = chr(newSymbol+26)
                else:
                    translated = chr(newSymbol)
            else:
                translated = symbol
            outFile.write(translated)
    outFile.write("\n")

def affine(keySet, inFile, outFile, mode="e"):
    N = [x for x in range(0, 26)]
    L = [x for x in string.ascii_lowercase]
    A = dict(zip(N, L))
    a = keySet[1]
    b = keySet[0]
    if mode == "d":
        b = -b
        a = getInverse(a)
    inFile.seek(0)
    for line in inFile:
        for symbol in line:
            translated = ""
            if symbol.isalpha():
                if symbol.isupper() and mode == "e":
                    newSymbol = ((a* (ord(symbol)-ord("A")) +b) %26)+ord("A")
                elif symbol.isupper() and mode == "d":
                    newSymbol = ((a* ((ord(symbol)-ord("A")) +b)) %26)+ord("A")
                elif symbol.islower() and mode == "e":
                    newSymbol = ((a* (ord(symbol)-ord("a")) +b) %26)+ord("a")
                elif symbol.islower() and mode == "d":
                    newSymbol = ((a* ((ord(symbol)-ord("a")) +b)) %26)+ord("a")
                else:
                    pass
                translated = chr(newSymbol)
            else:
                translated = symbol
            outFile.write(translated)
    outFile.write("\n")


def main(args):
    modeList = [k for k, v in vars(args).items() if v]

    if "e" in modeList:
        keyFile = open("key.txt", "a+")
        plain = open("plain.txt", "a+")
        if os.path.getsize("key.txt") != 0 and os.path.getsize("plain.txt") != 0:
            crypto = open("crypto.txt", "a+")
            crypto.truncate(0)
            if "c" in modeList:
                keySet = getKeySet(keyFile, "c")
                cezar(keySet[0], plain, crypto)
            else:
                keySet = getKeySet(keyFile)
                affine(keySet, plain, crypto)
            keyFile.close()
            plain.close()
            crypto.close()
        else:
            keyFile.close()
            plain.close()
            sys.exit("ERROR: no key in 'key.txt' or no text in 'plain.txt'")
    elif "d" in modeList:
        keyFile = open("key.txt", "a+")
        crypto = open("crypto.txt", "a+")
        if os.path.getsize("key.txt") != 0 and os.path.getsize("crypto.txt") != 0:
            plain = open("plain.txt", "a+")
            plain.truncate(0)
            if "c" in modeList:
                keySet = getKeySet(keyFile, "c")
                cezar(-keySet[0], crypto, plain)
            else:
                keySet = getKeySet(keyFile)
                affine(keySet, crypto, plain, "d")
            keyFile.close()
            crypto.close()
            plain.close()
        else:
            keyFile.close()
            crypto.close()
            sys.exit("ERROR: no key in 'key.txt' or no text in 'crypto.txt'")
    elif "k" in modeList:
        crypto = open("crypto.txt", "a+")
        if os.path.getsize("crypto.txt") != 0:
            plain = open("plain.txt", "a+")
            plain.truncate(0)
            if "c" in modeList:
                for i in range(1, 26):
                    plain.write("{} ".format(i))
                    cezar(-i, crypto, plain)
            else:
                for a in [1,3,5,7,9,11,15,17,19,21,23,25]:
                    for b in range(0, 26):
                        keySet = b, a
                        plain.write("{} {} ".format(b, a))
                        affine(keySet, crypto, plain, "d")
            crypto.close()
            plain.close()
        else:
            crypto.close()
            sys.exit("ERROR: no text in 'crypto.txt'")
    elif "j" in modeList:
        crypto = open("crypto.txt", "a+")
        extra = open("extra.txt", "a+")
        if os.path.getsize("crypto.txt") != 0 and os.path.getsize("extra.txt") != 0:
            keyNew = open("key-new.txt", "a+")
            keyNew.truncate(0)
            decrypt = open("decrypt.txt", "a+")
            decrypt.truncate(0)
            if "c" in modeList:
                key = extractCezarKey(extra, crypto)
                keyNew.write("{}".format(key))
                cezar(-key, crypto, decrypt)
            else:
                keySet = extractAffineKey(extra, crypto)
                if keySet == (0, 0):
                    crypto.close()
                    extra.close()
                    keyNew.close()
                    decrypt.close()
                    sys.exit("ERROR: key imposible to extract")
                else:
                    keyNew.write("{} {}".format(keySet[0], keySet[1]))
                    affine(keySet, crypto, decrypt, "d")
            crypto.close()
            extra.close()
            keyNew.close()
            decrypt.close()
        else:
            crypto.close()
            extra.close()
            sys.exit("ERROR: no text in 'crypto.txt' or in 'extra.txt'")
    else:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode/decode/cryptanalyse Cezar or affine cypher")
    cypherType = parser.add_mutually_exclusive_group(required=True)
    cypherType.add_argument("-c", action="store_true", help="use cezar cypher")
    cypherType.add_argument("-a", action="store_true", help="use affine cypher")
    actionType = parser.add_mutually_exclusive_group(required=True)
    actionType.add_argument("-e", action="store_true", help="encode")
    actionType.add_argument("-d", action="store_true", help="decode")
    actionType.add_argument("-k", action="store_true", help="cryptanalysis without text")
    actionType.add_argument("-j", action="store_true", help="cyptanalysis with text")
    args = parser.parse_args()
    main(args)
