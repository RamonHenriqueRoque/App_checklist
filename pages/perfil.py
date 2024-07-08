import flet as ft
from services import sqlLite
from components.tela import Fundo
from datetime import datetime
from re import findall
from flet.security import encrypt
from os import getenv

class Perfil(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.fundo = Fundo(self.page).fundo()
        self.fundo.content.controls[0].opacity = 0.5
        self.sql = sqlLite.SQLite()
        
    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def senha(self):
        texto = "Por favor, inserir a senha corretamente. As senhas precisam:"

        if self.popUP.actions[0].controls[0].value == "":
            texto += "\n- ter algo escrito."

        if len(self.popUP.actions[0].controls[0].value) < 6:
            texto += "\n- terem 6 ou mais caracteres."
        
        if findall(r'[A-Z]', self.popUP.actions[0].controls[0].value) ==  []:
            texto += "\n- 1 letra maiúscula."

        if findall(r'[0-9]', self.popUP.actions[0].controls[0].value) ==  []:
            texto += "\n- 1 caracter numerico."
        
        if texto != "Por favor, inserir a senha corretamente. As senhas precisam:":
            self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                        content=ft.Text(texto),
                                        actions=[ft.TextButton("OK", on_click= self.close_banner)])
            self.page.banner.open = True
            self.page.update()
            return True
        else:
            return False

    def save_password(self, e):
        if not self.senha():
            self.sql.db_execute(query = "UPDATE cadastro_usuario SET senha = ? WHERE login = ?",
                                params= [encrypt(self.popUP.actions[0].controls[0].value, secret_key= getenv("SENHA_BD")),
                                         self.page.session.get("login")])

            self.close_PopUP(e)

    def close_PopUP(self, e):
        self.page.dialog.open = False
        self.page.update()

    def troca_senha(self, e):
        self.popUP= ft.AlertDialog(title=  ft.Text(value= "Trocar senha"),
                                    modal = True,
                                    shape= ft.RoundedRectangleBorder(radius= 5),
                                    actions=[ft.Column(controls =[ft.TextField(color= ft.colors.BLACK, hint_text="nova senha:", bgcolor= ft.colors.WHITE, password= True, can_reveal_password=True),
                                                                  ft.Divider()]),
                                             ft.Row(alignment= ft.MainAxisAlignment.CENTER,
                                                    controls =[ft.ElevatedButton(text= "Salvar", style= ft.ButtonStyle(color=ft.colors.BLACK, bgcolor= ft.colors.GREY_400), on_click= self.save_password),
                                                               ft.ElevatedButton(text= "Cancelar", style= ft.ButtonStyle(color=ft.colors.BLACK, bgcolor= ft.colors.GREY_400), on_click= self.close_PopUP)])],
                                    actions_alignment= ft.MainAxisAlignment.CENTER)
        self.page.dialog = self.popUP
        self.page.dialog.open = True   
        self.page.update()
   
    def status(self):
        if self.page.session.get_keys() != []:
            try:
                nome = self.sql.db_execute(query = "SELECT nome_completo FROM cadastro_usuario WHERE login = ?", 
                                        params= [self.page.session.get("login")])[1][0][0]
                
                quant_Checklist = self.sql.db_execute(query = "SELECT COUNT(id_login) from aparelho WHERE id_login = ?",
                                                    params= [self.sql.db_execute(query = "SELECT id_login from cadastro_usuario WHERE login = ?", 
                                                                                params= [self.page.session.get("login")])[1][0][0]])[1][0][0]
                ultima_data_checklist = self.sql.db_execute(query = "SELECT MAX(data_checklist) from checklist WHERE id_aparelho = ?",
                                                            params = [self.sql.db_execute(query = "SELECT max(id_aparelho) from aparelho WHERE id_login = ?",
                                                                                        params= [self.sql.db_execute(query = "SELECT id_login from cadastro_usuario WHERE login = ?", 
                                                                                                                    params= [self.page.session.get("login")])[1][0][0]])[1][0][0]])[1][0][0]
                
                ultima_data_checklist = datetime.strptime(ultima_data_checklist, '%Y-%m-%d %H:%M:%S.%f').strftime("%d/%m/%Y %Hh %Mm %Ss")



                return ft.Container(ft.Column(controls= [ft.Text(spans= [ft.TextSpan(text= "Nome completo: ", 
                                                                                    style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15)),
                                                                        ft.TextSpan(text= str(nome), 
                                                                                    style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=15))]),
                                                        ft.Text(spans= [ft.TextSpan(text= "Quantidades de checklist realizado: ", 
                                                                                    style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15)),
                                                                        ft.TextSpan(text= str(quant_Checklist), 
                                                                                    style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=15))]),
                                                        ft.Text(spans= [ft.TextSpan(text= "Ultima data de checklist realizado: ", 
                                                                                    style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15)),
                                                                        ft.TextSpan(text= str(ultima_data_checklist), 
                                                                                    style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=15))])]))
            except:
                nome = self.sql.db_execute(query = "SELECT nome_completo FROM cadastro_usuario WHERE login = ?", 
                                        params= [self.page.session.get("login")])[1][0][0]
                
                return ft.Container(ft.Column(controls= [ft.Text(spans= [ft.TextSpan(text= "Nome completo: ", 
                                                                                    style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15)),
                                                                        ft.TextSpan(text= str(nome), 
                                                                                    style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=15))]),
                                                        ft.Text(spans= [ft.TextSpan(text= "Quantidades de checklist realizado: ", 
                                                                                    style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15)),
                                                                        ft.TextSpan(text= str(0), 
                                                                                    style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=15))]),
                                                        ft.Text(spans= [ft.TextSpan(text= "Ultima data de checklist realizada: ", 
                                                                                    style= ft.TextStyle(color= ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15)),
                                                                        ft.TextSpan(text= "Null", 
                                                                                    style= ft.TextStyle(color= ft.colors.AMBER, weight=ft.FontWeight.BOLD, size=15))])]))
    
    def bt(self):
        return ft.Row(alignment= ft.MainAxisAlignment.CENTER,
                    controls= [ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                                controls= [ft.Text(value= "Trocar Senha",
                                                                                    size= 15,
                                                                                    color= ft.colors.BLACK,
                                                                                    weight=ft.FontWeight.BOLD)]),
                                                bgcolor= ft.colors.AMBER,
                                                height= 50,
                                                width= 150,
                                                on_click= self.troca_senha),
                            ft.Text(value= "ou", color= ft.colors.WHITE, size= 15),              
                            ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                                controls= [ft.Text(value= "Reconhecimento Facial",
                                                                                size= 15,
                                                                                    color= ft.colors.BLACK,
                                                                                    weight=ft.FontWeight.BOLD)]),
                                                bgcolor= ft.colors.AMBER,
                                                height= 50,
                                                width= 225,
                                                on_click= lambda _: self.page.go("/reconhecimentoFacial"))])

    def main(self):        
        estruturacao_status = self.status()
        estruturacao_bt= ft.Container(alignment= ft.alignment.bottom_center,
                                      height= 470,
                                      content=self.bt())

        estruturacao = ft.Container(height= 560,
                                    content= ft.Column(controls= [estruturacao_status,
                                                                  estruturacao_bt]))


        return ft.Column(controls= [ft.Stack(controls= [self.fundo, estruturacao])])