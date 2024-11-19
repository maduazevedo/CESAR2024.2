from flask import Blueprint, redirect, url_for, session, render_template, flash, request
from service.user_service import UserService

main = Blueprint('main', __name__)

# Inicialize o serviço de usuário sem passar `mysql` aqui
user_service = None

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login')
def login():
    # Importe `google` aqui para evitar o ciclo de importação
    from main import google
    redirect_uri = url_for('main.authorized', _external=True)
    return google.authorize_redirect(redirect_uri)

@main.route('/login/google/authorized')
def authorized():
    # Importe `google` e `mysql` aqui para evitar o ciclo de importação
    from main import google, mysql
    global user_service

    if user_service is None:
        user_service = UserService(mysql)

    response = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    email = user_info.get('email')
    nome = user_info.get('name')
    foto_perfil = user_info.get('picture')

    if email.endswith('@cesar.school') or email.endswith('@cesar.org'):
        session['user'] = user_info
        session['email'] = email

        if user_service.cadastrar_usuario(nome, email):
            return render_template('home.html', email=email, foto_perfil=foto_perfil)
        else: 
            return render_template('primeiro_login.html', email=email, foto_perfil=foto_perfil)
    else:
        flash('Acesso restrito a domínios @cesar.school e @cesar.org')
        return redirect(url_for('main.home'))
    

@main.route('/process_first_login', methods=['POST'])
def process_first_login():
    
    from main import google, mysql
    global user_service

    # Captura dos dados do formulário
    roles = request.form.getlist('role')  # Retorna uma lista com os valores dos checkboxes
    curso_discente = request.form.get('curso_discente')  # Captura o curso se for discente
    curso_docente = request.form.getlist('curso_docente[]')  # Captura todos os cursos que o docente ensina
    cluster = request.form.get('cluster')  # Captura o cluster do colaborador
    nome_social = request.form.get('nome_social')  # Captura o nome social do usuário
    curriculo = request.form.get('curriculo')
    # Validação básica (adicionei para garantir que os campos necessários não estão vazios)
    
    # Verificar se pelo menos uma role foi selecionada
    if not roles:
        return "Erro: Você deve selecionar pelo menos uma função", 400
    
    # Aqui estamos chamando a função de inserção de dados
    try:
        
        # Chama a função para inserir os dados no banco de dados ou serviço
        user_service.inserir_dados_adicionais(
            curso_docente, 
            curso_discente, 
            cluster, 
            nome_social, 
            curriculo,
            session['email']
        )

        # Após a inserção, redireciona para a página inicial ou página de sucesso
        return render_template('home.html', email=session['email'])  # Redireciona para a página inicial
    
    except ValueError as ve:
        # Em caso de erro, como usuário já cadastrado
        return f"Erro: {ve}", 400

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        print("Detalhes do erro:", traceback.format_exc())
        return "Ocorreu um erro inesperado, tente novamente mais tarde.", 500
        
        
@main.route('/logout')
def logout():
    session.pop('user', None)  
    session.pop('email', None)  
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))  # Redireciona para a página de login

@main.route('/process_submit_form')
def form():
    return render_template('home.html', email = session['email'])


@main.route('/process_view_prod')
def producoes():
    return render_template('producoes.html', email = session['email'])


@main.route('/salvar_dados', methods=['POST'])
def salvar_dados():
    try:
        # Convertendo campos de texto para um dicionario, melhor visualização.
        #dados_texto = request.form.to_dict()
        dados_texto = {key: request.form.getlist(key) if len(request.form.getlist(key)) > 1 else value for key, value in request.form.items()}

        arquivos_recebidos = {}

        # Mostrar arquivos recebidos dentro do request
        for campo_arquivo, arquivo in request.files.items():
            if arquivo:
                # Apenas confirma que o arquivo foi recebido
                arquivos_recebidos[campo_arquivo] = "Arquivo recebido com sucesso."
                print(f"Arquivo recebido: {campo_arquivo} - {arquivo.filename}")

        # Combina os dados de texto com a confirmação dos arquivos recebidos
        dados_completos = {**dados_texto, **arquivos_recebidos}

        # Exibe o dicionário completo para verificação
        print("Dados recebidos:", dados_completos)

       #####LOGICA DE SALVAR NO BD#######

        # Redireciona para a página inicial após o processamento
        return render_template('home.html', email=session['email'])

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return "Ocorreu um erro inesperado, tente novamente mais tarde.", 500

@main.route('/perfil')
def perfil():
    
    foto_perfil = session['user'].get('picture', 'https://via.placeholder.com/150')
    nome = session['user']['name']
    
    return render_template('perfil.html', foto_perfil=foto_perfil, nome=nome)
