from flask import Flask
from flask_wtf import CSRFProtect

from . import config
from .appstrings import lcl

csrf = CSRFProtect()


def create_app(config_type=None):

    config_obj = None
    app = Flask(__name__)  # noqa

    if config_type is None:
        config_type = lcl.development

    app.config.from_object(config.config_classes[config_type])
    config.config_classes[config_type].init_app(app)
    config_obj = config.config_classes[config_type]
    config.Config.CONFIG_TYPE = config_type

    with app.app_context():
        csrf.init_app(app)

    @app.context_processor
    def context_processor():
        from datetime import datetime
        from dcmain.mainapp import utils
        from . import appstrings as app_str
        return dict(
            utils=utils,
            ccl=app_str.ccl,
            lcl=app_str.lcl,
            ucl=app_str.ucl,
            datetime=datetime,
            ccl_dict=app_str.ccl_dict,
            lcl_dict=app_str.lcl_dict,
            ucl_dict=app_str.ucl_dict,
            commit_hash=config_obj.COMMIT_HASH
        )

    # app.add_url_rule("/", view_func=mainapp.home)
    from dcmain.mainapp.routes import mainapp

    app.register_blueprint(mainapp)

    return app
