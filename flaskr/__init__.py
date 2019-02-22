from flask import Flask
import os
# from flask_graphql import GraphQLView
from graphene_file_upload.flask import FileUploadGraphQLView


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # from . import api
    # app.register_blueprint(api.bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import database, schema
        # env = os.environ.get('FLASK_ENV', 'development')
        # print('env', env)
        app.add_url_rule(
            '/graphql', view_func=FileUploadGraphQLView.as_view('graphql', schema=schema.schema, graphiql=True))

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            database.db_session.remove()

        database.init_db()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
