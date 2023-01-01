import yaml

from item import Item
from shopping_cart import ShoppingCart
from errors import TooManyMatchesError, ItemNotExistError, ItemAlreadyExistsError


class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def creating_a_list_without_cart_items(self, list_of_items_from_store) -> list:
        list_without_cart_items = [x for x in list_of_items_from_store if x not in self._shopping_cart]
        self.sort_items(list_without_cart_items)
        return list_without_cart_items

    def search_by_name(self, item_name: str) -> list:
        list_of_items_from_store = [x for x in self._items if item_name in x.name]
        return self.creating_a_list_without_cart_items(list_of_items_from_store)

    def search_by_hashtag(self, hashtag: str) -> list:
        list_of_items_from_store = [x for x in self._items if hashtag in x.hashtags]
        return self.creating_a_list_without_cart_items(list_of_items_from_store)

    def add_item(self, item_name: str):
        # edge case
        if item_name == '':
            item_as_list = self._items
        else:
            item_as_list = [x for x in self._items if item_name == x.name]
        if not item_as_list:
            raise ItemNotExistError("ItemNotExistError")
        item_to_add_as_object = item_as_list[0]
        if len(item_as_list) > 1:
            raise TooManyMatchesError("TooManyMatchesError")
        elif len(item_as_list) == 0:
            raise ItemNotExistError("ItemNotExistError")
        elif item_to_add_as_object in self._shopping_cart:
            raise ItemAlreadyExistsError("ItemAlreadyExistsError")
        self._shopping_cart.append(item_to_add_as_object)

    def remove_item(self, item_name: str):
        # edge case
        if item_name == '':
            item_to_delete_as_list = self._shopping_cart
        else:
            item_to_delete_as_list = [x for x in self._shopping_cart if item_name == x.name]
        if len(item_to_delete_as_list) == 0:
            raise ItemNotExistError("ItemNotExistError")
        elif len(item_to_delete_as_list) > 1:
            raise TooManyMatchesError("TooManyMatchesError")
        item_as_object = item_to_delete_as_list[0]
        self._shopping_cart.remove(item_as_object)

    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()

    def sort_items(self, list_of_items_unsorted: list):
        list_of_lists_of_hashtags = [x.hashtags for x in self._shopping_cart]
        list_of_tags_of_cart_items = [item for sublist in list_of_lists_of_hashtags for item in sublist]
        # bubble sort
        for i in range(len(list_of_items_unsorted) - 1, 0, -1):
            for j in range(0, i):
                if self.comparable(list_of_items_unsorted[j], list_of_items_unsorted[j + 1], list_of_tags_of_cart_items):
                    list_of_items_unsorted[j], list_of_items_unsorted[j+1] = list_of_items_unsorted[j+1], list_of_items_unsorted[j]

    # defining comparisons between 2 items based on absurd requirements
    @staticmethod
    def comparable(item1: Item, item2: Item, tags: list) -> bool:
        item1_common_hashtags = len([x for x in tags if x in item1.hashtags])
        item2_common_hashtags = len([x for x in tags if x in item2.hashtags])
        if item1_common_hashtags < item2_common_hashtags:
            return True
        elif item1_common_hashtags == item2_common_hashtags:
            test = item1.name < item2.name
            return not test
        return False
