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
            cursor.execute('SELECT p.ID, p.nome, p.descricao, p.tipo, p.veiculo, pu.nome FROM producao p INNER JOIN publicadores pu ON pu.email = p.email ORDER BY criado_em DESC')
            producoes = cursor.fetchall()
            cursor.close()

            # ID como o primeiro item da tupla
            return [(id_producao, nome_producao, descricao, tipo, veiculo, nome) for id_producao, nome_producao, descricao, tipo, veiculo, nome in producoes]

        except Exception as e:
            print(f"Erro ao recuperar produções: {e}")
            self.mysql.connection.rollback()
            return []

        

    def buscar_por_email(self, email):
        try:
            cursor = self.mysql.connection.cursor()
            query = '''
                SELECT p.ID, p.nome, p.descricao, p.tipo, p.veiculo, pu.email 
                FROM producao p
                INNER JOIN publicadores pu ON pu.email = p.email
                WHERE p.email = %s
                ORDER BY p.ID ASC
            '''
            cursor.execute(query, (email,))
            producoes = cursor.fetchall()
            cursor.close()
            return producoes
        except Exception as e:
            print(f"Erro ao recuperar produções por email: {e}")
            return []


    def get_producao_detalhada(self, producao_id):
        try:
            cursor = self.mysql.connection.cursor()
            query = """
            SELECT p.ID, p.nome, p.descricao, p.tipo, p.veiculo,
                p.vinculo, p.coautor, p.curso_relacionado, p.projeto_pesquisa, p.palavra_chave,
                p.grupo_pesquisa, p.laboratorio, p.inst_parceiras, p.email,
                p.carta_anuencia, p.arquivo, p.comprovante_submissao
            FROM producao p
            WHERE p.ID = %s
            """
            cursor.execute(query, (producao_id,))
            producao = cursor.fetchone()
            cursor.close()

            if producao:
                # Formatando a produção em um dicionário
                return {
                    'ID': producao[0],
                    'nome': producao[1],
                    'descricao': producao[2],
                    'tipo': producao[3],
                    'veiculo': producao[4],
                    'vinculo': producao[5],
                    'coautor': producao[6],
                    'curso_relacionado': producao[7],
                    'projeto_pesquisa': producao[8],
                    'palavra_chave': producao[9],
                    'grupo_pesquisa': producao[10],
                    'laboratorio': producao[11],
                    'inst_parceiras': producao[12],
                    'email': producao[13],
                    'carta_anuencia': "imagem" if producao[14] else None,
                    'arquivo': "imagem" if producao[15] else None,
                    'comprovante_submissao': "imagem" if producao[16] else None
                }
            else:
                print("Erro: Nenhuma produção encontrada para o ID:", producao_id)
                return None

        except Exception as e:
            print(f"Erro ao recuperar produção detalhada: {e}")
            self.mysql.connection.rollback()
            return None

