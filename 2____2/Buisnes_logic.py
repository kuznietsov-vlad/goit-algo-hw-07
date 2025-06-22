import DZ

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found"
        except IndexError:
            return 'Enter the argument for the command'

    return inner


def parse_input(user_input):
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
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record and not record.birthday:
        return f"{name} has no birthday set."
    else:
        return "Contact not found"


@input_error
def show_upcoming_birthdays(book: AddressBook):
    result = book.get_upcoming_birthdays()
    end_date = datetime.today().date() + timedelta(days=7)
    return f'Upcoming birthdays from {datetime.today().date()} to {end_date}:\n' + '\n'.join(result)


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

imag = r""""
  ___      _     _             _   
 / _ \    (_)   | |           | |  
/ /_\ \___ _ ___| |_ ___ _ __ | |_ 
|  _  / __| / __| __/ _ \ '_ \| __|
| | | \__ \ \__ \ ||  __/ | | | |_ 
\_| |_/___/_|___/\__\___|_| |_|\__|


"""


def main():
    book = AddressBook()
    print(imag)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

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

        elif command == "add_birthday":
            print(add_birthday(args, book))

        elif command == "show_birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_upcoming_birthdays(book))

        else:
            print("Invalid command.")


main()