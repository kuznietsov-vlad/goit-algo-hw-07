from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        if len(phone) < 10:
            raise ValueError('Phone is too short')
        elif len(phone) > 10:
            raise ValueError('Phone is too long')
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, value):
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date_value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def find_phone(self, phone_find: str):
        for phone in self.phones:
            if phone.value == phone_find:
                return phone

    def add_phone(self, phone):
        if phone.isdigit():
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
        else:
            print('Write correct phone please: ')


    def add_birthday(self,value):
        if self.birthday is not None:
            raise ValueError('Bithday already set')
        self.birthday=Birthday(value)





    def show_phones(self):
        return [phone.value for phone in self.phones]

    def remove_phone(self, phone):
        phone_deleted = self.find_phone(phone)
        if phone_deleted:
            self.phones.remove(phone_deleted)
        else:
            print(f"don't find number {phone} in {self.show_phones()}")

    def edit_phone(self, old_numb: str, new_numb: str):
        if not (old_numb.isdigit() and new_numb.isdigit()):
            raise ValueError(f"Can't find number {old_numb} in {self.show_phones()}")
        if not new_numb in [phone.value for phone in self.phones]:
            if old_numb == new_numb:
                print('Please write a new number different from the old one')
            old_phone_find = self.find_phone(old_numb)
            if old_phone_find:
                self.phones[self.phones.index(old_phone_find)] = Phone(new_numb)
                print(f"Number {old_numb} successfully changed to {new_numb}")

            else:
                print(f"Can't find number {old_numb} in {self.show_phones()}")
        else:
            print(f'Number "{old_numb}" was added previously')

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find_record(self, name: str):
        return self.data.get(name)

    def delete_record(self, name: str):
        if name in self.data:
            self.data.pop(name)
            print(f"Name '{name}' deleted successfully.")
        else:
            print(f"Name '{name}' not found.")

    def get_upcoming_birthdays(self, days=7):
        """ Повертає список людей, чиї дні народження будуть протягом `days` днів від сьогодні. """
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                birthday_this_year = birthday_date.replace(year= today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                b_day_const = (birthday_this_year - today).days
                if 0 <= b_day_const <= days:
                    upcoming_birthdays.append(f'{record.name} birthday on {birthday_this_year}')
        return upcoming_birthdays

    def __str__(self):
        return (f'\n=========Address book contacts========== \n'
                + f'\n'.join(str(record) for record in self.data.values())) +'\n'




try:
    print("_________________Test_____________________")
#__init__
    john_record = Record('John')
    daria_record = Record('Daria')
    vlados_record = Record('Vlados')
#__add_phone__
    john_record.add_phone('1234567890')
    vlados_record.add_phone('1234567890')
    daria_record.add_phone('1234567890')
#add_birthday
    john_record.add_birthday('18.06.2025')
    daria_record.add_birthday('18.06.2025')

# output
    print('book')
    book = AddressBook()
    book.add_record(john_record)
    book.add_record(daria_record)
    book.add_record(vlados_record)
    print(book)
#delete
    book.delete_record(john_record.name)
    print(book)
#find
    vlad = book.find_record("Vlados")
    vlad.edit_phone('0000000000', '5555555555')
    vlados_record.add_phone('1111111111')
    vlad.edit_phone('1111111111', '5555555555')
    print(book)
    print(vlad)
    print("AAAAAAAAAAAAAAAAAAAAAAAA")
    print(book.get_upcoming_birthdays())
except ValueError:
    print('Please write correct number')


