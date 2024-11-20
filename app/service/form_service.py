from flask import flash
from model.form_model import FormModel

class FormService:
    
    def __init__(self, mysql):
        self.form_model = FormModel(mysql)
        
    def cadastrar_producao(self, nome, descricao, tipo, arquivo, comprovante_submissao, veiculo, vinculo, coautores, curso_relacionado, projeto_pesquisa, palavra_chave, grupo_pesquisa, laboratorio, inst_parceiras, carta_anuencia, email):
        #TODO
        self.form_model.cadastrar_producao(nome, descricao, tipo, arquivo, comprovante_submissao, veiculo, vinculo, coautores, curso_relacionado, projeto_pesquisa, palavra_chave, grupo_pesquisa, laboratorio, inst_parceiras, carta_anuencia, email)

