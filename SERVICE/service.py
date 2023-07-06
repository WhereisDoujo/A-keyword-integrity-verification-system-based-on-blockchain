#!coding=utf-8
import threading
import socket
import struct
import sys
import os
import hmac
import hashlib
import ast
import Encrypt_Decrypt
def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定端口为9001
        s.bind(('127.0.0.1', 9001))
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
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    # conn.settimeout(500)
    # 收到请求后的回复
    conn.send('Hi, Welcome to the server!'.encode('utf-8'))

    while 1:
        function_number_struct = struct.calcsize('l')
        function_number_zip = conn.recv(function_number_struct)
        print('收到的字节流：', function_number_zip, type(function_number_zip))
        function_number = struct.unpack('l',function_number_zip)[0]
        print(11)
        if function_number == 1:
            accept_file(conn,addr)
        elif function_number == 2:
            download_file(conn,addr)
        elif function_number == 3:
            search(conn,addr)
        elif function_number == 4:
            delete(conn,addr)
        elif function_number == 5:
            Varify(conn,addr)
        break
def Merkle_Tree(hashs):
    print('asdaaaaaaaa')
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
def Varify(conn,addr):
    root = os.getcwd()

    index_struct = struct.calcsize('l')
    index_zip = conn.recv(index_struct)
    index = struct.unpack('l', index_zip)[0]



    id_file = open(root + r'\id_file.txt', 'r')
    ids = ast.literal_eval(id_file.read())
    hashs = []
    for i in range(len(ids)):
        file = open(root + r'\%d.txt'%ids[i],'rb')
        bytes = file.read()
        print(bytes)
        file_hash_f = hashlib.sha256()  # 获取上传文件的hash值
        file_hash_f.update(bytes)
        file_hash = file_hash_f.hexdigest()
        hashs.append(file_hash.encode())
        if index == ids[i]:
            now_hash = file_hash
        file.close()
    print(hashs)
    print(156)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9002))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    ROOOT = Merkle_Tree(hashs)
    index_zip = struct.pack('l', len(str(ROOOT).encode('utf-8')))
    s.send(index_zip)
    other = struct.pack('%ds' %len(str(ROOOT).encode('utf-8')), str(ROOOT).encode('utf-8'))
    s.send(other)
    izip = struct.pack('l', len(str(now_hash).encode('utf-8')))
    s.send(izip)
    oth = struct.pack('%ds' % len(str(now_hash).encode('utf-8')), str(now_hash).encode('utf-8'))
    s.send(oth)
    s.close()

def Terify(a,b):
    print(b,str(a[1]).encode())
    print(hmac.new(b,str(a[1]).encode(),hashlib.md5))
    if hmac.new(b,str(a[1]).encode(),hashlib.md5).hexdigest() == a[0]:
        return True
    else:
        return False

def accept_file(conn,addr):
    length_struct = struct.calcsize('l')
    T_length_zip = conn.recv(length_struct)
    T_length = struct.unpack('l', T_length_zip)[0]
    R_length_zip = conn.recv(length_struct)
    R_length = struct.unpack('l', R_length_zip)[0]
    # 申请相同大小的空间存放发送过来的文件名与文件大小信息
    # 接收文件名与文件大小信息
    buf_struct = struct.calcsize('l')
    buf = conn.recv(buf_struct)
    # 判断是否接收到文件头信息
    if buf:
        # 获取文件名和文件大小
        filesize = struct.unpack('l', buf)[0]
        id_struct = struct.calcsize('l')
        file_id_zip = conn.recv(id_struct)
        file_id = struct.unpack('l', file_id_zip)[0]
        other_struct = struct.calcsize('%ds%ds' % (T_length, R_length))
        other = conn.recv(other_struct)
        T_w, random_numbers = struct.unpack('%ds%ds'% (T_length, R_length), other)
        T_w = T_w.decode('utf-8')
        random_numbers = random_numbers.decode('utf-8')
        T_w =ast.literal_eval(T_w)
        random_numbers = ast.literal_eval(random_numbers)
        recvd_size = 0  # 定义已接收文件的大小
        # 存储在该脚本所在目录下面
        fp = open('./' + str(file_id)+'.txt', 'wb')
        print('start receiving...')

        # 将分批次传输的二进制流依次写入到文件
        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = conn.recv(1024)
                recvd_size += len(data)

            else:

                data = conn.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        fp.close()
        print('end receive...')
        root = os.getcwd()
        id_file = open(root + r'\id_file.txt','r')
        ids = ast.literal_eval(id_file.read())
        ids.append(file_id)

        T_w_file = open(root + r'\T_w_file.txt', 'r')
        T_ws = ast.literal_eval(T_w_file.read())
        for k in range(len(T_w)):
            T_ws.append([T_w[k],random_numbers[k],file_id])

        id_file.close()
        T_w_file.close()

        id_file = open(root + r'\id_file.txt', 'w')
        id_file.write(str(ids))

        T_w_file = open(root + r'\T_w_file.txt', 'w')
        T_w_file.write(str(T_ws))
        id_file.close()
        T_w_file.close()
    # 传输结束断开连接
    conn.close()
def download_file(conn,addr,):
    index_zip_struct = struct.calcsize('l')
    index_zip = conn.recv(index_zip_struct)
    index = struct.unpack('l', index_zip)[0]
    conn.close()
    print(index)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9002))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print (s.recv(1024))
    curr_dir = os.getcwd()
    # 判断是否为文件
    if os.path.isfile(curr_dir+'\\'+'%d'%index+'.txt'):

        # 定义文件头信息，包含文件大小
        fhead = struct.pack('l', os.stat(curr_dir+'\\'+'%d'%index+'.txt').st_size)
        # 发送文件名称与文件大小
        s.send(fhead)
        # 将传输文件以二进制的形式分多次上传至服务器
        fp = open(curr_dir+'\\'+'%d'%index + r'.txt','rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print ('{0} file send over...'.format(os.path.basename(curr_dir+'\\'+'%d'%index)))
                break
            s.send(data)
        # 关闭当期的套接字对象
        s.close()

def search(conn,addr):
    length_struct = struct.calcsize('l')
    length_zip = conn.recv(length_struct)
    length = struct.unpack('l', length_zip)[0]


    keyword_struct = struct.calcsize('%ds'%length)
    keyword_zip = conn.recv(keyword_struct)
    keyword = struct.unpack('%ds'%length,keyword_zip)[0]

    curr_dir = os.getcwd()
    fp = open(curr_dir + '\\' + 'T_w_file.txt')
    file_informayion = ast.literal_eval(fp.read())
    number = []
    for i in range(len(file_informayion)):
        flag = Terify(file_informayion[i],keyword)
        if flag == True:
            number.append(file_informayion[i][2])
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9002))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print(49561)
    st = str(number)
    string_length = len(st)
    string_len = struct.pack('l',string_length)
    print(49561)
    s.send(string_len)

    result = struct.pack('%ds'%string_length,st.encode())
    print(49561)
    s.send(result)
    s.close()
def delete(conn,addr):
    index_zip_struct = struct.calcsize('l')
    index_zip=conn.recv(index_zip_struct)
    index = struct.unpack('l', index_zip)[0]
    os.remove(os.getcwd()+'\\'+str(index)+'.txt')
    file = open(os.getcwd() + r"\id_file.txt","r")
    indexs = ast.literal_eval(file.read())
    id = indexs.index(index)
    del indexs[id]
    file_2 = open(os.getcwd() + r"\T_w_file.txt", "r")
    T_ws = ast.literal_eval(file_2.read())
    flag = 0
    while 1:
        if flag < len(T_ws):
            try:
                if T_ws[flag][2] == index:
                    del T_ws[flag]
                else:
                    flag+=1
            except:
                print(flag)
                print(len(T_ws))
        else:
            break
    file.close()
    file_2.close()
    file = open(os.getcwd() + r"\id_file.txt", "w")
    file_2 = open(os.getcwd() + r"\T_w_file.txt", "w")
    file.write(str(indexs))
    file_2.write(str(T_ws))
    file.close()
    file_2.close()
if __name__ == "__main__":
    socket_service()
