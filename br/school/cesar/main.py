from flask import Flask, redirect, url_for, session, render_template, flash, request
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'auth00'  # chave secreta real
oauth = OAuth(app)

banco=[]#SO PARA TESTE


# Configure o Google OAuth
google = oauth.register(
    name='google',
    client_id='1082510897120-c6ae4n7ggdmc6p03uahvbd0vr8qnmvr4.apps.googleusercontent.com',  # Client ID
    client_secret='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',  # Client Secret
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',  # URL para metadados do Google OAuth
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
def home():
    return render_template('login.html')  # Renderiza a página de login

@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/authorized')
def authorized():
    response = google.authorize_access_token()  # Obtém o token de acesso
    user_info = google.get('userinfo').json()  # Obtém as informações do usuário
    email = user_info.get('email')  # Recupera o e-mail do usuário
    #
    global banco
    #
    # Verifique se o e-mail pertence ao domínio permitido
    if email.endswith('@cesar.school') or email.endswith('@cesar.org'):
        session['user'] = user_info  # Salva as informações do usuário na sessão
        session['email'] = email  # Salva o e-mail na sessão


    #VERIFICAR SE USUARIO EXISTE NO BANCO
        if session['email'] in banco: #(JA CADASTRADO)
            return render_template('home.html', email=email)  # Passa o e-mail para o template
        else: #(NÃO CADASTRADO)
            return render_template('primeiro_login.html', email=email) 
    else:
        flash('Acesso restrito a domínios @cesar.school e @cesar.org')  # Mensagem de erro
        return redirect(url_for('home'))  # Redireciona para a página de login
    

@app.route('/process_first_login', methods=['POST'])
def process_first_login():
    global banco
    roles = request.form.getlist('role') 
    curso_discente = request.form.get('curso')  
    curso_docente = request.form.getlist('curso_docente')  # Use getlist para capturar todos os cursos
    cluster = request.form.get('cluster')  
    nome_chamado = request.form.get('nome_chamado')  # Captura o nome que o usuário quer ser chamado
    pessoa_cesar = {}

    pessoa_cesar['nome_chamado'] = nome_chamado  # Adiciona o nome ao dicionário
    
    # Adiciona informações ao dicionário com base no papel selecionado
    for role in roles:
        if role == 'discente':
            pessoa_cesar['discente'] = {'curso': curso_discente}
        elif role == 'docente':
            pessoa_cesar['docente'] = {'curso_docente': curso_docente}  # Salva a lista de cursos
        elif role == 'colaborador':
            pessoa_cesar['colaborador'] = {'cluster': cluster}
    

    # Exibir dicionário no prompt
    print(pessoa_cesar)

    banco.append(session['email'])  # Adiciona o e-mail ao banco
    print(session['email'] in banco)
    flash('Informações salvas com sucesso!')
    return render_template('home.html', email=session['email'])  # Redireciona para a página inicial

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove o usuário da sessão
    return redirect('/')  # Redireciona para a home

if __name__ == '__main__':
    app.run(debug=True)

