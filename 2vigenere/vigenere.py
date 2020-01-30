#!/usr/bin/env python3
import argparse, sys, os, re


def getKey(keyFile):
    with open(keyFile, "a+") as key:
        key.seek(0)
        if os.path.getsize(keyFile) == 0:
            sys.exit("ERROR: no key in '{}'".format(keyFile))
        key = re.sub(r'[^a-zA-Z]', "", key.read()).lower()
        keyList = [ord(x)-ord("a") for x in key]
        return keyList

def vigenere(keyList, inFile, outFile, mode="e"):
    with open(inFile, "a+") as a, open(outFile, "a+") as out:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to process in '{}'".format(inFile))
        a.seek(0)
        out.truncate(0)
        i = 0
        for line in a:
            for letter in line:
                if mode == "d":
                    key = -keyList[i%(len(keyList))]
                else:
                    key = keyList[i%(len(keyList))]
                translated = chr((ord(letter)-ord("a") + key)%26 + ord("a"))
                out.write(translated)
                i += 1

def prepareText(inFile, outFile):
    with open(inFile, "a+") as orig, open(outFile, "a+") as plain:
        orig.seek(0)
        plain.truncate(0)
        #orig = re.sub(r'[^a-zA-Z]', "", orig.read()).lower()
        orig = "".join(letter.lower() for line in orig for letter in line if letter.isalpha())
        plain.write(orig)
    if os.path.getsize(outFile) == 0:
        sys.exit("ERROR: no text to encode in 'plain.txt'")

def calcIC(text):
    counts = [0] * 26
    totCount = 0
    for i in range(0, len(text)):
        counts[ord(text[i]) - ord("a")] += 1
        totCount += 1
    sum = 0
    for i in range(0, 26):
        sum = sum + counts[i] * (counts[i] - 1)
    ic = sum / (totCount * (totCount - 1))
    return ic

def extractKeyLength(inFile):
    with open(inFile, "a+") as crypto:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to process in '{}'".format(inFile))
        crypto.seek(0)
        crypto = crypto.read()
        #1 znajdz dlugosc klucza
        keyLen = 0
        #testing2 IClist = []
        for n in range(6, 13):
            localIC = []
            #testig print("keyLen: {}".format(n))
            for i in range(1, n+1):
                #testing print("skok co {}".format(i))
                newText = "".join(crypto[i-1::n])
                #testing print(newText)
                localIC.append(calcIC(newText))
            avgIC = sum(localIC)/n
            #testing2 IClist.append(avgIC)
            if avgIC >= 0.06:
                keyLen = n
        if keyLen > 0:
            return keyLen
        else:
            sys.exit("ERROR: key length not found")

            #testing2 for i in range(0, len(IClist[:20])):
            #testing2    print("i: {} IC: {}\n".format(i, IClist[i]))

def extractKeyLength2(inFile):
    with open(inFile, "a+") as crypto:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to process in '{}'".format(inFile))
        crypto.seek(0)
        crypto = crypto.read()
        keyLen = 0
        for n in range(1, 13):
            ic = calcIC(crypto[::n])
            if ic >= 0.06:
                keyLen = n
                break
        if keyLen > 0:
            return keyLen
        else:
            sys.exit("ERROR: key length not found")

def freqAnalysis(keyLen, inFile, keyFile):
    with open(inFile, "a+") as crypto, open(keyFile, "a+") as keyFile:
        crypto.seek(0)
        keyFile.truncate(0)
        crypto = crypto.read()

        engFreq = [82, 15, 28, 43, 127, 22, 20, 61, 70, 2, 8, 40, 24, 67, 75, 29, 1, 60, 63, 91, 28, 10, 23, 1, 20, 1]
        key = ""
        for n in range(0, keyLen):
            alphaFreq = [0] * 26
            totCount = 1
            text = crypto[n::keyLen]
            #frequency for each ceasar cypher encoded with n
            for i in range(0, len(text)):
                alphaFreq[ord(text[i]) - ord("a")] += 1
                totCount += 1
            for i in range(0, 26):
                alphaFreq[i] = alphaFreq[i]/totCount * 1000

            #Scalar Multiplication 'SM' of cypher alphabet with rotated english alphabet
            smList = []
            suma = 0
            for r in range(0, 26):
                suma = sum(list(map(lambda x,y : x*y, engFreq, (alphaFreq[r:] + alphaFreq[:r]))))
                #print("{} {}".format(r, suma))
                smList.append(suma)
            shift = smList.index(max(smList))
            key += chr(shift + ord("a"))

        keyFile.write(key)



def main(args):
    modeList = [k for k, v in vars(args).items() if v]

    if "p" in modeList:
        prepareText("orig.txt", "plain.txt")
    elif "e" in modeList:
        key = getKey("key.txt")
        vigenere(key, "plain.txt", "crypto.txt")
    elif "d" in modeList:
        key = getKey("key.txt")
        vigenere(key, "crypto.txt", "decrypt.txt", "d")
    elif "k" in modeList:
        if "a" in modeList:
            keyLen = extractKeyLength("crypto.txt")
        else:
            keyLen = extractKeyLength2("crypto.txt")
        freqAnalysis(keyLen, "crypto.txt", "key-crypto.txt")
        key = getKey("key-crypto.txt")
        vigenere(key, "crypto.txt", "decrypt.txt", "d")
    else:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode/decode/cryptanalyse Vigenere cypher")
    actionType = parser.add_mutually_exclusive_group(required=True)
    actionType.add_argument("-p", action="store_true", help="prepare text for encoding")
    actionType.add_argument("-e", action="store_true", help="encode")
    actionType.add_argument("-d", action="store_true", help="decode")
    actionType.add_argument("-k", action="store_true", help="cyptanalysis without text")
    actionType = parser.add_mutually_exclusive_group(required=False)
    actionType.add_argument("-a", action="store_true", help="keyLength based on avg IC")
    args = parser.parse_args()
    main(args)
