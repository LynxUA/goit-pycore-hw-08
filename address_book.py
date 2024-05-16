'''
Address book module for managing user phones
'''

from collections import UserDict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
import re

class AddressBookException(Exception):
    '''
    Custom error class
    '''

class Field:
    '''
    Generic class for address book data
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, value) -> bool:
        return self.value == value.value

    def __hash__(self) -> int:
        return self.value.__hash__()

class Name(Field):
    '''
    Name field declaration
    '''

class Phone(Field):
    '''
    Phone field declaration with validations
    '''
    def __init__(self, phone):
        if re.match(r"^\d{10}$", phone):
            super().__init__(phone)
        else:
            raise AddressBookException("Phone should consist of 10 numbers.")

class Birthday(Field):
    '''
    Birthday field implementation
    '''
    def __init__(self, value):
        if re.match(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.([0-9]{4})$", value):
            super().__init__(value)
        else:
            raise AddressBookException("Invalid date format. Use DD.MM.YYYY")

class Record:
    '''
    Address record composite
    '''
    def __init__(self, name):
        self.name = Name(name)
        self.phones = {}
        self.birthday = None

    # реалізація класу

    def __str__(self):
        return f"Contact name: {self.name.value}{', phones: ' + '; '
                                                 .join(str(p) for p in self.phones)
         if self.phones else ''}, birthday: {str(self.birthday)}"

    def add_phone(self, phone: str):
        self.phones[Phone(phone)] = True

    def remove_phone(self, phone: str):
        self.find_phone(phone)
        del self.phones[Phone(phone)]

    def edit_phone(self, old_phone: str, phone: str):
        self.find_phone(old_phone)
        self.remove_phone(old_phone)
        self.add_phone(phone)
    
    def find_phone(self, phone: str):
        if self.phones.get(Phone(phone)) is not None:
            return phone
        raise AddressBookException(f"The phone {phone} is not present")
    
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

@dataclass
class Congratulation():
    '''
    DTO for congratulation dates
    '''
    user: Record
    congr_date: date
    def __str__(self):
        return f"{self.user}, congratulation date: {self.congr_date}"

class AddressBook(UserDict):
    '''
    Main Address book class
    '''
    def add_record(self, record: Record):
        self[str(record.name)] = record

    def find(self, name: str):
        if self.get(name) is not None:
            return self[name]
        raise AddressBookException(f"The name {name} is not present in the address book")

    def delete(self, name: str):
        self.find(name)
        del self[name]

    def get_upcoming_birthdays(self):
        '''
        Returns dictionaries that specify upcoming birthdays for this week 
        (or next monday, if the birthdays occur during the weekends)
        '''
        current_date = datetime.today().date()
        next_birthdays = []
        for user in self.values():
            if user.birthday is not None:
                birthday = datetime.strptime(str(user.birthday), "%d.%m.%Y").date()
                birthday_this_year = date(current_date.year, birthday.month, birthday.day)
                start_of_the_year = date(current_date.year, 1, 1)
                current_week = (current_date - start_of_the_year).days // 7
                birthday_week = (birthday_this_year - start_of_the_year).days // 7
                if current_week == birthday_week:
                    birthday_weekdate = birthday_this_year.isoweekday()
                    if birthday_weekdate == 6:
                        congr_date = birthday_this_year + timedelta(days=2)
                    elif birthday_weekdate == 7:
                        congr_date = birthday_this_year + timedelta(days=1)
                    else:
                        congr_date = birthday_this_year
                    next_birthdays.append(Congratulation(user, congr_date))
        return next_birthdays
