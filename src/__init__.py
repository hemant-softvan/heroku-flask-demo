from flask import Flask
import redis
from rq import Queue
from werkzeug.utils import import_string


redis_obj = redis.Redis()
que_conn = Queue(connection=redis_obj)


# This function is used to create flask application
def create_app():
    """
    This function is used to create flask application object
    Author: Softvan
    Created By:
    :return: app object
    """
    app = Flask(__name__, instance_relative_config=False)

    cfg = import_string('config.DevelopmentConfig')()
    app.config.from_object(cfg)

    app.config['LOGGER_HANDLER_POLICY'] = 'always'
    app.config['LOGGER_NAME'] = 'my_logger'
    app.debug = True

    with app.app_context():
        """
        This context used to build initial routes and register blueprints.
        Author: Softvan
        Created by:  
        """

        # @flask_app.after_request
        # def add_header(response):
        #     response.headers['Access-Control-Allow-Origin'] = '*'
        #     return response

        @app.route('/', methods=['GET'])
        def index():
            return "<h1>Hello World</h1>"

        # @app.before_request
        # def make_session_permanent():
        #     """
        #     This function is used to make session permanent false and expire in 15 minutes.
        #     Author: Softvan
        #     Created by:
        #     :return:
        #     """
        #     session.permanent = False
        #     app.permanent_session_lifetime = timedelta(minutes=15)

        from src.station_routes import STATION_BLUEPRINT
        from src.station_routes import station_ns

        # api.init_app(STATION_BLUEPRINT)
        # api.add_namespace(station_ns)

        app.register_blueprint(STATION_BLUEPRINT)

        return app



