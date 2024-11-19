from db_connection import create_connection, close_connection

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def salvar(self):
        conexao = create_connection()
        if conexao:
            cursor = conexao.cursor()
            sql = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)"
            valores = (self.nome, self.email, self.senha)
            try:
                cursor.execute(sql, valores)
                conexao.commit()
                print(f"Usuário {self.nome} gravado com sucesso!")
            except Exception as e:
                print(f"Erro ao inserir usuário: {e}")
            finally:
                cursor.close()
                close_connection(conexao)

    @staticmethod
    def listar_todos():
        conexao = create_connection()
        usuarios = []
        if conexao:
            cursor = conexao.cursor()
            sql = "SELECT nome, email FROM usuario"
            try:
                cursor.execute(sql)
                resultados = cursor.fetchall()
                for (nome, email) in resultados:
                    usuarios.append(Usuario(nome, email, None))  # Senha não precisa ser retornada
            except Exception as e:
                print(f"Erro ao buscar dados dos usuários: {e}")
            finally:
                cursor.close()
                close_connection(conexao)
        return usuarios
