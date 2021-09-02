class Book:

    def __init__(self, id: str, title: str, price: float):
        self.__id__ = id
        self.__title__ = title
        self.__price__ = price

    def id(self):
        return self.__id__

    def title(self):
        return self.__title__

    def price(self):
        return self.__price__

    def to_dict(self):
        return {
            'id': self.__id__,
            'title': self.__title__,
            'price': self.__price__
        }

    def to_tuple(self):
        return (self.__id__, self.__title__, self.__price__)

    @staticmethod
    def fields():
        return ['ID', 'TITLE', 'PRICE']

    @staticmethod
    def from_dict(dict):
        return Book(id=dict['id'], title=dict['title'], price=float(dict['price']))
