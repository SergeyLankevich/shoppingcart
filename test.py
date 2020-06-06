from main import *

Load.write_barcode('EAN-13.txt')

item1 = Item('Трансмиттер PB720', 2430, 4820024700016)
print(item1.price)
print(item1)

cart1 = ShoppingCart()
cart1.add_item(item1, 3)
print(cart1)
cart1.remove_item(item1, 2)
print(cart1)
print()
item2 = Item('Удлинитель RD100L20', 344, 12345678912345)
print(item2.price)
print()
item3 = Item('Парус Капитана Врунгеля натяжной ', 100)
item4 = Item('Ружьё Барона Мюнхгаузена', 2340.9)
cart1.add_item(item3)
cart1.add_item(item4)
item5 = Item('Патроны к ружью Барона Мюнхгаузена вишневые', 744)
cart1.add_item(item5)
print(cart1)
print(cart1)
print()
Load.write_Item('Item.txt')
cart2 = ShoppingCart()
for item in Load.goods:
    print(item)
cart2.add_item(Load.goods[0])
cart2.add_item(Load.goods[1])


cart2.output('output_Item.txt')