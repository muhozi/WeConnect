""" User Model """
from api.models.store import Store


class Business():
    """Users Model"""
    @classmethod
    def save(cls, data):
        """ Save business in the main store """
        Store.save_business(data)

    @classmethod
    def has_same_business(cls, user_id, business_name):
        """ Check if the user has the same business name"""
        for business in Store.businesses:
            if (business['user_id'] == user_id and
                    (business['name']).lower() == business_name.lower()):
                return True
        return False

    @classmethod
    def has_two_same_business(cls, user_id, business_name, business_id):
        """ Check if the user has the two same busines name #nt from the one to update"""
        for business in Store.businesses:
            if (business['user_id'] == user_id and
                    (business['name']).lower() == business_name.lower() and
                    business['id'] != business_id):
                return True
        return False

    @classmethod
    def has_business(cls, user_id):
        """ Check if the user has a business"""
        for business in Store.businesses:
            if business['user_id'] == user_id:
                return True
        return False

    @classmethod
    def has_this_business(cls, user_id, business_id):
        """ Check if the user own a given business"""
        for business in Store.businesses:
            if business['user_id'] == user_id and business['id'] == business_id:
                return True
        return False

    @classmethod
    def user_businesses(cls, user_id):
        """ Get all the businesses of the user"""
        businesses_owned = [
            business for business in Store.businesses if business['user_id'] == user_id]
        return businesses_owned

    @classmethod
    def delete_business(cls, business_id):
        """ Delete business from the store"""
        Store.delete_business(business_id)

    @classmethod
    def update(cls, business_id, data):
        """ Update business"""
        Store.update_business(business_id, data)
