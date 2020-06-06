class Load:

    barcode_dict = {}
    goods = []

    @classmethod
    def write_barcode(cls, f_barcodes):
        with open(f_barcodes, encoding='utf-8') as barcode_in:
            for pos in barcode_in:
                country = pos.split(': ')[0]
                code = pos[1][:-1]
                if not code.count('-'):
                    cls.barcode_dict[str(code)] = country
                else:
                    for number in range(int(code[:code.find('-')]), int(code[code.find('-') + 1:]) + 1):
                        if len(str(number)) == 1:
                            number = '0' + str(number)
                        cls.barcode_dict[number] = country

    @classmethod
    def write_items(cls, f_items):
        with open(f_items, encoding='utf-8') as catalogue:
            for position in catalogue:
                separated = position.split(';')
                cls.goods.append(Item(*separated[:-1]))


class ShoppingCart:

    def __init__(self):
        self.items = {}

    def __str__(self):
        return str(self.items)

    def add_item(self, item, quantity=1):
        if quantity <= 0:
            print('Некорректный ввод')
        if self.items[item]:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item, quantity=1):
        if not self.items[item] or self.items[item] < quantity:
            print('Некорректный ввод')
        else:
            self.items[item] -= quantity
        if self.items[item] == 0:
            del self.items[item]

    def output_sum(self):
        output_sum = 0
        for item, quantity in self.items.items():
            if item.price:
                output_sum += item * quantity * item.price
            else:
                pass  # no price
        return output_sum

    def output(self, f_out):
        output = ''
        for item in self.items:
            output += item.name + ';'
            if item.price:
                output += str(item.price) + ';'
            else:
                output += ';'
            if item.barcode is None:
                output += ';'
            else:
                output += str(item.barcode) + ';'
            output += '\n'
        with open(f_out, 'w', encoding='utf-8') as out:
            out.write(output)


class Item:
    barcode_dict = Load.barcode_dict

    def __init__(self, name, price, barcode=None):
        self.name = name
        self.__price = price
        if self.is_valid(barcode):
            self.barcode = barcode
            self.country = str(self.barcode)[:2]
            self.manufacturer = str(self.barcode)[2:7]
            self.item_code = str(self.barcode)[7:12]
            self.check_digit = str(self.barcode)[-1]
        else:
            self.barcode = None
            self.country = None
            self.manufacturer = None
            self.item_code = None
            self.check_digit = None

    @staticmethod
    def is_valid(barcode):
        try:
            if not isinstance(barcode, int):
                return False
            if not barcode or len(str(barcode)) != 13:
                return False
            for digit in str(barcode):
                if str(digit) not in '1234567890':
                    return False
        except:
            return False
        return True

    def __str__(self):
        output = ''
        output += 'Товар: ' + self.name + '\n'
        if self.__price:
            output += 'Цена: ' + str(self.__price) + '\n'
        else:
            output += 'Ценник утерян'
        if self.barcode:
            output += 'Производитель: ' + Item.barcode_dict[self.country] + '\n'
        return output

    def __repr__(self):
        output = 'name: ' + str(self.name)
        return output

    @property
    def price(self):
        return self.__price

    @price.getter
    def price(self):
        return self.__price

    @price.setter
    def price(self, cost):
        try:
            if cost >= 0:
                self.__price = cost
            else:
                pass
        except ValueError:
            pass

