from uscc_api import uscc_eng_app


if __name__ == '__main__':

    uscc_eng_app.run(debug=uscc_eng_app.config.get('DEBUG'), threaded=uscc_eng_app.config.get('THREADED'),
                     port=uscc_eng_app.config.get('PORT'), host=uscc_eng_app.config.get('HOST'))
