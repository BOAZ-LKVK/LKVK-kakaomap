class Shop:
    def __init__(self, id_str, name, address, contact, star, review_cnt, time, category, menu_list, source):
        self.id_str = id_str
        self.name = name
        self.address = address
        self.contact = contact
        self.star = star
        self.review_cnt = review_cnt
        self.time = time
        self.category = category
        self.menu_list = menu_list
        self.source = source

    def __str__(self):
        return (f"Shop ID: {self.id_str}\n"
                f"Name: {self.name}\n"
                f"Address: {self.address}\n"
                f"Contact: {self.contact}\n"
                f"Rating: {self.star} stars ({self.review_cnt} reviews)\n"
                f"Operating Hours: {self.time}\n"
                f"Category: {self.category}\n"
                f"Menu List: {self.menu_list}\n"
                f"Source: {self.source}\n")