from collections import UserDict
import cmd
from datetime import date, datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        try:
            self.__value = datetime.strptime(value, '%Y.%m.%d').date()
        except ValueError:
            raise ValueError('The birsday date must be in format: 2022.01.01')


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('The phone number should be digits only and have 10 symbols')
        self.__value = value


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value: str):
        phone = Phone(value)
        self.phones.append(phone)

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return phone
        raise ValueError(f'Phone: {old_phone} not found!')

    def find_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def days_to_birthday(self):
        if self.birthday is None:
            return None
        date_today = date.today()
        birthday_date = self.birthday.value.replace(year=date_today.year)
        if date_today == birthday_date:
            return 'Birsday today'
        if birthday_date <= date_today - timedelta(days=1):
            birthday_date = birthday_date.replace(year=date_today.year + 1)
        day_to_birthday = (birthday_date - date_today).days
        return day_to_birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, " \
               f"day to birthday: {self.days_to_birthday()}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        return None
        
    def search(self, value: str):                    
        if len(value) < 3:
            return 'To search by name you need at least 3 letters or 3 numbers to search by phone number'
        search_contact = []
        for name, rec in self.data.items():
            if value in name:
                search_contact.append(name)
            for item in rec.phones:
                if value in item.value:
                    search_contact.append(name)    
        if len(search_contact) != 0:
            return search_contact
        else:
            return 'No matches found'

    def delete(self, name: str):
        if name in self.data:
            return self.data.pop(name)

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        yield result
     
    def write_to_file(self):
        self.file = 'Phone_Book'
        with open(self.file, 'wb') as file:
            pickle.dump(self.data, file)
    
    def read_from_file(self):
        self.file = 'Phone_Book'
        with open(self.file, 'rb') as file:
            self.data = pickle.load(file)
        return self.data
        
    class Controller(cmd.Cmd):
        def exit(self):
            self.book.dump()
            return True 


if __name__ == "__main__":

    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("2022.11.01")

    john1_record = Record("John1")
    john1_record.add_phone("1234567890")
    john1_record.add_phone("5555555555")
    john1_record.add_birthday("1992.01.01")

    john2_record = Record("John2")
    john2_record.add_phone("1234567890")
    john2_record.add_phone("5555555555")
    john2_record.add_birthday("1990.12.01")

    # Додавання запису John до адресної кни.ги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")

    book.add_record(jane_record)
    book.add_record(john1_record)
    book.add_record(john2_record)
    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)
    
    print('='*24)

    # Знаходження та редагування телефону для John
    john = book.find("John")

    # Знаходження всіх співпадань по номеру телефона
    search = book.search('123')

    print(search)
    print('='*24)

    john.edit_phone("1234567890", "1112223333")

    # print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
   
    # book.write_to_file()
   
    gen = book.iterator(2)
    print(next(gen))
    # print(type(next(gen)))
    print(next(gen))
    print(next(gen))