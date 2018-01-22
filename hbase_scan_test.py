import requests
import kerberos


def main():
    """

    :return:
    """

    uscc_eng_api_base_url = 'http://127.0.0.1:5000/v1'

    uscc_eng_parser_url_table_columns = uscc_eng_api_base_url + '/scan'
    action_params = dict(
        db_name='hbase',
        table_name='enodeb',
        scan_file_data=None
    )
    filepath = '/home/aspea002/IdeaProjects/USCC_ENG_API/local_test_library/hbase_scan_file'
    with open(filepath) as fh:
        action_params['scan_file_data'] = fh.read()
        print(action_params.get('scan_file_data'))
    # Call USCC Eng API to get HBASE URL
    uscc_eng_parser_status, hbase_url = call_uscc_eng_parser_api(uscc_eng_parser_url_table_columns, action_params)
    # If returned a HBASE URL call HBASE REST API with URL
    if hbase_url is not None:
        pass
        # hbase_resp = call_hbase_api(hbase_url)

        # else:
        #     print(hbase_resp.status_code)
        #     print(hbase_resp.text)
    else:
        print("USCC Engineering API did not provide a URL")
        print(uscc_eng_parser_status)
        return


def call_uscc_eng_parser_api(uscc_eng_parser_url, query_params_dict):
    """
    Call the USCC Engineering API to get the HBASE URL based on parameter.
    :return:
    """

    # Call to USCC Engineering API_API to get HBASE URL needed.
    print('Calling USCC Engineering API to get HBASE URL')
    uscc_eng_parser_api_resp = requests.put(uscc_eng_parser_url, params=query_params_dict, headers={'content-type': 'text/xml'})
    if uscc_eng_parser_api_resp.status_code == requests.codes.ok:
        uscc_eng_parser_resp_json = uscc_eng_parser_api_resp.json()
        print('\nHBASE url returned - %s' % uscc_eng_parser_resp_json.get('hbase_url'))
        return uscc_eng_parser_api_resp.status_code, uscc_eng_parser_resp_json.get('hbase_url')
    else:
        print(uscc_eng_parser_api_resp.text)
        return uscc_eng_parser_api_resp.status_code, None


def call_hbase_api(hbase_url):
    """

    :return:
    """
    # Kerberos Init
    rc, krb_context = kerberos.authGSSClientInit("HTTP/ilscha03-hden-01.uscc.com@INT.USC.LOCAL")
    # Obtain Kerberos auth token
    kerberos.authGSSClientStep(krb_context, "")
    kerb_auth_token = kerberos.authGSSClientResponse(krb_context)
    # Set header with auth token
    hbase_header = {"Authorization": "Negotiate" + kerb_auth_token, "Accept": "application/json"}

    # Call HBASE with URL provided by USCC Engineering API_API.
    print("Calling HBASE URL....")
    hbase_resp = requests.get(hbase_url, headers=hbase_header)
    return hbase_resp


if __name__ == '__main__':
    main()
