__all__ = ['register_blueprints']
from .main import main_bp
from .code_activity import code_activity_bp
from quart import Quart
from src.configs import MainConfig

def register_blueprints(app: Quart):
  '''
  Register blueprints to the app
  '''
  cfg = MainConfig()
  app.register_blueprint(main_bp)
  app.register_blueprint(code_activity_bp, url_prefix=cfg.URL_PREFIX + 'code_activity/')
