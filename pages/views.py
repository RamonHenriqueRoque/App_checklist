import flet as ft

#View
from pages.checklist import Checklist
from pages.perfil import Perfil
from pages.login import Login, Login_cadastrar, Login_EsqueceuSenha
from pages.faceid import faceid_detecao, faceid_login
from components.tela import Fundo


class Views:
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.fonts= {"Myriad": "fonts/Myriad.ttf"}

    def main(self):
        font_family = "Myriad"
        return {'/perfil':ft.View(route='/perfil', 
                            appbar= Fundo(self.page).appbar(title = ft.Text(value= "Perfil", font_family= font_family, size= 30)), 
                            controls=[Perfil(self.page).main(), 
                                      Fundo(self.page).rodape()], 
                            bgcolor = "#282a36"),
                '/home':ft.View(route='/home', 
                            appbar= Fundo(self.page).appbar(title = ft.Text(value= "Home", font_family= font_family, size= 30)), 
                            controls=[Fundo(self.page).fundo(), 
                                      Fundo(self.page).rodape()], 
                            bgcolor = "#282a36"),
                '/checklist':ft.View(route='/checklist', 
                                     appbar= Fundo(self.page).appbar(title = ft.Text(value= "Checklist", font_family= font_family, size= 30)), 
                                     controls=[Checklist(self.page).main(),
                                               Fundo(self.page).rodape()], 
                                     bgcolor = "#282a36",
                                     scroll= ft.ScrollMode.HIDDEN),
                '/dashboard':ft.View(route='/dashboard', 
                                     appbar= Fundo(self.page).appbar(title = ft.Text(value= "Dashboard", font_family= font_family, size= 30)), 
                            controls=[Fundo(self.page).fundo(), 
                                      Fundo(self.page).rodape()], 
                            bgcolor = "#282a36"),
                '/login':ft.View(route='/login', 
                                 appbar= ft.AppBar(title= ft.Text(value= "Login", color= ft.colors.WHITE, font_family= font_family, size= 30), 
                                                   bgcolor= "#3a3c4e", center_title= False, toolbar_height= 100, 
                                                   actions= [ft.Image(src= "icons/Logo Ramon White.png", height= 60, fit= ft.ImageFit.FILL)]),
                                 controls=[Login(self.page).main(),
                                           Fundo(self.page).rodape()], 
                                 bgcolor = "#282a36"),
                '/login/cadastroUsuario':ft.View(route='/login/cadastroUsuario', 
                                 appbar= ft.AppBar(title= ft.Text(value= "Cadastro dos usuários", color= ft.colors.WHITE, font_family=font_family, size= 30), 
                                                   bgcolor= "#3a3c4e", center_title= False, toolbar_height= 100, 
                                                   actions= [ft.Image(src= "icons/Logo Ramon White.png", height= 60, fit= ft.ImageFit.FILL)]),
                                controls=[Login_cadastrar(self.page).main(),
                                          Fundo(self.page).rodape()], 
                                bgcolor = "#282a36"),
                '/login/esqueceuSenha':ft.View(route='/login/esqueceuSenha', 
                                 appbar=  ft.AppBar(title= ft.Text(value= "Esqueceu a senha", color= ft.colors.WHITE, font_family= font_family, size= 30), 
                                                   bgcolor= "#3a3c4e", center_title= False, toolbar_height= 100, 
                                                   actions= [ft.Image(src= "icons/Logo Ramon White.png", height= 60, fit= ft.ImageFit.FILL)]),
                                controls=[Login_EsqueceuSenha(self.page).main(),
                                          Fundo(self.page).rodape()], 
                                bgcolor = "#282a36"),
                '/login/reconhecimentoFacial':ft.View(route='/login/reconhecimentoFacial', 
                                 appbar=  ft.AppBar(title= ft.Text(value= "Reconhecimento Facial", color= ft.colors.WHITE, font_family= font_family, size= 30), 
                                                   bgcolor= "#3a3c4e", center_title= False, toolbar_height= 100, 
                                                   actions= [ft.Image(src= "icons/Logo Ramon White.png", height= 60, fit= ft.ImageFit.FILL)]),
                                controls=[faceid_login(self.page).main()], 
                                bgcolor = "#282a36")
                                ,
                '/reconhecimentoFacial':ft.View(route='/reconhecimentoFacial', 
                                 appbar=  ft.AppBar(title= ft.Text(value= "Reconhecimento Facial", color= ft.colors.WHITE, font_family= font_family, size= 30), 
                                                   bgcolor= "#3a3c4e", center_title= False, toolbar_height= 100, 
                                                   actions= [ft.Image(src= "icons/Logo Ramon White.png", height= 60, fit= ft.ImageFit.FILL)]),
                                controls=[faceid_detecao(self.page).main()], 
                                bgcolor = "#282a36")}