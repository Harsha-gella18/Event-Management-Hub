from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    from .views import views
    from .auth import auth
    from .admin import admin
    from .superadmin import superadmin

    app.register_blueprint(superadmin, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin,url_prefix='/')

    return app
