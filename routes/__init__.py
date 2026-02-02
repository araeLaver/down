from routes.core import core_bp
from routes.meetings import meetings_bp
from routes.suggestions import suggestions_bp
from routes.discovery import discovery_bp
from routes.history import history_bp
from routes.startup_support import startup_support_bp
from routes.admin import admin_bp


def register_blueprints(app):
    """모든 Blueprint를 Flask 앱에 등록"""
    app.register_blueprint(core_bp)
    app.register_blueprint(meetings_bp)
    app.register_blueprint(suggestions_bp)
    app.register_blueprint(discovery_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(startup_support_bp)
    app.register_blueprint(admin_bp)
