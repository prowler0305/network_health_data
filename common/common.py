import os
import json


class Common(object):
    """
    Common class that encapsulates static methods for common functionality.

    """

    @staticmethod
    def check_path_exists(path):
        """
        Check if a file exists within the USCC-ENG-API file structure.

        :param path: Path to the directory or file
        :return: True or False the directory or file exists
        """

        return os.path.exists(path)

    @staticmethod
    def read_json_file(json_file_path):
        """

        :param json_file_path:
        :return:
        """

        # if os.path.exists(json_file_path):
        if Common.check_path_exists(json_file_path):
            with open(json_file_path) as jsfh:
                return True, json.load(jsfh)

        else:
            return False, "Path: '%s' doesn't exist." % json_file_path
