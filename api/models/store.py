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

    def save_user(self, data):
        """Save user method"""
        self.users.append(data)

    def save_token(self, token):
        """Save token method"""
        self.auth_tokens.append(token)

    def update_password(self, id, new_password):
        """Change password"""
        for user in self.users:
            if user['id'] == id:
                user['password'] = new_password
                break

    # Business methods
    def save_business(self, data):
        """Save user method"""
        self.businesses.append(data)

    def remove_token(self, token):
        """Save user method"""
        self.auth_tokens.remove(token)
