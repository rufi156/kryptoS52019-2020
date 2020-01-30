#!/usr/bin/env python3
import sys, os, re
from PIL import Image
import hashlib
#TODO
#-remove PIL
#-ask about CBC


imgFile = "plain.bmp"
ECBoutFile = "ecb_crypto.bmp"
CBCoutFile = "cbc_crypto.bmp"
keyFile = "key.txt"

blockSize = (5,4) #ONLY even divisors of img width and height
IV = [125,185,223,206,91,8,249,232,243,218,89,202,159,155,236,61,96,52,249,195] #length of blockSize[0] * blockSize[1]



def getKey(keyFile):
    with open(keyFile, "a+") as key:
        if os.path.getsize(keyFile) == 0:
            sys.exit("ERROR: no key in '{}'".format(keyFile))
        key.seek(0)
        key = re.sub(r'\s+', ' ', key.read().strip())
        key = [int(x) for x in key.split(" ")]
        keyLength = blockSize[0] * blockSize[1]
        if len(key) != keyLength:
            sys.exit("ERROR: key must be {} bytes long".format(keyLength))
        return key

def streamify(blockArray, imgSize):
    blockColumns = imgSize[0]//blockSize[0]
    blockRows = imgSize[1]//blockSize[1]
    endArray = []
    for k in range(blockRows):
        for j in range(len(blockArray[0])):
            for i in range(blockColumns*k, (blockColumns*k)+blockColumns):
                endArray.append(blockArray[i][j])
    endByteArray = []
    for i in range(len(endArray)):
        endByteArray += endArray[i]
    return endByteArray

def blockify(pixelArray, imgSize):
    imgLinesArray = [pixelArray[i:i + imgSize[0]] for i in range(0, len(pixelArray), imgSize[0])]
    blockArray = [] #100x120blocks
    for k in range((imgSize[1]//blockSize[1])): #for each of 120 block rows
        for i in range((imgSize[0]//blockSize[0])): #for each of 100 block columns
            block = []
            for j in range(k*blockSize[1], (k*blockSize[1])+blockSize[1]):  #0-3, 3-6, 6-9
                block.append(imgLinesArray[j][blockSize[0]*i:(blockSize[0]*i)+blockSize[0]]) #0-5, 5-10, 10-15
            blockArray.append(block)
    return blockArray

def singleBlockToStream(block):
    stream = []
    for i in range(len(block)):
        stream += block[i]
    return stream

def streamToSingleBlock(stream):
    block = [stream[i:i + blockSize[0]] for i in range(0, len(stream), blockSize[0])]
    return block


def ECBencrypt(blockArray, key):
    newBlockArray = []
    for block in blockArray:
        blockStream = singleBlockToStream(block)

        #encrypt (F(k, m1) = k XOR m1) stream with key
        blockStream = list(map(lambda x,y: (x^y)%256, blockStream, key))

        singleBlock = streamToSingleBlock(blockStream)
        newBlockArray.append(singleBlock)
    return newBlockArray

def CBCencrypt(blockArray, key):
    newBlockArray = []
    previousStream = IV
    for block in blockArray:
        blockStream = singleBlockToStream(block)

        #xor with previous crypt
        blockStream = list(map(lambda x,y: (x^y)%256, blockStream, previousStream))

        #apply encode function
        blockStream = list(map(lambda x,y: (x^y)%256, blockStream, key))

        #NOW:finishing is done in main() after img reassembly
        #or: SHA1 each pixel
        #blockStream = list(map(lambda x: int(hashlib.sha1(str(x).encode()).hexdigest(), 16)%256, blockStream))

        #pass results to next block calculation
        previousStream = blockStream

        singleBlock = streamToSingleBlock(blockStream)
        newBlockArray.append(singleBlock)
    return newBlockArray


def main():
    key = getKey(keyFile)

    img = Image.open(imgFile)
    img = img.convert("L")
    imgSize = img.size #(400,360)

    pixelArray = list(img.getdata()) #1 byte for monochrome, 3channel tuple for RGB
    blockArray = blockify(pixelArray, imgSize)

    #ECB
    ECBblockArray = ECBencrypt(blockArray, key)

    byteStreamArray = streamify(ECBblockArray, imgSize)
    tobytes = bytes(byteStreamArray)

    img2 = Image.frombytes("L", (400, 360), tobytes)
    img2 = img2.convert("1", dither=Image.NONE)
    img2.save(ECBoutFile)

    #CBC
    CBCblockArray = CBCencrypt(blockArray, key)

    byteStreamArray = streamify(CBCblockArray, imgSize)
    tobytes = bytes(byteStreamArray)

    #QUICKFIX transposition to finish encoding
    #or comment out if using SHA1 in CBCencrypt()
    img2 = Image.frombytes("L", (400, 360), tobytes)
    tobytes = bytes(streamify(CBCencrypt(CBCencrypt(blockify(list(img2.rotate(90).getdata()), imgSize), key), key), imgSize))

    img2 = Image.frombytes("L", (400, 360), tobytes)
    img2 = img2.convert("1", dither=Image.NONE)
    img2.save(CBCoutFile)


if __name__ == "__main__":
    main()
