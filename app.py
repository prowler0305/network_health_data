from flask import Flask, url_for
from flask import request, jsonify
import logging
app = Flask(__name__)
file_handler = logging.FileHandler('app.log.py')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')


@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid


@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'


@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():

    if request.method == 'GET':
        return "ECHO: GET\n"
    elif request.method == 'POST':
        return "ECHO: POST\n"
    elif request.method == 'PATCH':
        return "ECHO: PATCH\n"
    elif request.method == 'DELETE':
        return "ECHO: DELETE"


@app.route('/data', methods=['GET'])
def api_return_data():

    data = {
        'hello': 'world',
        'number': 3
    }
    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app.route('/users/<userid>', methods=['GET'])
def api_users(userid):

    users = {'1': 'john', '2': 'steve', '3': 'bill'}
    if userid in users:
        return jsonify({userid:users[userid]})
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):

    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    app.logger.info('informing')
    app.logger.warning('warning')
    app.logger.error('screaming bloody murder!')
    logging.warning('Watch out!')
    logging.info('I told you so!')

    return resp

if __name__ == '__main__':
    app.run()