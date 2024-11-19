# veiculo.py
from db_connection import create_connection, close_connection

class Veiculo:
    def __init__(self, placa, marca, modelo, ano, preco, foto):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.preco = preco
        self.foto = foto

    # Função para salvar o veículo no banco
    def salvar(self):
        conexao = create_connection()
        if conexao:
            cursor = conexao.cursor()
            sql = "INSERT INTO veiculo (placa, marca, modelo, ano, preco, foto) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (self.placa, self.marca, self.modelo, self.ano, self.preco, self.foto)
            try:
                cursor.execute(sql, valores)
                conexao.commit()
                print("Veículo gravado com sucesso.")
            except Exception as e:
                print(f"Erro ao gravar veículo: {e}")
            finally:
                cursor.close()
                close_connection(conexao)

    # Método estático para excluir um veículo
    @staticmethod
    def delete(placa):
        try:
            conexao = create_connection()
            if conexao:
                cursor = conexao.cursor()
                sql = "DELETE FROM veiculo WHERE placa = %s"
                valores = (placa,)
                cursor.execute(sql, valores)
                conexao.commit()  # Confirma a transação
                print(f"Veículo com placa {placa} excluído do banco de dados.")
        except Exception as e:
            print(f"Erro ao excluir veículo: {e}")
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                close_connection(conexao)
                print("Conexão foi finalizada.")

    # Método estático para listar todos os veículos
    @staticmethod
    def listar_todos_veiculos():
        veiculos = []
        conexao = create_connection()
        if conexao:
            cursor = conexao.cursor()
            sql = "SELECT placa, marca, modelo, ano, preco, foto FROM veiculo"
            try:
                cursor.execute(sql)
                resultados = cursor.fetchall()
                for (placa, marca, modelo, ano, preco, foto) in resultados:
                    veiculos.append(Veiculo(placa, marca, modelo, ano, preco, foto))
            except Exception as e:
                print(f"Erro ao buscar dados dos veículos: {e}")
            finally:
                cursor.close()
                close_connection(conexao)
        return veiculos
