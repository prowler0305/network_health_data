import requests
import kerberos


def main():
    """

    :return:
    """

    uscc_eng_api_base_url = 'http://127.0.0.1:5000/v1'

    uscc_eng_parser_url_table_columns = uscc_eng_api_base_url + '/action'
    action_params = dict(
        db_name='hbase',
        table_name='enodeb',
        action_type='schema',
    )
    # Call USCC Eng API to get HBASE URL
    uscc_eng_parser_status, hbase_url = call_uscc_eng_parser_api(uscc_eng_parser_url_table_columns, action_params)
    # If returned a HBASE URL call HBASE REST API with URL
    if hbase_url is not None:
        hbase_resp = call_hbase_api(hbase_url)
        # If successful return from HBASE REST API
        if hbase_resp.status_code == requests.codes.ok:
            # Extract and convert the response content into JSON format
            hbase_json_content = hbase_resp.json()
            print("Original JSON object retured by HBASE API: \n%s" % hbase_json_content)
            # Get the ColumnSchema value (aka list of Columns) into a list object
            list_o_columns = hbase_json_content.get('ColumnSchema')
            print("\nValue of key ColumnSchema: \n%s" % list_o_columns)
            print("\nTable '%s' has the following columns:" % hbase_json_content.get('name'))
            # Index through the list of JSON objects
            for index in range(len(list_o_columns)):
                # For each item in the list traverse each key in the JSON object to find the name key and print its value
                # i.e. print the column name.
                for key in list_o_columns[index]:
                    if key == 'name':
                        print('Column name: %s' % list_o_columns[index].get(key))
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
