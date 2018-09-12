from common.common import Common

def main():
    """
    
    :return: 
    """

    carrier_smtp_syntax = dict(att='mms.att.net', verizon='vtext.com', uscc='email.uscc.net')

    svt_rc, svt_dict = Common.read_json_file('svt_tests')
    if svt_rc:
        for test_name in svt_dict.get('test_names'):
            print(test_name)
            

if __name__ == '__main__':
    main()