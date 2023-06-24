from datetime import datetime, timedelta
import pickle


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)

    def iterator(self, page_size):
        return AddressBookIterator(self.records, page_size)

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.records, file)

    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            self.records = pickle.load(file)

    def search(self, query):
        results = []
        for record in self.records:
            if query in record.name.value or query in record.phone.value:
                results.append(record)
        return results

class AddressBookIterator:
    def __init__(self, records, page_size):
        self.records = records
        self.page_size = page_size
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.records):
            raise StopIteration

        start = self.current_index
        end = self.current_index + self.page_size
        page_records = self.records[start:end]
        self.current_index += self.page_size

        return page_records


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self):
        super().__init__()
        self.value = []

    def add_number(self, number):
        # Перевірка на правильність номера телефону
        if not number.isdigit() or len(number) != 10:
            raise ValueError("Invalid phone number.")
        self.value.append(number)

    def remove_number(self, number):
        if number in self.value:
            self.value.remove(number)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

def is_valid_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        # Перевірка на правильність дня народження
        if not is_valid_date(new_value):
            raise ValueError("Invalid birthday.")
        self._value = new_value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phone = Phone()
        self.birthday = birthday

    def add_phone_number(self, number):
        self.phone.add_number(number)

    def remove_phone_number(self, number):
        self.phone.remove_number(number)

    def days_to_birthday(self):
        if self.birthday is None:
            return None

        today = datetime.now().date()
        next_birthday_year = today.year
        next_birthday = self.birthday.value.replace(year=next_birthday_year)

        if today > next_birthday:
            next_birthday = self.birthday.value.replace(
                year=next_birthday_year + 1)

        days_left = (next_birthday - today).days
        return days_left


def main():
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").lower()
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            contact_info = input("Enter name and phone number: ")
            name, phone = contact_info.split()
            record = Record(name)
            record.add_phone_number(phone)
            address_book.add_record(record)
            print("Contact added successfully.")
        elif command.startswith("change"):
            name = input("Enter contact name: ")
            if any(record.name.value == name for record in address_book.records):
                new_phone = input("Enter new phone number: ")
                for record in address_book.records:
                    if record.name.value == name:
                        record.remove_phone_number(record.phone.value[0])
                        record.add_phone_number(new_phone)
                        print("Phone number changed successfully.")
                        break
            else:
                print("Contact not found.")
        elif command.startswith("phone"):
            name = input("Enter contact name: ")
            for record in address_book.records:
                if record.name.value == name:
                    phone_numbers = ", ".join(record.phone.value)
                    print(f"Phone number(s) for {name}: {phone_numbers}")
                    break
            else:
                print("Contact not found.")
        elif command == "show all":
            if address_book.records:
                for record in address_book.records:
                    phone_numbers = ", ".join(record.phone.value)
                    print(
                        f"Name: {record.name}, Phone number(s): {phone_numbers}")
            else:
                print("No contacts found.")
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()