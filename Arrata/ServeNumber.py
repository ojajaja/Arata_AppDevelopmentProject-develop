
class ServeNumber():
    def __init__(self):
        self.__now_serving = 0

    def get_now_serving(self):
        return self.__now_serving

    def set_now_serving(self , now_serving):
        self.__now_serving = now_serving
