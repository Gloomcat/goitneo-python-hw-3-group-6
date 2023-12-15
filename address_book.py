import csv

from collections import UserDict
from address_book_fields import Name, Phone, Birthday, FieldError
from address_book_birthdays import get_birthdays_per_week


class _Record(UserDict):
    def __init__(self, name: str, phone: str, birthday: str = ""):
        super().__init__()
        self.data["name"] = ""
        self.data["phone"] = ""
        self.data["birthday"] = ""
        self.name = name
        self.phone = phone
        self.birthday = birthday

    @property
    def name(self):
        return self.data["name"]

    @name.setter
    def name(self, name: str):
        try:
            self.data["name"] = Name(name)
        except FieldError as e:
            raise e

    @property
    def phone(self):
        return self.data["phone"]

    @phone.setter
    def phone(self, phone: str):
        try:
            self.data["phone"] = Phone(phone)
        except FieldError as e:
            raise e

    @property
    def birthday(self):
        return self.data["birthday"]

    @birthday.setter
    def birthday(self, birthday: str):
        try:
            self.data["birthday"] = Birthday(birthday)
        except FieldError as e:
            raise e

    def __str__(self):
        return f"Contact name: {self.name}, phone: {self.phone}, birthday: {self.birthday if self.birthday else 'Not provided.'}"


class _PersistantBook(UserDict):
    def __init__(self, filename="address_book_data.csv", fields=("name", "phone", "birthday")):
        super().__init__()
        self.filename = filename
        self.fields = fields
        self.__key_field = self.fields[0]
        self.__dict_file_handle = None

    def __enter__(self):
        try:
            self.__dict_file_handle = open(self.filename, "r+")
            self.__csv_processor = csv.DictReader(self.__dict_file_handle)
            for row in self.__csv_processor:
                self.data[row[self.__key_field]] = _Record(
                    *(row[field] for field in self.fields))
        except FileNotFoundError:
            self.__dict_file_handle = open(self.filename, "w")
        return self

    def __exit__(self, *_):
        # For now we ignore possible errors on this step
        self.__dict_file_handle.close()

    def update(data_change_func):
        def wrapper(self, *args):
            result = data_change_func(self, *args)
            if self.__dict_file_handle and self.data:
                self.__dict_file_handle.truncate(0)
                self.__dict_file_handle.seek(0)
                self.__csv_processor = csv.DictWriter(
                    self.__dict_file_handle, fieldnames=self.fields)
                self.__csv_processor.writeheader()
                for record in self.data.values():
                    self.__csv_processor.writerow(record.data)
            return result
        return wrapper


class AddressBook(_PersistantBook):
    def __init__(self):
        super().__init__()

    @_PersistantBook.update
    def add_contact(self, name, phone):
        if name in self.data:
            return "Contact already exists."
        self.data[name] = _Record(name, phone)
        return "Contact added."

    @_PersistantBook.update
    def add_birthday(self, name, birthday):
        if name in self.data:
            self.data[name].birthday = birthday
            return "Birthday added."
        return "Contact doesn't exist."

    def get_birthday(self, name):
        if name in self.data:
            return self.data[name].birthday.value
        return "Contact doesn't exist."

    def birthdays(self):
        if not self.data:
            return "Contacts book is empty."
        stored_birthdays = []
        for name, record in self.data.items():
            if record.birthday:
                stored_birthdays.append(
                    {"name": name, "birthday": record.birthday.value})
        return get_birthdays_per_week(stored_birthdays)

    @_PersistantBook.update
    def change_phone(self, name, phone):
        if name in self.data:
            self.data[name].phone = phone
            return "Contact's phone updated."
        return "Contact doesn't exist."

    def get_phone(self, name):
        if name in self.data:
            return self.data[name].phone
        return "Contact doesn't exist."

    def all(self):
        if not self.data:
            return "Contacts book is empty."
        return "\n".join(str(v) for v in self.data.values())


if __name__ == "__main__":
    # Create new AddressBook context
    book = AddressBook()
    # Try add `John` record with invalid name
    try:
        book.add_contact("John123", "1234567890")
    except FieldError as e:
        print(e)

    # Try add `John` record with invalid phone
    try:
        book.add_contact("John", "asdd12889133+")
    except FieldError as e:
        print(e)

    # Add `John` record
    book.add_contact("John", "1234567890")

    # Try add invalid birthday to `John` record
    try:
        book.add_birthday("John", "13-06-1999")
    except FieldError as e:
        print(e)

    with AddressBook() as book:
        from faker import Faker
        from random import randrange
        from datetime import datetime

        # Add test data to the book
        fake = Faker()
        for _ in range(100):
            name = fake.name().replace(". ", "").split()[0]
            phone = str(randrange(1000000000, 9999999999))
            birthday = fake.date_time().strftime("%d.%m.%Y")
            book.add_contact(name, phone)
            book.add_birthday(name, birthday)

            print(book.change_phone(name, str(randrange(1000000000, 9999999999))))
            print(book.get_phone(name))
            print(book.get_birthday(name))
            contact_birthday = datetime.strptime(
                book.get_birthday(name), "%d.%m.%Y").date()

    with AddressBook() as book:
        # Print all stored records from the book
        print(book.all())
        print("Number of records:", len(book.data.items()))

        # Print birthdays for the next week
        print(book.birthdays())
