from . import Customer


class GenerateQueueNo(Customer.Customer):
    def __init__(self, generate_queue_no, your_queue_no, acc_queue_no, update_no,serve_no,plus):
        self.__generate_queue_no = generate_queue_no
        self.__your_queue_no = your_queue_no
        self.__acc_queue_no = acc_queue_no
        self.__update_no = update_no
        self.__serve_no = serve_no
        self.__plus = plus

    def get_plus(self):
        return self.__plus

    def set_plus(self , plus):
        self.__plus = plus

    def get_serve_no(self):
        return self.__serve_no

    def set_serve_no(self , serve_no):
        self.__serve_no = serve_no

    def get_update_no(self):
        return self.__update_no

    def set_update_no(self, update_no):
        self.__update_no = update_no

    def get_acc_queue_no(self):
        return self.__acc_queue_no

    def set_acc_queue_no(self , acc_queue_no):
        self.__acc_queue_no = acc_queue_no

    def get_generate_queue_no(self):
        return self.__generate_queue_no

    def set_generate_queue_no(self, generate_queue_no):
        self.__generate_queue_no = generate_queue_no

    def get_your_queue_no(self):
        return self.__your_queue_no

    def set_your_queue_no(self, your_queue_no):
        self.__your_queue_no = your_queue_no

    def __str__(self):
        return 'Generated Queue No is {}'.format(self.__generate_queue_no)
