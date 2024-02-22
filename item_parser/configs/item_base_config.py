from item_parser.configs.affix_config import AffixConfig
from item_parser.constants import Operator
from item_parser.item import Item

class BaseItemConfig:
  Jade = {
    "name": "Jade",
    "class": "Utility Flasks",
    "prefixes": [
      AffixConfig("Abecedarian", None, Operator.ANY),
      AffixConfig("Alchemist", None, Operator.ANY),
      AffixConfig("Dabbler", None, Operator.ANY)
    ],
    "suffixes": [
      AffixConfig("Rainbow", [40], Operator.GE),
      AffixConfig("Impala", [56], Operator.GE),
      # AffixConfig("Owl", [65], Operator.GE),
      # AffixConfig("Cheetah", [14], Operator.GE),
      # AffixConfig("Armadillo", [60], Operator.GE),
      AffixConfig("Bog Moss", [53], Operator.GE)
    ],
    "should_aug": True,
    "min_item_level": 85
  }

  Quicksilver = {
    "name": "Quicksilver",
    "class": "Utility Flasks",
    "prefixes": [
      AffixConfig("Abecedarian", None, Operator.ANY),
      AffixConfig("Alchemist", None, Operator.ANY),
      AffixConfig("Dabbler", None, Operator.ANY)
    ],
    "suffixes": [
      AffixConfig("Rainbow", [40], Operator.GE),
      # AffixConfig("Impala", [60], Operator.GE),
      # AffixConfig("Owl", [64], Operator.GE),
      AffixConfig("Cheetah", [12], Operator.GE),
      # AffixConfig("Armadillo", [60], Operator.GE),
      AffixConfig("Bog Moss", [53], Operator.GE)
    ],
    "should_aug": True,
    "min_item_level": 85
  }

  Granite = {
    "name": "Granite",
    "class": "Utility Flasks",
    "prefixes": [
      AffixConfig("Abecedarian", None, Operator.ANY),
      AffixConfig("Alchemist", None, Operator.ANY),
      AffixConfig("Dabbler", None, Operator.ANY)
    ],
    "suffixes": [
      AffixConfig("Rainbow", [40], Operator.GE),
      AffixConfig("Impala", [60], Operator.GE),
      # AffixConfig("Owl", [65], Operator.GE),
      # AffixConfig("Cheetah", [14], Operator.GE),
      AffixConfig("Armadillo", [56], Operator.GE),
      AffixConfig("Bog Moss", [53], Operator.GE)
    ],
    "should_aug": True,
    "min_item_level": 85
  }

  Silver = {
    "name": "Silver",
    "class": "Utility Flasks",
    "prefixes": [
      AffixConfig("Abecedarian", None, Operator.ANY),
      AffixConfig("Alchemist", None, Operator.ANY),
      AffixConfig("Dabbler", None, Operator.ANY)
    ],
    "suffixes": [
      AffixConfig("Rainbow", [40], Operator.GE),
      AffixConfig("Impala", [60], Operator.GE),
      AffixConfig("Owl", [65], Operator.GE),
      AffixConfig("Cheetah", [14], Operator.GE),
      AffixConfig("Armadillo", [60], Operator.GE),
      AffixConfig("Bog Moss", [53], Operator.GE)
    ],
    "should_aug": True,
    "min_item_level": 85
  }


  ElementalFlask = {
    "name": "Elemental Flask",
    "class": "Utility Flasks",
    "prefixes": [
      AffixConfig("Abecedarian", None, Operator.ANY),
      AffixConfig("Alchemist", None, Operator.ANY),
      AffixConfig("Dabbler", None, Operator.ANY)
    ],
    "suffixes": [
      AffixConfig("Rainbow", [39], Operator.GE),
      AffixConfig("Impala", [59], Operator.GE),
      AffixConfig("Owl", [63], Operator.GE),
      AffixConfig("Cheetah", [12], Operator.GE),
      AffixConfig("Armadillo", [59], Operator.GE),
      AffixConfig("Bog Moss", [52], Operator.GE)
    ],
    "should_aug": True
  }

  SpineBow = {
    "name": "Spine Bow",
    "class": "Bows",
    "prefixes": [
    ],
    "suffixes": [
      AffixConfig("Many", None, Operator.ANY)
      # AffixConfig("Many", [2], Operator.GE),
    ],
    "should_aug": True,
    "min_item_level": 86
  }

  Amulet = {
    "name": "Amulet",
    "class": "Amulets",
    "prefixes": [
      AffixConfig("Exalter", None, Operator.ANY),
      # AffixConfig("Vulcanist", None, Operator.ANY),
    ],
    "suffixes": [
      AffixConfig("Dissolution", None, Operator.ANY),
      AffixConfig("Destruction", None, Operator.ANY)
    ],
    "should_aug": True
  }

  # Hunter Tailwind
  Boots = {
    "name": "Boots",
    "class": "Boots",
    "prefixes": [
    ],
    "suffixes": [
      AffixConfig("Hunt", [None, 8], Operator.GE), # For tailwind
    ],
    "should_aug": False
  }

  # Warlord +1 Frenzy
  Gloves = {
    "name": "Gloves",
    "class": "Gloves",
    "prefixes": [
      AffixConfig("Warlord", [1], Operator.EQ),
    ],
    "suffixes": [
    ],
    "should_aug": False
  }

  # Warlord +1 Power
  Helmet = {
    "name": "Helmet",
    "class": "Helmets",
    "prefixes": [
      AffixConfig("Warlord", [1], Operator.EQ),
    ],
    "suffixes": [
    ],
    "should_aug": False
  }

  # Large Cluster 12 Passives Spell Damage: Can go for str,attribute,effect,life or int,attribute,effect,energy shield (both can also use % increased damage)
  # Wand Elder/Hunter
  Wand = {
    "name": "Wand",
    "class": "Wands",
    "prefixes": [
      AffixConfig("The Elder", [1, 16], Operator.EQ),
      AffixConfig("The Shaper", [1, 5, 10], Operator.GE),
      AffixConfig("Hunter", [1, 16], Operator.EQ),
      AffixConfig("Hunter", [1, 5, 10], Operator.GE),
    ],
    "suffixes": [ 
    ],
    "should_aug": False
  }


  def get_config_by_base_name(item: Item):
    ret = None
    item_base_name = item.item_base
    item_class = item.item_class
    item_level = item.item_level
    name_arr = item_base_name.split()

    if item_class == "Utility Flasks" and "Jade" in name_arr:
      ret = BaseItemConfig.Jade
    elif item_class == "Utility Flasks" and "Quicksilver" in name_arr:
      ret = BaseItemConfig.Quicksilver
    elif item_class == "Utility Flasks" and "Granite" in name_arr:
      ret = BaseItemConfig.Granite
    elif item_class == "Utility Flasks" and "Silver" in name_arr:
      ret = BaseItemConfig.Silver
    elif item_class == "Utility Flasks" and ("Ruby" in name_arr or "Topaz" in name_arr or "Sapphire" in name_arr):
      ret = BaseItemConfig.ElementalFlask
    elif item_class == "Bows" and "Spine" in name_arr:
      ret = BaseItemConfig.SpineBow
    elif item_class == "Amulets" and "Amulet" in name_arr:
      ret = BaseItemConfig.Amulet
    elif item_class == "Boots":
      ret = BaseItemConfig.Boots
    elif item_class == "Gloves":
      ret = BaseItemConfig.Gloves
    elif item_class == "Helmets":
      ret = BaseItemConfig.Helmet
    elif item_class == "Wands":
      ret = BaseItemConfig.Wand
    else:
      raise ValueError(f"Unknown base name: {item_base_name}")
    
    if ret.get("min_item_level") is not None and int(item_level) < ret.get("min_item_level"):
      raise ValueError(f"Item level too low: {item_level} < {ret.get('min_item_level')}")
    
    print(f"💡 Using \"{ret.get('name')}\" config for \n\tbase name=\"{item_base_name}\" \n\tbase class=\"{item_class}\" \n\titem level=\"{item_level}\"")
    return ret
  