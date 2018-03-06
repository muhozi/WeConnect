from api.models.store import store

class user(object):
    """Users Model"""
    def save(self, data):
        store().save_user(data)