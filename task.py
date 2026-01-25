from collections import UserDict
from dataclasses import dataclass
from datetime import datetime, timedelta
import pickle



@dataclass
class Field:
    value: str

    def __str__(self):
        return self.value



class Name(Field):
    pass



class Phone(Field):
    def __init__(self, value: str):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)



class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")
        super().__init__(value)



class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))


    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None


    def edit_phone(self, old_phone: str, new_phone: str):
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError("Old phone not found.")
        index = self.phones.index(phone_obj)
        self.phones[index] = Phone(new_phone)


    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)


    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value if self.birthday else "—"
        return f"{self.name.value}: {phones}, birthday: {birthday}"



class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


    def find(self, name: str):
        return self.data.get(name)


    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            bday_this_year = bday.replace(year=today.year)

            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            delta = (bday_this_year - today).days

            if 0 <= delta <= 7:
                congratulate_date = bday_this_year

                if congratulate_date.weekday() >= 5:
                    congratulate_date += timedelta(days=(7 - congratulate_date.weekday()))

                upcoming.append({
                    "name": record.name.value,
                    "birthday": congratulate_date.strftime("%d.%m.%Y")
                })

        return upcoming


    def __str__(self):
        if not self.data:
            return "Address book is empty."
        return "\n".join(str(record) for record in self.data.values())



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments."
        except KeyError:
            return "Contact not found."
        except AttributeError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
    return inner



def parse_input(user_input: str):
    parts = user_input.split()
    if not parts:
        return "", []
    command, *args = parts
    return command.lower(), args



@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added or updated."



@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Phone number updated."



@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return "; ".join(p.value for p in record.phones)



@input_error
def show_all(_, book):
    return str(book)



@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."



@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record.birthday:
        return "Birthday not set."
    return record.birthday.value



@input_error
def birthdays(_, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays this week."
    return "\n".join(f"{u['name']}: {u['birthday']}" for u in upcoming)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("exit", "close"):
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")



if __name__ == "__main__":
    main()
