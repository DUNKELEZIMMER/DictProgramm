"""
    这个模块用于dict 中 与数据库交互的部分
    用户注册 成功放回"OK TO LOGIN"  失败返回"RE DO"
    用户登录 成功返回"LOGIN PASS"    失败返回"NO WAY"
    用户查询并且写入历史记录 有单词返回一个元祖 没有的话返回("NONE",)
    历史记录直接返回 元祖套元祖 失败报错返回(("NONE",),)
"""

import pymysql
import hashlib


def hash_something(something):
    return hashlib.md5(something.encode()).hexdigest()


def sql_io(datebase="DICT", doing=""):
    """
    doing是一个sql语句 => str()
    """
    db = pymysql.connect(host="127.0.0.1",
                         user="root",
                         password="123456",
                         database=datebase,
                         charset="utf8")
    cur = db.cursor()
    cur.execute(doing)
    db.commit()
    cur.close()
    db.close()
    return cur


class UserIO:

    @staticmethod
    def user_creat(user_id="text", user_pwd="12345678"):
        try:
            sql = """insert into `USERINFO` value('%s','%s','%s')""" % (user_id,
                                                                        hash_something(user_pwd),
                                                                        "user")
            # print(sql)
            sql_io(doing=sql)
        except Exception as e:
            print("用户名已存在,请重新注册", e)
            return "RE DO"
        else:
            SearchIO.do_search(user_id=user_id, user_words="[history]")
            return "OK TO LOGIN"

    @staticmethod
    def user_login(user_id="100000", user_pwd="12345678"):
        haha = hashlib.md5(user_pwd.encode()).hexdigest()
        sql = """SELECT upwd from `USERINFO` WHERE uid='%s'""" % user_id
        if haha == sql_io(doing=sql).fetchone()[0]:
            return "LOGIN PASS"
        else:
            return "NO WAY"


class SearchIO:

    @staticmethod
    def do_search(user_id, user_words):
        sql_s = """SELECT WORD,MAIN FROM `ENDICT` WHERE WORD='%s'""" % user_words
        # print(sql_s)
        back = sql_io(doing=sql_s).fetchone()
        sql = """insert into `USERHISTORY` (uid,history) values('%s','%s')""" % (user_id,
                                                                                 user_words)
        sql_io(doing=sql)
        if not back:
            back = ("NONE",)
        return back  # 返回值为元祖

    @staticmethod
    def search_his(user_id):
        sql = """SELECT history from `USERHISTORY` WHERE uid='%s' ORDER BY searchdate desc LIMIT 10""" % user_id
        backs = sql_io(doing=sql).fetchall()
        return backs


if __name__ == '__main__':
    # UserIO.user_creat(100000, 'textuser', '12345678')
    # print(UserIO.user_login())
    # print(SearchIO.search_his("jijiahui"))
    # print(SearchIO.search_his("jijiawen"))
    # print(SearchIO.do_search(100000, "啦啦啦"))  # 还未处理
    pass
