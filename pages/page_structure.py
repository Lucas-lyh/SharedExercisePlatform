from nicegui import app,ui
from tools.search import search
from tools.loginout import logout

def init_page():
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
