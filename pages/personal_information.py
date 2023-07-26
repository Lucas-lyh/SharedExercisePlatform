import hashlib

from nicegui import ui,app

import orm
from tools.search import search
from tools.loginout import logout
from orm import manager

def update_information():
    password = app.storage.user.get("input_password", "None")
    if password == "None":
        ui.notify("请输入新密码")
        return
    md5 = hashlib.md5()
    md5.update((password + "buaa2023").encode())
    password_hash = md5.hexdigest()
    succ, res = manager.update_information(username=app.storage.user['username'], pwhash=password_hash)
    ui.notify(res)

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
            ui.button("首页   ", on_click=lambda: ui.open("/user"), color='text-indigo-700', icon='home') \
                .classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("我的用户组", on_click=lambda: ui.open("/user_groups"), color='text-indigo-700',
                      icon='group').classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("我的问题组", on_click=lambda: ui.open("/question_groups"), color='text-indigo-700',
                      icon='receipt_long').classes('bg-gradient-to-br from-purple-200 to-blue-200')
    with ui.right_drawer(fixed=True).classes('bg-gradient-to-r from-blue-100 to-purple-50') \
            .props('bordered') as right_drawer:
        with ui.column():
            ui.button("个人信息 ", on_click=lambda: ui.open("/personal_information"), color='text-indigo-700',
                      icon='person').classes('bg-gradient-to-br from-purple-200 to-blue-200')
            ui.button("退出   ", on_click=logout, color='text-indigo-700',
                      icon='logout').classes('bg-gradient-to-br from-purple-200 to-blue-200')
    ui.query('body').classes('bg-gradient-to-r from-blue-100 to-white')
    ui.label('个人信息')
    global username,password
    with ui.row():
        with ui.column():
            ui.label("用户名")
            username = ui.input(app.storage.user['username'])
            username.set_enabled(False)
        with ui.column():
            ui.label("密码")
            password = ui.input(app.storage.user["password"], password=True, password_toggle_button=True).bind_value_to(app.storage.browser, 'input_password')
            password.set_enabled(False)

    def start_modify():
        password.set_enabled(True)
        app.storage.user["input_password"] = "None"

    ui.button("修改信息", on_click=lambda: start_modify())
    ui.button("保存信息", on_click=lambda: update_information())

