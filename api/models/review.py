""" User Model """
from api.models.store import Store


class Review():
    """Users Model"""
    @classmethod
    def save(cls, business_id, data):
        """ Save business in the main store """
        Store.save_review(business_id, data)
