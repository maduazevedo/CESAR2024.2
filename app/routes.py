from flask import Blueprint, redirect, url_for, session, render_template, flash, request, jsonify
from service.user_service import UserService
from service.form_service import FormService
import traceback

main = Blueprint('main', __name__)

# Inicialize o serviço de usuário sem passar `mysql` aqui
user_service = None
form_service = None

#Lista de gestores pré cadastrados
l_gestores=[]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def home():
    return render_template('home.html')

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
    global user_service, form_service

    if user_service is None:
        user_service = UserService(mysql)

    if form_service is None:
        form_service = FormService(mysql)

    response = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    email = user_info.get('email')
    nome = user_info.get('name')
    foto_perfil = user_info.get('picture')

    if email.endswith('@cesar.school') or email.endswith('@cesar.org'):
        session['user'] = user_info
        session['email'] = email

        # Se for um gestor, recupere as produções
        if email in l_gestores:
            # Recupera as produções
            producoes = form_service.recuperar_producoes()
            # Passa as produções para o template
            return render_template('gestores.html', nome=nome, email=email, foto_perfil=foto_perfil, producoes=producoes)
        
        # Para outros casos, continua o fluxo de cadastro ou redirecionamento
        elif user_service.cadastrar_usuario(nome, email):
            print("Usuário cadastrado com sucesso, redirecionando para home.")
            return render_template('home.html', email=email, foto_perfil=foto_perfil)
        else:
            print("Usuário não cadastrado, redirecionando para primeiro login.")
            return render_template('primeiro_login.html', email=email, foto_perfil=foto_perfil)

    else:
        flash('Acesso restrito a domínios @cesar.school e @cesar.org')
        return redirect(url_for('main.index'))
   

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

@main.route('/process_submit_form', methods=['POST'])
def process_submit_form():
    
    from main import mysql
    global form_service
    
    if form_service is None:
        form_service = FormService(mysql)

    #coletando dados do form 
    nome = request.form.get('nome_producao')
    descricao = request.form.get('descricao_producao')
    tipo = request.form.get('tipo_producao')
    arquivo = request.files.get('arquivo_producao')
    comprovante_submissao = request.files.get('comprovante')
    veiculo = request.form.get('nome_veiculo')
    vinculo = request.form.get('vinculo')
    curso_relacionado = request.form.get('curso_relacionado')
    projeto_pesquisa = request.form.get('projeto_pesq')
    palavra_chave = request.form.get('palavras_chave')
    grupo_pesquisa = request.form.get('grupo_pesquisa')
    laboratorio = request.form.getlist('laboratorios[]')
    inst_parceiras = request.form.getlist('inst_parceiras')
    carta_anuencia = request.files.get('carta_anuencia')
    
    #coletando dados que serão inseridos na tabela de coautores
    colaborador_coautor = request.form.get('colaborador_coautor', ' ')
    colaborador_externo = request.form.get('colaborador_externo', ' ')
    docente_coautor = request.form.get('docente_coautor', ' ')
    aluno_coautor = request.form.get('aluno_coautor', ' ')
    
    # Formatar coautores para um texto simples
    coautores = []
    if colaborador_coautor:
        coautores.append(f"Colaboradores do Cesar: {colaborador_coautor}")
    if colaborador_externo:
        coautores.append(f"Colaboradores Externos: {colaborador_externo}")
    if docente_coautor:
        coautores.append(f"Docentes da School: {docente_coautor}")
    if aluno_coautor:
        coautores.append(f"Alunos da School: {aluno_coautor}")
    
    # Convertendo a lista de coautores para um único texto separado por vírgulas
    laboratorio = ', '.join(laboratorio)
    coautores = ', '.join(coautores) 
    
    try:
        # Chamada ao serviço para cadastrar a produção com os dados fornecidos
        form_service.cadastrar_producao(
            nome, 
            descricao, 
            tipo, 
            arquivo, 
            comprovante_submissao, 
            veiculo,
            vinculo,
            coautores, 
            curso_relacionado, 
            projeto_pesquisa, 
            palavra_chave, 
            grupo_pesquisa, 
            laboratorio, 
            inst_parceiras, 
            carta_anuencia, 
            session.get('email')  # Use session.get() para evitar KeyError caso 'email' não exista
        )
        

        # Redireciona o usuário para a página 'home.html' após o sucesso
        return render_template('home.html', email=session.get('email'))

    except Exception as e:
        # Captura e exibe o erro detalhado
        print(f"Erro inesperado: {str(e)}")
        print("Detalhes do erro:", traceback.format_exc())
        return render_template('home.html')



@main.route('/process_view_prod')
def producoes():
    return render_template('producoes.html', email = session['email'])


@main.route('/perfil')
def perfil():
    from main import mysql
    global user_service
    
    if user_service is None:
        user_service = UserService(mysql)
        

    foto_perfil = session['user'].get('picture', 'https://via.placeholder.com/150')
    email = session['user']['email'] 
    nome = user_service.recuperar_nome(email)
    
    # Recuperando o currículo do usuário
    curriculo = user_service.buscar_curriculo(email)
    curso_discente = user_service.recuperar_curso_discente(email)
    curso_docente = user_service.recuperar_curso_docente(email)
    cluster = user_service.recuperar_cluster(email)
            
    # Passando tudo para o template
    return render_template('perfil.html', foto_perfil=foto_perfil, nome=nome, email=email, curriculo=curriculo, curso_discente=curso_discente, curso_docente=curso_docente, cluster=cluster)


@main.route('/publicacoes')
def publicacoes():
    global form_service
    
    from main import mysql

    # Obter o email do usuário logado
    email = session['user']['email']
    
    if form_service is None:
        form_service = FormService(mysql)
    
    # Recupera as produções para o email logado
    producoes = form_service.buscar_por_email(email)

    return render_template('producao.html', email=email, producoes=producoes)


@main.route('/publicacoesgestor')
def publicacoesgestor():
    global form_service
    
    from main import mysql
    
    if form_service is None:
        form_service = FormService(mysql)
    
    # Recupera as produções para o gestor
    producoes = form_service.recuperar_producoes()
    
    # Passa as produções diretamente para o template
    return render_template('gestores.html', producoes=producoes)



@main.route('/producoes_detalhadas', methods=['POST'])
def producao_detalhada():
    producao_id = request.form.get('producao_id')

    if not producao_id:
        return redirect(url_for('main.publicacoes'))  # Redireciona para a página de produções

    # Recuperar os detalhes da produção
    producao = form_service.get_producao_detalhada(producao_id)

    if producao:
        return render_template('producao_detalhada.html', producao=producao)
    else:
        flash('Produção não encontrada.')
        return redirect(url_for('main.publicacoes'))  # Redireciona para a página de produções

