from . import Customer

class Point(Customer.Customer):
    point_count = 0

    def __init__(self, email, password_type,  name, gender, date_of_birth, phone_number, customer_id, profile_picture, point):
        super().__init__(email, password_type, name, gender, date_of_birth, phone_number, customer_id, profile_picture)
        Point.point_count += 1
        self.__point = point

    def set_point(self, point):
        self.__point = point

    def get_point(self):
        return self.__point

    def statement(self):
        print("You have ", self.__point, ' point')

class my_voucher():


    def __init__(self, my_voucher, expiring_date):

        self.__expiring_date = expiring_date
        self.__my_voucher = my_voucher

    def set_voucher(self, my_voucher):
        self.__my_voucher = my_voucher

    def get_my_voucher(self):
        return self.__my_voucher

    def set_expiring_date(self, expiring_date):
        self.__expiring_date = expiring_date

    def get_expiring_date(self):
        return self.__expiring_date




class Voucher:
    voucher_count = 0

    def __init__(self, voucher, Detail, Value, price_in_points, balance):

        Voucher.voucher_count += 1
        self.__balance = balance + 1
        self.__voucher = voucher
        self.__Detail = Detail
        self.__Value = Value
        self.__price_in_points = price_in_points

    def set_voucher(self, voucher):
        self.__voucher = voucher

    def get_voucher(self):
        return self.__voucher

    def set_balance(self, balance):
        self.__balance = balance

    def set_Detail(self, Detail):
        self.__Detail = Detail

    def get_Detail(self):
        return self.__Detail


    def set_Value(self, Value):
        self.__Value = Value

    def get_Value(self):
        return self.__Value

    def set_ID(self, ID):
        self.__ID = ID

    def get_ID(self):
        return self.__balance

    def set_price_in_points(self, price_in_points):
        self.__price_in_points = price_in_points

    def get_price_in_points(self):
        return self.__price_in_points

class Count_all:
    def __init__(self, count):
        self.__count = count + 1

    def set_count(self, count):
        self.__count = count

    def get_count(self):
        return self.get_count
