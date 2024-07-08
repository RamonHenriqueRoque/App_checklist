import flet as ft
from os import environ, system

class Fundo(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.on_keyboard_event = self.on_keyboard

    def on_keyboard(self, e: ft.KeyboardEvent):
        if e.key  == "Escape":
            self.PopUp(e)

    def close_app(self, e):
        self.page.window_close()

    def close_PopUP(self, e):
        self.page.dialog.open = False
        self.page.update()

    def PopUp(self, e):
        popUP= ft.AlertDialog(title=  ft.Text(value= "Deseja fechar o aplicativo?"),
                            modal = True,
                            shape= ft.RoundedRectangleBorder(radius= 5),
                            actions=[ft.ElevatedButton(text= "Não", style= ft.ButtonStyle(color=ft.colors.BLACK, bgcolor= ft.colors.GREY_400), on_click= self.close_PopUP),
                                    ft.ElevatedButton(text= "Sim", style= ft.ButtonStyle(color=ft.colors.BLACK, bgcolor= ft.colors.GREY_400), on_click= self.close_app)],
                            actions_alignment= ft.MainAxisAlignment.CENTER)
        self.page.dialog = popUP
        self.page.dialog.open = True   
        self.page.update()



    def appbar(self, title: ft.Text):
        nome= self.page.session.get("NomeUsuario")
        appbar= ft.AppBar(title= title,
                        bgcolor= "#3a3c4e",
                        center_title= False,
                        toolbar_height= 100,
                        color= ft.colors.WHITE,
                        leading= ft.CircleAvatar(content= ft.Text(value= "" if nome == None else "".join([list(i)[0] for i in nome.upper().split(" ")[:2]]),
                                                                  color= ft.colors.BLACK), 
                                                bgcolor= ft.colors.WHITE),
                        actions= [ft.PopupMenuButton(bgcolor= ft.colors.GREY_800,
                                                       items= [ft.PopupMenuItem(content= ft.Row(controls= [ft.Icon(name= ft.icons.PERSON, color= ft.colors.WHITE),
                                                                                                        ft.Text(value= "Perfil", color= ft.colors.WHITE)]),
                                                                                on_click= lambda _: self.page.go("/perfil")),
                                                                ft.PopupMenuItem(content= ft.Row(controls= [ft.Icon(name= ft.icons.HOME, color= ft.colors.WHITE),
                                                                                                        ft.Text(value= "Home", color= ft.colors.WHITE)]),
                                                                                on_click= lambda _: self.page.go("/home")),
                                                                ft.PopupMenuItem(content= ft.Row(controls= [ft.Icon(name= ft.icons.COMPUTER, color= ft.colors.WHITE),
                                                                                                            ft.Text(value= "Checklist", color= ft.colors.WHITE)]),
                                                                                    on_click = lambda _: self.page.go("/checklist")),
                                                                ft.PopupMenuItem(content= ft.Row(controls= [ft.Icon(name= ft.icons.DASHBOARD, color= ft.colors.WHITE),
                                                                                                            ft.Text(value= "Dashboard", color= ft.colors.WHITE)]),
                                                                                    on_click = lambda _: system('streamlit run dashboard/app.py --server.port 5353 --theme.primaryColor="#ffc107" --theme.backgroundColor="#282a36" --theme.secondaryBackgroundColor="#262626" --theme.textColor="#ffffff" --theme.font="monospace"')),
                                                                ft.PopupMenuItem(content= ft.Row(controls= [ft.Icon(name= ft.icons.LOGIN, color= ft.colors.WHITE),
                                                                                                            ft.Text(value= "Deslogar", color= ft.colors.WHITE)]),
                                                                                    on_click = lambda _: self.page.go("/login")),
                                                                ft.PopupMenuItem(content= ft.Row(controls= [ft.Icon(name=  ft.icons.CLOSE, color= ft.colors.WHITE),
                                                                                                            ft.Text(value= "Sair", color= ft.colors.WHITE)]),
                                                                                    on_click = self.PopUp)],
                                                        )])
        return appbar
    
    def fundo(self):
        fundo = ft.Container(content= ft.Row(vertical_alignment= ft.MainAxisAlignment.CENTER,
                                            alignment= ft.CrossAxisAlignment.CENTER,
                                            controls= [ft.Image(src= "icons/Logo Ramon White.png",
                                                                fit=ft.ImageFit.CONTAIN,
                                                                opacity= 0.5,
                                                                height= self.page.window_height - 250,
                                                                width= self.page.window_width)]))
        return fundo
    def rodape(self):        
        rodape = ft.BottomAppBar(bgcolor= "#3a3c4e",
                                        content= ft.ResponsiveRow(columns= 12,
                                                                controls= [ft.Text(col= 6,
                                                                                        text_align= ft.TextAlign.START,
                                                                                        spans= [ft.TextSpan(text= "₢ 2024 Todos os direitos reservados", style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=12))]),
                                                                            ft.Text(col= 6,
                                                                                        spans= [ft.TextSpan(text= "Email: ", style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=12)),
                                                                                            ft.TextSpan(text= "hramonroque@gmail.com", style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=12),
                                                                                                        url= "mailto: hramonroque@gmail.com")],
                                                                                        text_align= ft.TextAlign.END),

                                                                            ft.Text(col= 6,
                                                                                        spans= [ft.TextSpan(text= "Linkedin: ", style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=12)),
                                                                                            ft.TextSpan(text= "linkedin.com/in/ramonhroque/", style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=12),
                                                                                                        url= "https://www.linkedin.com/in/ramonhroque/")],
                                                                                        text_align= ft.TextAlign.START),
                                                                                        
                                                                            ft.Text(col= 6,
                                                                                        spans= [ft.TextSpan(text= "Github: ", style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=12)),
                                                                                            ft.TextSpan(text= "github.com/RamonHenriqueRoque", style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=12),
                                                                                                        url= "https://github.com/RamonHenriqueRoque")],
                                                                                        text_align= ft.TextAlign.END)]))
        return rodape
        