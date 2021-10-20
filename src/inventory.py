def concat_item_stacks(stacks):
    l = []
    for stack in stacks:
        l += stack.items_list

    return l

class Item:
    def __init__(self, name):
        self.name = name

    def print_self(self):
        print("[Item name: %s]" % self.name)

    def __repr__(self):
        return '[Item name: %s]' % self.name


class ItemStack:
    def __init__(self, item, amount):
        '''
        Create a "pile" of a certain item.
        '''
        self.items = {item: amount}
        self.items_list = [item] * amount
        self.item = item
        self.amount = amount

    def add_amount(self, amount):
        self.amount += amount
        self.items_list = [self.item] * self.amount

    def sub_amount(self, amount):
        self.amount -= amount
        assert self.amount > 0, "Amount of items in an item stack can't be less than 1"
        self.items_list = [self.item] * self.amount

    def set_amount(self, amount):
        assert amount > 0, "Amount of items in an item stack can't be less than 1"
        self.amount = amount
        self.items_list = [self.item] * self.amount

    def print_self(self):
        print("[ItemStack with %s items of %s]" % (self.amount, self.item.__repr__()))

class Recipe:
    def __init__(self, item_stacks):
        '''
        item_stacks format : [ItemStack(copper_nugget, 3), ItemStack(rough_hewn_wood, 2)] -> copper pickaxe
        or
        {copper_nugget: 3, rough_hewn_wood: 2}
        '''
        self.item_stacks = []
        if type(item_stacks) == dict:
            for item in item_stacks:
                self.item_stacks.append(ItemStack(item, item_stacks[item])) # item and amount
        else:
            self.item_stacks = item_stacks




    def can_craft(self, materials):
        needed_mats = concat_item_stacks(self.item_stacks)
        has_mats = concat_item_stacks(materials)

        for i in has_mats:
            if needed_mats == []: return True #minor efficiency check, if it's already done it doesn't need to keep checking
            if i in needed_mats:
                needed_mats.remove(i)

        if needed_mats == []: return True
        else: return False

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        for item_stacks in self.items:
            if item_stacks.item.name == item.name:
                item_stacks.add_amount(1)
                return
        self.items.append(ItemStack(item, 1))
        
    def add_item_stack(self, stack):
        for item_stacks in self.items:
            if item_stacks.item.name == stack.item.name:
                item_stacks.add_amount(stack.amount)
                return
        self.items.append(stack)

    def print_self(self):
        for stack in self.items:
            print(f'{stack.amount}x of {stack.item.name}')

if __name__ == '__main__':
    dirt = Item('dirt')
    stick = Item('stick')
    shiny_jewel = Item('shiny_jewel')
    
    my_dirt_stack = ItemStack(dirt, 3)
    my_stick_stack = ItemStack(stick, 2)
    my_diamond_stack = ItemStack(shiny_jewel, 2**16)
    dirt_pick_recipe = Recipe({dirt: 3, stick: 2})
    print(dirt_pick_recipe.can_craft([my_dirt_stack, my_stick_stack, my_diamond_stack]))

    dirt.print_self()
    my_dirt_stack.print_self()
