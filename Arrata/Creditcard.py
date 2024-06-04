from . import Customer


class Creditcard(Customer.Customer):
    aratapay_balance = 0

    def __init__(self, aratapay_balance, last_four_digit, front_digit_hash, expired_date, cvv, email, password_type, name, gender, date_of_birth, phone_number, customer_id, profile_picture):
        super().__init__(email, password_type, name, gender, date_of_birth, phone_number, customer_id, profile_picture)
        self.__cvv = cvv
        self.__expired_date = expired_date
        self.__last_four_digit = last_four_digit
        self.__front_digit_hash = front_digit_hash
        self.__aratapay_balance = aratapay_balance


    # def get_credit_card_number(self):
    #     return self.__credit_card_number

    def get_expired_date(self):
        return self.__expired_date

    def get_cvv(self):
        return self.__cvv

    def get_last_four_digit(self):
        return self.__last_four_digit

    def get_front_digit_hash(self):
        return self.__front_digit_hash

    def get_aratapay_balance(self):
        return self.__aratapay_balance

    # def set_credit_card_number(self, credit_card_number):
    #     self.__credit_card_number = credit_card_number

    def set_expired_date(self, expired_date):
        self.__expired_date = expired_date

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def set_last_four_digit(self, last_four_digit):
        self.__last_four_digit = last_four_digit

    def set__front_digit_hash(self, front_digit_hash):
        self.__front_digit_hash = front_digit_hash

    def set_aratapay_balance(self, aratapay_balance):
        self.__aratapay_balance = aratapay_balance



