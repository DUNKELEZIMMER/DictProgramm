"""
    字典客户端
"""

from socket import *
import getpass
import hashlib
from time import sleep

CUTER = "&&"

# 创建套接字
sockfd = socket()
server_addr = ("127.0.0.1", 22222)
sockfd.connect(server_addr)
print("已连接")


def log_view(head):
    try:
        user_id = login(head)
        if sockfd.recv(512).decode() == "NONE":
            raise Exception("用户名或密码不合法!")
        else:
            print("登录成功!")
    except Exception as e:
        print(e, "\n用户名或密码不可用,请检查用户名或密码!")
    else:
        search_view(user_id)


def login(head):
    user_id = input("[请输入用户ID:]").replace(" ", "")
    user_pwd = getpass.getpass("[请输入用户密码:]")
    pwdlock = hashlib.md5(user_pwd.encode()).hexdigest()
    sockfd.send((head + CUTER + str(user_id) + CUTER + pwdlock).encode())
    return user_id


def history(user_id):
    sleep(0.01)
    sockfd.send(("HL" + CUTER + user_id).encode())
    history_list = sockfd.recv(512).decode().split("&&")
    print("========" * len(history_list))
    for item in history_list:
        print(item, end="\t")
    print("\n" + "========" * len(history_list))
    sleep(0.01)


def search_view(user_id):
    while 1:
        user_chose2 = input("[1:查单词    2:历史记录   3:注销]\n")
        if user_chose2 == "1":
            history(user_id)
            user_word = input("\n[请输入要查询的单词:]")
            sockfd.send(("SW" + CUTER + user_id + CUTER + user_word).encode())
            back = sockfd.recv(512).decode()
            if back != "NONE":
                print(user_word, ":", back)
            else:
                print(back)
        elif user_chose2 == "2":
            history(user_id)
        else:
            return


def main():
    while 1:
        print("==欢迎使用在线英文词典==")
        user_chose = input("[1:登录    2:注册   3:退出]\n")
        if user_chose == "1":
            log_view("LI")
        elif user_chose == "2":
            log_view("CI")
        else:
            sockfd.send(("ET" + CUTER + "exit" + CUTER + "quit").encode())
            exit()


def get_out():
    sockfd.send(("ET" + CUTER + "exit" + CUTER + "quit").encode())
    print("bye~~")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        get_out()
