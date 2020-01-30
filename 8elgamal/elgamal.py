import random
import argparse, sys, os

GEN = "elgamal.txt"
PRIV = "private.txt"
PUB = "public.txt"
PLAIN = "plain.txt"
CRYPTO = "crypto.txt"
DECRYPT = "decrypt.txt"
MSG = "message.txt"
SIG = "signature.txt"
VER = "verify.txt"

def NWD(a, b):
    if b != 0:
        return NWD(b, a % b )
    return a

def modInverse(a, mod):
    m0 = mod
    y = 0
    x = 1
    if mod == 1 :
        return 0
    while a > 1 :
        q = a // mod
        t = mod
        mod = a % mod
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0 :
        x = x + m0
    return x

def encrypt(p, g, B, strMsg):
    m = int(strMsg.encode().hex(), 16)
    k = random.randint(0, p)
    gk = pow( g, k, p )
    Bk = m*pow( B, k, p)
    encryptedStr = str(gk) + ' ' + str(Bk)
    return encryptedStr

def decrypt(p, b, cipher):
    cipherArray = cipher.split()
    gk = int(cipherArray[0])
    mBk = int(cipherArray[1])
    Bk = pow(gk, b, p)
    m = mBk//Bk
    hexm = hex(m)[2:]
    decryptedText = bytes.fromhex(hexm).decode()
    return decryptedText

def sigGen(p, g, b, m):
    while 1:
        k = random.randint(1, p-1)
        if NWD(k, p-1) == 1:
            break
    r = pow(g,k,p)
    invk = modInverse(k, p-1)
    s = invk*(m-b*r)%(p-1)
    return r,s

def sigVer(p, g, B, r, x, m):
    v1 = pow(g,m,p)
    v2 = pow(B,r,p)%p * pow(r,x,p)%p
    return v1 == v2

def genKeys(genFile, outPrivFile, outPubFile):
    elga = open(genFile, "r")
    elgalines = elga.readlines()
    p = int(elgalines[0])
    g = int(elgalines[1])
    x = random.randint(1, p)
    h = pow( g, x, p )

    epriv = open(outPrivFile, "w")
    epriv.write('%s\n%s\n%s' % (str(p), str(g), str(x)))

    epub = open(outPubFile, "w")
    epub.write('%s\n%s\n%s' % (str(p), str(g), str(h)))

    elga.close()
    epriv.close()
    epub.close()

def encryptMsg(pubFile, msgFile, outFile):
    epub = open(pubFile, "r")
    epublines = epub.readlines()
    pubkp = int(epublines[0])
    pubkg = int(epublines[1])
    pubkh = int(epublines[2])

    eplain = open(msgFile, "r")
    eplainlines = eplain.readlines()
    message = str(eplainlines[0])

    if len(message) >= pubkp:
        sys.exit("ERROR: m<p test failed.")

    cipher = encrypt(pubkp, pubkg, pubkh, message)

    ecrypto = open(outFile, "w")
    ecrypto.write('%s' % (str(cipher)))

    epub.close()
    eplain.close()
    ecrypto.close()

def decryptMsg(privFile, msgFile, outFile):
    epriv = open(privFile, "r")
    eprivlines = epriv.readlines()
    privkp = int(eprivlines[0])
    privkx = int(eprivlines[2])

    ecrypt = open(msgFile, "r")
    ecryptlines = ecrypt.readlines()
    encryptMsg = str(ecryptlines[0])

    decrypted = decrypt(privkp, privkx, encryptMsg)

    edecrypt = open(outFile, "w")
    edecrypt.write('%s' % (decrypted))

    epriv.close()
    ecrypt.close()
    edecrypt.close()

def genSignature(privFile, msgFile, outFile):
    epriv = open(privFile, "r")
    eprivlines = epriv.readlines()
    privkp = int(eprivlines[0])
    privkg = int(eprivlines[1])
    privkx = int(eprivlines[2])

    message = open(msgFile, "r")
    messagelines = message.readlines()
    content = int(messagelines[0].encode().hex(), 16)

    rr, ss = sigGen(privkp, privkg, privkx, content)

    signature = open(outFile, "w")
    signature.write('%s\n%s' % (str(rr), str(ss)))

    epriv.close()
    message.close()
    signature.close()

def verifySig(pubFile, msgFile, sigFile, outFile):
    epub = open(pubFile, "r")
    epublines = epub.readlines()
    pubkp = int(epublines[0])
    pubkg = int(epublines[1])
    pubky = int(epublines[2])

    message = open(msgFile, "r")
    messagelines = message.readlines()
    content = int(messagelines[0].encode().hex(), 16)

    signature = open(sigFile, "r")
    siglines = signature.readlines()
    sigr = int(siglines[0])
    sigs = int(siglines[1])

    isvalid = sigVer(pubkp, pubkg, pubky, sigr, sigs, content)
    print("Weryfikacja: %s" % isvalid)

    verify = open(outFile, "w")
    verify.write('Weryfikacja: %s' % isvalid)

    signature.close()
    message.close()
    epub.close()
    verify.close()


def main(args):
    modeList = [k for k, v in vars(args).items() if v]
    if "k" in modeList:
        genKeys(GEN, PRIV, PUB)
    elif "e" in modeList:
        encryptMsg(PUB, PLAIN, CRYPTO)
    elif "d" in modeList:
        decryptMsg(PRIV, CRYPTO, DECRYPT)
    elif "s" in modeList:
        genSignature(PRIV, MSG, SIG)
    elif "v" in modeList:
        verifySig(PUB, MSG, SIG, VER)
    else:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode/decode/sign/verify elgemal")
    actionType = parser.add_mutually_exclusive_group(required=True)
    actionType.add_argument("-k", action="store_true", help="generate pub,priv keys")
    actionType.add_argument("-e", action="store_true", help="encrypt")
    actionType.add_argument("-d", action="store_true", help="decrypt")
    actionType.add_argument("-s", action="store_true", help="sign")
    actionType.add_argument("-v", action="store_true", help="verify signature")
    args = parser.parse_args()
    main(args)
