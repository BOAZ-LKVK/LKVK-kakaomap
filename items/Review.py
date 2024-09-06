class Review:
    def __init__(self, id_str, shop_name, username, star, time, comment):
        self.id_str = id_str
        self.shop_name = shop_name
        self.username = username
        self.star = star
        self.time = time
        self.comment = comment

    def __str__(self):
        return (f"Shop ID: {self.id_str}\n"
                f"Shop name: {self.shop_name}\n"
                f"Username: {self.username}\n"
                f"Rating: {self.star} stars\n"
                f"Time: {self.time}\n"
                f"Conmment: {self.comment}\n")