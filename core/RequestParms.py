class RequestParms(object):
    """
    static class with methods for finding and interacting with USCC Engineering API request parameters
    """

    @staticmethod
    def check_parms(request_args, parameter_name):
        """
        Checks to see if the request arguments contain the requested parameter name. Also checks to see that the
        parameter requested has a value given. This serves as a way for HBASE subclass resources to do parameter
        validation beyond the request.RequestParser mechanism.

        :param request_args: dictionary of parameters.
        :param parameter_name: name of the parameter to search for
        :return: Tuple:
                    Found and has a value = (True, parameter value)
                    Not Found or doesn't have a value - (False, "")
        """

        if parameter_name in request_args:
            arg_value = request_args.get(parameter_name)
            if arg_value != "":
                return True, arg_value
            else:
                return False, ""
        else:
            return False, ""
