
import jieba.analyse
import socket
import os
import sys
import struct
from web3 import Web3
import json
import ast
import threading
import Encrypt_Decrypt
import hashlib
import time
# 定义一个MyThread.py线程类
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
    def run(self):
        time.sleep(2)
        self.result = self.func(*self.args)
    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None

def Merkle_Tree(hashs):

    print(hashs)
    if len(hashs) == 1:
        return hashs[0]
    new_hashs = []
    if len(hashs) % 2 == 0:
        for i in range(int(len(hashs)/2)):
            file_hash = hashlib.sha256()  # 获取上传文件的hash值
            new = hashs[2 * i - 2] + hashs[2 * i - 1]
            file_hash.update(new)
            new_hashs.append(file_hash.hexdigest())
        result = Merkle_Tree(new_hashs)
    else:
        for j in range(int(len(hashs) / 2)):
            file_hash = hashlib.sha256()  # 获取上传文件的hash值
            new = hashs[2 * j - 2] + hashs[2 * j - 1]
            file_hash.update(new)
            new_hashs.append(file_hash.hexdigest())
        new_hashs.append(hashs[len(hashs)-1])
        result = Merkle_Tree(new_hashs)
    return result
def TF(text):
    tags = jieba.analyse.extract_tags(text,topK=4)
    return(tags)

def socket_client(file_path, cipher,file_id,T_w,random_numbers):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9001))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print (s.recv(1024))

    # 判断是否为文件
    if os.path.isfile(file_path):
        # 定义文件头信息，包含文件名和文件大小
        model = struct.pack('l',1)
        s.send(model)   #选择服务功能
        T_length = len(str(T_w).encode('utf-8'))
        T_length = struct.pack('l',T_length)
        s.send(T_length)
        R_length = len(str(random_numbers).encode('utf-8'))  #计算可搜索加密长度为接受做好准备
        R_length = struct.pack('l', R_length)
        s.send(R_length)
        fhead = struct.pack('l',  len(cipher))
        # 发送文件名称与文件大小
        s.send(fhead)
        fid = struct.pack('l',  file_id)
        s.send(fid)

        T_w = str(T_w)
        random_numbers = str(random_numbers)

        other = struct.pack('%ds%ds'%(len(str(T_w).encode('utf-8')),len(str(random_numbers).encode('utf-8'))),T_w.encode('utf-8'),random_numbers.encode('utf-8'))
        s.send(other)

        # 将传输文件以二进制的形式分多次上传至服务器
        # fp = cipher
        i = 0
        while ((i + 1) * 1024  < len(cipher)):
            data = cipher[1024 * i:(i+1) * 1024]
            i = i+1
            if not data:
                print ('{0} file send over...'.format(os.path.basename(file_path)))
                break

            s.send(data)

        data = cipher[1024 * i:len(cipher)]

        s.send(data)
        # 关闭当期的套接字对象
        s.close()


def upload(file_id,file_hash):    #更新索引和merkle树
    w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
    accounts = w3.eth.accounts
    artifact = 'Enabling_Reliable_Keyword_Search'
    fn_abi = 'D:\pythonProject/{0}.abi'.format(artifact)
    fn_addr = r'D:\pythonProject\addr.txt'
    with open(fn_abi, 'r') as f:
        abi = json.load(f)
    with open(fn_addr, 'r') as f:
        addr = f.read()
    factory = w3.eth.contract(abi=abi, address=Web3.to_checksum_address(addr))
    factory.functions.upload(file_id,file_hash).transact({'from': accounts[1]})

def delete(file_id):   #删除索引和更新merkle树
    w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
    accounts = w3.eth.accounts
    artifact = 'Enabling_Reliable_Keyword_Search'
    fn_abi = 'D:\pythonProject/{0}.abi'.format(artifact)
    fn_addr = r'D:\pythonProject\addr.txt'
    with open(fn_abi, 'r') as f:
        abi = json.load(f)
    with open(fn_addr, 'r') as f:
        addr = f.read()
    factory = w3.eth.contract(abi=abi, address=Web3.to_checksum_address(addr))
    print(123)
    factory.functions.delete_file(file_id).transact({'from': accounts[1]})
    print(156)

def create_search(keyword,id):
    w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
    accounts = w3.eth.accounts
    artifact = 'Enabling_Reliable_Keyword_Search'
    fn_abi = 'D:\pythonProject/{0}.abi'.format(artifact)
    fn_addr = r'D:\pythonProject\addr.txt'
    with open(fn_abi, 'r') as f:
        abi = json.load(f)
    with open(fn_addr, 'r') as f:
        addr = f.read()
    factory = w3.eth.contract(abi=abi, address=Web3.to_checksum_address(addr))
    factory.functions.construct_search(keyword, id).transact({'from': accounts[1]})  # 更新区块链的倒排索引

def search_by_keyword(new_keyword): #根据关键词进行检索
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9001))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(s.recv(1024))
    model = struct.pack('l', 3)
    s.send(model)
    print(789)
    print(type(new_keyword))
    length = struct.pack('l', len(new_keyword))
    print(8941)
    s.send(length)
    print(489)
    keyword = struct.pack('%ds' % len(new_keyword), new_keyword)
    print(891)
    s.send(keyword)
    print(84484)
    s.close()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定端口为9001
        s.bind(('127.0.0.1', 9002))
        # 设置监听数
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        # 等待请求并接受(程序会停留在这一旦收到连接请求即开启接受数据的线程)
        conn, addr = s.accept()
        print(156)
        t = MyThread(deal_data, (conn, addr,new_keyword,))
        t.start()
        return (t.get_result())


def deal_data(conn,addr,keyword):
    print(15995)
    length_struct = struct.calcsize('l')
    length_zip = conn.recv(length_struct)
    length = struct.unpack('l', length_zip)[0]
    print(295121)
    file_index_struct = struct.calcsize('%ds'%length)
    file_index_zip = conn.recv(file_index_struct)
    file_index = struct.unpack('%ds'%length, file_index_zip)[0]  #接受匹配的文件序号
    print(file_index)
    print(8915)
    file_index = file_index.decode()

    file_index = ast.literal_eval(file_index)
    root = os.getcwd()
    f_name = open(root + r'\file_name.txt','r')  # 读取文件内容获取已上传的文件名和id
    f_id = open(root + r'\file_id.txt','r')
    file_name = ast.literal_eval(f_name.read())
    file_id = ast.literal_eval(f_id.read())
    result = []
    print(1561)
    print(file_index)
    f_name.close()
    f_id.close()
    for l in range(len(file_index)):
        file_ids = file_id.index(str(file_index[l]))
        result.append([file_index[l], file_name[file_ids]])
    print(result)
    return result

def download_file(index):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9001))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print (s.recv(1024))
    model_zip = struct.pack('l',2)
    s.send(model_zip)
    index = int(index)
    index_zip = struct.pack('l',index)
    s.send(index_zip)
    s.close()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定端口为9001
        s.bind(('127.0.0.1', 9002))
        # 设置监听数
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        # 等待请求并接受(程序会停留在这一旦收到连接请求即开启接受数据的线程)
        conn, addr = s.accept()
        # 接收数据
        t = MyThread(deal_file,(conn,addr,))
        t.start()
        return (t.get_result())

def deal_file(conn,addr):
    print('Accept new connection from {0}'.format(addr))
    # conn.settimeout(500)
    # 收到请求后的回复
    conn.send('Hi, Welcome to the server!'.encode('utf-8'))
    # 申请相同大小的空间存放发送过来的文件名与文件大小信息
    fileinfo_size = struct.calcsize('l')
    # 接收文件名与文件大小信息
    buf_zip = conn.recv(fileinfo_size)
    buf = struct.unpack('l', buf_zip)[0]
    # 判断是否接收到文件头信息
    if buf:
        # 获取文件名和文件大小
        filesize = buf
        root = os.getcwd()
        file_name = open(root + '\\file_name.txt' , 'r')
        file_id = open(root + '\\file_id.txt' , 'r')
        file_ids = ast.literal_eval(file_id.read())
        file_names = ast.literal_eval(file_name.read())
        recvd_size = 0  # 定义已接收文件的大小
        # 存储在该脚本所在目录下面

        data = b''
        # 将分批次传输的二进制流依次写入到文件
        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = data + conn.recv(1024)
                recvd_size += len(data)
            else:
                data = data + conn.recv(filesize - recvd_size)
                recvd_size = filesize
    # 传输结束断开连接
    conn.close()
    return data

def Verify(file_name,index):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9001))
    except socket.error as msg:
        sys.exit(1)
    print(s.recv(1024))
    print('Waiting connection...')
    model_zip = struct.pack('l', 5)
    s.send(model_zip)
    id_zip = struct.pack('l',int(index))
    s.send(id_zip)
    s.close()
    print(1)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定端口为9001
        s.bind(('127.0.0.1', 9002))
        # 设置监听数
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        # 等待请求并接受(程序会停留在这一旦收到连接请求即开启接受数据的线程)
        conn, addr = s.accept()
        # 接收数据
        t = MyThread(Varify_data,(conn,addr,index,))
        t.start()
        return (t.get_result())


def Varify_data(conn,addr,index):
    length_struct = struct.calcsize('l')
    length_zip = conn.recv(length_struct)
    length = struct.unpack('l',length_zip)[0]

    file_hash_struct = struct.calcsize('%ds'%length)
    file_hash_zip = conn.recv(file_hash_struct)
    file_hash = struct.unpack('%ds'%length,file_hash_zip)[0]
    file_hash = file_hash.decode('utf-8')

    length_struct = struct.calcsize('l')
    length_zip = conn.recv(length_struct)
    length = struct.unpack('l', length_zip)[0]

    file_struct = struct.calcsize('%ds' % length)
    file_zip = conn.recv(file_struct)
    file_h = struct.unpack('%ds' % length, file_zip)[0]
    file_h = file_h.decode('utf-8')
    print('file_h')
    print(file_h)
    print('file_hash')
    print(file_hash)

    w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
    accounts = w3.eth.accounts
    artifact = 'Enabling_Reliable_Keyword_Search'
    fn_abi = 'D:\pythonProject/{0}.abi'.format(artifact)
    fn_addr = r'D:\pythonProject\addr.txt'
    with open(fn_abi, 'r') as f:
        abi = json.load(f)
    with open(fn_addr, 'r') as f:
        addr = f.read()
    factory = w3.eth.contract(abi=abi, address=Web3.to_checksum_address(addr))
    solidity_hash=factory.functions.getleafs().call()
    solidity_h =factory.functions.gethashs(int(index)).call()
    print('solidity_hash')
    print(solidity_hash)
    print('solidity_h')
    print(solidity_h)
    for i in range(len(solidity_hash)):
        solidity_hash[i] = solidity_hash[i].encode()
    solidity_hash = solidity_hash[0:2]
    root = Merkle_Tree(solidity_hash)
    if root ==file_hash:
        return 1
    else:
        if solidity_h == file_h:
            return 2
        else:
            return 3
def delete_service_file(index):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9001))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print (s.recv(1024))
    model_zip = struct.pack('l',4)
    s.send(model_zip)
    index_zip = struct.pack('l',int(index))
    s.send(index_zip)
    s.close()