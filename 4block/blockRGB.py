#!/usr/bin/env python3
import sys, os, re, random
from PIL import Image
#TODO
#remove PIL
#CBC doesnt work :(


imgFile = "plain.bmp"
ECBoutFile = "ecb_crypto.bmp"
CBCoutFile = "cbc_crypto.bmp"
keyFile = "key.txt"
#IV = [125, 185, 223, 206, 91, 8, 249, 232, 243, 218, 89, 202]
IV = [66,  126,  112,  173  , 65  ,129 , 230 , 125 ,  40, 151, 143 , 200 , 231 , 183 , 212 , 135 ,  89 , 172,  207 , 161,  120 , 244 ,  45,  206, 125, 185, 223, 206, 91, 8, 249, 232, 243, 218, 89, 202]
#IV = [255,255,0,255,0,255,0,0,255,255,0,255]
blockSize = (4,3)

def getKey(keyFile):
    with open(keyFile, "a+") as key:
        if os.path.getsize(keyFile) == 0:
            sys.exit("ERROR: no key in '{}'".format(keyFile))
        key.seek(0)
        key = key.read().strip()
        key = re.sub(r'\s+', ' ', key)
        key = key.split(" ")
        key = [int(x) for x in key]
        keyLength = blockSize[0] * blockSize[1] *3
        if len(key) != keyLength:
            sys.exit("ERROR: key must be {} bits long".format(keyLength*8))
        return key

def blockToStream(blockArray, blockColumns, blockRows):
    endArray = []
    for k in range(blockRows):
        for j in range(len(blockArray[0])):
            for i in range(blockColumns*k, (blockColumns*k)+blockColumns):
                endArray.append(blockArray[i][j])
    endByteArray = []
    for i in range(len(endArray)):
        endByteArray += endArray[i]
    return endByteArray

def singleBlockToStream(block):
    stream = []
    for i in range(len(block)):
        stream += block[i]
    return stream

def singleStreamToBlock(stream):
    block = [stream[i:i + blockSize[0]] for i in range(0, len(stream), blockSize[0])]
    return block

def streamToRGBTupleStream(stream):
    lol = [stream[i:i + 3] for i in range(0, len(stream), 3)]
    tupleStream = [tuple(i) for i in lol]
    return tupleStream

def RGBTupleStreamToStream(stream):
    lol = [list(i) for i in stream]
    flatList = [i for sublist in lol for i in sublist]
    return flatList

def ECBencrypt(blockArray, key):
    newBlockArray = []
    for block in blockArray:
        blockStream = singleBlockToStream(block)
        blockStream = RGBTupleStreamToStream(blockStream)
        #encrypt (F(k, m1) = k XOR m1) stream with key
        blockStream = list(map(lambda x,y: (x^y)%256, blockStream, key))

        blockStream = streamToRGBTupleStream(blockStream)
        singleBlock = singleStreamToBlock(blockStream)
        newBlockArray.append(singleBlock)
    return newBlockArray

def CBCencrypt(blockArray, key):
    newBlockArray = []
    previousStream = IV
    for block in blockArray:
        blockStream = singleBlockToStream(block)
        blockStream = RGBTupleStreamToStream(blockStream)
        #xor with previous crypt
        blockStream = list(map(lambda x,y: (x^y)%256, blockStream, previousStream))

        #apply encode function
        blockStream = list(map(lambda x,y: (x^y)%256, blockStream, key))

        #pass results to next block calculation
        previousStream = blockStream
        #previousStream = [random.randint(0, 256) for i in range(12)]

        blockStream = streamToRGBTupleStream(blockStream)
        singleBlock = singleStreamToBlock(blockStream)
        newBlockArray.append(singleBlock)
    return newBlockArray


def main():
    #open
    img = Image.open(imgFile)
    #img = img.convert("L")
    width, height = img.size #400x360

    #blockify
    imgArray = list(img.getdata())
    imgLinesArray = [imgArray[i:i + width] for i in range(0, len(imgArray), width)]

    blockArray = [] #100x120blocks
    for k in range((height//blockSize[1])): #for each of 120 block rows
        for i in range((width//blockSize[0])): #for each of 100 block columns
            block = []
            for j in range(k*blockSize[1], (k*blockSize[1])+blockSize[1]):  #0-3, 3-6, 6-9
                block.append(imgLinesArray[j][blockSize[0]*i:(blockSize[0]*i)+blockSize[0]]) #0-5, 5-10, 10-15
            blockArray.append(block)

    #extra data for encryption
    blockColumns = width//blockSize[0] #y coordinates
    blockRows = height//blockSize[1] #x coordinates
    key = getKey(keyFile)

    #encrypt with ECB
    ECBblockArray = ECBencrypt(blockArray, key)
    #save
    byteStreamArray = blockToStream(ECBblockArray, blockColumns, blockRows)
    byteStreamArray = RGBTupleStreamToStream(byteStreamArray)
    #img2 = Image.new(img.mode, img.size)
    #img2.putdata(bytes(byteStreamArray))
    tobytes = bytes(byteStreamArray)
    img2 = Image.frombytes("RGB", (400, 360), tobytes)
    #img2 = img2.convert("1", dither=Image.NONE) #, dither=Image.NONE
    img2.save(ECBoutFile)

    #encrypt with CBC
    CBCblockArray = CBCencrypt(blockArray, key)
    #save
    byteStreamArray = blockToStream(CBCblockArray, blockColumns, blockRows)
    byteStreamArray = RGBTupleStreamToStream(byteStreamArray)
    #img2 = Image.new(img.mode, img.size)
    #img2.putdata(bytes(byteStreamArray))
    tobytes = bytes(byteStreamArray)
    img2 = Image.frombytes("RGB", (400, 360), tobytes)
    #img2 = img2.convert("1", dither=Image.NONE)
    img2.save(CBCoutFile)

if __name__ == "__main__":
    main()
