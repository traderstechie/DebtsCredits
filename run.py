import os  # noqa


from dcmain import create_app  # noqa
from dcmain.appstrings import ucl, lcl  # noqa


if os.environ.get(ucl.PRODUCTION_ENV):
    app = create_app(config_type=lcl.production)
else:
    app = create_app()


if __name__ == '__main__':
    if app.config.get(ucl.PRODUCTION_ENV):
        app.run(threaded=True)
    else:
        app.run(host='0.0.0.0', port=5001, threaded=True)
