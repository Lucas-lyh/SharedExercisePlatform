import hashlib

from nicegui import ui,app

import orm
from tools.search import search
from tools.loginout import logout
from orm import manager
from pages.page_structure import init_page

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
    init_page()
    ui.label('个人信息').classes('tracking-wide text-2xl py-8 text-black')
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

