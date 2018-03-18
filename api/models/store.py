"""
	Storage class to handle data using data structures
"""


class Store():
    """Main store  for storing data"""
    users = []  # Users storage list
    businesses = []  # Businesses storage list
    reviews = {}  # Reviews storage dictionary
    auth_tokens = []  # Authentication tokens staorage list
    # User methods

    @classmethod
    def save_user(cls, data):
        """Save user method"""
        cls.users.append(data)

    @classmethod
    def save_token(cls, token):
        """Save token method"""
        cls.auth_tokens.append(token)

    @classmethod
    def update_password(cls, user_id, new_password):
        """Change password"""
        for user in cls.users:
            if user['id'] == user_id:
                user['password'] = new_password
                break

    # Business methods
    @classmethod
    def save_business(cls, data):
        """Save business method"""
        cls.businesses.append(data)

    @classmethod
    def remove_token(cls, token):
        """Remove auth token method"""
        cls.auth_tokens.remove(token)

    @classmethod
    def delete_business(cls, business_id):
        """ Delete business"""
        cls.businesses[:] = [
            business for business in cls.businesses if business.get('id') != business_id]

    @classmethod
    def update_business(cls, business_id, data):
        """Update business method"""
        for key in range(0, len(cls.businesses)):
            if cls.businesses[key]['id'] == business_id:
                # Append existing business id to the data
                data['id'] = business_id
                cls.businesses[key] = data
                break

    # Reviews methods

    @classmethod
    def save_review(cls, business_id, data):
        """Save review method"""
        if not business_id in cls.reviews:
            cls.reviews[business_id] = []
        cls.reviews[business_id].append(data)
