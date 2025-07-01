from collections import UserDict
from datetime import datetime, timedelta


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
        if not phone.isdigit():
            raise ValueError("Phone must contain only digits")
        if len(phone) < 10:
            raise ValueError('Phone is too short')
        if len(phone) > 10:
            raise ValueError('Phone is too long')
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def find_phone(self, phone_find: str):
        return next((phone for phone in self.phones if phone.value == phone_find), None)

    def add_phone(self, phone: str):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
        return phone_obj

    def add_birthdays(self, value: str):
        if self.birthday is not None:
            raise ValueError('Birthday already set')

        self.birthday = Birthday(value)
        return self.birthday

        self.birthday = Birthday(bday_date.strftime("%d.%m.%Y"))
        return self.birthday

    def show_phones(self):
        return [phone.value for phone in self.phones]

    def remove_phone(self, phone: str):
        phone_deleted = self.find_phone(phone)
        if phone_deleted:
            self.phones.remove(phone_deleted)
            return phone_deleted
        return None

    def edit_phone(self, old_numb: str, new_numb: str):
        old_phone = self.find_phone(old_numb)
        if not old_phone:
            raise ValueError("Old number not found")
        if old_numb == new_numb:
            raise ValueError("Old and new numbers are the same")
        new_phone = Phone(new_numb)  # валідація тут
        self.phones[self.phones.index(old_phone)] = new_phone
        return new_phone

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        bday_str = self.birthday.value if self.birthday else 'N/A'
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, name: str):
        return self.data.get(name)

    def delete_record(self, name: str):
        return self.data.pop(name, None)

    def get_upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_date.replace(year=today.year)
            delta_days = (birthday_this_year - today).days
            adjusted_birthday = birthday_this_year
            if birthday_this_year.weekday() == 5:
                adjusted_birthday += timedelta(days=2)
            elif birthday_this_year.weekday() == 6:
                adjusted_birthday += timedelta(days=1)
            delta_days = (adjusted_birthday - today).days
            if 0 <= delta_days <= days:
                upcoming_birthdays.append((record.name.value, adjusted_birthday))

        return upcoming_birthdays

    def __str__(self):
        return (f'\n=========Address book contacts========== \n'
                + f'\n'.join(str(record) for record in self.data.values())) +'\n'



#Buisnes logic ================================================================================================
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Incorrect values"
        except KeyError:
            return "Contact not found"
        except IndexError:
            return 'Enter the argument for the command'
    return inner

def parse_input(user_input):
    user_input = user_input.strip()
    if not user_input:
        return "",
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find_record(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book: AddressBook):
    name, old_number, new_number = args
    record = book.find_record(name)
    if record:
        record.edit_phone(old_number, new_number)
        return f"Phone number for {name} changed from {old_number} to {new_number}."
    else:
        return f"Contact {name} not found."
@input_error
def phone(args, book: AddressBook):
    name = args[0]
    record = book.find_record(name)
    if record:
        return f'{name}: ' + ', '.join(record.show_phones())

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find_record(name)
    if record:
        record.add_birthdays(birthday)
        return f'Birthday {birthday} was added to contact {name}'
    else:
        raise ValueError

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find_record(name)
    if record and record.birthday:
        date_obj = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
        return f"{name}'s birthday is on {date_obj.strftime('%d.%m.%Y')}"
    elif record and not record.birthday:
        return f"{name} has no birthday set."
    else:
        return "Contact not found"
@input_error
def show_upcoming_birthdays(book: AddressBook):
    result = book.get_upcoming_birthdays()
    end_date = datetime.today().date() + timedelta(days=7)

    if not result:
        return f"No upcoming birthdays from {datetime.today().date()} to {end_date}."

    formatted = [f"{name}: {date.strftime('%d.%m.%Y')}" for name, date in result]
    return f'Upcoming birthdays from {datetime.today().date()} to {end_date}:\n' + '\n'.join(formatted)
#templates ===============================================================================================

menu = """
Команди:

add [ім'я] [телефон]              — Додати контакт або номер телефону
change [ім'я] [старий] [новий]    — Змінити телефонний номер
phone [ім'я]                      — Показати номери телефону контакту
all                               — Показати всі контакти

add-birthday [ім'я] [дата]        — Додати день народження (формат: ДД.ММ.РРРР)
show-birthday [ім'я]              — Показати день народження контакту
birthdays                         — Дні народження на 7 днів наперед

hello                             — Привітання від бота
menu                              — Меню
close / exit                      — Вийти з програми
"""

imag =r""""
  ___      _     _             _   
 / _ \    (_)   | |           | |  
/ /_\ \___ _ ___| |_ ___ _ __ | |_ 
|  _  / __| / __| __/ _ \ '_ \| __|
| | | \__ \ \__ \ ||  __/ | | | |_ 
\_| |_/___/_|___/\__\___|_| |_|\__|
                                   
                                  
"""

#Bot =========================================================================================================

def main():

    book = AddressBook()
    print(imag)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        parsed = parse_input(user_input)
        if not parsed:
            continue
        command, *args = parsed
        if not command:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "menu":
            print(menu)

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(phone(args, book))

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            print(add_birthday(args,book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_upcoming_birthdays(book))
        else:
            print("Invalid command.")

main()


