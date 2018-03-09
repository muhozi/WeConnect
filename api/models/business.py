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
    def has_two_same_business(self, user_id, business_name, business_id):
        for business in Store.businesses:
            if (business['user_id'] == user_id and (business['name']).lower() == business_name.lower() and business['id'] != business_id):
                return True
        return False

    @classmethod
    def has_business(self, user_id):
        for business in Store.businesses:
            if business['user_id'] == user_id:
                return True
        return False

    @classmethod
    def has_this_business(self, user_id, business_id):
        for business in Store.businesses:
            if business['user_id'] == user_id and business['id'] == business_id:
                return True
        return False

    @classmethod
    def user_businesses(self, user_id):
       	businesses_owned = [business for business in Store.businesses if business['user_id']==user_id]
        return businesses_owned

    @classmethod
    def delete_business(self, id):
        Store.delete_business(id)

    @classmethod
    def update(self, id, data):
        Store.update_business(id, data)
