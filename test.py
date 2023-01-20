from collections import UserDict
from datetime import datetime
import pickle


class Field():
    pass
    

class Name(Field):

    def __init__(self, name: str):
        self.__private_name = None
        self.name = name

    def __repr__(self):
        return f'Name: {self.name}'

    @property
    def name(self):
        return self.__private_name
    
    # Перевірка коректності імені
    @name.setter
    def name(self, value: str):
        if value.isalpha():
            self.__private_name = value
        else:
            raise ValueError('Wrong name.')

class Phone(Field):
    
    def __init__(self, phone=None):
        self.__private_value = None
        self.value = phone

    def __repr__(self):
        return f'{self.value}'

    @property
    def value(self):
        return self.__private_value

    # перевірка коректності номера. Додавання +38    
    @value.setter
    def value(self, value):
        if value:
            if value.isdigit() == True:
                if len(value) == 12:
                    self.__private_value = "+" + value
                elif len(value) < 12:
                    self.__private_value = "+38" + value
            else:
                raise ValueError('Wrong number.')
        
        

class Birthday(Field):

    def __init__(self, value=None):
        self.__private_value = None
        self.value = value

    @property
    def value(self):
        return self.__private_value

    # перевірка коректності номера. Додавання +38
    @value.setter
    def value(self, value):
        try:
            if value != None:
                self.__private_value = datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            print (f'Please, input the date in format dd/mm/yyyy ')     


class Record():

    def __init__(self, name: Name, birthday: Birthday, *phones):
        self.name = name
        self.phones = list(phones)
        self.birthday = birthday

    def __repr__(self):
        rec = f'{self.name}, phones: {self.phones}, birthday: {self.birthday.value}'
        return rec

    def add_phone(self, value: Phone):
        self.phones.append(value)
    
    def change_phone(self, phone_old: Phone, phone_new: Phone):
        self.phones.remove(phone_old)
        self.phones.append(phone_new)

    def del_phone(self, value: Phone):
        self.phones.remove(value)

    def days_to_birthday(self, birthday: Birthday):
        
        self.birthday = birthday
        if self.birthday.value:
            try:
                current_date = datetime.now().date()
                user_date = self.birthday.value.replace(year = current_date.year)
                delta_days = user_date - current_date
                    
                if 0 < delta_days.days:
                    return f'Лишилось до Дня народження: {delta_days.days} днів.'
                else:
                    user_date = self.birthday.value.replace(year=user_date.year + 1)
                    delta_days = user_date - current_date
                    if 0 < delta_days.days:
                        return f'Лишилось до Дня народження: {delta_days.days} днів.'
            except ValueError:
                return f'Please, input date in format dd/mm/yyyy '
        else:
            return f'Date of birth is not found. Please, add day of birth, if you want. '


class AddressBook(UserDict):

    def iterator(self):
        for record in self.data.values():
            yield record.__repr__()

    def print_page(self, user_range=2):
        for _ in range(user_range):
            try:
                print(next(ab_iter))
            except StopIteration:
                print('The end of contact book. ')

    def add_record(self, record: Record):
        self.data[record.name.name] = record

    file_name = 'data.bin'
    def write_file(self):
        with open(self.file_name, "wb") as fh:
            pickle.dump(ab, fh)        

    def read_file(self):
        with open(self.file_name, "rb") as fh:
            self.unpacked_contacts = pickle.load(fh)

    def search_contact(self, user_search):
        
        for record in ab.data.values():
            result = str(record).lower().find(user_search)
            if result != -1:
                print (record)

    

if __name__ == '__main__':
    
    try:
        AddressBook.read_file(AddressBook)
    except FileNotFoundError:
        print('Немає файлу з контактами. ')
    
    ab = AddressBook()
    print(AddressBook.unpacked_contacts)
    
    name = Name('Bill')
    phone = Phone('1234567890')
    birth = Birthday('26/02/2002')
    rec = Record(name, birth, phone)
    ab.add_record(rec)
   
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    print(ab['Bill'].days_to_birthday(birth))
    assert ab['Bill'].phones[0].value == '+381234567890'
    
    print('All Ok)')

    name = Name('Nasik')
    phone = Phone('0671603025')
    birth = Birthday('26/03/2002')
    rec = Record(name, birth, phone)
    ab.add_record(rec)
    name = Name('Nasiya')
    phone = Phone('0554603025')
    birth = Birthday()
    rec = Record(name, birth, phone)
    ab.add_record(rec)
    name = Name('Anna')
    phone = Phone('0994123425')
    birth = Birthday('06/08/1999')
    rec = Record(name, birth, phone)
    ab.add_record(rec)
    name = Name('German')
    phone = Phone(None)
    birth = Birthday('7/10/2000')
    rec = Record(name, birth, phone)
    ab.add_record(rec)
    name = Name('Alania')
    phone = Phone('3060939559')
    birth = Birthday('3/11/1978')
    rec = Record(name, birth, phone)
    ab.add_record(rec)
    # Вивід всієї книги:
    # print(ab)
    # print(ab.values)
    ab_iter = ab.iterator()

    # Вивід по user_range записів:
    # AddressBook.print_page(AddressBook, 3)
    # AddressBook.print_page(AddressBook, 3)

    # Пошук в книзі контактів
    user_search = 'Ger'
    AddressBook.search_contact(AddressBook, user_search.lower())
    AddressBook.write_file(AddressBook)

