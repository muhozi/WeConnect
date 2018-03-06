from api.models.store import store
class user(object):
    '''Users Model'''
    def save(self, data):
        store().save_user(data)
    def user_exists(self,email):
        ''''Check if user exists '''
        for user in store().users:
            if user['email'] == email :
                return True
        return False

    def get_user(self,email):
        ''''Check if user exists and return user details'''
        for user in store().users:
            if user['email'] == email :
                return user
        return False