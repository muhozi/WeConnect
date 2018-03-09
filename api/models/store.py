"""
	Storage class to handle data using data structures
"""


class Store():
    """Main store  for storing data"""
    users = []  # Users storage list
    businesses = []  # Businesses storage list
    reviews = []  # Reviews storage list
    auth_tokens = []  # Authentication tokens staorage list
    # User methods

    @classmethod
    def save_user(self, data):
        """Save user method"""
        self.users.append(data)

    @classmethod
    def save_token(self, token):
        """Save token method"""
        self.auth_tokens.append(token)

    @classmethod
    def update_password(self, id, new_password):
        """Change password"""
        for user in self.users:
            if user['id'] == id:
                user['password'] = new_password
                break

    # Business methods
    @classmethod
    def save_business(self, data):
        """Save business method"""
        self.businesses.append(data)

    @classmethod
    def remove_token(self, token):
        """Remove auth token method"""
        self.auth_tokens.remove(token)

    @classmethod
    def delete_business(self, business_id):
        self.businesses[:] = [
            business for business in self.businesses if business.get('id') != business_id]

    @classmethod
    def update_business(self, id, data):
        """Update business method"""
        print("Before")
        print(self.businesses)
        for key in range(0, len(self.businesses)):
            if self.businesses[key]['id'] == id:
                data['id'] = id # Append existing business id to the data
                self.businesses[key] = data
                break
        print("Before")
        print(self.businesses)

