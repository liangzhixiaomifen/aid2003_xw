"""
文件服务器 客户端
"""

from socket import *
from time import sleep
import sys

# 服务器地址
ADDR = ('127.0.0.1',8888)

class FTPClient:
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L") # 发请求
        data = self.sockfd.recv(128).decode() # 等反馈
        # 根据反馈选择做什么
        if data == 'OK':
            # 接收文件列表
            data = self.sockfd.recv(1024 * 1024)
            print(data.decode())
        else:
            print("文件库为空")

    # 下载文件
    def do_get(self,filename):
        data = "D "+filename
        self.sockfd.send(data.encode()) # 发送请求
        data = self.sockfd.recv(128).decode() # 等待回复
        if data == 'OK':
            # 接收文件
            f = open(filename,'wb')
            # 边接收，边写入
            while True:
                data = self.sockfd.recv(1024*10)
                # 接收完毕
                if data == b'##':
                    break
                f.write(data)
            f.close()
        else:
            print("文件不存在")


    def do_put(self,filename):
        try:
            f = open(filename,'rb')
        except:
            print("文件不存在")
            return

        # 提取文件名 防止文件名有路径
        filename = filename.split('/')[-1]

        data = "U " + filename
        self.sockfd.send(data.encode())  # 发送请求
        data = self.sockfd.recv(128).decode()  # 等待回复
        if data == 'OK':
            while True:
                data = f.read(1024 * 10)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b"##")
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print("文件已经存在")

    # 退出
    def do_quit(self):
        self.sockfd.send(b'E')
        self.sockfd.close()
        sys.exit("谢谢使用")

# 客户端启动函数
def main():
    # 链接服务器
    sockfd = socket()
    sockfd.connect(ADDR)

    ftp = FTPClient(sockfd) # 实例化对象，调用类中的方法

    while True:
        print("=================命令选项====================")
        print("*****            list               *****")
        print("*****          get file             *****")
        print("*****          put file             *****")
        print("*****            quit               *****")
        print("============================================")
        cmd = input("输入命令:")

        if cmd == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1] # 提取文件名
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1] # 提取文件名
            ftp.do_put(filename)
        elif cmd == "quit":
            ftp.do_quit()
        else:
            print("请输入正确命令")

if __name__ == '__main__':
    main()
