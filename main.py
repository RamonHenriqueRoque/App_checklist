import flet as ft
from pages.views import Views
from services import sqlLite

class App_Checklist:
    def __init__(self, page: ft.Page):
        self.page= page
        self.page.bgcolor = "#282a36"
        self.page.window_height= 800
        self.page.window_width = 600
        self.page.window_resizable= False          # não redimensiona
        self.page.windor_always_on_top= True       # sempre como primeiro plano
        self.page.window_maximizable = False
        self.page.title = "Ferramenta de Checklist"
        
        sqlLite.SQLite().criacao_base()
        self.page.session.clear()

        self.page.on_route_change = self.route_change
        self.page.go("/login")

    def route_change(self, e: ft.RouteChangeEvent):
        self.page.views.clear()
        self.page.views.append(Views(self.page).main()[self.page.route])
        self.page.go(self.page.route)
        self.page.update()

if __name__ == '__main__':
    ft.app(target= App_Checklist, assets_dir="assets", view=ft.AppView.FLET_APP_WEB, port= 5354)