import flet as ft
from services import sqlLite
from re import findall
from datetime import datetime
from os import getenv
from flet.security import encrypt, decrypt
from flet.auth.providers import GitHubOAuthProvider

class Login(ft.UserControl):
  def __init__(self, page):
    super().__init__()
    self.page = page
    self.sql= sqlLite.SQLite()

    self.page.on_login = self.on_login

  def close_banner(self, e):
    self.page.banner.open = False
    self.page.update()

  def entrar_home(self, e):
    if findall(r'\b[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.painel.controls[1].value) != []:
      
      login = self.sql.db_execute(query = "SELECT login, senha, nome_completo FROM cadastro_usuario WHERE login = ?", 
                                  params= [self.painel.controls[1].value.lower()])[1]
      if login != []:
        if decrypt(login[0][1], getenv("SENHA_BD")) == self.painel.controls[3].value:
          self.page.session.set("login", self.painel.controls[1].value.lower())
          self.page.session.set("NomeUsuario", login[0][2])
          self.page.go("/home")
          

        else:
          self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                   content=ft.Text("Senha Incorreta."),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
          self.page.banner.open = True
          self.page.update()
      else:
        self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                   content=ft.Text("Email Incorreto."),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
        self.page.banner.open = True
        self.page.update()
    else:
        self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                   content=ft.Text("Email Incorreto."),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
        self.page.banner.open = True
        self.page.update()

  def entrar_github(self, e):
    self.page.login(provider = GitHubOAuthProvider(client_id=getenv("GITHUB_CLIENT_ID"),
                                                   client_secret=getenv("GITHUB_CLIENT_SECRET"),
                                                   redirect_url="http://127.0.0.1:5354/oauth_callback"))

  def on_login(self, e):
        if not e.error:
          login = self.sql.db_execute(query = "SELECT login FROM cadastro_usuario WHERE login = ?", 
                                      params= [self.page.auth.user["email"]])[1]
    
          if login != []:
            self.page.session.set("NomeUsuario", self.page.auth.user["name"])
            self.page.session.set("login", self.page.auth.user["email"])
            self.page.go("/home")
          else:
            self.sql.db_execute(query = "INSERT INTO cadastro_usuario(nome_completo, login, senha, data_criacao, data_ultima_senha) VALUES (?, ?, ?, ?, ?)", 
                params= [self.page.auth.user["name"],
                        self.page.auth.user["email"],
                        encrypt(str(self.page.auth.user["id"]), secret_key= getenv("SENHA_BD")),
                        datetime.now(),
                        datetime.now()])
        else:
          #Mensagem de error
          self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                              leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                              content=ft.Text("Por favor, inserir o nome corretamente."),
                              actions=[ft.TextButton("OK", on_click= self.close_banner)])
          self.page.banner.open = True
          print(f"Login error: {e.error}\nDescription error: {e.error_description}", e.error)
          self.page.update()


  def main(self):
    bt = ft.Row(alignment= ft.MainAxisAlignment.CENTER,
                controls= [ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                             controls= [ft.Text(value= "Entrar",
                                                                                size= 15,
                                                                                color= ft.colors.BLACK,
                                                                                weight=ft.FontWeight.BOLD)]),
                                             bgcolor= ft.colors.AMBER,
                                             height= 50,
                                             width= 150,
                                             on_click= self.entrar_home),
                          ft.Text(value= "ou", color= ft.colors.WHITE, size= 15),              
                          ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                             controls= [ft.Text(value= "Criar Conta",
                                                                               size= 15,
                                                                                color= ft.colors.BLACK,
                                                                                weight=ft.FontWeight.BOLD)]),
                                             bgcolor= ft.colors.AMBER,
                                             height= 50,
                                             width= 150,
                                             on_click= lambda _: self.page.go('/login/cadastroUsuario')),
                          ft.Text(value= "ou", color= ft.colors.WHITE, size= 15),                   
                          ft.IconButton(content= ft.Image(src= "icons/github.png", height= 50),
                                        on_click= self.entrar_github),
                          ft.Text(value= "ou", color= ft.colors.WHITE, size= 15),                   
                          ft.IconButton(content= ft.Image(src= "icons/reconhecimento-facial.png", height= 50),
                                        on_click= lambda _: self.page.go("/login/reconhecimentoFacial"))])
    
    self.painel = ft.Column(alignment= ft.MainAxisAlignment.CENTER,
                            controls= [ft.Text(value= "Email cadastrado", color= ft.colors.WHITE),
                                        ft.TextField(hint_text= "Digite seu email cadastrado aqui.",
                                                    border_color= ft.colors.WHITE,
                                                    color= ft.colors.WHITE,
                                                    bgcolor= ft.colors.with_opacity(0.5, ft.colors.BLACK12),
                                                    hint_style= ft.TextStyle(color= ft.colors.WHITE)),
                                        ft.Text(value= "Senha", color= ft.colors.WHITE),
                                        ft.TextField(hint_text= "Digite sua senha aqui.",
                                                    border_color= ft.colors.WHITE,
                                                    color= ft.colors.WHITE,
                                                    bgcolor= ft.colors.with_opacity(0.5, ft.colors.BLACK12),
                                                    hint_style= ft.TextStyle(color= ft.colors.WHITE),
                                                    password=True, 
                                                    can_reveal_password=True),
                                        ft.Container(alignment= ft.alignment.center_right,
                                                    content= ft.TextButton(on_click= lambda _: self.page.go("/login/esqueceuSenha"),
                                                                            content= ft.Column(controls= [ft.Text(value= "Esqueceu a senha?",
                                                                                                                  color= ft.colors.RED,
                                                                                                                  weight=ft.FontWeight.BOLD)]))),
                                        bt])
    
    return ft.Container(content= self.painel,
                        alignment=ft.alignment.bottom_center,
                        height= self.page.window_height - 250)

class Login_cadastrar(ft.UserControl):
  def __init__(self, page):
    super().__init__()
    self.page = page
    self.sql= sqlLite.SQLite()

  def verificar_email(self):
    login = self.sql.db_execute(query = "SELECT login FROM cadastro_usuario WHERE login = ?", 
                                params= [self.campos.controls[3].value.lower()])[1]
    
    if login != []:
      self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                   content=ft.Text("Email já cadastrado."),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
      self.page.banner.open = True
      self.page.update()
      return True

    return False


  def senha(self):
    texto = "Por favor, inserir a senha corretamente. As senhas precisam:"

    if self.campos.controls[5].value != self.campos.controls[7].value:
      texto += "\n- ser iguais."
    
    if self.campos.controls[5].value == "":
      texto += "\n- ter algo escrito."

    if len(self.campos.controls[5].value) < 6:
      texto += "\n- terem 6 ou mais caracteres."
    
    if findall(r'[A-Z]', self.campos.controls[5].value) ==  []:
      texto += "\n- 1 letra maiúscula."

    if findall(r'[0-9]', self.campos.controls[5].value) ==  []:
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

  def close_banner(self, e):
    self.page.banner.open = False
    self.page.update()

  def cadastrar(self, e):
    if self.campos.controls[1].value ==  "" or len(self.campos.controls[1].value.split(" ")) <= 1:
      self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                   content=ft.Text("Por favor, inserir o nome corretamente."),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
      self.page.banner.open = True
      self.page.update()

    elif self.verificar_email() or self.senha():
      pass

    elif findall(r'\b[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.campos.controls[3].value) == []:
      self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                   content=ft.Text("Por favor, inserir o email corretamente."),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
      self.page.banner.open = True
      self.page.update()

    else:
       self.sql.db_execute(query = "INSERT INTO cadastro_usuario(nome_completo, login, senha, data_criacao, data_ultima_senha) VALUES (?, ?, ?, ?, ?)", 
                       params= [self.campos.controls[1].value,
                                self.campos.controls[3].value.lower(),
                                encrypt(self.campos.controls[5].value, secret_key= getenv("SENHA_BD")),
                                datetime.now(),
                                datetime.now()])
       self.page.banner = ft.Banner(bgcolor=ft.colors.GREEN_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.GREEN, size=40),
                                   content=ft.Text("Cadastro com sucesso."),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
       self.page.banner.open = True
       self.page.update()
       self.page.go('/login')

  def main(self):
    bt = ft.Row(alignment= ft.MainAxisAlignment.CENTER,
                controls= [ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                          controls= [ft.Text(value= "Criar Conta",
                                                                            size= 15,
                                                                            color= ft.colors.BLACK,
                                                                            weight=ft.FontWeight.BOLD)]),
                                          bgcolor= ft.colors.AMBER,
                                          height= 50,
                                          width= 150,
                                          on_click= self.cadastrar),
                          ft.Text(value= "ou", color= ft.colors.WHITE, size= 15),                 
                          ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                            controls= [ft.Text(value= "Voltar",
                                                                              size= 15,
                                                                              color= ft.colors.BLACK,
                                                                              weight=ft.FontWeight.BOLD)]),
                                              bgcolor= ft.colors.AMBER,
                                              height= 50,
                                              width= 150,
                                              on_click= lambda _: self.page.go('/login'))])

    self.campos= ft.Column(alignment= ft.MainAxisAlignment.START,
                          controls= [ft.Text(value= "Nome Completo", color= ft.colors.WHITE),
                                      ft.TextField(hint_text= "Insira o nome completo.",
                                                  border_color= ft.colors.WHITE,
                                                  color= ft.colors.WHITE,
                                                  bgcolor= ft.colors.with_opacity(0.5, ft.colors.BLACK12),
                                                  hint_style= ft.TextStyle(color= ft.colors.WHITE)),
                                    ft.Text(value= "Insira seu email", color= ft.colors.WHITE),
                                      ft.TextField(hint_text= "Digite seu email.",
                                                  border_color= ft.colors.WHITE,
                                                  color= ft.colors.WHITE,
                                                  bgcolor= ft.colors.with_opacity(0.5, ft.colors.BLACK12),
                                                  hint_style= ft.TextStyle(color= ft.colors.WHITE)),
                                      ft.Text(value= "Senha", color= ft.colors.WHITE),
                                      ft.TextField(hint_text= "Digite sua senha aqui.",
                                                  border_color= ft.colors.WHITE,
                                                  color= ft.colors.WHITE,
                                                  bgcolor= ft.colors.with_opacity(0.5, ft.colors.BLACK12),
                                                  hint_style= ft.TextStyle(color= ft.colors.WHITE),
                                                  password=True, 
                                                  can_reveal_password=True),
                                      ft.Text(value= "Senha novamente", color= ft.colors.WHITE),
                                      ft.TextField(hint_text= "Digite sua senha aqui.",
                                                  border_color= ft.colors.WHITE,
                                                  color= ft.colors.WHITE,
                                                  bgcolor= ft.colors.with_opacity(0.5, ft.colors.BLACK12),
                                                  hint_style= ft.TextStyle(color= ft.colors.WHITE),
                                                  password=True, 
                                                  can_reveal_password=True),
                                      ft.Container(height= 15),
                                      bt])

    return ft.Container(content= self.campos,
                        alignment=ft.alignment.bottom_center,
                        height= self.page.window_height - 250)
  
class Login_EsqueceuSenha(ft.UserControl):
  def __init__(self, page):
    super().__init__()
    self.page = page
    self.sql= sqlLite.SQLite()

  def verificar_email(self):
    login = self.sql.db_execute(query = "SELECT login FROM cadastro_usuario WHERE login = ?", 
                                params= [self.painel.controls[1].value.lower()])[1]
    
    if login == []:
      self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                   content=ft.Text("Email incorreto."),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
      self.page.banner.open = True
      self.page.update()
      return False
    else:
      return True
  
  def enviar_email(self, e):
    if self.verificar_email() == True:
      self.page.go("/login")
    else:
      self.page.go("/login")

  def close_banner(self, e):
    self.page.banner.open = False
    self.page.update()

  def login(self):
    bt = ft.Row(alignment= ft.MainAxisAlignment.CENTER,
                controls= [ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                             controls= [ft.Text(value= "Enviar",
                                                                               size= 15,
                                                                                color= ft.colors.BLACK,
                                                                                weight=ft.FontWeight.BOLD)]),
                                             bgcolor= ft.colors.AMBER,
                                             height= 50,
                                             width= 150,
                                             on_click= self.enviar_email),
                          ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                             controls= [ft.Text(value= "Voltar",
                                                                               size= 15,
                                                                                color= ft.colors.BLACK,
                                                                                weight=ft.FontWeight.BOLD)]),
                                             bgcolor= ft.colors.AMBER,
                                             height= 50,
                                             width= 150,
                                             on_click= lambda _: self.page.go("/login"))])
    
    self.painel = ft.Column(alignment= ft.MainAxisAlignment.CENTER,
                       controls= [ft.Text(value= "Email cadastrado", color= ft.colors.WHITE),
                                  ft.TextField(hint_text= "Digite seu email aqui.",
                                               border_color= ft.colors.WHITE,
                                               color= ft.colors.WHITE,
                                               bgcolor= ft.colors.with_opacity(0.5, ft.colors.BLACK12),
                                               hint_style= ft.TextStyle(color= ft.colors.WHITE)),
                                  bt])
    
    return ft.Container(content= self.painel,
                        height= self.page.window_height - 250,
                        width= self.page.window_width - 45)

  def main(self):
    return ft.Row(controls= [self.login()])