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

    def print_self(self):
        print("[ItemStack with %s items of %s]" % (self.amount, self.item.__repr__()))

class Recipe:
    def __init__(self, item_stacks):
        '''
        item_stacks format : [ItemStack(copper_nugget, 3), ItemStack(rough_hewn_wood, 2)] -> copper pickaxe
        or
        {copper_nugget: 3, rough_hewn_wood: 2}
        '''
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

    


if __name__ == '__main__':
    dirt = Item('dirt')
    stick = Item('stick')
    
    my_dirt_stack = ItemStack(dirt, 3)
    my_stick_stack = ItemStack(stick, 3)
    my_recipe = Recipe({dirt: 3, stick: 2})
    print(my_recipe.can_craft([my_dirt_stack, my_stick_stack]))

    dirt.print_self()
    my_dirt_stack.print_self()
