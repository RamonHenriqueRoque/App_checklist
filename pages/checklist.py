import flet as ft
from datetime import datetime
import requests
from string import digits
from services import sqlLite
from os import environ
from components.tela import Fundo

class API_Correio():
    def api(self, cep):
        link_api = "https://brasilapi.com.br/api/cep/v2/" + cep
        json = requests.get(link_api)

        if json.status_code == 200:
            return json.json()

class Checklist(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.fundo = Fundo(self.page).fundo()

        self.fundo.content.controls[0].height= self.page.window_height - 40
        self.fundo.content.controls[0].opacity = 0.05
        
    def soma_itens_respondido(self):
        ################### Pessoas
        nome = 1 if self.nome.controls[2].value != "" else 0
        residencia= 1 if self.n_pessoas.controls[1].value != "Informe a quantidade de pessoas na sua residência." else 0
        data= 1 if self.data_nascimento.controls[2].content.controls[1].placeholder_text != "" else 0
        uf= 1 if self.cep.controls[3].controls[0].value != "" else 0
        estado_civil= 1 if self.estado_civil_genero.controls[1].controls[1].value != None else 0
        genero = 1 if self.estado_civil_genero.controls[2].controls[1].value != None else 0

        ################### Conhecimento
        linguagem = 1 if sum([i.selected for i in self.linguagem_programacao.content.controls[1].controls]) > 0 else 0
        software = sum([1 if i.value != None else 0 for i in self.software.content.controls[1].controls])
        ################### Comida
        #comida = 1 if sum([i.value for i in self.tipo_comida.content.controls[4].controls]) > 0 else 0
        ################### Personalidade
        personalidade = 1 if self.personalidade.content.controls[1].controls[1].value != None else 0
        ################### Comida
        cv= 1 if self.arquivo_cv.content.controls[1].controls[1].value != "" else 0


        lista = [nome, residencia, data, uf, estado_civil, genero, linguagem, software, 0, 0, 0, personalidade, cv]
        valor = round(sum(lista) / len(lista) * 100,0)

        # Botão de salvar. Quando inicia a ferramenta, o objeto ainda não foi criado
        try:
            if int(valor) == 100:
                self.status.content.controls[2].content.visible = True
            else:
                self.status.content.controls[2].content.visible = False
            self.status.update()
        except:
            pass

        return valor

    def status_checklist(self,e):
        self.status.content.controls[1].value = self.soma_itens_respondido()
        self.status.update()

    def arquivo_selecionado(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.seletor.value = e.files[0].path
            self.arquivo_cv.content.controls[1].controls[1].value = "Arquivo selecionado."
            self.status_checklist(e)
        else:
            self.arquivo_cv.content.controls[1].controls[1].value = ""
            self.status_checklist(e)

        self.arquivo_cv.update()

    def teste_psico(self):
        lista = ["ISTJ – Introvertido, Sensorial, Pensador, Julgador",
                 "ISFJ – Introvertido, Sensorial, Sentimental, Julgador",
                 "INFJ – Introvertido, Intuitivo, Sentimental, Julgador",
                 "INTJ– Introvertido, Intuitivo, Pensador, Julgador",
                 "ISTP – Introvertido, Sensorial, Pensador, Perceptivo",
                 "ISFP – Introvertido, Sensorial, Sentimental, Perceptivo",
                 "INFP – Introvertido, Intuitivo, Sentimental, Perceptivo",
                 "INTP – Introvertido, Intuitivo, Pensador, Perceptivo",
                 "ESTP – Extrovertido, Sensorial, Pensador, Perceptivo",
                 "ESFP – Extrovertido, Sensorial, Sentimental, Perceptivo",
                 "ENFP – Extrovertido, Intuitivo, Sentimental, Perceptivo",
                 "ENTP – Extrovertido, Intuitivo, Pensador, Perceptivo",
                 "ESTJ – Extrovertido, Sensorial, Pensador, Julgador",
                 "ESFJ – Extrovertido, Sensorial, Sentimental, Julgador",
                 "ENFJ – Extrovertido, Intuitivo, Sentimental, Julgador",
                 "ENTJ – Extrovertido, Intuitivo, Pensador, Julgador"]
        return lista

    def selecionado_linguagem_programacao(self, e):
        if e.control.label.value != "Nenhum" and self.linguagem_programacao.content.controls[1].controls[-1].selected == False:
            self.linguagem_programacao.update()
            self.status_checklist(e)
        else:
            for selecionado in range(len(self.linguagem_programacao.content.controls[1].controls[:-1])):
                self.linguagem_programacao.content.controls[1].controls[selecionado].selected = False
                self.linguagem_programacao.update()
                self.status_checklist(e)

    def linguagem_programacao_chip(self):

        lista= ["Java", "Python", "R", "C#", "Nenhum"]

        return ft.Row(alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                      spacing= 10,
                      controls= [ft.Chip(label=ft.Text(prog), on_select=self.selecionado_linguagem_programacao) for prog in lista])

    def comidas(self):
        list_comida = ['Abadejo','Rapadura','Pepino','Dobradinha','Cacau','Porco','Romã','Aveia','Virado à paulista','Ameixa','Sardinha','Milho','Canjica','Refrigerante',
                       'Coentro','Abobrinha','Tamarindo','Quibe','Alfavaca','Toucinho','Barreado','Paçoca','Corvina de água doce','Açúcar','Laranja','Tangerina','Azeite',
                       'Bolinho de arroz']
        return [ft.Checkbox(label=comida, value=False, on_change=self.status_checklist) for comida in list_comida]

    def genero(self):
        list_genero= ["Masculino", "Feminino", "Outros"]
        return [ft.dropdown.Option(genero) for genero in list_genero]
    
    def estado_civil(self):
        list_estado_civil = ["Casado", "Solteiro", "Separado (judicial)", "Separado (extrajudicialmente)", "Divorciado", "Viúvo"]
        return [ft.dropdown.Option(estado) for estado in list_estado_civil] 

    def fechar_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def obter_info_CEP(self, e):
        if self.cep.controls[2].controls[0].error_text == "" and len(self.cep.controls[2].controls[0].value) == 8:
            api= API_Correio().api(cep = str(self.cep.controls[2].controls[0].value))
            if "erro" not in api.keys():
                self.cep.controls[3].controls[0].value = api["state"]
                self.cep.controls[3].controls[1].value = api["city"]
                self.cep.controls[4].value = api["neighborhood"]
                self.cep.controls[5].value = api["street"]
                try:
                    self.page.session.set("lon", api["location"]["coordinates"]["longitude"])
                    self.page.session.set("lat", api["location"]["coordinates"]["latitude"])
                except:
                    self.page.session.set("lon", None)
                    self.page.session.set("lat", None)
                self.status_checklist(e)
                self.cep.update()
            else:
                self.page.banner = ft.Banner(bgcolor=ft.colors.RED_100,
                    leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                    content=ft.Text("Erro ao inserir o CEP, verificar se foi escrito corretamente."),
                    actions=[ft.TextButton("OK", on_click= self.close_banner)])
                self.page.banner.open = True
                self.page.update()
        else:
            self.cep.controls[3].controls[0].value = ""
            self.cep.controls[3].controls[1].value = ""
            self.cep.controls[4].value = ""
            self.cep.controls[5].value = ""
            
            self.page.banner = ft.Banner(bgcolor=ft.colors.RED_200,
                                         leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                                         content=ft.Text("Preencha o CEP completo ou verifica se há erro."),
                                         actions=[ft.TextButton("OK", on_click= self.fechar_banner)])
            self.page.banner.open = True

            self.status_checklist(e)
            self.page.update()
            self.cep.update()

    def apenas_numero_cep(self, e):
        e.control.error_text = ""
        e.control.update()
        for i in e.data:
            if i not in list(digits):
                e.control.error_text = "Apenas numeros"
                e.control.update()
                break    

    def quant_pessoas(self, e):
        quant = str(e.control.value).split(".")[0] if e.control.value != 12 else str(e.control.value).split(".")[0] + "+"
        self.n_pessoas.controls[1].value= "Pessoa(s) na residência: " + quant
        e.control.label = quant

        self.status_checklist(e)
        self.n_pessoas.update()

    def selecionar_Data_Nascimento(self, e):
        self.data_nasc= ft.DatePicker(first_date= datetime(1900, 1, 1), 
                                      last_date= datetime.now(),
                                      on_change= self.valor_Data_Nascimento,
                                      cancel_text = "Cancelar",
                                      confirm_text = "Confimar",
                                      date_picker_mode = ft.DatePickerMode.YEAR,
                                      date_picker_entry_mode= ft.DatePickerEntryMode.CALENDAR_ONLY)

        
        self.page.overlay.append(self.data_nasc)
        self.page.update()
        self.data_nasc.pick_date()

    def valor_Data_Nascimento(self, e):
        self.data_nascimento.controls[2].content.controls[1].placeholder_text = e.control.value.strftime('%d/%m/%Y')
        self.data_nascimento.controls[2].content.controls[2].placeholder_text = str((datetime.now() - e.control.value).days // 365) + " anos"
        
        self.status_checklist(e)
        self.data_nascimento.update()

    def checklist_Pessoa(self):
        self.nome = ft.Column(spacing= 10,
                            horizontal_alignment= ft.CrossAxisAlignment.START,
                            controls=[ft.Container(),
                                    ft.Text(value = "Nome", weight=ft.FontWeight.W_500, size= 14),
                                    ft.TextField(color= ft.colors.BLACK,
                                                hint_text="Digita seu nome.",
                                                bgcolor= ft.colors.WHITE,
                                                on_change= self.status_checklist)])
    
        
        self.data_nascimento = ft.Column(spacing= 10,
                                         horizontal_alignment= ft.CrossAxisAlignment.START,
                                         controls=[ft.Container(),
                                                   ft.Text(value = "Data de nascimento", weight=ft.FontWeight.W_500, size= 14),
                                                   ft.Container(alignment= ft.alignment.center,
                                                                content= ft.Row(width= 330,
                                                                                controls= [ft.Chip(label=ft.Text("Data"),
                                                                                                    leading=ft.Icon(ft.icons.CALENDAR_TODAY),
                                                                                                    on_click= self.selecionar_Data_Nascimento),
                                                                                           ft.CupertinoTextField(placeholder_text="",
                                                                                                                 text_align= ft.TextAlign.CENTER, 
                                                                                                                 color= ft.colors.BLACK,
                                                                                                                 disabled=True,
                                                                                                                 expand= True),
                                                                                            ft.CupertinoTextField(placeholder_text="",
                                                                                                                  text_align= ft.TextAlign.CENTER, 
                                                                                                                  color= ft.colors.BLACK,
                                                                                                                  disabled=True,
                                                                                                                  width= 85)]))])

        # API CORREIO
        self.cep = ft.Column(spacing= 10,
                             horizontal_alignment= ft.CrossAxisAlignment.START,
                             controls=[ft.Container(),
                                       ft.Text(value = "Digite seu cep", weight=ft.FontWeight.W_500, size= 14),
                                       ft.Row(controls= [ft.TextField(value= "", color= ft.colors.BLACK, expand= True, max_length = 8, on_change= self.apenas_numero_cep, bgcolor= ft.colors.WHITE),
                                                         ft.IconButton(icon= ft.icons.ARROW_BACK, icon_color= ft.colors.BLACK, on_click= self.obter_info_CEP)]),
                                       ft.Row(alignment= ft.alignment.center,
                                              controls= [ft.TextField(label= "UF", color= ft.colors.BLACK, hint_text="", disabled= True, bgcolor= ft.colors.WHITE, width= 50, text_align= ft.TextAlign.CENTER),
                                                         ft.TextField(label= "Cidade", color= ft.colors.BLACK, hint_text="", disabled= True, bgcolor= ft.colors.WHITE, width= 485)]),
                                       ft.TextField(label= "Bairro", color= ft.colors.BLACK, hint_text="", disabled= True, bgcolor= ft.colors.WHITE),
                                       ft.TextField(label= "Endereço", color= ft.colors.BLACK, hint_text="", disabled= True, bgcolor= ft.colors.WHITE)])

        self.estado_civil_genero = ft.Column(spacing= 10, 
                                             horizontal_alignment= ft.CrossAxisAlignment.START,
                                             controls=[ft.Container(),
                                                       ft.Column(controls= [ft.Text(value = "Estado Civil", weight=ft.FontWeight.W_500, size= 14),
                                                                            ft.Dropdown(hint_text="Escolha o estado civil.",
                                                                                        options= self.estado_civil(),
                                                                                        autofocus=True,
                                                                                        bgcolor= ft.colors.WHITE,
                                                                                        on_change=self.status_checklist)]),
                                                       ft.Column(controls= [ft.Text(value = "Gênero", weight=ft.FontWeight.W_500, size= 14),
                                                                            ft.Dropdown(hint_text="Escolha o gênero.",
                                                                                        options=self.genero(),
                                                                                        autofocus=True,
                                                                                        bgcolor= ft.colors.WHITE,
                                                                                        on_change=self.status_checklist)]),
                                                      ft.Container()])

        self.n_pessoas = ft.Column(spacing= 10,
                          horizontal_alignment= ft.CrossAxisAlignment.START,
                          controls=[ft.Container(),
                                    ft.Text(value = "Informe a quantidade de pessoas na sua residência.", weight=ft.FontWeight.W_500, size= 14),
                                    ft.Slider(min=0, max=12, divisions= 12, label="{value}" , on_change= self.quant_pessoas)])

        return ft.Container(content= ft.ExpansionTile(trailing= ft.Icon(name= ft.icons.PERSON, color= ft.colors.BLACK),
                                                      title= ft.Text(value="Informação Pessoal.", size = 16, weight=ft.FontWeight.W_900),
                                                      controls= [ft.Divider(),
                                                                 ft.Container(margin= 10, content= self.nome),
                                                                 ft.Container(margin= 10, content= self.n_pessoas),
                                                                 ft.Container(margin= 10, content= self.data_nascimento),
                                                                 ft.Divider(),
                                                                 ft.Container(margin= 10, content= self.cep),
                                                                 ft.Divider(),
                                                                 ft.Container(margin= 10, content= self.estado_civil_genero)],
                                                      bgcolor= ft.colors.GREY_100,
                                                      initially_expanded=False,
                                                      affinity=ft.TileAffinity.LEADING),
                            bgcolor= "#7F7F7F",
                            alignment=ft.alignment.center,
                            border_radius=10)

    def checklist_Conhecimento(self):
        self.linguagem_programacao = ft.Container(margin = 10,
                                                  content= ft.Column(controls= [ft.Text(value = "Linguagem de programação", weight=ft.FontWeight.W_500, size= 14),
                                                                                self.linguagem_programacao_chip()]))

        self.software = ft.Container(margin = 10,
                                     content= ft.Column(controls= [ft.Text(value = "Software", weight=ft.FontWeight.W_500, size= 14),
                                                                   ft.Row(alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                                                                          spacing= 10,
                                                                          controls= [ft.RadioGroup(on_change=self.status_checklist,
                                                                                                   content= ft.Column(horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                                                                                                      controls= [ft.Text(value = "PBI", weight=ft.FontWeight.W_200, size= 12, text_align= ft.TextAlign.CENTER),
                                                                                                                                 ft.Radio(value= "sim", label="SIM"),
                                                                                                                                 ft.Radio(value= "não", label="NÃO")])),
                                                                                     ft.RadioGroup(on_change=self.status_checklist,
                                                                                                   content= ft.Column(horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                                                                                                      controls= [ft.Text(value = "SQL", weight=ft.FontWeight.W_200, size= 12, text_align= ft.TextAlign.CENTER),
                                                                                                                                 ft.Radio(value= "sim", label="SIM"),
                                                                                                                                 ft.Radio(value= "não", label="NÃO")])),
                                                                                     ft.RadioGroup(on_change=self.status_checklist,
                                                                                                   content= ft.Column(horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                                                                                                      controls= [ft.Text(value = "MATLAB", weight=ft.FontWeight.W_200, size= 12, text_align= ft.TextAlign.CENTER),
                                                                                                                                 ft.Radio(value= "sim", label="SIM"),
                                                                                                                                 ft.Radio(value= "não", label="NÃO")])),
                                                                                     ft.RadioGroup(on_change=self.status_checklist,
                                                                                                   content= ft.Column(horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                                                                                                      controls= [ft.Text(value = "FIGMA", weight=ft.FontWeight.W_200, size= 12, text_align= ft.TextAlign.CENTER),
                                                                                                                                 ft.Radio(value= "sim", label="SIM"),
                                                                                                                                 ft.Radio(value= "não", label="NÃO")]))])]))

        return ft.Container(content= ft.ExpansionTile(trailing= ft.Icon(name= ft.icons.BOOK, color= ft.colors.BLACK),
                                                      title= ft.Text(value="Informação de conhecimento.", size = 16, weight=ft.FontWeight.W_900),
                                                      controls= [ft.Container(),
                                                                 self.linguagem_programacao,
                                                                 ft.Divider(),
                                                                 self.software,
                                                                 ft.Divider()],
                                                      bgcolor= ft.colors.GREY_100,
                                                      initially_expanded=False,
                                                      affinity=ft.TileAffinity.LEADING),
                            bgcolor= "#7F7F7F",
                            alignment=ft.alignment.center,
                            border_radius=10)

    def checklist_Comida(self):
        self.tipo_comida = ft.Container(margin= 10,
                                        content= ft.Column(controls= [ft.Row(alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                                                                             controls= [ft.Text(value = "Alergico?", weight=ft.FontWeight.W_500, size= 14),
                                                                                        ft.Switch(label="",value=False, on_change=self.status_checklist)]),
                                                                      ft.Row(alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                                                                             controls= [ft.Text(value = "Vegano ou Vegetariano?", weight=ft.FontWeight.W_500, size= 14),
                                                                                        ft.Switch(label="", value=False, on_change=self.status_checklist)]),
                                                                      ft.Divider(),
                                                                      ft.Text(value = "Comida que você come.", weight=ft.FontWeight.W_500, size= 14),
                                                                      ft.Column(controls= self.comidas())]))

        return ft.Container(content= ft.ExpansionTile(trailing= ft.Icon(name= ft.icons.FASTFOOD, color= ft.colors.BLACK),
                                                      title= ft.Text(value="Informação sobre comida.", size = 16, weight=ft.FontWeight.W_900),
                                                      controls= [self.tipo_comida],
                                                      bgcolor= ft.colors.GREY_100,
                                                      initially_expanded=False,
                                                      affinity=ft.TileAffinity.LEADING),
                            bgcolor= "#7F7F7F",
                            alignment=ft.alignment.center,
                            border_radius=10)

    def checklist_Personalidade(self):
        self.personalidade =  ft.Container(margin= 10,
                                      alignment= ft.alignment.center_left,
                                      content= ft.Column(controls= [ft.Text(value = "Teste de personalidade", weight=ft.FontWeight.W_500, size= 14),
                                                                    ft.Row(alignment= ft.MainAxisAlignment.START,
                                                                           controls= [ft.ElevatedButton(text= "Ir para o teste...",
                                                                                                        color= ft.colors.WHITE,
                                                                                                        icon= ft.icons.ARROW_RIGHT,
                                                                                                        icon_color= ft.colors.WHITE,
                                                                                                        bgcolor= ft.colors.BLACK45,
                                                                                                        url= "https://www.16personalities.com/br"),
                                                                                      ft.Dropdown(hint_text="Escolha o resultado do teste.",text_size= 12, on_change=self.status_checklist,
                                                                                                  options= [ft.dropdown.Option(i) for i in self.teste_psico()])])]))

        return ft.Container(content= ft.ExpansionTile(trailing= ft.Icon(name= ft.icons.DIVERSITY_2, color= ft.colors.BLACK),
                                                      title= ft.Text(value="Informação sobre personalidade.", size = 16, weight=ft.FontWeight.W_900),
                                                      controls= [ft.Container(),
                                                                 self.personalidade],
                                                      bgcolor= ft.colors.GREY_100,
                                                      initially_expanded=False,
                                                      affinity=ft.TileAffinity.LEADING),
                            bgcolor= "#7F7F7F",
                            alignment=ft.alignment.center,
                            border_radius=10)

    def checklist_Curriculo(self):
        self.seletor = ft.FilePicker(on_result=self.arquivo_selecionado)
        self.page.overlay.append(self.seletor)
        
        self.arquivo_cv = ft.Container(margin= 10,
                                      alignment= ft.alignment.center_left,
                                      content= ft.Column(controls= [ft.Text(value = "Escolhe seu curriculo", weight=ft.FontWeight.W_500, size= 14),
                                                                    ft.Row(controls = [ft.ElevatedButton(text= "Buscar...",
                                                                                                        color= ft.colors.WHITE,
                                                                                                        icon= ft.icons.ARROW_RIGHT,
                                                                                                        icon_color= ft.colors.WHITE,
                                                                                                        bgcolor= ft.colors.BLACK45,
                                                                                                        on_click= lambda _: self.seletor.pick_files(allow_multiple=False, allowed_extensions= ["pdf"])),
                                                                                        ft.Text(value= "", color= ft.colors.BLUE_400)])]))

        return ft.Container(content= ft.ExpansionTile(trailing= ft.Icon(name= ft.icons.SCHOOL, color= ft.colors.BLACK),
                                                      title= ft.Text(value="Informação curricular.", size = 16, weight=ft.FontWeight.W_900),
                                                      controls= [ft.Container(),
                                                                 self.arquivo_cv ],
                                                      bgcolor= ft.colors.GREY_100,
                                                      initially_expanded=False,
                                                      affinity=ft.TileAffinity.LEADING),
                            bgcolor= "#878787",
                            alignment=ft.alignment.center,
                            border_radius=10)

    def checklist_Status(self):

        self.status = ft.Container(ft.Column(controls= [ft.Divider(),
                                                        ft.Slider(min=0, max=100, divisions=100, label="{value}%", 
                                                                  value= self.soma_itens_respondido(), disabled=False, on_change= self.status_checklist,
                                                                  inactive_color= "#F51800", 
                                                                  active_color= "#00F50C",
                                                                  thumb_color= "#00F50C"),
                                                        ft.Container(alignment= ft.alignment.center,
                                                                     content= ft.ElevatedButton(text= "Salvar", visible= False, on_click= self.salvar_checklist))]))


        return self.status
    
    def salvar_checklist(self, e):
        sql= sqlLite.SQLite()
        
        sql.db_execute(query = "INSERT INTO pessoal(nome, n_residencia, data_nascimento, cep, uf, bairro, endereco, estado_civil, genero, cidade, lat, lon) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       params= [self.nome.controls[2].value,
                                self.n_pessoas.controls[1].value.split("Pessoa(s) na residência: ")[1],
                                self.data_nascimento.controls[2].content.controls[1].placeholder_text,
                                self.cep.controls[2].controls[0].value,
                                self.cep.controls[3].controls[0].value,
                                self.cep.controls[4].value,
                                self.cep.controls[5].value,
                                self.estado_civil_genero.controls[1].controls[1].value,
                                self.estado_civil_genero.controls[2].controls[1].value,
                                self.cep.controls[3].controls[1].value,
                                float(self.page.session.get("lat")),
                                float(self.page.session.get("lon"))
                                ])
        
        sql.db_execute(query = "INSERT INTO conhecimento(valor) VALUES (true)")

        sql.db_execute(query = "INSERT INTO comida(alergia, vegano_vegetariano) VALUES (?, ?)", 
                       params= [self.tipo_comida.content.controls[0].controls[1].value,
                                self.tipo_comida.content.controls[1].controls[1].value])
        
        sql.db_execute(query = "INSERT INTO personalidade(nome) VALUES (?)", 
                       params= [self.personalidade.content.controls[1].controls[1].value])

        sql.db_execute(query = "INSERT INTO aparelho(id_login, sistema_operacional, nome_computador) VALUES (?, ?, ?)", 
                       params= [sql.db_execute(query = "SELECT id_login from cadastro_usuario WHERE login = ?", 
                                               params= [self.page.session.get("login")])[1][0][0],
                                environ["OS"],
                                environ["USERNAME"]])
        
        sql.db_execute(query = "INSERT INTO checklist(id_aparelho, id_pessoal, id_conhecimento, id_comida, id_personalidade, data_checklist) VALUES (?, ?, ?, ?, ?, ?)", 
                       params= [sql.db_execute(query = "SELECT MAX(id_aparelho) from aparelho")[1][0][0],
                                sql.db_execute(query = "SELECT MAX(id_pessoal) from pessoal")[1][0][0],
                                sql.db_execute(query = "SELECT MAX(id_conhecimento) from conhecimento")[1][0][0],
                                sql.db_execute(query = "SELECT MAX(id_comida) from comida")[1][0][0],
                                sql.db_execute(query = "SELECT MAX(id_personalidade) from personalidade")[1][0][0],
                                datetime.now()
                                ])
        
        for selecionado in self.linguagem_programacao.content.controls[1].controls:
            if selecionado.selected:
                sql.db_execute(query = "INSERT INTO linguagem_programacao(id_conhecimento, nome) VALUES (?, ?)", 
                               params= [sql.db_execute(query = "SELECT MAX(id_conhecimento) from conhecimento")[1][0][0],
                                        selecionado.label.value])
                
        for n, selecionado in enumerate(self.software.content.controls[1].controls):
            if selecionado.value == "sim":
                sql.db_execute(query = "INSERT INTO software(id_conhecimento, nome) VALUES (?, ?)", 
                               params= [sql.db_execute(query = "SELECT MAX(id_conhecimento) from conhecimento")[1][0][0],
                                        self.software.content.controls[1].controls[n].content.controls[0].value])
                
        for selecionado in self.tipo_comida.content.controls[4].controls:
            if selecionado.value:
                sql.db_execute(query = "INSERT INTO cardapio(id_comida, nome) VALUES (?, ?)", 
                               params= [sql.db_execute(query = "SELECT MAX(id_comida) from comida")[1][0][0],
                                        selecionado.label])
        self.page.go("/home")
        self.page.update()


    def main(self):        

        list_checklist = ft.Column(controls= [self.checklist_Pessoa(),
                                                self.checklist_Conhecimento(),
                                                self.checklist_Comida(),
                                                self.checklist_Personalidade(),
                                                self.checklist_Curriculo(),
                                                self.checklist_Status()
                                                ])
        return ft.Column(controls= [ft.Stack(controls= [self.fundo, list_checklist])])