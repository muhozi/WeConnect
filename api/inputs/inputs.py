class RegisterInputs():
    def __init__(self):
        self.error = ''
    def validate(self,inputs):
        if 'names' in inputs and 'email' in inputs and 'password' in inputs and 'confirm_password' in inputs:
            return True
        self.error = 'Please provide all the required data'
        return False
class LoginInputs():
    def __init__(self):
        self.error = ''
    def validate(self,inputs):
        if 'email' in inputs and 'password' in inputs:
            return True
        self.error = 'Please fill provide email and password to login'
        return False

        
        