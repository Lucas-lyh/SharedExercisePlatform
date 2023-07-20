# This is a sample Python script
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from nicegui import ui,app
from uuid import uuid4
import asyncio

async def async_try_login():
    app.storage.user["login"] = 'true'
    ui.open(register_page)

async def async_try_register():
    app.storage.user["login"] = 'false'

number= [1]
@ui.page("/login")
def login_page():
    with ui.card().classes("mx-auto my-auto h-96 w-96"):
        ui.label().bind_text_from(app.storage.user, 'login')
        with ui.column().classes("mx-auto my-auto"):
            with ui.row():
                ui.input(label="用户名")
            with ui.row():
                ui.input(label="密码")
            with ui.row().classes("mx-auto"):
                ui.button("登录", on_click=async_try_login).classes("mx-auto")
                ui.button("返回", on_click=lambda: ui.open("/")).classes("mx-auto")
    if(app.storage.user.get('login', 'false') == 'true'):
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
                ui.input(label="用户名")
            with ui.row():
                ui.input(label="密码")
            with ui.row().classes("mx-auto"):
                ui.button("注册", on_click=async_try_register).classes("mx-auto")
                ui.button("返回", on_click=lambda: ui.open("/")).classes("mx-auto")


with ui.column().classes("mx-auto"):
    ui.label("欢迎！Welcome!")
    ui.button("新来的？", on_click=lambda: ui.open(register_page))
    ui.button("回到原点", on_click=lambda: ui.open(login_page))
ui.run(storage_secret='buaa2023')
