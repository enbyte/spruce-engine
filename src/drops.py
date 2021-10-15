import json
import random

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
    return thing.replace('_', ' ').title()
    

class ItemDrops:
  def __init__(self, json_file, is_file=True):
    '''
    Load an item-drop calc from a json file. 
    File format: (note: @'s are for multiple drops, stripped at the end.)
    {
      "name": "drops_blackthorn",
      "drops": {
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
    self.name = f['name']
    drops = f['drops']
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
    blackthorn_drops = ItemDrops('''{
      "name": "drops_blackthorn",
      "drops": {
        "item_blackthorn": 100,
        "item_blackthorn@": 50,
        "item_blackthorn@@": 25,
        "item_impure_thorn_essence": 2,
        "item_sharp_thorn": 10
       }
     }''', is_file = False)
    piggin_drops = ItemDrops('''{
      "name": "drops_piggin",
      "drops": {
          "item_piggin_meat": 100,
          "item_piggin_meat@": 30,
          "item_piggin_entrails": 10,
          "item_piggin_skin": 100,
          "item_piggin_skin@": 30,
          "item_piggin_pet": 0.1
        }
      }
    ''', is_file=False)
    for i in range(1000):
      d = piggin_drops.get_drops()
      if 'item_piggin_pet' in d:
          print(f"It took {i + 1} tries to get a Piggin pet!")
      
