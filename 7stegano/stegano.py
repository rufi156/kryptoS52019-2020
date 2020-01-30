#!/usr/bin/env python3
import argparse, sys, os, re
from bs4 import BeautifulSoup

#TODO: one write call per option, then nthOptionFunction()

# s = "text"
#  str > hex
# h = s.encode().hex()
# h = bytes.hex(s.encode())
#  hex > bin
# bi = bin(int(h, 16))[2:]
#  bin > hex
# reh = hex(int(bi, 2))[2:]
#  hex > str
# res = bytes.fromhex(reh).decode()
# res = reh.encode().fromhex(reh).decode()

ORIG = "orig.txt"
MESSAGE = "mess.txt"
WEB = "cover.html"
WATER = "watermark.html"
REMESS = "detect.txt"


def prepareText(inFile, outFile):
    with open(inFile, "a+") as orig, open(outFile, "a+") as message:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to prepare in {}".format(inFile))
        orig.seek(0)
        message.truncate(0)
        content = orig.read()
        message.write(content.encode().hex())


def steganoEn(inFile, coverPage, outPage, mode = "1"):
    with open(inFile, "a+") as message, open(coverPage, "a+") as cover, open(outPage, "a+") as watermarked:
        if os.path.getsize(inFile) == 0 or os.path.getsize(coverPage) == 0:
            sys.exit("ERROR: no text to process in '{}' or '{}'".format(inFile, coverPage))
        message.seek(0)
        cover.seek(0)
        watermarked.truncate(0)
        binMsg = bin(int(message.read(), 16))[2:]
        binMsgLen = len(binMsg)
        if mode == "1":
            #eol spaces
            coverLines = cover.readlines()
            maxMsgLen = len(coverLines)
            if binMsgLen > maxMsgLen:
                sys.exit("ERROR: cover file too short/ message too long")
            startIndex = maxMsgLen - binMsgLen
            watermarked.writelines(coverLines[:startIndex])
            for line, bit in zip(coverLines[startIndex:], binMsg):
                if int(bit):
                    watermarked.write(line.rstrip("\n") + " \n")
                else:
                    watermarked.write(line)

        elif mode == "2":
            #double spaces
            maxMsgLen = 0
            for line in cover:
                for char in line:
                    if char == " ":
                        maxMsgLen += 1
            if binMsgLen > maxMsgLen:
                sys.exit("ERROR: cover file too short/ message too long")
            cover.seek(0)
            startIndex = maxMsgLen
            binIndex = binMsgLen
            for line in cover:
                for char in line:
                    if char == " ":
                        if startIndex == binMsgLen:
                            bit = binMsg[::-1][binIndex-1]
                            binIndex -= 1
                            if int(bit):
                                watermarked.write("  ")
                            else:
                                watermarked.write(" ")
                        else:
                            startIndex -= 1
                            watermarked.write(" ")
                    else:
                        watermarked.write(char)

        elif mode == "3":
            #<a style:line-height ..
            soup = BeautifulSoup(cover, "lxml")
            atags = soup.find_all("a")
            maxMsgLen = len(atags)
            if binMsgLen > maxMsgLen:
                sys.exit("ERROR: cover file too short/ message too long")
            for bit, tag in zip(binMsg, atags):
                if int(bit):
                    tag.attrs["style"] = "lineheight: 100%"
                else:
                    tag.attrs["style"] = "line-height: 100%"
            watermarked.write(str(soup))

        elif mode == "4":
            # 1 = <a to <a></a><a
            # 0 = /> to /><a></a>
            soup = BeautifulSoup(cover, "lxml")
            atags = soup.find_all("a")
            maxMsgLen = len(atags)
            if binMsgLen > maxMsgLen:
                sys.exit("ERROR: cover file too short/ message too long")
            for bit, tag in zip(binMsg, atags):
                if int(bit):
                    newTag = soup.new_tag("a")
                    tag.insert_before(newTag)
                else:
                    newTag = soup.new_tag("a")
                    tag.insert_after(newTag)
            watermarked.write(str(soup))

def steganoDe(inFile, outFile, mode = "1"):
    with open(inFile, "a+") as waterpage, open(outFile, "a+") as message:
        if os.path.getsize(inFile) == 0:
            sys.exit("ERROR: no text to process in '{}'".format(inFile))
        waterpage.seek(0)
        message.truncate(0)
        binMsg = ""
        if mode == "1":
            waterLines = waterpage.readlines()
            for line in waterLines:
                if line.rstrip("\n").endswith(" "):
                    binMsg += "1"
                else:
                    binMsg += "0"

        elif mode == "2":
            doubleSpace = False
            for line in waterpage:
                for char in line:
                    if char == " ":
                        if doubleSpace:
                            binMsg += "1"
                            doubleSpace = False
                        else:
                            doubleSpace = True
                    elif doubleSpace:
                        binMsg += "0"
                        doubleSpace = False
                    else:
                        doubleSpace = False

        elif mode == "3":
            soup = BeautifulSoup(waterpage, "lxml")
            atags = soup.find_all(lambda tag: tag.name == "a" and tag.has_attr("style"))
            for tag in atags:
                if tag.attrs["style"] == "lineheight: 100%":
                    binMsg += "1"
                elif tag.attrs["style"] == "line-height: 100%":
                    binMsg += "0"

        elif mode == "4":
            soup = BeautifulSoup(waterpage, "lxml")
            atags = soup.find_all("a")
            emptyTags = soup.find_all(lambda tag : tag.name =="a" and tag.string == None and len(tag.attrs) == 0)
            msgLen = len(emptyTags)
            for i, (tag1, tag2) in enumerate(zip(atags[::2], atags[1::2])):
                if i >= msgLen:
                    break
                if tag1.string == None and len(tag1.attrs) == 0:
                    binMsg += "1"
                elif tag2.string == None and len(tag2.attrs) == 0:
                    binMsg += "0"
                else:
                    break

        message.write(hex(int(binMsg, 2))[2:])


def main(args):
    modeList = [k for k, v in vars(args).items() if v]
    if "p" in modeList:
        prepareText(ORIG, MESSAGE);
    if "e" in modeList:
        steganoEn(MESSAGE, WEB, WATER, modeList[1])
    elif "d" in modeList:
        steganoDe(WATER, REMESS, modeList[1])
    else:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode/decode steganographicly")
    actionType = parser.add_mutually_exclusive_group(required=True)
    actionType.add_argument("-p", action="store_true", help="prepare message")
    actionType.add_argument("-e", action="store_true", help="encode")
    actionType.add_argument("-d", action="store_true", help="decode")
    algorithm = parser.add_mutually_exclusive_group(required=False)
    algorithm.add_argument("-1", action="store_true", help="eol space algorithm")
    algorithm.add_argument("-2", action="store_true", help="double space algorithm")
    algorithm.add_argument("-3", action="store_true", help="fake atributes typo algorithm ")
    algorithm.add_argument("-4", action="store_true", help="excessive tag open/close algorithm")
    args = parser.parse_args()
    main(args)
