class Profile:
    def __init__(self, id, username, email, allowed_buy,
                 first_name, last_name, is_staff):
        self.id = id
        self.user_name = username
        self.email = email
        self.allowed_buy = allowed_buy
        self.first_name = first_name
        self.last_name = last_name
        self.is_staff = is_staff

    @property
    def name(self):
        name = ''
        if len(self.first_name) > 0:
            name += self.first_name
        if len(self.last_name) > 0:
            name += ' ' + self.last_name
        if len(name) == 0:
            name += self.user_name
        return name


class Product:
    def __init__(self, id, name, quantity, price_cent):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price_cent = price_cent


class SaleEntry:
    def __init__(self, profile, product):
        self.profile = profile
        self.product = product


class Event:
    def __init__(self, id, name, price_group, active):
        self.id = id
        self.name = name
        self.price_group = price_group
        self.active = active


class Comment:
    def __init__(self, profile, comment):
        self.profile = profile
        self.comment = comment
