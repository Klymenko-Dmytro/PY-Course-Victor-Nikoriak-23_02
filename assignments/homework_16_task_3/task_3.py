class Product:
    def __init__(self, type, name, price):
        self.type = type
        self.name = name
        self.price = price


class ProductStore:
    def __init__(self):
        self.quantity = 0
        self.dict_product = {}
        self.price_premium = 30
        self.income = 0

    def add(self, products, quantity):
        products_tuple = tuple(vars(products).values())
        if products_tuple in self.dict_product:
            self.dict_product[products_tuple]['quantity'] += quantity
        else:
            self.dict_product[products_tuple] = {'quantity': quantity}

    def get_all_products(self):
        return print(self.dict_product)

    def set_discount(self, identifier, percent):
        i = 0
        for product, value in self.dict_product.items():
            if identifier in product:
                value['discount'] = percent
                i += 1
        if i == 0:
            print('Product is not found')

    def sell_product(self, product_name, amount):
        i = 0
        for product, value in self.dict_product.items():
            if product_name in product:
                i += 1
                if value['quantity'] >= amount:
                    value['quantity'] -= amount
                    if 'discount' in value:
                        self.income += amount * (product[2] * ((100 + self.price_premium) / 100)) * ((100 - value['discount'])/100)
                    else:
                        self.income += amount * (product[2] * ((100 + self.price_premium) / 100))
                    print('Successfully sell!')
                else:
                    print('Not enough product to sell')
        if i == 0:
            print('Product is not found')

    def get_income(self):
        return print(f'Total income: {self.income}')

    def get_product_info(self, product_name):
        i = 0
        for product, value in self.dict_product.items():
            if product_name in product:
                product_tuple =(product_name, value['quantity'])
                i += 1
                print(product_tuple)
        if i == 0:
            print('Product is not found')




p = Product('Sport', 'Football T-Shirt', 100)
p2 = Product('Food', 'Ramen', 1.5)

s = ProductStore()
s.add(p, 10)
s.add(p2, 300)
s.set_discount('Ramen', 20)
s.sell_product('Ramen', 10)
s.get_all_products()
s.get_income()
s.get_product_info('Sport')
s.get_product_info('Ramen')