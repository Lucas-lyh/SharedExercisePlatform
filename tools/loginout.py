from nicegui import app,ui

from uuid import uuid4
import asyncio
import hashlib
def try_login(manager):
    username = (app.storage.browser.get("input_username", 'None'))
    password = app.storage.browser.get("input_password", "None")
    if username == "None" or password == "None":
        return False,"请输入用户名和密码"
    md5 = hashlib.md5()
    md5.update((password + "buaa2023").encode())
    password_hash = md5.hexdigest()
    if manager.try_login(username=username, pwhash=password_hash):
        app.storage.user["login"] = "True"
        app.storage.user["username"] = username
        app.storage.user["password"] = "*"*len(password)
        ui.open("/user")
        return True, "登录成功"
    else:
        app.storage.user["login"] = "False"
        return True,"登录失败，请输入正确的用户名和密码"


def try_register(manager):
    username = (app.storage.browser.get("input_username", 'None'))
    password = app.storage.browser.get("input_password", "None")
    if username == "None" or password == "None":
        return False, "请输入用户名和密码"
    md5 = hashlib.md5()
    md5.update((password + "buaa2023").encode())
    password_hash = md5.hexdigest()
    if manager.try_register(username=username, pwhash=password_hash):
        ui.open("/login")
        return True, "注册成功"
    else:
        return False,"用户名已存在或密码不符合要求"


def logout():
    app.storage.user['login'] = 'False'
    ui.open('/')