from flask import Flask, url_for, request, jsonify


import logging

app = Flask(__name__)
api_logger = logging.getLogger('uscc_eng_parser_api')
api_logger.setLevel(logging.DEBUG)
api_fh = logging.FileHandler('app.log', mode='w')
api_fh.setLevel(logging.INFO)
api_ch = logging.StreamHandler()
api_ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s:%(module)s - %(levelname)s - %(message)s',
                              datefmt='%m/%d/%Y - %I:%M:%S %p')
api_fh.setFormatter(formatter)
api_logger.addHandler(api_fh)
api_ch.setFormatter(formatter)
api_logger.addHandler(api_ch)


@app.route('/')
def api_root():
    """
    curl http://127.0.0.1:5000/
    :return:
    """
    return 'Welcome'


@app.route('/articles')
def api_articles():
    """
    curl http://127.0.0.1:5000/articles
    :return:
    """
    return 'List of ' + url_for('api_articles')


@app.route('/articles/<articleid>')
def api_article(articleid):
    """
    curl http://127.0.0.1:5000/articles/123
    :param articleid:
    :return:
    """
    return 'You are reading ' + articleid


@app.route('/hello')
def api_hello():
    """
    curl http://127.0.0.1:5000/hello?name=Andrew
    :return:
    """
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'


@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    """
    curl -X GET http://127.0.0.1:5000/echo
    :return:
    """

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
    """
    curl -i http://127.0.0.1:5000/data
    :return:
    """

    data = {
        'hello': 'world',
        'number': 3
    }
    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app.route('/users/<userid>', methods=['GET'])
def api_users(userid):
    """
    curl -i http://127.0.0.1:5000/users/1 for successful run
    curl -i http://127.0.0.1:5000/users/4 for unsuccessful call which triggers errorhandler
    :param userid:
    :return:
    """

    users = {'1': 'john', '2': 'steve', '3': 'bill'}
    if userid in users:
        return jsonify({userid: users[userid]})
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

    api_logger.debug("this message won't go to the filehandler cause of its severity. Instead goes to console")
    api_logger.info('informing')
    api_logger.warning('warning')
    api_logger.error('screaming bloody murder!')
    return resp

if __name__ == '__main__':
    app.run()
