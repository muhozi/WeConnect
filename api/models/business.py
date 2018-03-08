""" User Model """
from api.models.store import Store


class Business():
    """Users Model"""
    @classmethod
    def save(self, data):
        """ Save user in the main store """
        Store.save_business(data)

    @classmethod
    def has_same_business(self, user_id, business_name):
        for business in Store.businesses:
            if business['user_id'] == user_id and (business['name']).lower() == business_name.lower():
                return True
        return False

    @classmethod
    def has_this_business(self, user_id, business_id):
        for business in Store.businesses:
            if business['user_id'] == user_id and business['id'] == business_id:
                return True
        return False

    @classmethod
    def delete_business(self,id):
        Store.delete_business(id)
