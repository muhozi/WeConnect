"""
Validations Methods Class
"""

import re


class Validations():
    """Validations class"""

    def __init__(self, all_inputs):
        """ All inputs dictionary should be available to the class"""
        self.all = all_inputs

    def string(self, key, string):
        """Check if input is required"""
        if key in self.all and self.all[key] is not None:
            if self.all[key].isalpha():
                return True
            return key + " should be string"
        return True

    def minimum(self, key, minimum):
        """Check required character size"""
        if key in self.all and self.all[key] is not None:
            if len(self.all[key]) < int(minimum):
                return key + " should not be less than " + str(minimum) + " characters"
            return True
        return True

    def maximum(self, key, maximum):
        """Check required character size"""
        if key in self.all and self.all[key] is not None:
            if len(self.all[key]) > int(maximum):
                return key + " should not be greater than " + str(maximum) + " characters"
            return True
        return True

    def email(self, key, email):
        """Check required character size"""
        if key in self.all:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.all[key]):
                return "Invalid email address"
            return True
        return True

    def same(self, key, same):
        """Check if given """
        if key in self.all and same in self.all:
            # print(self.all[key]+self.all[key])
            if self.all[same] != self.all[key]:
                return same + " don't match"
            return True
        return True

    def required(self, key, is_required=True):
        """Check input it is required"""
        if key in self.all:
            if self.all[key] is None:
                return key + " should not be empty"
            return True
        return key + " is required"
