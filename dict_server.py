"""
    字典服务器
"""

import socket
from select import select
from sql_inout import *
from time import sleep


class ServerBase:

    def __init__(self, host="0.0.0.0", port=22222):
        self.HOST = host
        self.PORT = port
        self.dict_s = socket.socket()
        self.LISTEN_NUMBER = 13
        self.first_run()
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def first_run(self):
        self.dict_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.dict_s.bind((self.HOST, self.PORT))
        self.dict_s.listen(self.LISTEN_NUMBER)
        print("Open post:%d" % self.PORT)

    def run_server(self):
        self.rlist.append(self.dict_s)

        # 循环监控
        while 1:
            rs, rw, rx = select(self.rlist, self.wlist, self.xlist)

            for r in rs:
                if r is self.dict_s:
                    user_tmp, user_addr = r.accept()
                    self.rlist.append(user_tmp)
                else:
                    # 处理请求
                    try:
                        self.fd_back(r)
                    except Exception as e:
                        print(e)
                        r.send(b"NONE")
                        continue

    def fd_back(self, connfd):  # 解析请求头,分解请求体 decoode()->切片
        sleep(0.01)
        data = connfd.recv(1024 * 10).decode().split("&&")
        if data[0] == "ET":
            self.rlist.remove(connfd)
            connfd.close()
            return
        elif data[0] == "LI":
            if UserIO.user_login(user_id=data[1], user_pwd=data[2]) == "LOGIN PASS":
                connfd.send(b"OK")
            else:
                connfd.send(b"NONE")
        elif data[0] == "CI":
            if UserIO.user_creat(user_id=data[1], user_pwd=data[2]) == "OK TO LOGIN":
                connfd.send(b"OK")
            else:
                connfd.send(b"NONE")
        elif data[0] == "SW":
            back = SearchIO.do_search(user_id=data[1], user_words=data[2])
            if back[0] == "NONE":
                connfd.send("Can not found the word {}".format(data[2]).encode())
            else:
                connfd.send(back[1].encode())
        elif data[0] == "HL":
            history_list = []
            history = SearchIO.search_his(user_id=data[1])
            for item in history:
                history_list.append(item[0])
            sender = "&&".join(history_list)
            connfd.send(sender.encode())


if __name__ == '__main__':
    try:
        dict_pro = ServerBase()
        dict_pro.run_server()
    except KeyboardInterrupt:
        print("Bye~~")
