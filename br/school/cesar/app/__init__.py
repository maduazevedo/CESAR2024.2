from flask import Flask
from authlib.integrations.flask_client import OAuth
from .routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = 'auth00'  # chave secreta real

    # Configuração do OAuth
    oauth = OAuth(app)
    oauth.register(
        name='google',
        client_id='1082510897120-c6ae4n7ggdmc6p03uahvbd0vr8qnmvr4.apps.googleusercontent.com',  # Client ID
        client_secret='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',  # Client Secret
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )

    # Registrar o blueprint e passar o objeto oauth
    app.register_blueprint(main_blueprint, url_prefix='/')
    main_blueprint.oauth = oauth  # Adiciona oauth ao blueprint

    return app
