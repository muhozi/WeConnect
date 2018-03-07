""" Validation Classes """


class RegisterInputs():
    """ register validation class"""

    def __init__(self):
        self.error = ''

    def validate(self, inputs):
        """ Register validation method """
        if ('names' in inputs and
                'email' in inputs and
                'password' in inputs and
                'confirm_password' in inputs):
            return True
        self.error = 'Please provide all the required data'
        return False


class LoginInputs():
    """Login validation class"""

    def __init__(self):
        self.error = ''

    def validate(self, inputs):
        """ Register validation method """
        if 'email' in inputs and 'password' in inputs:
            return True
        self.error = 'Please provide email and password to login'
        return False
