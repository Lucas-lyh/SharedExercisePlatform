# This is a sample Python script
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from nicegui import ui, app
from uuid import uuid4
import asyncio
import hashlib
from orm import Manager

manager = Manager()


async def async_try_login():
    username = (app.storage.browser.get("input_username", 'None'))
    password = app.storage.browser.get("input_password", "None")
    if username == "None" or password == "None":
        return
    md5 = hashlib.md5()
    md5.update((password + "buaa2023").encode())
    password_hash = md5.hexdigest()
    if manager.try_login(username=username, pwhash=password_hash):
        app.storage.user["login"] = "True"
        ui.open(user_page)
    else:
        app.storage.user["login"] = "False"
        ui.open(login_page)


async def async_try_register():
    username = (app.storage.browser.get("input_username", 'None'))
    password = app.storage.browser.get("input_password", "None")
    if username == "None" or password == "None":
        return
    md5 = hashlib.md5()
    md5.update((password + "buaa2023").encode())
    password_hash = md5.hexdigest()
    if manager.try_register(username=username, pwhash=password_hash):
        ui.open(login_page)
    else:
        ui.open(register_page)


async def logout():
    app.storage.user['login'] = 'False'
    ui.open('/')


number = [1]


@ui.page("/login")
def login_page():
    ui.query('body').classes('bg-gradient-to-br from-blue-200 to-purple-200')
    with ui.row().classes('mx-auto'):
        ui.image('https://pic.imgdb.cn/item/64bcdda21ddac507cc03cdde.png').classes('w-12 h-12 py-8 px-8')
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
        ui.open(register_page)


@ui.page("/register")
def register_page():
    app.storage.user['count'] = app.storage.user.get('count', 0) + 1
    """with ui.row():
        ui.label('your own page visits:')
        ui.label().bind_text_from(app.storage.user, 'count')
    """
    ui.query('body').classes('bg-gradient-to-br from-blue-200 to-purple-200')
    with ui.row().classes('mx-auto'):
        ui.image('https://pic.imgdb.cn/item/64bcdda21ddac507cc03cdde.png').classes('w-12 h-12 py-8 px-8')
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
        with ui.header(elevated=True) \
                .classes('items-center justify-between bg-gradient-to-br from-blue-400 to-purple-300'):
            ui.label("星汉 Starry Sky").classes('text-2xl font-bold tracking-wide font-serif text-white italic')
            ui.button(on_click=lambda: search, icon='search').props('flat color=white')
            ui.button(on_click=lambda: right_drawer.toggle(), icon='more_vert').props('flat color=white')
        with ui.left_drawer(top_corner=False, bottom_corner=True) \
                .classes('bg-gradient-to-r from-blue-100 to-purple-50'):
            with ui.column():
                ui.button("首页   ", on_click=lambda: ui.open(user_page), color='text-indigo-700', icon='home') \
                    .classes('bg-gradient-to-br from-purple-200 to-blue-200')
                ui.button("我的用户组", on_click=lambda: ui.open(user_groups_page), color='text-indigo-700',
                          icon='group').classes('bg-gradient-to-br from-purple-200 to-blue-200')
                ui.button("我的问题组", on_click=lambda: ui.open(question_groups_page), color='text-indigo-700',
                          icon='receipt_long').classes('bg-gradient-to-br from-purple-200 to-blue-200')
        with ui.right_drawer(fixed=True).classes('bg-gradient-to-r from-blue-100 to-purple-50') \
                .props('bordered') as right_drawer:
            with ui.column():
                ui.button("个人信息 ", on_click=lambda: ui.open(personal_information_page), color='text-indigo-700',
                          icon='person').classes('bg-gradient-to-br from-purple-200 to-blue-200')
                ui.button("退出   ", on_click=logout, color='text-indigo-700',
                          icon='logout').classes('bg-gradient-to-br from-purple-200 to-blue-200')
        ui.query('body').classes('bg-gradient-to-r from-blue-100 to-white')
        ui.image('https://pic.imgdb.cn/item/64bcdda21ddac507cc03cd98.jpg').classes('mx-auto')
        with ui.row():
            with ui.card().classes("mx-auto h-96 w-96 bg-gradient-to-br from-purple-50 to-purple-50"):
                ui.label('公告').classes('mx-auto tracking-wide text-2xl text-black')
                ui.label('敬请期待')
            with ui.card().classes("mx-auto h-96 w-96 bg-gradient-to-br from-purple-50 to-purple-50"):
                ui.label('做题记录').classes('mx-auto tracking-wide text-2xl text-black')


@ui.page("/user_groups")
async def user_groups_page():
    with ui.header(elevated=True) \
            .classes('items-center justify-between bg-gradient-to-br from-blue-400 to-purple-300'):
        ui.label("星汉 Starry Sky").classes('text-2xl font-bold tracking-wide font-serif text-white italic')
        ui.button(on_click=lambda: search, icon='search').props('flat color=white')
        ui.button(on_click=lambda: right_drawer.toggle(), icon='more_vert').props('flat color=white')
    with ui.left_drawer(top_corner=False, bottom_corner=True) \
            .classes('bg-gradient-to-r from-blue-100 to-purple-50'):
        with ui.column():
            ui.button("首页   ", on_click=lambda: ui.open(user_page), color='text-indigo-700', icon='home') \
                .classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("我的用户组", on_click=lambda: ui.open(user_groups_page), color='text-indigo-700',
                      icon='group').classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("我的问题组", on_click=lambda: ui.open(question_groups_page), color='text-indigo-700',
                      icon='receipt_long').classes('bg-gradient-to-br from-purple-200 to-blue-200')
    with ui.right_drawer(fixed=True).classes('bg-gradient-to-r from-blue-100 to-purple-50') \
            .props('bordered') as right_drawer:
        with ui.column():
            ui.button("个人信息 ", on_click=lambda: ui.open(personal_information_page), color='text-indigo-700',
                      icon='person').classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("退出   ", on_click=logout, color='text-indigo-700',
                      icon='logout').classes('bg-gradient-to-br from-purple-200 to-blue-200')
    ui.query('body').classes('bg-gradient-to-r from-blue-100 to-white')
    ui.label('用户组列表')


@ui.page("/question_groups")
async def question_groups_page():
    with ui.header(elevated=True) \
            .classes('items-center justify-between bg-gradient-to-br from-blue-400 to-purple-300'):
        ui.label("星汉 Starry Sky").classes('text-2xl font-bold tracking-wide font-serif text-white italic')
        ui.button(on_click=lambda: search, icon='search').props('flat color=white')
        ui.button(on_click=lambda: right_drawer.toggle(), icon='more_vert').props('flat color=white')
    with ui.left_drawer(top_corner=False, bottom_corner=True) \
            .classes('bg-gradient-to-r from-blue-100 to-purple-50'):
        with ui.column():
            ui.button("首页   ", on_click=lambda: ui.open(user_page), color='text-indigo-700', icon='home') \
                .classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("我的用户组", on_click=lambda: ui.open(user_groups_page), color='text-indigo-700',
                      icon='group').classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("我的问题组", on_click=lambda: ui.open(question_groups_page), color='text-indigo-700',
                      icon='receipt_long').classes('bg-gradient-to-br from-purple-200 to-blue-200')
    with ui.right_drawer(fixed=True).classes('bg-gradient-to-r from-blue-100 to-purple-50') \
            .props('bordered') as right_drawer:
        with ui.column():
            ui.button("个人信息 ", on_click=lambda: ui.open(personal_information_page), color='text-indigo-700',
                      icon='person').classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("退出   ", on_click=logout, color='text-indigo-700',
                      icon='logout').classes('bg-gradient-to-br from-purple-200 to-blue-200')
    ui.query('body').classes('bg-gradient-to-r from-blue-100 to-white')
    ui.label('问题组列表')


@ui.page("/personal_information")
async def personal_information_page():
    with ui.header(elevated=True) \
            .classes('items-center justify-between bg-gradient-to-br from-blue-400 to-purple-300'):
        ui.label("星汉 Starry Sky").classes('text-2xl font-bold tracking-wide font-serif text-white italic')
        ui.button(on_click=lambda: search, icon='search').props('flat color=white')
        ui.button(on_click=lambda: right_drawer.toggle(), icon='more_vert').props('flat color=white')
    with ui.left_drawer(top_corner=False, bottom_corner=True) \
            .classes('bg-gradient-to-r from-blue-100 to-purple-50'):
        with ui.column():
            ui.button("首页   ", on_click=lambda: ui.open(user_page), color='text-indigo-700', icon='home') \
                .classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("我的用户组", on_click=lambda: ui.open(user_groups_page), color='text-indigo-700',
                      icon='group').classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("我的问题组", on_click=lambda: ui.open(question_groups_page), color='text-indigo-700',
                      icon='receipt_long').classes('bg-gradient-to-br from-purple-200 to-blue-200')
    with ui.right_drawer(fixed=True).classes('bg-gradient-to-r from-blue-100 to-purple-50') \
            .props('bordered') as right_drawer:
        with ui.column():
            ui.button("个人信息 ", on_click=lambda: ui.open(personal_information_page), color='text-indigo-700',
                      icon='person').classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("退出   ", on_click=logout, color='text-indigo-700',
                      icon='logout').classes('bg-gradient-to-br from-purple-200 to-blue-200')
    ui.query('body').classes('bg-gradient-to-r from-blue-100 to-white')
    ui.label('个人信息')


def search():
    a = 2


with ui.column().classes("mx-auto my-auto"):
    ui.query('body').classes('bg-gradient-to-br from-blue-200 to-purple-200')
    with ui.row().classes('mx-auto'):
        ui.image('https://pic.imgdb.cn/item/64bcdda21ddac507cc03cdde.png').classes('w-12 h-12 py-8 px-8')
        ui.label("星汉 Starry Sky").classes('tracking-wide font-serif font-bold text-4xl py-8 px-8 text-black italic')
    with ui.card().classes("mx-auto my-auto h-96 w-96 bg-gradient-to-br from-purple-100 to-blue-100"):
        ui.label("Shared Exercise Platform").classes('mx-auto tracking-wide text-2xl text-black')
        ui.label("欢迎 Welcome!").classes('mx-auto tracking-wide text-2xl text-black')
        ui.button("注册 Sign Up", on_click=lambda: ui.open(register_page), color='text-indigo-700', icon='history_edu') \
            .classes('mx-auto bg-gradient-to-br from-purple-300 to-blue-300')
        ui.button("登录 Log  In", on_click=lambda: ui.open(login_page), color='text-indigo-700', icon='login') \
            .classes('mx-auto bg-gradient-to-br from-purple-300 to-blue-300')
ui.run(storage_secret='buaa2023')
