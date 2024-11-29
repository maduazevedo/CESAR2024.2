from flask import flash

class FormModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def cadastrar_producao(self, nome, descricao, tipo, arquivo, comprovante_submissao, veiculo, vinculo, coautores, curso_relacionado, projeto_pesquisa, palavra_chave, grupo_pesquisa, laboratorio, inst_parceiras, carta_anuencia, email):

        cursor = self.mysql.connection.cursor()
        
        try:
            arquivo = arquivo.read()
            comprovante_submissao = comprovante_submissao.read()
            carta_anuencia = carta_anuencia.read()
            
            cursor.execute("INSERT INTO producao (nome, descricao, tipo, arquivo, comprovante_submissao, veiculo, vinculo, coautor, curso_relacionado, projeto_pesquisa, palavra_chave, grupo_pesquisa, laboratorio, inst_parceiras, carta_anuencia, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (nome, descricao, tipo, arquivo, comprovante_submissao, veiculo, vinculo, coautores, curso_relacionado, projeto_pesquisa, palavra_chave, grupo_pesquisa, laboratorio, inst_parceiras, carta_anuencia, email))
            self.mysql.connection.commit()
            
        except Exception as e:
            print(f"Erro ao inserir produção: {e}")
            self.mysql.connection.rollback()
            
    def recuperar_producoes(self):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute('SELECT p.nome, p.descricao, p.tipo, p.veiculo, pu.nome FROM producao p inner join publicadores pu on pu.email = p.email ORDER BY id ASC')
            producoes = cursor.fetchall()
            cursor.close()
            return [(nome_producao, descricao, tipo, veiculo, nome, ) for nome_producao, descricao, tipo, veiculo, nome in producoes]
        
        except Exception as e:
            print(f"Erro ao inserir produção: {e}")
            self.mysql.connection.rollback()

        