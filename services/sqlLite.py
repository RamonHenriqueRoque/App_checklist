import sqlite3 as sql
from services.treinamentoFaceID import treinamento
from os import path

class SQLite:

    def db_execute(self, query, params= []):
        with sql.connect("assets/database/app.db") as con:
            cur= con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.description, cur.fetchall()

    def criacao_base(self):
        #Modelo de reconhecimento facial
        if not path.exists("assets/cv2/modelo/classificadorEigen.yml"):
            treinamento()

        #Base de dados
        self.db_execute("""CREATE TABLE IF NOT EXISTS personalidade(
                            id_personalidade INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            nome VARCHAR(50) NOT NULL
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS comida(
                            id_comida INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            alergia BOOLEAN NOT NULL,
                            vegano_vegetariano BOOLEAN NOT NULL
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS conhecimento(
                            id_conhecimento INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            valor BOOLEAN DEFAUL True
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS pessoal(
                            id_pessoal INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            nome VARCHAR(50) NOT NULL,
                            n_residencia VARCHAR(50) NOT NULL,
                            data_nascimento VARCHAR(50) NOT NULL,
                            cep VARCHAR(50) NOT NULL,
                            uf VARCHAR(50) NOT NULL,
                            cidade VARCHAR(50) NOT NULL,
                            bairro VARCHAR(50) NOT NULL,
                            endereco VARCHAR(50) NOT NULL,
                            estado_civil VARCHAR(50) NOT NULL,
                            genero VARCHAR(50) NOT NULL,
                            lat FLOAT NOT NULL,
                            lon FLOAT NOT NULL
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS cardapio(
                            id_cardapio INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            id_comida INTEGER NOT NULL,
                            nome VARCHAR(50) NOT NULL,
                            FOREIGN KEY (id_comida) REFERENCES comida(id_comida)
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS software(
                            id_software INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            id_conhecimento INTEGER NOT NULL,
                            nome VARCHAR(50) NOT NULL,
                            FOREIGN KEY (id_conhecimento) REFERENCES conhecimento(id_conhecimento)
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS linguagem_programacao (
                            id_linguagem_programacao INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            id_conhecimento INTEGER NOT NULL,
                            nome VARCHAR(50) NOT NULL,
                            FOREIGN KEY (id_conhecimento) REFERENCES conhecimento(id_conhecimento)
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS cadastro_usuario (
                            id_login INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            nome_completo VARCHAR(255) NOT NULL,
                            login VARCHAR(50) NOT NULL,
                            senha VARCHAR(255) NOT NULL,
                            data_criacao DATE NOT NULL,
                            data_ultima_senha DATE NOT NULL
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS aparelho (
                            id_aparelho INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            id_login INTEGER NOT NULL,
                            sistema_operacional VARCHAR(25),
                            nome_computador VARCHAR(25),
                            FOREIGN KEY (id_login) REFERENCES cadastro_usuario(id_login)
                        )""")
        
        self.db_execute("""CREATE TABLE IF NOT EXISTS checklist (
                            id_checklist INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            id_aparelho INTEGER NOT NULL,
                            id_pessoal INTEGER NOT NULL,
                            id_conhecimento INTEGER NOT NULL,
                            id_comida INTEGER NOT NULL,
                            id_personalidade INTEGER NOT NULL,
                            data_checklist DATETIME NOT NULL,
                            FOREIGN KEY (id_aparelho) REFERENCES aparelho(id_aparelho),
                            FOREIGN KEY (id_pessoal) REFERENCES pessoal(id_pessoal),
                            FOREIGN KEY (id_conhecimento) REFERENCES conhecimento(id_conhecimento),
                            FOREIGN KEY (id_comida) REFERENCES comida(id_comida),
                            FOREIGN KEY (id_personalidade) REFERENCES personalidade(id_personalidade)
                        )""")