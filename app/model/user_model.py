from flask import flash

class UserModel:
    def __init__(self, mysql):
        self.mysql = mysql
    
    def buscar_usuario_por_email(self, email):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute("SELECT email FROM publicadores WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if usuario:
                return usuario[0]  # Retorna o email do usuário
            return None  # Se não encontrar, retorna None
        except Exception as e:
            flash(f"Erro ao buscar usuário: {e}", "erro")
            return None
        
    def inserir_usuario(self, nome, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO publicadores (nome, email) VALUES (%s, %s)", (nome, email))
            self.mysql.connection.commit()
        except Exception as e:
            self.mysql.connection.rollback()
            raise e
        finally:
            cursor.close()
            
    def inserir_discente(self, curso_discente, nome_social, curriculo, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO discente (curso, nome_social, curriculo, email) VALUES (%s, %s, %s, %s)", (curso_discente, nome_social, curriculo, email))
            self.mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Erro ao inserir discente: {e}")
            self.mysql.connection.rollback()

    def inserir_docente(self, curso_docente, nome_social, curriculo, email):
        cursor = self.mysql.connection.cursor()
        try:
            
            cursos_concatenados = ', '.join(curso_docente)
            cursor.execute("INSERT INTO docente (curso, nome_social, curriculo, email) VALUES (%s, %s, %s, %s)", (cursos_concatenados, nome_social, curriculo, email)) 
            self.mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Erro ao inserir docente: {e}")
            self.mysql.connection.rollback()

    def inserir_cluster(self, cluster, nome_social, curriculo, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO colaborador (cluster, nome_social, curriculo, email) VALUES (%s, %s, %s, %s)", (cluster, nome_social, curriculo, email))
            self.mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Erro ao inserir cluster: {e}")
            self.mysql.connection.rollback()
        
    def recuperar_nome(self, email):
        
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("""
                SELECT COALESCE(di.nome_social, do.nome_social, c.nome_social) 
                FROM publicadores p
                LEFT JOIN discente di ON p.email = di.email
                LEFT JOIN docente do ON p.email = do.email
                LEFT JOIN colaborador c ON p.email = c.email
                WHERE p.email = %s
                LIMIT 1;""", (email,))
            resultado = cursor.fetchone()  # Recupera o primeiro resultado da consulta
            return resultado[0] if resultado else None  # Retorna o link do currículo ou None se não encontrado
        except Exception as e:
            print(f"Erro ao recuperar informações: {e}")
            return None
        finally:
            cursor.close()
            
            
    def recuperar_curriculo(self, email):
        
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("""
                SELECT COALESCE(di.curriculo, do.curriculo, c.curriculo) 
                FROM publicadores p
                LEFT JOIN discente di ON p.email = di.email
                LEFT JOIN docente do ON p.email = do.email
                LEFT JOIN colaborador c ON p.email = c.email
                WHERE p.email = %s
                LIMIT 1;""", (email,))
            resultado = cursor.fetchone()  # Recupera o primeiro resultado da consulta
            return resultado[0] if resultado else None  # Retorna o link do currículo ou None se não encontrado
        except Exception as e:
            print(f"Erro ao recuperar informações: {e}")
            return None
        finally:
            cursor.close()


    def recuperar_curso_discente(self, email):
        
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(""" SELECT curso from discente where email = %s""", (email,))
            
            resultado = cursor.fetchone()  # Recupera o primeiro resultado da consulta
            
            if resultado:
                return resultado[0]
            return None
        except Exception as e:
            print(f"Erro ao recuperar cursos: {e}")
            return None
        finally:
            cursor.close()


    def recuperar_curso_docente(self, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(""" SELECT curso from docente where email = %s""", (email,))
            resultado = cursor.fetchone()  # Recupera o primeiro resultado da consulta
            if resultado:
                return resultado[0]
            return None
        except Exception as e:
            print(f"Erro ao recuperar cursos: {e}")
            return None
        finally:
            cursor.close()

    def recuperar_cluster(self, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(""" SELECT cluster from colaborador where email = %s""", (email,))
            resultado = cursor.fetchone()  # Recupera o primeiro resultado da consulta
            if resultado:
                return resultado[0]
            return None
        except Exception as e:
            print(f"Erro ao recuperar cluster: {e}")
            return None
        finally:
            cursor.close()
        