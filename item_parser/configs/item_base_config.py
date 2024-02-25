from item_parser.configs.affix_config import AffixConfig
from item_parser.constants import Operator
from item_parser.item import Item

class CustomIsValid:
  def LargeClusterSpellDamage(item: Item):
    mustHaveIncreasedEffectIfTwoPrefix = item.num_prefixes < 2 or (item.affixes.get("Potent") or item.affixes.get("Powerful")) and item.num_prefixes >= 2
    mustHaveOneT1MaxStrOrIntIfTwoSuffix = item.num_suffixes < 2 or (item.affixes.get("Bear") or item.affixes.get("Prodigy")) and item.num_suffixes >= 2
    mustNotHaveStrAndIntTogether = not ((item.affixes.get("Wrestler") or item.affixes.get("Bear")) and (item.affixes.get("Student") or item.affixes.get("Prodigy")))
    mustNotHaveStrAndES = not ((item.affixes.get("Glimmering") or item.affixes.get("Glowing")) and (item.affixes.get("Wrestler") or item.affixes.get("Bear")))
    mustNotHaveIntAndLife = not ((item.affixes.get("Healthy") or item.affixes.get("Sanguine")) and (item.affixes.get("Student") or item.affixes.get("Prodigy")))
    ret = bool(mustHaveIncreasedEffectIfTwoPrefix) and bool(mustNotHaveStrAndIntTogether) and bool(mustHaveOneT1MaxStrOrIntIfTwoSuffix) and bool(mustNotHaveIntAndLife)
    print(f"Passed custom LargeClusterSpellDamage test" if ret else f"Failed custom LargeClusterSpellDamage test")
    print(f"\tmustHaveIncreasedEffectIfTwoPrefix={bool(mustHaveIncreasedEffectIfTwoPrefix)}")
    print(f"\tmustNotHaveStrAndIntTogether={bool(mustNotHaveStrAndIntTogether)}")
    print(f"\tmustHaveOneT1MaxStrOrIntIfTwoSuffix={bool(mustHaveOneT1MaxStrOrIntIfTwoSuffix)}")
    print(f"\tmustNotHaveStrAndES={bool(mustNotHaveStrAndES)}")
    print(f"\tmustNotHaveIntAndLife={bool(mustNotHaveIntAndLife)}")
    return ret
  
  def LargeClusterBow(item: Item):
    mustHaveIncreasedEffectIfTwoPrefix = item.num_prefixes < 2 or (item.affixes.get("Potent") or item.affixes.get("Powerful")) and item.num_prefixes >= 2
    print(f"Passed custom LargeClusterBow test" if ret else f"Failed custom LargeClusterBow test")
    print(f"\tmustHaveIncreasedEffectIfTwoPrefix={bool(mustHaveIncreasedEffectIfTwoPrefix)}")
    ret = bool(mustHaveIncreasedEffectIfTwoPrefix)
    return ret
    
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
    "num_affixes_required": 2,
    "min_item_level": 84
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
    "num_affixes_required": 2,
    "min_item_level": 84
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
    "num_affixes_required": 2,
    "min_item_level": 84
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
      AffixConfig("Rainbow", [39], Operator.GE),
      AffixConfig("Impala", [59], Operator.GE),
      AffixConfig("Owl", [64], Operator.GE),
      AffixConfig("Cheetah", [13], Operator.GE),
      AffixConfig("Armadillo", [59], Operator.GE),
      AffixConfig("Bog Moss", [53], Operator.GE)
    ],
    "num_affixes_required": 2,
    "min_item_level": 84
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
    "num_affixes_required": 2,
    "min_item_level": 84
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
    "num_affixes_required": 1,
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
    "num_affixes_required": 2,
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
    "num_affixes_required": 1,
    "min_item_level": 76
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
    "num_affixes_required": 1,
    "min_item_level": 76
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
    "num_affixes_required": 1,
    "min_item_level": 76
  }

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
    "num_affixes_required": 1,
  }

  AdornedJewels = {
    "name": "Adorned Jewels", 
    "class": "Jewels",
    "prefixes": [
      AffixConfig("Arctic", [15], Operator.GE),             # Cold Crit Multi (15-18)
      AffixConfig("Surging", [15], Operator.GE),            # Lightning Crit Multi (15-18)
      AffixConfig("Infernal", [15], Operator.GE),           # Fire Crit Multi (15-18)
      AffixConfig("Puncturing", [15], Operator.GE),         # Dual Wield Crit Multi (15-18)
      AffixConfig("Piercing", [15], Operator.GE),           # One Handed Melee Crit Multi (15-18)
      AffixConfig("Rupturing", [15], Operator.GE),          # Two Handed Melee Crit Multi (15-18)

      AffixConfig("Vivid", [5], Operator.GE),               # Life (5-7)
      AffixConfig("Shimmering", [6], Operator.GE),          # ES (6-8)
      AffixConfig("Arming", [6], Operator.GE),              # Mine Throw Speed (6-8)
    ],
    "suffixes": [ 
      AffixConfig("Elements", [12], Operator.GE),           # Elemental Crit Multi (12-15)
      AffixConfig("Potency", [9], Operator.GE),             # Global Crit Multi (9-12)
      AffixConfig("Unmaking", [12], Operator.GE),           # Spell Crit Multi (12-15)
      AffixConfig("Demolishing", [12], Operator.GE),        # Melee Crit Multi (12-15)
      
      AffixConfig("Zealousness", [6], Operator.GE),         # Fire DoT Multi (6-8)
      # AffixConfig("Gelidity", [6], Operator.GE),            # Cold DoT Multi (6-8)
      # AffixConfig("Atrophy", [6], Operator.GE),             # Chaos DoT Multi (6-8)
      AffixConfig("Exsanguinating", [6], Operator.GE),      # Phys DoT Multi (6-8)

      # AffixConfig("Intelligence", [12], Operator.GE),       # Int (12-16)
      # AffixConfig("Strength", [12], Operator.GE),           # Str (12-16)
      # AffixConfig("Spirit", [8], Operator.GE),              # Int/Str (8-10)
      
    ],
    "num_affixes_required": 2,
  }

  SadistGarb = {
    "name": "Sadist Garb",
    "class": "Body Armours",
    "prefixes": [
    ],
    "suffixes": [
      # AffixConfig("Abjuration", None, Operator.ANY),
      AffixConfig("Nullification", [22], Operator.GE),
    ],
    "num_affixes_required": 1,
    "min_item_level": 86
  }

  # Large Cluster 12 Passives Spell Damage
  LargeClusterSpellDamage = {
    "name": "Large Cluster Jewel - Spell Damage",
    "class": "Jewels",
    "prefixes": [
      AffixConfig("Potent", None, Operator.ANY),          # T2 Effect
      AffixConfig("Powerful", None, Operator.ANY),        # T1 Effect

      AffixConfig("Healthy", None, Operator.ANY),         # T2 Life
      AffixConfig("Sanguine", None, Operator.ANY),        # T1 Life
      
      AffixConfig("Glimmering", None, Operator.ANY),      # T2 ES
      AffixConfig("Glowing", None, Operator.ANY),         # T1 ES

      AffixConfig("Hazardous", None, Operator.ANY),       # T2 % Damage
      AffixConfig("Dangerous", None, Operator.ANY),       # T1 % Damage
    ],
    "suffixes": [
      AffixConfig("Sky", None, Operator.ANY),             # T2 Attribute
      AffixConfig("Meteor", None, Operator.ANY),          # T1 Attribute

      # AffixConfig("Wrestler", None, Operator.ANY),        # T2 Str
      AffixConfig("Bear", None, Operator.ANY),            # T1 Str

      # AffixConfig("Student", None, Operator.ANY),         # T2 Int 
      AffixConfig("Prodigy", None, Operator.ANY),         # T1 Int 
    ],
    "custom_is_valid": CustomIsValid.LargeClusterSpellDamage,
    "num_affixes_required": 3,
    "min_item_level": 84
  }

  # Large Cluster 12 Passives Bow Damage
  LargeClusterBow = {
    "name": "Large Cluster Jewel - Bow Damage",
    "class": "Jewels",
    "prefixes": [
      AffixConfig("Potent", None, Operator.ANY),          # T2 Effect
      AffixConfig("Powerful", None, Operator.ANY),        # T1 Effect

      AffixConfig("Healthy", None, Operator.ANY),         # T2 Life
      AffixConfig("Sanguine", None, Operator.ANY),        # T1 Life
      
      AffixConfig("Hazardous", None, Operator.ANY),       # T2 % Damage
      AffixConfig("Dangerous", None, Operator.ANY),       # T1 % Damage
    ],
    "suffixes": [
      # AffixConfig("Sky", None, Operator.ANY),             # T2 Attribute
      # AffixConfig("Meteor", None, Operator.ANY),          # T1 Attribute

      # AffixConfig("Wrestler", None, Operator.ANY),        # T2 Str
      AffixConfig("Bear", None, Operator.ANY),            # T1 Str

      # AffixConfig("Student", None, Operator.ANY),         # T2 Int 
      AffixConfig("Prodigy", None, Operator.ANY),         # T1 Int 

      # AffixConfig("Lynx", None, Operator.ANY),            # T2 Dex 
      AffixConfig("Fox", None, Operator.ANY),             # T1 Dex

      AffixConfig("Ease", None, Operator.ANY),            # T2 Attack Speed 
      AffixConfig("Mastery", None, Operator.ANY),         # T1 Attack Speed
    ],
    "custom_is_valid": CustomIsValid.LargeClusterBow,
    "num_affixes_required": 3,
    "min_item_level": 84
  }

  def get_config_by_base_name(item: Item):
    ret = None
    item_base_name = item.base
    item_class = item.type
    item_level = item.ilvl
    item_rarity = item.rarity
    item_num_prefixes = item.num_prefixes
    item_num_suffixes = item.num_suffixes
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
    elif item_class == "Jewels" and "Large" in name_arr and "Cluster" in name_arr:
      if item.cluster_jewel_has("Bow"):
        ret = BaseItemConfig.LargeClusterBow
      else:
        ret = BaseItemConfig.LargeClusterSpellDamage
    elif item_class == "Jewels":
      ret = BaseItemConfig.AdornedJewels
    elif item_class == "Body Armours" and "Sadist" in name_arr:
      ret = BaseItemConfig.SadistGarb
    else:
      raise ValueError(f"Unknown base name: {item_base_name}")
    
    if ret.get("min_item_level") is not None and int(item_level) < ret.get("min_item_level"):
      raise ValueError(f"Item level too low: {item_level} < {ret.get('min_item_level')}")
    
    print(f"💡 Using \"{ret.get('name')}\" config for \
          \n\titem base =\"{item_base_name}\" \
          \n\titem class=\"{item_class}\" \
          \n\titem level=\"{item_level}\" \
          \n\titem rarity=\"{item_rarity}\" \
          \n\titem num_prefixes=\"{item_num_prefixes}\" \
          \n\titem num_suffixes=\"{item_num_suffixes}\"")
    return ret
  