from peewee import *
import pymysql
db = MySQLDatabase("testdatabase", user='root', password='buaa2023', host='43.143.129.27',
                           port=3306)


class User(Model):
    id = AutoField(primary_key=True)
    username = CharField()
    password = CharField()

    class Meta:
        database = db


class Manager:
    def try_login(self, username, pwhash):
        users = User.select().where(User.username == username)
        if len(users) == 0:
            return False
        return users[0].password == pwhash
    def try_register(self, username, pwhash):
        users = User.select().where(User.username == username)
        if len(users) !=0:
            return False
        new_user = User(username = username, password = pwhash)
        new_user.save()
        return True


# User.create_table()
# user = User(username = "lucas", password = "buaa2023")
# user.save()
# all = User.get()
# all.delete_instance()
