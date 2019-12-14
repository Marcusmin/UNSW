from flask import Flask, request
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)

todos = {}

@api.route('/hello', endpoint='todo_ep')
class Hello(Resource):
    def get(self):
        return {'hello':'world'}

@api.route('/<string:todo_id>')
class Try(Resource):
    def get(self, todo_id):
        return {todo_id : todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id : todos[todo_id]}

@api.route('/test')
class test(Resource):
    def get(self):
        return {'hello':'world'}, 201, {'fuck':'me'}

if __name__ == '__main__':
    app.run(debug = True)