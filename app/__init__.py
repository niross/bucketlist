from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config


db = SQLAlchemy()


def create_app(config_name):
    from models import Bucketlist

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/bucketlists/', methods=['GET', 'POST'])
    def bucketlists():
        if request.method == 'POST':
            name = str(request.data.get('name'))
            if name is not None:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
        else:
            results = []
            for bucketlist in Bucketlist.get_all():
                results.append({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist(id, **kwargs):
        bucketlist = Bucketlist.query.filter_by(id=id).first()

        if not bucketlist:
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
                'message': 'Bucketlist {} deleted successfully'.format(
                    bucketlist.id
                )
            }, 200

        if request.method == 'PUT':
            name = request.data.get('name')
            if name is None:
                abort(400, 'Name cannot be None')

            bucketlist.name = name
            bucketlist.save()

        response = jsonify({
            'id': bucketlist.id,
            'name': bucketlist.name,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified
        })
        response.status_code = 200
        return response

    return app
