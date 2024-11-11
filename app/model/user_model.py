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
            
    def inserir_discente(self, curso_discente, nome_social, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO discente (curso, nome_social, email) VALUES (%s, %s, %s)", (curso_discente, nome_social, email))
            self.mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Erro ao inserir discente: {e}")
            self.mysql.connection.rollback()

    def inserir_docente(self, curso_docente, nome_social, email):
        cursor = self.mysql.connection.cursor()
        try:
            
            cursos_concatenados = ', '.join(curso_docente)
            cursor.execute("INSERT INTO docente (curso, nome_social, email) VALUES (%s, %s, %s)", (cursos_concatenados, nome_social, email))
            self.mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Erro ao inserir docente: {e}")
            self.mysql.connection.rollback()

    def inserir_cluster(self, cluster, nome_social, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO colaborador (cluster, nome_social, email) VALUES (%s, %s, %s)", (cluster, nome_social, email))
            self.mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Erro ao inserir cluster: {e}")
            self.mysql.connection.rollback()
        
    