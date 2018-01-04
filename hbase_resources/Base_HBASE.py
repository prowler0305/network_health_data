from flask import jsonify


class BaseHbase(object):
    """
    Base parent class in which other specific Hbase classes can inherit from. This class can and will contain either
    generic methods or methods which are overloaded by specific test class methods.
    """

    hbase_rool_url = "http://ilscha03-hden-01.uscc.com:20550/"

    def __init__(self, request_keyword):
        self.request = request_keyword
        self.hbase_url = None
        self.hbase_msg_key = "hbase_msg"

    def service_request(self):
        """
        Base method that can be overridden in subclasses
        :return:
        """
        return

    def get_url(self):
        """
        Base method that can be overridden in subclasses
        :return:
        """
        return
