class Account():
    def __init__(self, email, password_type):
        self.__email = email
        self.__password_type = password_type

    def get_email(self):
        return self.__email

    def get_password_type(self):
        return self.__password_type

    def set_email(self, email):
        self.__email = email

    def set_password_type(self, password_type):
        self.__password_type = password_type

    def account_type_added(self):
        print('New Account id added.')