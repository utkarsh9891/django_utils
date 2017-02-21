class Validators:
    @classmethod
    def is_valid_string(cls, text):
        """
        Checks if a value is a non zero length string
        :param text: a text string
        :return: True/False value
        """
        if type(text) != str or text == '':
            return False
        else:
            return True

    @classmethod
    def is_valid_int(cls, text):
        """
        Checks if a value is a valid integer value
        :param text: the text string
        :return: True/False value
        """
        try:
            int(text)
            return True
        except (ValueError, TypeError):
            return False

    @classmethod
    def is_positive_int(cls, text):
        """
        Checks if a value is a non zero positive integer value
        :param text: the text string
        :return: True/False value
        """
        if cls.is_valid_int(text) and int(text) > 0:
            return True
        else:
            return False

    @classmethod
    def is_valid_float(cls, text):
        """
        Checks if a value is a valid float value
        :param text: the text string
        :return: True/False value
        """
        try:
            float(text)
            return True
        except (ValueError, TypeError):
            return False
