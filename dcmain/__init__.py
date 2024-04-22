from flask import Flask

from . import config
# from . import mainapp
from .appstrings import ccl, lcl, ucl


def create_app(config_type=None):

    config_obj = None
    app = Flask(__name__)  # noqa

    if config_type is None:
        config_type = lcl.development

    app.config.from_object(config.config_classes[config_type])
    config.config_classes[config_type].init_app(app)
    config_obj = config.config_classes[config_type]
    config.Config.CONFIG_TYPE = config_type

    @app.context_processor
    def context_processor():
        from datetime import datetime
        from dcmain.mainapp import utils
        return dict(
            ccl=ccl,
            lcl=lcl,
            ucl=ucl,
            utils=utils,
            datetime=datetime,
            commit_hash=config_obj.COMMIT_HASH
        )

    # app.add_url_rule("/", view_func=mainapp.home)
    from dcmain.mainapp.routes import mainapp

    app.register_blueprint(mainapp)

    return app
