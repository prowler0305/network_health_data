import requests
import kerberos


def main():
    """

    :return:
    """

    uscc_eng_api_base_url = 'http://127.0.0.1:5000/v1'

    uscc_eng_parser_url_list_all = uscc_eng_api_base_url + '/list_all'
    list_all_params = dict(
        db_name='hbase',
    )
    uscc_eng_parser_url_table_columns = uscc_eng_api_base_url + '/action'
    action_params = dict(
        db_name='hbase',
        table_name=None,
        action_type='schema',
    )
    uscc_eng_parser_status, hbase_url = call_uscc_eng_parser_api(uscc_eng_parser_url_list_all, list_all_params)
    if hbase_url is not None:
        hbase_resp = call_hbase_api(hbase_url)
        if hbase_resp.status_code == requests.codes.ok:
            hbase_json = hbase_resp.json()
            list_table_names = hbase_json.get('table')
            for table in list_table_names:
                for key in table:
                    print(table[key])
                    action_params['table_name'] = table[key]
                    uscc_eng_parser_status, hbase_url = call_uscc_eng_parser_api(uscc_eng_parser_url_table_columns, action_params)
                    if hbase_url is not None:
                        hbase_resp = call_hbase_api(hbase_url)
                        if hbase_resp.status_code == requests.codes.ok:
                            hbase_json = hbase_resp.json()
                            print(hbase_json)
        else:
            print(hbase_resp.status_code)
            print(hbase_resp.text)
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
    uscc_eng_parser_api_resp = requests.get(uscc_eng_parser_url, params=query_params_dict)
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
