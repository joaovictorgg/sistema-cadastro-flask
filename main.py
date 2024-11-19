from flask import Flask, render_template, request, redirect, url_for, flash
from usuario import Usuario
from veiculo import Veiculo
from db_connection import create_connection, close_connection
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename

# Instância do objeto app
app = Flask(__name__)

# Configurações para upload de arquivos
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 's3cr3t'  # Adicionar chave secreta para uso de sessões e mensagens flash

# Objeto para uploads e definir caminho para upload de arquivos
upload_dir = os.path.join(app.config['UPLOAD_FOLDER'])

# Se a pasta 'static/uploads' não existir, cria ela
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# Objeto para criptografar a senha
bcrypt = Bcrypt(app)

# Configuração da rota principal
@app.route('/')
def index():
    conexao = create_connection()
    close_connection(conexao)
    return render_template('index.html')


# Rota para listar usuários
@app.route('/listar')
def lista_usuarios():
    usuarios = Usuario.listar_todos()  # Chama a função de listagem de usuários
    if not usuarios:
        flash("Nenhum usuário encontrado!", "warning")
    return render_template('listar.html', usuarios=usuarios)


# Rota para listar veículos
@app.route('/listar_veiculo')
def lista_veiculos():
    veiculos = Veiculo.listar_todos_veiculos()  # Chama a função de listagem de veículos
    if not veiculos:
        flash("Nenhum veículo encontrado!", "warning")
    return render_template('listar_veiculo.html', veiculos=veiculos)


# Rota para excluir um veículo
@app.route('/delete_veiculo/<placa>', methods=['GET'])
def delete_veiculo(placa):
    Veiculo.delete(placa)  # Chama o método estático delete
    flash(f"Veículo com placa {placa} excluído com sucesso!", "success")
    return redirect(url_for('lista_veiculos'))



# Rota de cadastro de usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_crypt = bcrypt.generate_password_hash(senha).decode('utf-8')

        # Criar uma instância de usuário
        novo_usuario = Usuario(nome, email, senha_crypt)
        novo_usuario.salvar()
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for('lista_usuarios'))

    return render_template('cadastro.html')


# Rota de cadastro de veículos
@app.route('/cadastro_veiculo', methods=['GET', 'POST'])
def cadastro_veiculo():
    if request.method == 'POST':
        placa = request.form['placa']
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano = request.form['ano']
        preco = request.form['preco']
        foto = request.files.get('foto')

        if foto:
            nome_arquivo = secure_filename(foto.filename)
            caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
            print('Caminho completo:', caminho_completo)
            foto.save(caminho_completo)
            foto_path = f"uploads/{nome_arquivo}".replace("\\", "/")
        else:
            foto_path = None

        veiculo = Veiculo(placa, marca, modelo, ano, preco, foto_path)
        veiculo.salvar()
        flash("Veículo cadastrado com sucesso!", "success")
        return redirect(url_for('lista_veiculos'))

    return render_template('cadastro_veiculo.html')


# Função principal para rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)
