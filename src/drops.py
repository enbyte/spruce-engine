import json
import random
import inventory as inv

def do_roll(percent):
  ''' Returns True percent % of the time and False (100 - percent) % of the time. '''
  mult = 1
  p = percent
  while p < 1:
    mult *= 10
    p *= 10
  rand = random.randint(1, mult * 100)
  if rand <= p:
    return True
  return False
  
def prettify(thing):
    return thing.lstrip('item').replace('_', ' ').title().strip()
    

class ItemDrops:
  def __init__(self, json_file, is_file=True, name=None):
    '''
    Load an item-drop calc from a json file. 
    Get the section "name" from the file. If name is none, use the entire file.
    File format: (note: @'s are for multiple drops, stripped at the end.)
    {
      "drops_blackthorn": {
        "item_blackthorn": 100,
        "item_blackthorn@": 50,
        "item_blackthorn@@": 25,
        "item_impure_thorn_essence": 2,
        "item_sharp_thorn": 10
       }
     }
    '''
    if is_file:
      f = json.load(open(json_file))
    else:
      f = json.loads(json_file)
    if name == None:
      drops = f
    else:
      drops = f[name]
    self.drops = {}
    self.item_name_keys = []
    for item_name_k in drops:
        self.item_name_keys.append(item_name_k)
        self.drops[len(self.item_name_keys) - 1] = drops[item_name_k]
    #print(self.drops, self.item_name_keys)
    
  def get_drops(self):
    drops = []
    for item_name_k in self.drops:
      if do_roll(self.drops[item_name_k]):
        drops.append(self.item_name_keys[item_name_k].strip('@'))
        
    return drops
  
if __name__ == '__main__':
  drops_str = '''{
      "drops_blackthorn": {
        "item_blackthorn": 100,
        "item_blackthorn@": 50,
        "item_blackthorn@@": 25,
        "item_impure_thorn_essence": 2,
        "item_sharp_thorn": 10
       }, 
       "drops_piggin": {
          "item_piggin_meat": 100,
          "item_piggin_meat@": 30,
          "item_piggin_entrails": 10,
          "item_piggin_skin": 100,
          "item_piggin_skin@": 30,
          "item_piggin_pet": 0.1
      }
    }
    '''
  blackthorn_drops = ItemDrops(drops_str, is_file=False, name='drops_blackthorn')
  piggin_drops = ItemDrops(drops_str, is_file=False, name='drops_piggin')
  player_inv = inv.Inventory()
  while True:
    response = ''
    while not response in ('piggin', 'blackthorn', 'inventory'):
      response = input("Enter piggin, blackthorn or inventory: ")
    
    is_drops = response in ('piggin', 'blackthorn')
    if is_drops:
      if response == 'piggin':
        d = piggin_drops
      elif response == 'blackthorn':
        d = blackthorn_drops
      pgdrps = d.get_drops()
      cds = []
      for i in pgdrps:
        cds.append(prettify(i))
        player_inv.add_item(inv.Item(i))
      printable = ', '.join(cds)
      print(f"You got {printable}!")
    else:
      if response == 'inventory':
        player_inv.print_self()