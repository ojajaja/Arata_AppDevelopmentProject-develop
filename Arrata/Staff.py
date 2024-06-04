from . import Account


class Staff(Account.Account):
    def __init__(self, email, password_type, date_added, staff_id, staff_profile_image):
        super().__init__(email, password_type)
        self.__date_added = date_added
        self.__staff_id = staff_id
        self.__staff_profile_image = staff_profile_image

    def get_date_added(self):
        return self.__date_added

    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id

    def get_staff_id(self):
        return self.__staff_id

    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id

    def get_staff_profile_image(self):
        return self.__staff_profile_image

    def set_staff_profile_image(self, staff_profile_image):
        self.__staff_profile_image = staff_profile_image

    def account_type_added(self):
        print('New Staff id:', self.__staff_id, 'is added.')




