class UserError(Exception):
    def __init__(self, msg,):
        self.msg = f"USER ERROR -> {msg}"
        super().__init__(self.msg)

class UserEmailAlreadyExists(UserError):
    def __init__(self, email):
        self.msg = f'Email ({email}) already exists'
        super().__init__(self.msg)
    
class UserNotFoundError(UserError):
    def __init__(self):
        self.msg = f"Not found a user with this attribute"
        super().__init__(self.msg)