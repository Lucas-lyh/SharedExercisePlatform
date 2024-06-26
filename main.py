# This is a sample Python script
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from nicegui import ui, app
from uuid import uuid4
import asyncio
import hashlib
from orm import manager
from tools.search import search
from pages.personal_information import personal_information_page
from tools import loginout

from pages.page_structure import init_page
app.add_static_files('/img', 'img')


async def async_try_login():
    succ, res = loginout.try_login(manager)
    ui.notify(res)

async def async_try_register():
    succ, res = loginout.try_register(manager)
    ui.notify(res)


async def logout():
    app.storage.user['login'] = 'False'
    ui.open('/')


number = [1]




@ui.page("/login")
def login_page():
    ui.query('body').classes('bg-gradient-to-br from-blue-200 to-purple-200')
    with ui.row().classes('mx-auto'):
        ui.image('/img/StarrySky_Logo.png').classes('w-12 h-12 py-8 px-8')
        ui.label("星汉 Starry Sky").classes('tracking-wide font-serif font-bold text-4xl py-8 px-8 text-black italic')
    with ui.card().classes("mx-auto my-auto h-96 w-96 bg-gradient-to-br from-purple-100 to-blue-100"):
        ui.label("Shared Exercise Platform").classes('mx-auto tracking-wide text-2xl text-black')
        ui.label("登录 Log In:").classes('mx-auto tracking-wide text-2xl text-black')
        with ui.column().classes("mx-auto my-auto"):
            with ui.row():
                ui.icon('person', color='text-indigo-400')
                ui.input(label="用户名 Username").bind_value_to(app.storage.browser, 'input_username')
            with ui.row():
                ui.icon('password', color='text-indigo-400')
                ui.input(label="密码 Password", password=True).bind_value_to(app.storage.browser, 'input_password')
            with ui.row().classes("mx-auto"):
                ui.button("登录 Log  In", on_click=async_try_login, color='text-indigo-700', icon='login') \
                    .classes('mx-auto bg-gradient-to-br from-purple-300 to-blue-300')
                ui.button("返回 Back   ", on_click=lambda: ui.open("/"), color='text-indigo-700', icon='logout') \
                    .classes('mx-auto bg-gradient-to-br from-purple-300 to-blue-300')
    if app.storage.user.get('login', "False") == "True":
        print('redirect')
        ui.open("/register")


@ui.page("/register")
def register_page():
    app.storage.user['count'] = app.storage.user.get('count', 0) + 1
    ui.query('body').classes('bg-gradient-to-br from-blue-200 to-purple-200')
    with ui.row().classes('mx-auto'):
        ui.image('/img/StarrySky_Logo.png').classes('w-12 h-12 py-8 px-8')
        ui.label("星汉 Starry Sky").classes('tracking-wide font-serif font-bold text-4xl py-8 px-8 text-black italic')
    with ui.card().classes("mx-auto my-auto h-96 w-96 bg-gradient-to-br from-purple-100 to-blue-100"):
        ui.label("Shared Exercise Platform").classes('mx-auto tracking-wide text-2xl text-black')
        ui.label("注册 Sign Up:").classes('mx-auto tracking-wide text-2xl text-black')
        with ui.column().classes("mx-auto my-auto"):
            with ui.row():
                ui.icon('person', color='text-indigo-400')
                ui.input(label="用户名 Username").bind_value_to(app.storage.browser, 'input_username')
            with ui.row():
                ui.icon('password', color='text-indigo-400')
                ui.input(label="密码 Password", password=True).bind_value_to(app.storage.browser, 'input_password')
            with ui.row().classes("mx-auto"):
                ui.button("注册 Sign Up", on_click=async_try_register, color='text-indigo-700', icon='history_edu') \
                    .classes('mx-auto bg-gradient-to-br from-purple-300 to-blue-300')
                ui.button("返回 Back   ", on_click=lambda: ui.open("/"), color='text-indigo-700', icon='logout') \
                    .classes('mx-auto bg-gradient-to-br from-purple-300 to-blue-300')


@ui.page("/user")
async def user_page():
    if app.storage.user.get('login', 'False') != 'True':
        ui.button("无权限，返回主页", on_click=lambda: ui.open('/'))
        print("error")
    else:
        init_page()
        ui.image('/img/StarrySky_Cover.jpg').classes('mx-auto')
        with ui.row():
            with ui.card().classes("mx-auto h-96 w-96 bg-gradient-to-br from-purple-50 to-purple-50"):
                ui.label('公告').classes('mx-auto tracking-wide text-2xl text-black')
                ui.label('敬请期待')
            with ui.card().classes("mx-auto h-96 w-96 bg-gradient-to-br from-purple-50 to-purple-50"):
                ui.label('做题记录').classes('mx-auto tracking-wide text-2xl text-black')


@ui.page("/user_groups")
async def user_groups_page():
    init_page()
    ui.label('用户组列表').classes('tracking-wide text-2xl py-8 text-black')


@ui.page("/question_groups")
async def question_groups_page():
    init_page()
    ui.label('问题组列表').classes('tracking-wide text-2xl py-8 text-black')









with ui.column().classes("mx-auto my-auto"):
    ui.query('body').classes('bg-gradient-to-br from-blue-200 to-purple-200')
    with ui.row().classes('mx-auto'):
        ui.image('/img/StarrySky_Logo.png').classes('w-12 h-12 py-8 px-8')
        ui.label("星汉 Starry Sky").classes('tracking-wide font-serif font-bold text-4xl py-8 px-8 text-black italic')
    with ui.card().classes("mx-auto my-auto h-96 w-96 bg-gradient-to-br from-purple-100 to-blue-100"):
        ui.label("Shared Exercise Platform").classes('mx-auto tracking-wide text-2xl text-black')
        ui.label("欢迎 Welcome!").classes('mx-auto tracking-wide text-2xl text-black')
        ui.button("注册 Sign Up", on_click=lambda: ui.open("/register"), color='text-indigo-700', icon='history_edu') \
            .classes('mx-auto bg-gradient-to-br from-purple-300 to-blue-300')
        ui.button("登录 Log  In", on_click=lambda: ui.open("/login"), color='text-indigo-700', icon='login') \
            .classes('mx-auto bg-gradient-to-br from-purple-300 to-blue-300')
ui.run(storage_secret='buaa2023')
