from flask import flash
from model.user_model import UserModel

class UserService:
    def __init__(self, mysql):
        self.user_model = UserModel(mysql)

    def cadastrar_usuario(self, nome, email):
        # Verifica se o usuário já existe no banco de dados
        usuario_existente = self.user_model.buscar_usuario_por_email(email)

        if usuario_existente is not None:
            flash("Usuário já está registrado.", "info")
            return True  # Se o usuário já existir, retorna True

        try:
            # Insere o usuário se não existir
            self.user_model.inserir_usuario(nome, email)
            flash("Cadastro realizado com sucesso!", "sucesso")
            return False
        
        except Exception as e:
            flash(f"Ocorreu um erro ao cadastrar: {e}", "erro")
            return False
        

    def inserir_dados_adicionais(self, curso_docente=None, curso_discente=None, cluster=None, nome_social= None, email = None):
        if curso_discente:
            self.user_model.inserir_discente(curso_discente, nome_social, email)
        if curso_docente:
            self.user_model.inserir_docente(curso_docente, nome_social, email)
        if cluster:
            self.user_model.inserir_cluster(cluster, nome_social, email)

            
    def buscar_usuario_por_email(self, email):
        # Buscar o ID do usuário com base no e-mail
        return self.user_model.buscar_usuario_por_email(email)