from item import Item
from errors import ItemAlreadyExistsError, ItemNotExistError


class ShoppingCart(list):
    def add_item(self, item_to_add: Item):
        if len(self) == 0:
            self.append(item_to_add)
        elif item_to_add in self:
            raise ItemAlreadyExistsError("already exists")
        else:
            self.append(item_to_add)

    def remove_item(self, item_name: str):
        item_deleted = False
        for item in self:
            if item.name == item_name:
                self.remove(item)
                item_deleted = True
        if not item_deleted:
            raise ItemNotExistError("not exists")

    def get_subtotal(self) -> int:
        cart_sum = 0
        for item in self:
            cart_sum += item.price
        return cart_sum



