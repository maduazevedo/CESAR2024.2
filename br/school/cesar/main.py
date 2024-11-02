from flask import Flask, redirect, url_for, session, render_template, flash
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'auth00'  # chave secreta real
oauth = OAuth(app)

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

    # Verifique se o e-mail pertence ao domínio permitido
    if email.endswith('@cesar.school') or email.endswith('@cesar.org'):
        session['user'] = user_info  # Salva as informações do usuário na sessão
        return render_template('home.html')  # Renderiza a página home após o login
    else:
        flash('Acesso restrito a domínios @cesar.school e @cesar.org')  # Mensagem de erro
        return redirect(url_for('home'))  # Redireciona para a página de login

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove o usuário da sessão
    return redirect('/')  # Redireciona para a home

if __name__ == '__main__':
    app.run(debug=True)
