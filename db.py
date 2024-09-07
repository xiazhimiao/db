# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from plugins import *
import mysql.connector


@plugins.register(
    name="db",
    desire_priority=-1,
    hidden=True,
    desc="A plug-in to manipulate a database",
    version="0.1",
    author="XiaZhiMiao",
)
class db(Plugin):
    host = "localhost"
    user = "root"
    # 创建数据库连接
    db = None
    # 创建游标对象
    cursor = None

    def __init__(self):
        super().__init__()
        try:
            self.config = super().load_config()
            if not self.config:
                return
            self.host = self.config.get("host", self.host)
            self.user = self.config.get("user", self.user)
            self.password = self.config.get("password")
            self.database = self.config.get("database")
            # 创建数据库连接
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.db = db
            # 创建游标对象
            cursor = db.cursor()
            self.cursor = cursor

            logger.info("[db] inited")
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        except Exception as e:
            logger.error(f"[db]初始化异常：{e}")
            raise "[db] init failed, ignore "

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT,
        ]:
            return

        content = e_context["context"].content
        prefix = content[:3]
        sql = content[3:]

        if prefix == "数据库":
            reply = Reply()
            reply.content = ''
            reply.type = ReplyType.TEXT

            # 执行语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            if results:
                for row in results:
                    reply.content += str(row)
                    reply.content += "\n"
            else:
                reply.content = "查询失败"

            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  

        if content == "Sql菜单":
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "以'数据库'为前缀，之后写sql语句，中间不能有空格，不能有语法错误"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS


    def get_help_text(self, **kwargs):
        help_text = "输入'Sql菜单'我会告诉你如何进行操作\n嘿嘿嘿\n"
        return help_text
