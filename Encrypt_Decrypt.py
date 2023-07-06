from Crypto.Cipher import AES
from tkinter import filedialog
import jieba.analyse
import socket
import os
import sys
import struct
from binascii import b2a_hex, a2b_hex
import base64
import hashlib
import hmac
import random
AES_BLOCK_SIZE = AES.block_size     # AES 加密数据块大小, 只能是16
AES_KEY_SIZE = 16                   # AES 密钥长度（单位字节），可选 16、24、32，对应 128、192、256 位密钥

# 待加密文本补齐到 block size 的整数倍
def PadTest(bytes):
    while len(bytes) % AES_BLOCK_SIZE != 0:     # 循环直到补齐 AES_BLOCK_SIZE 的倍数
        bytes += ' '.encode()                   # 通过补空格（不影响源文件的可读）来补齐
    return bytes                                # 返回补齐后的字节列表

# 待加密的密钥补齐到对应的位数
def PadKey(key):
    if len(key) > AES_KEY_SIZE:                 # 如果密钥长度超过 AES_KEY_SIZE
        return key[:AES_KEY_SIZE]               # 截取前面部分作为密钥并返回
    while len(key) % AES_KEY_SIZE != 0:         # 不到 AES_KEY_SIZE 长度则补齐
        key += ' '.encode()                     # 补齐的字符可用任意字符代替
    return key                                  # 返回补齐后的密钥

# 文件AES 加密
def EnCrypt(key, bytes,model):
    if model == 1:
        myCipher = AES.new(key, AES.MODE_ECB)       # 新建一个 AES 算法实例，使用 ECB（电子密码本）模式

        encryptData = myCipher.encrypt(bytes)       # 调用加密方法，得到加密后的数据

        return encryptData                          # 返回加密数据
    elif model == 2:
        myCipher = AES.new(key, AES.MODE_CBC)
        encryptData = myCipher.encrypt(bytes)
        return encryptData
    elif model == 3:
        myCipher = AES.new(key, AES.MODE_CFB)
        encryptData = myCipher.encrypt(bytes)
        return encryptData
    elif model == 4:
        myCipher = AES.new(key, AES.MODE_OFB)
        encryptData = myCipher.encrypt(bytes)
        return encryptData
    else:
        myCipher = AES.new(key, AES.MODE_CTR)
        encryptData = myCipher.encrypt(bytes)
        return encryptData
def DeCrypt(key, encryptData,model):
    if model == 1:
        print(key)
        print()
        myCipher = AES.new(key, AES.MODE_ECB)  # 新建一个 AES 算法实例，使用 ECB（电子密码本）模式
        DecryptData = myCipher.decrypt(encryptData)  # 调用加密方法，得到加密后的数据
        return DecryptData  # 返回加密数据
    elif model == 2:
        myCipher = AES.new(key, AES.MODE_CBC)
        DecryptData = myCipher.decrypt(encryptData)
        return DecryptData
    elif model == 3:
        myCipher = AES.new(key, AES.MODE_CFB)
        DecryptData = myCipher.decrypt(encryptData)
        return DecryptData
    elif model == 4:
        myCipher = AES.new(key, AES.MODE_OFB)
        DecryptData = myCipher.decrypt(encryptData)
        return DecryptData
    else:
        myCipher = AES.new(key, AES.MODE_CTR)
        DecryptData = myCipher.decrypt(encryptData)
        return DecryptData
