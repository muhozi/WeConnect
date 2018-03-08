""" Input Validation Classes """
from api.validations import Validations
# Registration validations
REGISTER_RULES = [
    {'names': [('string', True), ('min', 4), ('required', True)]},
    {'email': [('min', 6), ('required', True)]},
    {'password': [('min', 6), ('required', True)]},
    {'confirm_password': [('min', 6), ('required', True)]},
]
# Login validation
LOGIN_RULES = [
    {'email': [('min', 6), ('required', True)]},
    {'password': [('min', 6), ('required', True)]},
]
# Reset password validations
RESET_PWD_RULES = [
    {'new_password': [('min', 6), ('required', True)]},
    {'old_password': [('min', 6), ('required', True)]},
]
# Register business validation rules
REGISTER_BUSINESS_RULES = [
    {'name': [('min', 2), ('required', True)]},
    {'description': [('min', 6), ('required', True)]},
    {'country': [('min', 4), ('required', True)]},
    {'city': [('min', 6), ('required', True)]},
]


def validate(inputs, all_rules):
    """ Register validation method """
    error_bag = {}
    valid = Validations(inputs)
    for rules in all_rules:
        for key in rules:
            rule_key = key
            for rule in rules[rule_key]:
                execute = getattr(valid, rule[0])(
                    rule_key, rule[1])
                if execute is True:
                    pass
                if execute != True:
                    if rule_key in error_bag:
                        error_bag[rule_key].append(execute)
                    else:
                        error_bag[rule_key] = []
                        error_bag[rule_key].append(execute)
    if len(error_bag) > 0:
        return error_bag
    return True
