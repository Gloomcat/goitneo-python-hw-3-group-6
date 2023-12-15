from abc import abstractmethod
from datetime import datetime


class FieldError(Exception):
    pass


class _Field:
    def __init__(self, value: str):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.validation_func and not self.validation_func(value):
            raise FieldError(self.validation_fail_msg())
        self.__value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, value):
        return self.value == value

    @abstractmethod
    def validation_func(self, value):
        return NotImplemented

    @abstractmethod
    def validation_fail_msg(self):
        return NotImplemented


class Name(_Field):
    def validation_func(self, value: str):
        return value.isalpha()

    def validation_fail_msg(self):
        return "Incorrect name provided. Name must contain only letters."


class Phone(_Field):
    def validation_func(self, value: str):
        return value.isnumeric() and len(value) == 10

    def validation_fail_msg(self):
        return "Incorrect phone provided. Phone must consist of 10 digits."


class Birthday(_Field):
    def validation_func(self, value: str):
        if value == "":
            return True
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
            if datetime.today() < birthday:
                return False
        except Exception:
            return False
        return True

    def validation_fail_msg(self):
        return "Incorrect birthday provided. Birthday data must be like DD.MM.YYYY and in the past."
