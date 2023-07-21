# This is a sample Python script
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from nicegui import ui,app
from uuid import uuid4
import asyncio
import hashlib
from orm import Manager

manager = Manager()

async def async_try_login():
    username = (app.storage.browser.get("input_username", 'None'))
    password = app.storage.browser.get("input_password", "None")
    if(username == "None" or password == "None"):
        return
    md5 = hashlib.md5()
    md5.update( (password+"buaa2023").encode())
    password_hash = md5.hexdigest()
    if manager.try_login(username=username, pwhash = password_hash):
        app.storage.user["login"] = "True"
        ui.open(user_page)
    else:
        app.storage.user["login"] = "False"
        ui.open(login_page)

async def async_try_register():
    username = (app.storage.browser.get("input_username", 'None'))
    password = app.storage.browser.get("input_password", "None")
    if (username == "None" or password == "None"):
        return
    md5 = hashlib.md5()
    md5.update((password + "buaa2023").encode())
    password_hash = md5.hexdigest()
    if manager.try_register(username=username, pwhash = password_hash):
        ui.open(login_page)
    else:
        ui.open(register_page)

async def logout():
    app.storage.user['login'] = 'False'
    ui.open('/')


number= [1]
@ui.page("/login")
def login_page():
    with ui.card().classes("mx-auto my-auto h-96 w-96"):
        ui.label().bind_text_from(app.storage.user, 'login')
        with ui.column().classes("mx-auto my-auto"):
            with ui.row():
                ui.input(label="用户名").bind_value_to(app.storage.browser, 'input_username')
            with ui.row():
                ui.input(label="密码").bind_value_to(app.storage.browser, 'input_password')
            with ui.row().classes("mx-auto"):
                ui.button("登录", on_click=async_try_login).classes("mx-auto")
                ui.button("返回", on_click=lambda: ui.open("/")).classes("mx-auto")
    if(app.storage.user.get('login', "False") == "True"):
        print('redirect')
        ui.open(register_page)
@ui.page("/register")
def register_page():
    app.storage.user['count'] = app.storage.user.get('count', 0) + 1
    with ui.row():
        ui.label('your own page visits:')
        ui.label().bind_text_from(app.storage.user, 'count')
    with ui.card().classes("mx-auto my-auto h-96 w-96"):
        with ui.column().classes("mx-auto my-auto"):
            with ui.row():
                ui.input(label="用户名").bind_value_to(app.storage.browser, 'input_username')
            with ui.row():
                ui.input(label="密码").bind_value_to(app.storage.browser, 'input_password')
            with ui.row().classes("mx-auto"):
                ui.button("注册", on_click=async_try_register).classes("mx-auto")
                ui.button("返回", on_click=lambda: ui.open("/")).classes("mx-auto")
@ui.page("/user")
async def user_page():
    if app.storage.user.get('login', 'False') != 'True':
        ui.button("无权限，返回主页", on_click=lambda: ui.open('/'))
        print("error")
    else:
        ui.button("退出", on_click=logout).classes('mx-auto')


with ui.column().classes("mx-auto"):
    ui.label("欢迎！Welcome!")
    ui.button("新来的？", on_click=lambda: ui.open(register_page))
    ui.button("登录", on_click=lambda: ui.open(login_page))
ui.run(storage_secret='buaa2023')
