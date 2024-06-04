from . import Account


class Customer(Account.Account):
    def __init__(self, email, password_type, name, gender, date_of_birth, phone_number, customer_id, profile_picture):
        super().__init__(email, password_type)
        self.__name = name
        self.__gender = gender
        self.__date_of_birth = date_of_birth
        self.__phone_number = phone_number
        self.__customer_id = customer_id
        self.__profile_picture = profile_picture

    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_date_of_birth(self):
        return self.__date_of_birth

    def get_phone_number(self):
        return self.__phone_number

    def get_customer_id(self):
        return self.__customer_id

    def get_profile_picture(self):
        return self.__profile_picture

    def set_name(self, name):
        self.__name = name

    def set_gender(self, gender):
        self.__gender = gender

    def set_date_of_birth(self, date_of_birth):
        self.__date_of_birth = date_of_birth

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_profile_picture(self, profile_picture):
        self.__profile_picture = profile_picture

    def account_type_added(self):
        print('New Customer id:', self.__customer_id, 'is added.')

