from address_book import AddressBook
from address_book_fields import FieldError

SUPPORTED_COMMANDS = """
    hello         - supported commands list
    add           - save contact with username and phone (required: <username> <phone>)
    add_birthday  - add birthday to previously added contact (required: <username> <birthday>)
    show_birthday - show birthday from contact (required: <username>)
    birthdays     - show birthdays recorded in contacts for next week from today
    change        - change contact phone by username provided (required: <username> <phone>)
    phone         - show contact by username provided (required: <username>)
    all           - show all saved contacts
    exit          - exit from assistant
    close         - same as `exit`
"""


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FieldError as e:
            return e
        except (ValueError, IndexError):
            return "Give me name (and phone/birthday) please."
        except KeyError:
            return "Contact doesn't exist."
        except:
            return "Oops! Something wrong happened."

    return wrapper


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Command processors section


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    return book.add_contact(name, phone)


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    return book.add_birthday(name, birthday)


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    return book.get_birthday(name)


def show_birthdays(book: AddressBook):
    return book.birthdays()


@input_error
def change_contact(args, book: AddressBook):
    name, phone = args
    return book.change_phone(name, phone)


@input_error
def show_contact(args, book: AddressBook):
    name = args[0]
    return book.get_phone(name)


def show_all(book):
    return book.all()


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    return book.get_birthday(name)


def main():
    with AddressBook() as book:
        print("Welcome to the assistant bot!")
        print(SUPPORTED_COMMANDS)
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command == "hello":
                print("How can I help you?")
                print(SUPPORTED_COMMANDS)
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_contact(args, book))
            elif command == "all":
                print(show_all(book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
                pass
            elif command == "show-birthday":
                print(show_birthday(args, book))
                pass
            elif command == "birthdays":
                print(show_birthdays(book))
                pass
            elif command in ["close", "exit"]:
                print("Good bye!")
                break
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
