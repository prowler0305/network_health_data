import requests
import json, sys, time


def main():
    """

    :return:
    """

    fut_url = 'http://127.0.0.1:5000/v1/fut'
    delete_imsi_list = dict(imsi='311580704895154,311580707305677,311580705520444,311580702595068,311580704830154,'
                                 '311580702594425,311580704830207,311580704862845,311580707592017,311580705869630,'
                                 '311580706045064')
    fut_headers = {'content-type': 'application/json'}

    fut_post_response = requests.delete(fut_url, json=delete_imsi_list, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.ok:
        print("IMSI(s) deleted successfully")


if __name__ == '__main__':
    main()
