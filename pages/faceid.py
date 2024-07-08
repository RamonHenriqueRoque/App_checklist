import flet as ft
import cv2
import base64
from services import sqlLite
from os import path, remove
from glob import glob
import numpy as np
from time import time

class faceid_detecao(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.sql= sqlLite.SQLite()
        
    def treinamento(self):
        eigenface = cv2.face.EigenFaceRecognizer_create()
        eigenface.read('assets/cv2/modelo/classificadorEigen.yml')
        
        caminho_completo = path.join("assets/cv2/fotos", '*.png')
        arquivos = glob(caminho_completo)

        ids= []
        faces= []
        for arquivo in arquivos:
            imageFace= cv2.cvtColor(cv2.imread(arquivo), cv2.COLOR_BGR2GRAY)
            id= arquivo.split("assets/cv2/fotos\\")[1].split(" -")[0]

            ids.append(int(id))
            faces.append(imageFace)

            remove(arquivo)

        eigenface.train(faces, np.array(ids))
        eigenface.write('assets/cv2/modelo/classificadorEigen.yml')
      
    def camera(self, e):
        self.estruturacao.controls[1].visible = True
        self.estruturacao.controls[2].controls[0].visible = False
        self.estruturacao.controls[2].controls[1].visible = False

        id_user = str(self.sql.db_execute(query= "SELECT id_login, nome_completo FROM cadastro_usuario WHERE login = ?",
                                         params= [self.page.session.get("login")])[1][0][0])

        haar_cascade = cv2.CascadeClassifier("venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
        face = cv2.VideoCapture(0)
        img = ft.Image(border_radius=ft.border_radius.all(20), height= 450, width= 600)
        self.estruturacao.controls[0].content= img
        n_png = -1

        while True:
            _, frame = face.read()

            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 4, minSize= (35,35)) 
            for (x, y, w, h) in faces_rect: 
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
            if len(faces_rect) == 1:
                face_off = cv2.resize(gray_img[y:y + h, x:x + w], (64, 64))

                caminho_completo = path.join("assets/cv2/fotos", '*.png')
                n_png = len(glob(caminho_completo))

                self.estruturacao.controls[1].value = n_png                #Slider

                if n_png >= 100:
                    break
            
                cv2.imwrite(f"assets/cv2/fotos/{id_user} - {n_png}.png", face_off)
            
            _, im_arr = cv2.imencode('.png', frame)
            im_b64 = base64.b64encode(im_arr)
            img.src_base64= im_b64.decode("utf-8")
            self.estruturacao.update()

        face.release()
        cv2.destroyAllWindows()
        
        self.treinamento()
        self.page.go("/home")
        self.page.update()

    def main(self):
        self.estruturacao = ft.Column(controls= [ft.Container(margin= 15),
                                                 ft.Slider(min=0, 
                                                           max=100, 
                                                           divisions=100, 
                                                           label="{value}%", 
                                                           value= 0.0, 
                                                           disabled=False, 
                                                           inactive_color= "#F51800", 
                                                           active_color= "#00F50C",
                                                           thumb_color= "#00F50C", visible= False),
                                                 ft.Row(controls= [ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                                                                     controls= [ft.Text(value= "Reconhecimento Facial   ",
                                                                                                                        size= 15,
                                                                                                                        color= ft.colors.BLACK,
                                                                                                                        weight=ft.FontWeight.BOLD)]),
                                                                                     bgcolor= ft.colors.AMBER,
                                                                                     height= 50,
                                                                                     width= 240,
                                                                                     on_click= self.camera),
                                                                   ft.Text(value= "ou", size= 25, color= ft.colors.WHITE),
                                                                   ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                                                                     controls= [ft.Text(value= "Voltar",
                                                                                                                        size= 15,
                                                                                                                        color= ft.colors.BLACK,
                                                                                                                        weight=ft.FontWeight.BOLD)]),
                                                                                    bgcolor= ft.colors.AMBER,
                                                                                    height= 50,
                                                                                    width= 150,
                                                                                    on_click= lambda _: self.page.go("/perfil"))],
                                                        alignment= ft.MainAxisAlignment.CENTER)])


        return ft.Container(content= self.estruturacao)

class faceid_login:
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.sql= sqlLite.SQLite()

    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()     

    def camera(self):
        haar_cascade = cv2.CascadeClassifier("venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
        face = cv2.VideoCapture(0)
        img = ft.Image(border_radius=ft.border_radius.all(20), height= 450, width= 600)
        model = cv2.face.EigenFaceRecognizer_create()
        model.read('assets/cv2/modelo/classificadorEigen.yml')

        tempo_inicial = time()
        self.estruturacao.controls[2].content= img

        while True:
            _, frame = face.read()

            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 4, minSize= (145,145)) 
            for (x, y, w, h) in faces_rect: 
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                face_off = cv2.resize(gray_img[y:y + h, x:x + w], (64, 64))

                id, confianca = model.predict(face_off)
                
                #print(id, confianca)
                
                if int(self.email[0][0]) == int(id) and confianca < 1800:
                    self.page.session.set("NomeUsuario", self.email[0][1])
                    self.page.session.set("login", self.estruturacao.controls[1].value)
                    self.page.go("/home")
                    self.page.update()
                    break

            _, im_arr = cv2.imencode('.png', frame)
            im_b64 = base64.b64encode(im_arr)
            img.src_base64= im_b64.decode("utf-8")
            self.estruturacao.update()

            if time() - tempo_inicial > 10:
                 self.page.go("/login")
                 break
            
        face.release()
        cv2.destroyAllWindows()
    
    def login(self, e):
        self.email = self.sql.db_execute(query= "SELECT COUNT(id_login), nome_completo FROM cadastro_usuario WHERE login = ?",
                                        params= [e.control.value.lower()])[1]
        
        if self.email[0][0] > 0:
            self.estruturacao.controls[1].disabled = True
            self.camera()
        else:
            self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                                   leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                   content=ft.Text("Email não encontrado"),
                                   actions=[ft.TextButton("OK", on_click= self.close_banner)])
            self.page.banner.open = True
            self.page.update()

    def main(self):
        self.estruturacao = ft.Column(controls= [ft.Text(value= "Login", color= ft.colors.WHITE, size= 20),
                                                 ft.TextField(label= "Clicar enter para enviar", 
                                                              label_style= ft.TextStyle(color= ft.colors.WHITE),
                                                              hint_text= "Inserir o email aqui.",
                                                              border_color= ft.colors.WHITE,
                                                              color= ft.colors.WHITE,
                                                              bgcolor= ft.colors.with_opacity(0.5, ft.colors.BLACK12),
                                                              hint_style= ft.TextStyle(color= ft.colors.WHITE),
                                                              on_submit= self.login),
                                                 ft.Container(margin= 15),
                                                 ft.Container(content = ft.ElevatedButton(content= ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                                                                            controls= [ft.Text(value= "Voltar",
                                                                                                                                size= 15,
                                                                                                                                color= ft.colors.BLACK,
                                                                                                                                weight=ft.FontWeight.BOLD)]),
                                                                                                                bgcolor= ft.colors.AMBER,
                                                                                                                height= 50,
                                                                                                                width= 150,
                                                                                                                on_click= lambda _: self.page.go("/login")),
                                                              alignment= ft.alignment.center)])


        return ft.Container(content= self.estruturacao)