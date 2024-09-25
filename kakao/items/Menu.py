class Menu:
    def __init__(self, id_str, shop_name, name, price, url):
        self.id_str = id_str
        self.shop_name = shop_name
        self.name = name
        self.price = price
        self.url = url

    def __str__(self):
        return (f"Shop ID: {self.id_str}\n"
                f"Shop name: {self.shop_name}\n"
                f"Name: {self.name}\n"
                f"Price : {self.price}\n"
                f"URL: {self.url}\n")