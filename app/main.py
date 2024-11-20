# main.py
from flask import Flask
from authlib.integrations.flask_client import OAuth
from flask_mysqldb import MySQL
from config import Config
from routes import main

app = Flask(__name__)
app.secret_key = 'auth00'
app.config.from_object(Config)


# Configuração do MySQL
mysql = MySQL(app)

# Configuração do OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='1082510897120-c6ae4n7ggdmc6p03uahvbd0vr8qnmvr4.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
