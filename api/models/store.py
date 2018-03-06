class store():
    """Main store  for storing data"""
    users = []
    businesses = []
    reviews = []
    def __init__(self):
        super(store, self).__init__()
    def save_user(self,data):
        self.users.append(data)