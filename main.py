'''
Assistant bot module
'''

import pickle
import atexit
from functools import wraps
from address_book import AddressBook, AddressBookException, Record

class BotException(Exception):
    '''
    Bot exception handling class
    '''


def save_data(book, filename="addressbook.pkl"):
    '''
    Saves addressbook into a file
    '''
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    '''
    Loads addressbook from a file
    '''
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def input_error(func):
    '''
    Inputs error handling decorator
    '''
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "There should be two arguments."
        except BotException as e:
            return e.args[0]
        except AddressBookException as e:
            return e.args[0]

    return inner

def parse_input(user_input: str) -> str:
    '''
    Parses the user input from the command line
    '''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def change_contact(args: slice, book: AddressBook) -> str:
    '''
    Changes a phone for a specific user
    '''
    if len(args) != 3:
        raise BotException("There should be 3 arguments: name,"
                           " the phone you want to change, the new phone")
    name, old_phone, new_phone = args
    if book.get(name) is None:
        raise BotException("Contact is not created yet")
    book[name].edit_phone(old_phone, new_phone)
    return "Contact changed."

@input_error
def get_phone(args: slice, book: AddressBook) -> str:
    '''
    Lists a phone for a specific user
    '''
    name = args[0]
    if book.get(name) is None:
        raise BotException("Contact is not created yet")
    return book[name].phone

def get_all_phones(book: AddressBook) -> str:
    '''
    Lists all the phones in the contacts
    '''
    phones = ""
    for val in book.values():
        phones += f"{val}\n"
    return phones

@input_error
def add_contact(args, book: AddressBook):
    '''
    Adds a new contact or adds a new phone
    '''
    name, phone, *_ = args
    record = book.get(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def add_birthday(args, book: AddressBook):
    '''
    Specifies birthday for a contact
    '''
    name, birthday, *_ = args
    if book.get(name) is None:
        raise BotException("Contact is not created yet")
    book[name].add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    '''
    Shows a birthday for a user
    '''
    name, *_ = args
    if book.get(name) is None:
        raise BotException("Contact is not created yet")
    return book[name].birthday

@input_error
def birthdays(book: AddressBook):
    '''
    Shows all the upcoming birthdays
    '''
    return '; '.join(str(p) for p in book.get_upcoming_birthdays())
def exit_handler(book):
    '''
    Saves data on exit
    '''
    return lambda : save_data(book)

def main():
    '''
    Main function
    '''
    book = load_data()
    atexit.register(exit_handler(book))

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(get_phone(args, book))

        elif command == "all":
            print(get_all_phones(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
