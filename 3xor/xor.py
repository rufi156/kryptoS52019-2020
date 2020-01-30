#!/usr/bin/env python3
import argparse, sys, os, re

LINE_LEN = 32
LINE_NO = 79

def prepareText(inFile, outFile):
    with open(inFile, "a+") as orig, open(outFile, "a+") as plain:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to prepare in {}".format(inFile))
        orig.seek(0)
        plain.truncate(0)
        orig = re.sub(r'[^a-zA-Z\s]', "", orig.read()).lower()
        orig = " ".join(orig.split()) #remove double spaces
        orig = orig[:LINE_LEN*(len(orig)//LINE_LEN)]

        i = 0
        j = LINE_LEN
        #l = 0
        while j <= len(orig):
            plain.write(orig[i:j])
            plain.write("\n")
            i = j
            j += LINE_LEN
            #l += 1
            #print(l)
        #parts = [orig[i:i+n] for i in range(0, length(orig), n)]
        #list(map(''.join, zip(*[iter(orig)]*LINE_LEN)))

def getKey(keyFile):
    with open(keyFile, "a+") as key:
        if os.path.getsize(keyFile) == 0:
            sys.exit("ERROR: no key in '{}'".format(keyFile))
        key.seek(0)
        key = re.sub(r'[^a-zA-Z\s]', "", key.read()).lower()
        return key

def xor(key, inFile, outFile, mode="e"):
    with open(inFile, "a+") as plain, open(outFile, "a+") as crypto:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to process in '{}'".format(inFile))
        plain.seek(0)
        crypto.truncate(0)

        plain = list(plain.read())
        del plain[LINE_LEN::LINE_LEN+1]
        line_count = (len(plain))//LINE_LEN
        #plain.seek(0)
        for l in range(line_count):
            line = plain[l*LINE_LEN:(l*LINE_LEN)+LINE_LEN] #plain.read(LINE_LEN+1)[:-1]
            for i in range(LINE_LEN):
                letter = chr(ord(line[i]) ^ ord(key[i]))
                crypto.write(letter)
            crypto.write("\n")

def xorBin(key, inFile, outFile, mode="e"):
    with open(inFile, "a+") as plain, open(outFile, "a+") as crypto:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to process in '{}'".format(inFile))
        plain.seek(0)
        crypto.truncate(0)
        line_count = plain.read().count("\n")
        plain.seek(0)
        for l in range(line_count):
            line = plain.readline()[:-1]
            if mode == "d":
                binList = line.split("b")[1:]
                for i in range(len(binList)):
                    letter = chr(int(binList[i], 2) ^ ord(key[i]))
                    crypto.write(letter)
                crypto.write("\n")
            else:
                for i in range(LINE_LEN):
                    letter = bin(ord(line[i]) ^ ord(key[i]))[1:] #0b0000 > remove head 0
                    crypto.write(letter)
                crypto.write("\n")

def cryptXorKey(keyLen, inFile, mode = "txt"):
    with open(inFile, "a+") as crypto:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to process in '{}'".format(inFile))
        crypto.seek(0)
        lines = []
        intLines = []
        if mode == "bin":
            lines = crypto.read().strip().split("\n")
            intLines = list(map(lambda line : [int(word, 2) for word in line.split("b")[1:]], lines))
        else:
            crypto = list(crypto.read())
            del crypto[LINE_LEN::LINE_LEN+1] #remove artificial '\n'
            line_count = (len(crypto))//LINE_LEN
            for l in range(line_count):
                line = crypto[l*LINE_LEN:(l*LINE_LEN)+LINE_LEN] #crypto.read(LINE_LEN+1)[:-1]
                lines.append(line)
            intLines = list(map(lambda line : [ord(word) for word in line], lines))
        #METHOD
        #xor intLines[0]..[LINE_LEN] with intLines[1]..[LINE_LEN] and make deductions?
        #look for word >= 64(s^l combo) ? digdeeper(word) : k, word = letter (ERROR)
        #digdeeper:
        # look for word ^ wordx[1:column_length, not 0] >=64(s^l) ?  k=l,word=s : k=s, word=l
        #digdeeperer:
        # look for wordx ^ wordx[1:column_length] >=64(s^l combo) ?
        key = ""
        for c in range(LINE_LEN):
            column = [line[c] for line in intLines]
            #column1 = [line[c] for line in intLines]
            noSpaceColumn = True
            for word in column:
                if word >= 64: #space^letter | letter^space
                    noSpaceColumn = False
                    #test print("word: {}".format(word))
                    for wordx in column:
                        if wordx == 0 or wordx == word: #space^space | letter^same letter OR word==wordx
                            continue
                        notFound = True
                        #test print("wordx: {}".format(wordx))
                        if (word ^ wordx) >= 64: #sl ^ x > sl when sl ^ ll, then key=letter, encodedletter=space
                            notFound = False
                            letter = chr(word ^ ord(" ")) #(space^letter)^space > letter
                            #test print("letter at :word ^ wordx: {} ^ {} is {}".format(word, wordx, letter))
                            key += letter
                            break
                        if notFound:
                            key += " "
                            #test print("' ' at word : {}".format(word))
                            break
                    break
            if noSpaceColumn:
                print("ERROR no space in column {}".format(c))
        return key

def makeKeyFile(key, keyFile):
    with open(keyFile, "a+") as keyf:
        keyf.truncate(0)
        keyf.write(key)

def main(args):
    modeList = [k for k, v in vars(args).items() if v]
    if "p" in modeList:
        prepareText("orig.txt", "plain.txt")
    elif "e" in modeList:
        key = getKey("key.txt")
        if "b" in modeList:
            xorBin(key, "plain.txt", "crypto_bin.txt")
        else:
            xor(key, "plain.txt", "crypto.txt")
    elif "d" in modeList:
        key = getKey("key.txt")
        if "b" in modeList:
            xorBin(key, "crypto_bin.txt", "decrypt.txt", "d")
        else:
            xor(key, "crypto.txt", "decrypt.txt", "d")
    elif "k" in modeList:
        key = ""
        if "klucz" and "b" in modeList:
            key = cryptXorKey(LINE_LEN, "crypto_bin.txt", "bin")
            makeKeyFile(key, "key-crypt.txt")
            xorBin(key, "crypto_bin.txt", "decrypt.txt", "d")
        elif "klucz" in modeList:
            key = cryptXorKey(LINE_LEN, "crypto.txt", "txt")
            makeKeyFile(key, "key-crypt.txt")
            xor(key, "crypto.txt", "decrypt.txt", "d")
        elif "b" in modeList:
            key = cryptXorKey(LINE_LEN, "crypto_bin.txt", "bin")
            xorBin(key, "crypto_bin.txt", "decrypt.txt", "d")
        else:
            key = cryptXorKey(LINE_LEN, "crypto.txt", "txt")
            xor(key, "crypto.txt", "decrypt.txt", "d")
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
    actionType.add_argument("-b", action="store_true", help="binary file cryptanalysis")
    actionType = parser.add_mutually_exclusive_group(required=False)
    actionType.add_argument("-klucz", action="store_true", help="add crypto-key file")
    args = parser.parse_args()
    main(args)
