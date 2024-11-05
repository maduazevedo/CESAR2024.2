from flask import Blueprint, redirect, url_for, session, render_template, flash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('login.html')

@main.route('/login')
def login():
    redirect_uri = url_for('main.authorized', _external=True)
    return main.oauth.google.authorize_redirect(redirect_uri)  # Usa oauth do blueprint

@main.route('/login/google/authorized')
def authorized():
    response = main.oauth.google.authorize_access_token()
    user_info = main.oauth.google.get('userinfo').json()
    email = user_info.get('email')

    if email.endswith('@cesar.school') or email.endswith('@cesar.org'):
        session['user'] = user_info
        return render_template('home.html')
    else:
        flash('Acesso restrito a domínios @cesar.school e @cesar.org')
        return redirect(url_for('main.home'))

@main.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.home'))
