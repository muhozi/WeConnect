class Validations():
    """Validations class"""

    def __init__(self, all_inputs):
        """ All inputs dictionary should be available to the class"""
        self.all = all_inputs

    def string(self, key, expected_value):
        """Check if input is required"""
        if key in self.all:
            if self.all[key].isalpha():
                return True
            return key + " should be string"
        return True

    def min(self, key, min):
        """Check required character size"""
        if key in self.all:
            if len(self.all[key]) < int(min):
                return key + " should not be less than " + str(min) + " characters"
            return True
        return True

    def required(self, key, is_required=True):
        """Check input it is required"""
        if key in self.all:
            if self.all[key] is '':
                return key + " should not be empty"
            return True
        return key + " is required"
