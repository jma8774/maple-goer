from item_parser.configs.affix_config import AffixConfig, ExtraStringConfig
from item_parser.constants import Operator
from item_parser.item import Item
from typing import TypedDict, Callable

class Config(TypedDict):
  name: str
  prefixes: list[AffixConfig]
  suffixes: list[AffixConfig]
  num_affixes_required: int
  min_item_level: int | None
  custom_should_exalt: Callable[[Item], bool] | None
  custom_is_valid: Callable[[Item], bool] | None 
  custom_is_valid_pre: Callable[[Item], bool] | None

class CustomIsValidPre:
  def LeagueStartFlasks(item: Item) -> bool:
    # If has bad prefix, return false
    if item.affixes.get("Doled") or \
      item.affixes.get("Provisioned") or \
      item.affixes.get("Measured") or \
      item.affixes.get("Allocated") or \
      item.affixes.get("Rationed"):
      return False
    
    if "Granite Flask" in item.base and item.affixes.get("Armadillo"):
      return True
    
    if "Jade Flask" in item.base and item.affixes.get("Impala"):
      return True
      
    return item.affixes.get("Cheetah")
  
class CustomIsValid:
  def LargeClusterSpellDamage(item: Item) -> bool:
    # If we have 4 tier 1 affixes, we don't need to check anything else
    t1_affixes = {"Powerful", "Sanguine", "Glowing", "Bear", "Prodigy", "Meteor", "Dangerous"}
    if len([a for a in t1_affixes if item.affixes.get(a)]) >= 4:
      print(f"[✅] Passed T1 LargeClusterSpellDamage validation test")
      return True
    
    mustHave3GoodAffixes = ConfigsModule.good_prefixes(item, ConfigsModule.LargeClusterSpellDamage) + ConfigsModule.good_suffixes(item, ConfigsModule.LargeClusterSpellDamage) >= 3
    mustHaveIncreasedEffectIfTwoPrefix = item.num_prefixes < 2 or (item.affixes.get("Potent") or item.affixes.get("Powerful"))
    mustHaveOneT1MaxStrOrIntIfTwoSuffix = item.num_suffixes < 2 or (item.affixes.get("Bear") or item.affixes.get("Prodigy"))
    mustHaveT1EverythingIf25Effect = not item.affixes.get("Potent") or (item.affixes.get("Potent") and (item.affixes.get("Bear") or item.affixes.get("Prodigy")) and item.affixes.get("Meteor"))
    mustNotHaveStrAndIntTogether = not ((item.affixes.get("Wrestler") or item.affixes.get("Bear")) and (item.affixes.get("Student") or item.affixes.get("Prodigy")))
    mustNotHaveStrAndES = not ((item.affixes.get("Glimmering") or item.affixes.get("Glowing")) and (item.affixes.get("Wrestler") or item.affixes.get("Bear")))
    mustNotHaveIntAndLife = not ((item.affixes.get("Healthy") or item.affixes.get("Sanguine")) and (item.affixes.get("Student") or item.affixes.get("Prodigy")))
    mustNotHaveNotable = not (item.affixes.get("Notable") or item.affixes.get("Significance"))
    validFor3Affixes = bool(mustHave3GoodAffixes) and bool(mustHaveIncreasedEffectIfTwoPrefix) and bool(mustNotHaveStrAndIntTogether) and bool(mustHaveOneT1MaxStrOrIntIfTwoSuffix) and bool(mustNotHaveIntAndLife) and bool(mustNotHaveStrAndES) and bool(mustNotHaveNotable) and bool(mustHaveT1EverythingIf25Effect)
    print(f"[✅] Passed custom LargeClusterSpellDamage validation test" if validFor3Affixes else f"[❌] Failed custom LargeClusterSpellDamage validation test")
    print(f"\tmustHave3GoodAffixes={bool(mustHave3GoodAffixes)}")
    print(f"\tmustHaveIncreasedEffectIfTwoPrefix={bool(mustHaveIncreasedEffectIfTwoPrefix)}")
    print(f"\tmustHaveT1EverythingIf25Effect={bool(mustHaveT1EverythingIf25Effect)}")
    print(f"\tmustNotHaveStrAndIntTogether={bool(mustNotHaveStrAndIntTogether)}")
    print(f"\tmustHaveOneT1MaxStrOrIntIfTwoSuffix={bool(mustHaveOneT1MaxStrOrIntIfTwoSuffix)}")
    print(f"\tmustNotHaveStrAndES={bool(mustNotHaveStrAndES)}")
    print(f"\tmustNotHaveIntAndLife={bool(mustNotHaveIntAndLife)}")
    print(f"\tmustNotHaveNotable={bool(mustNotHaveNotable)}")

    # This will be the final check after exalting
    validFor4Affixes = True # Will always be true if we have less than 4 affixes

    return validFor3Affixes and validFor4Affixes

  def LargeClusterBow(item: Item) -> bool:
    # If we have 4 tier 1 affixes, we don't need to check anything else
    t1_affixes = {"Powerful", "Bear", "Prodigy", "Dangerous", "Fox", "Penguin", "Eviction", "Kaleidoscope"}
    if len([a for a in t1_affixes if item.affixes.get(a)]) >= 4:
      print(f"[✅] Passed T1 LargeClusterBow validation test")
      return True
    
    mustHave3GoodAffixes = ConfigsModule.good_prefixes(item, ConfigsModule.LargeClusterBow12) + ConfigsModule.good_suffixes(item, ConfigsModule.LargeClusterBow12) >= 3
    mustHaveIncreasedEffectIfTwoPrefix = item.num_prefixes < 2 or (item.affixes.get("Potent") or item.affixes.get("Powerful"))
    mustHaveLifeOrDamageIfTwoPrefix = item.num_prefixes < 2 or (item.affixes.get("Healthy") or item.affixes.get("Sanguine") or item.affixes.get("Hazardous") or item.affixes.get("Dangerous"))
    mustHaveAtLeast1GoodSuffixIfTwoSuffix = item.num_suffixes < 2 or (item.affixes.get("Ease") or item.affixes.get("Mastery"))
    mustNotHaveNotable = not (item.affixes.get("Notable") or item.affixes.get("Significance"))
    ret = bool(mustHaveIncreasedEffectIfTwoPrefix) and bool(mustHave3GoodAffixes) and bool(mustNotHaveNotable) and bool(mustHaveAtLeast1GoodSuffixIfTwoSuffix) and bool(mustHaveLifeOrDamageIfTwoPrefix)
    print(f"[✅] Passed custom LargeClusterBow validation test" if ret else f"[❌] Failed custom LargeClusterBow validation test")
    print(f"\tmustHaveIncreasedEffectIfTwoPrefix={bool(mustHaveIncreasedEffectIfTwoPrefix)}")
    print(f"\tmustHaveLifeOrDamageIfTwoPrefix={bool(mustHaveLifeOrDamageIfTwoPrefix)}")
    print(f"\tmustHave3GoodAffixes={bool(mustHave3GoodAffixes)}")
    print(f"\tmustNotHaveNotable={bool(mustNotHaveNotable)}")
    print(f"\tmustHaveAtLeast1GoodSuffixIfTwoSuffix={bool(mustHaveAtLeast1GoodSuffixIfTwoSuffix)}")
    return ret
  
  def LargeClusterMinion(item: Item) -> bool:
    mustHave3GoodAffixes = ConfigsModule.good_prefixes(item, ConfigsModule.LargeClusterMinion) + ConfigsModule.good_suffixes(item, ConfigsModule.LargeClusterMinion) >= 3
    mustHaveMinionAttackSpeed = item.affixes.get("Ravaging") or item.affixes.get("Razing")
    mustHaveIncreasedEffect = item.affixes.get("Powerful") or item.affixes.get("Potent")
    mustNotHaveNotable = not (item.affixes.get("Notable") or item.affixes.get("Significance"))
    ret = bool(mustHave3GoodAffixes) and bool(mustHaveMinionAttackSpeed) and bool(mustHaveIncreasedEffect) and bool(mustNotHaveNotable)
    print(f"[✅] Passed custom LargeClusterMinion validation test" if ret else f"[❌] Failed custom LargeClusterMinion validation test")
    print(f"\tmustHave3GoodAffixes={bool(mustHave3GoodAffixes)}")
    print(f"\tmustHaveMinionAttackSpeed={bool(mustHaveMinionAttackSpeed)}")
    print(f"\tmustHaveIncreasedEffect={bool(mustHaveIncreasedEffect)}")
    print(f"\tmustNotHaveNotable={bool(mustNotHaveNotable)}")
    return ret
  
  def AdornedJewels(item: Item) -> bool:
    mustHaveLifeIfFireDoTMulti = not item.affixes.get("Zealousness") or (item.affixes.get("Zealousness") and item.affixes.get("Vivid"))
    mustHaveMineSpeedIfGlobalCrit = not item.affixes.get("Potency") or (item.affixes.get("Potency") and item.affixes.get("Arming"))
    mustHaveLifeIfChaosDoTMulti = not item.affixes.get("Atrophy") or (item.affixes.get("Atrophy") and item.affixes.get("Vivid"))
    mustHaveLifeIfChaosDamage = not item.affixes.get("Chaotic") or (item.affixes.get("Chaotic") and item.affixes.get("Vivid"))
    mustHaveLifeIfDot = not item.affixes.get("Entropy") or (item.affixes.get("Entropy") and item.affixes.get("Vivid"))
    mustHaveLifeIfArea = not item.affixes.get("Blasting") or (item.affixes.get("Blasting") and item.affixes.get("Vivid"))
    mustHaveLifeIfProj = not item.affixes.get("Archery") or (item.affixes.get("Archery") and item.affixes.get("Vivid"))
    ret = bool(mustHaveLifeIfFireDoTMulti) and bool(mustHaveMineSpeedIfGlobalCrit) and bool(mustHaveLifeIfChaosDoTMulti) and bool(mustHaveLifeIfChaosDamage) and bool(mustHaveLifeIfDot) and bool(mustHaveLifeIfArea) and bool(mustHaveLifeIfProj)
    print(f"[✅] Passed custom AdornedJewels validation test" if ret else f"[❌] Failed custom AdornedJewels validation test")
    print(f"\tmustHaveLifeIfFireDoTMulti={bool(mustHaveLifeIfFireDoTMulti)}")
    print(f"\tmustHaveMineSpeedIfGlobalCrit={bool(mustHaveMineSpeedIfGlobalCrit)}")
    print(f"\tmustHaveLifeIfChaosDoTMulti={bool(mustHaveLifeIfChaosDoTMulti)}")
    print(f"\tmustHaveLifeIfChaosDamage={bool(mustHaveLifeIfChaosDamage)}")
    print(f"\tmustHaveLifeIfDot={bool(mustHaveLifeIfDot)}")
    return ret
  
  def Maps(item: Item) -> bool:
    mustNotHaveInsulation = not item.affixes.get("Insulation")
    mustNotHaveExposure = not item.affixes.get("Exposure")
    mustNotHaveSmothering = not item.affixes.get("Smothering")
    mustNotHaveStasis = not item.affixes.get("Stasis")
    ret = bool(mustNotHaveInsulation) and bool(mustNotHaveExposure) and bool(mustNotHaveSmothering) and bool(mustNotHaveStasis)
    print(f"[✅] Passed custom Maps validation test" if ret else f"[❌] Failed custom Maps validation test")
    print(f"\tmustNotHaveInsulation={bool(mustNotHaveInsulation)}")
    print(f"\tmustNotHaveExposure={bool(mustNotHaveExposure)}")
    print(f"\tmustNotHaveSmothering={bool(mustNotHaveSmothering)}")
    print(f"\tmustNotHaveStasis={bool(mustNotHaveStasis)}")
    return ret
  
  def LeagueStartFlasks(item: Item) -> bool:
    mustHaveEffectIfBogMoss = not item.affixes.get("Bog Moss") or (item.affixes.get("Bog Moss") and (item.affixes.get("Abecedarian") or item.affixes.get("Alchemist") or item.affixes.get("Dabbler")))
    mustHaveEffectIfRainbow = not item.affixes.get("Rainbow") or (item.affixes.get("Rainbow") and (item.affixes.get("Abecedarian") or item.affixes.get("Alchemist") or item.affixes.get("Dabbler")))
    ret = bool(mustHaveEffectIfBogMoss) and bool(mustHaveEffectIfRainbow)
    return ret
  
class CustomShouldExalt:
  def LargeClusterSpellDamage(item: Item) -> bool:
    # If we have t1 int/str, t1 attribute, and t1 effect (don't exalt) the last slot
    if (item.affixes.get("Bear") or item.affixes.get("Prodigy")) and item.affixes.get("Meteor") and item.affixes.get("Powerful"):
      return False
    return CustomIsValid.LargeClusterSpellDamage(item)
  
  def LargeClusterBow(item: Item) -> bool:
    return CustomIsValid.LargeClusterBow(item)
  
  def LargeClusterMinion(item: Item) -> bool:
    return CustomIsValid.LargeClusterMinion(item)
    
class CustomShouldRegal:
  def LargeClusterSpellDamage(item: Item) -> bool:
    mustHave2GoodAffixes = ConfigsModule.good_prefixes(item, ConfigsModule.LargeClusterSpellDamage) + ConfigsModule.good_suffixes(item, ConfigsModule.LargeClusterSpellDamage) >= 2
    mustHaveOneImportantAffix = item.affixes.get("Powerful") or item.affixes.get("Potent") or item.affixes.get("Meteor") or item.affixes.get("Bear") or item.affixes.get("Prodigy")
    mustNotHaveStrAndES = not ((item.affixes.get("Glimmering") or item.affixes.get("Glowing")) and (item.affixes.get("Wrestler") or item.affixes.get("Bear")))
    mustNotHaveIntAndLife = not ((item.affixes.get("Healthy") or item.affixes.get("Sanguine")) and (item.affixes.get("Student") or item.affixes.get("Prodigy")))
    ret = bool(mustHave2GoodAffixes) and bool(mustNotHaveStrAndES) and bool(mustNotHaveIntAndLife) and bool(mustHaveOneImportantAffix)
    # print(f"[✅] Passed custom LargeClusterSpellDamage regal test" if ret else f"[❌] Failed custom LargeClusterSpellDamage regal test")
    # print(f"\tmustHave2GoodAffixes={bool(mustHave2GoodAffixes)}")
    # print(f"\tmustNotHaveStrAndES={bool(mustNotHaveStrAndES)}")
    # print(f"\tmustNotHaveIntAndLife={bool(mustNotHaveIntAndLife)}")
    # print(f"\tmustHaveOneImportantAffix={bool(mustHaveOneImportantAffix)}")
    return ret
  
  def LargeClusterBow(item: Item) -> bool:
    mustHave2GoodAffixes = ConfigsModule.good_prefixes(item, ConfigsModule.LargeClusterBow12) + ConfigsModule.good_suffixes(item, ConfigsModule.LargeClusterBow12) >= 2
    mustHaveEffectOrAttackSpeed = item.affixes.get("Powerful") or item.affixes.get("Potent") or item.affixes.get("Ease") or item.affixes.get("Mastery") or item.affixes.get("Dangerous")
    ret = bool(mustHave2GoodAffixes) and bool(mustHaveEffectOrAttackSpeed)
    return ret
  
  def LargeClusterMinion(item: Item) -> bool:
    mustHave2GoodAffixes = ConfigsModule.good_prefixes(item, ConfigsModule.LargeClusterMinion) + ConfigsModule.good_suffixes(item, ConfigsModule.LargeClusterMinion) >= 2
    mustHaveEffectOrAttackSpeed = item.affixes.get("Powerful") or item.affixes.get("Potent") or item.affixes.get("Ravaging") or item.affixes.get("Razing")
    ret = bool(mustHave2GoodAffixes) and bool(mustHaveEffectOrAttackSpeed)
    return ret
  
class ConfigsModule:
  def good_prefixes(item: Item, item_config: Config):
    good_prefixes = item_config.get("prefixes")
    if len(good_prefixes) == 0:
      return 0
    num_good = 0
    for p in good_prefixes:
      if p._operator == Operator.PASS:
        return item.num_prefixes
      if item.affixes.get(p._affix_name) and p.pass_check(item.affixes.get(p._affix_name)):
        num_good += 1
    return num_good

  def good_suffixes(item: Item, item_config: Config):
    good_suffixes= item_config.get("suffixes")
    if len(good_suffixes) == 0:
      return 0
    num_good = 0
    for s in good_suffixes:
      if s._operator == Operator.PASS:
        return item.num_suffixes
      if item.affixes.get(s._affix_name) and s.pass_check(item.affixes.get(s._affix_name)):
        num_good += 1
    return num_good 

  Jade: Config = {
    "name": "Jade",
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

  Quicksilver: Config = {
    "name": "Quicksilver",
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
      AffixConfig("Bog Moss", [53], Operator.GE),
    ],
    "num_affixes_required": 2,
    "min_item_level": 84
  }

  Granite: Config = {
    "name": "Granite",
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

  Silver: Config = {
    "name": "Silver",
    "prefixes": [
      AffixConfig("Abecedarian", None, Operator.ANY),
      AffixConfig("Alchemist", None, Operator.ANY),
      AffixConfig("Dabbler", None, Operator.ANY)
    ],
    "suffixes": [
      AffixConfig("Rainbow", [39], Operator.GE),
      AffixConfig("Impala", [60], Operator.GE),
      AffixConfig("Owl", [64], Operator.GE),
      AffixConfig("Cheetah", [13], Operator.GE),
      AffixConfig("Armadillo", [60], Operator.GE),
      AffixConfig("Bog Moss", [53], Operator.GE)
    ],
    "num_affixes_required": 2,
    "min_item_level": 84
  }

  OtherFlask: Config = {
    "name": "Other Flask",
    "prefixes": [
      AffixConfig("Abecedarian", None, Operator.ANY),
      AffixConfig("Alchemist", None, Operator.ANY),
      AffixConfig("Dabbler", None, Operator.ANY)
    ],
    "suffixes": [
      AffixConfig("Rainbow", [39], Operator.GE),
      AffixConfig("Impala", [60], Operator.GE),
      AffixConfig("Owl", [64], Operator.GE),
      AffixConfig("Cheetah", [13], Operator.GE),
      AffixConfig("Armadillo", [60], Operator.GE),
      AffixConfig("Bog Moss", [53], Operator.GE),
    ],
    "num_affixes_required": 2,
    "min_item_level": 84
  }

  LeagueStartFlasks: Config = {
    "name": "League Start Flasks",
    "prefixes": [
      AffixConfig("Abecedarian", None, Operator.ANY),
      AffixConfig("Alchemist", None, Operator.ANY),
      AffixConfig("Dabbler", None, Operator.ANY),

      # Charge Recovery
      # AffixConfig("Continuous", None, Operator.ANY),
      # AffixConfig("Endless", None, Operator.ANY),
      # AffixConfig("Bottomless", None, Operator.ANY),
      AffixConfig("Perpetual", None, Operator.ANY),

      # Reduced Charges Used
      # AffixConfig("Practitioner", None, Operator.ANY),
      # AffixConfig("Brewer", None, Operator.ANY),
      AffixConfig("Chemist", None, Operator.ANY),

      # Increased Duration
      # AffixConfig("Examiner", None, Operator.ANY),
      # AffixConfig("Clinician", None, Operator.ANY),
      # AffixConfig("Experimenter", None, Operator.ANY),

      # Max Chargrs
      # AffixConfig("Ample", None, Operator.ANY),

      # Critical Strike Charge Gain
      # AffixConfig("Specialist", None, Operator.ANY),
      AffixConfig("Surgeon", None, Operator.ANY),

      # Charge on Hit
      AffixConfig("Flagellant", None, Operator.ANY),
      # AffixConfig("Masochist", None, Operator.ANY), # 2 charge on hit
    ],
    "suffixes": [
      AffixConfig("Rainbow", None, Operator.ANY),
      AffixConfig("Impala", None, Operator.ANY),
      AffixConfig("Owl", None, Operator.ANY),
      AffixConfig("Cheetah", None, Operator.ANY),
      AffixConfig("Armadillo", None, Operator.ANY),
      AffixConfig("Bog Moss", None, Operator.ANY),
      AffixConfig("Dove", None, Operator.ANY),
      # AffixConfig("Tenaciousness", None, Operator.ANY),
    ],
    "num_affixes_required": 2,
    "min_item_level": 84,
    "custom_is_valid_pre": CustomIsValidPre.LeagueStartFlasks,
    "custom_is_valid": CustomIsValid.LeagueStartFlasks
  }

  SpineBow: Config = {
    "name": "Spine Bow",
    "prefixes": [
    ],
    "suffixes": [
      AffixConfig("Many", None, Operator.ANY)
      # AffixConfig("Many", [2], Operator.GE),
    ],
    "num_affixes_required": 1,
    "min_item_level": 86
  }

  Quiver: Config = {
    "name": "Quiver",
    "prefixes": [
      AffixConfig(None, None, Operator.PASS),
    ],
    "suffixes": [
      AffixConfig("Dissolution", None, Operator.ANY),
      # AffixConfig("Melting", None, Operator.ANY),
    ],
    "num_affixes_required": 2,
    "min_item_level": 82
  }

  Amulet: Config = {
    "name": "Fractured Amulet",
    "prefixes": [
      AffixConfig("Exalter", None, Operator.ANY),
      # AffixConfig("Vulcanist", None, Operator.ANY),
    ],
    "suffixes": [
      AffixConfig("Dissolution", None, Operator.ANY),
      AffixConfig("Destruction", None, Operator.ANY),
      AffixConfig("Melting", None, Operator.ANY)
    ],
    "num_affixes_required": 2,
  }

  FocusedAmulet: Config = {
    "name": "Focused Amulet",
    "prefixes": [
      AffixConfig("Exalter", None, Operator.ANY),
    ],
    "suffixes": [
    ],
    "num_affixes_required": 1,
  }

  # Amulet: Config = {
  #   "name": "Shaper Amulet",
  #   "prefixes": [
  #     # AffixConfig("Exalter", None, Operator.ANY),
  #     # AffixConfig("Vulcanist", None, Operator.ANY),
  #   ],
  #   "suffixes": [
  #     AffixConfig("Shaping", [6], Operator.GE, [
  #       ExtraStringConfig("butes", Operator.ENDS_WITH)
  #     ]),
  #   ],
  #   "num_affixes_required": 1,
  # }

  # Hunter Tailwind
  Boots: Config = {
    "name": "Boots",
    "prefixes": [
    ],
    "suffixes": [
      AffixConfig("Hunt", [None, 8], Operator.GE), # For tailwind
    ],
    "num_affixes_required": 1,
    "min_item_level": 76
  }

  # Warlord +1 Frenzy
  Gloves: Config = {
    "name": "Gloves",
    "prefixes": [
      AffixConfig("Warlord", [1], Operator.EQ),
    ],
    "suffixes": [
    ],
    "num_affixes_required": 1,
    "min_item_level": 76
  }

  # Warlord +1 Power
  Helmet: Config = {
    "name": "Helmet",
    "prefixes": [
      AffixConfig("Warlord", [1], Operator.EQ),
    ],
    "suffixes": [
    ],
    "num_affixes_required": 1,
    "min_item_level": 76
  }

  # Wand Elder/Hunter
  Wand: Config = {
    "name": "Wand",
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

  AdornedJewels: Config = {
    "name": "Adorned Jewels", 
    "prefixes": [
      AffixConfig("Arctic", [15], Operator.GE),             # Cold Crit Multi (15-18)
      # AffixConfig("Surging", [15], Operator.GE),            # Lightning Crit Multi (15-18)
      # AffixConfig("Infernal", [15], Operator.GE),           # Fire Crit Multi (15-18)
      # AffixConfig("Puncturing", [15], Operator.GE),         # Dual Wield Crit Multi (15-18)
      # AffixConfig("Piercing", [15], Operator.GE),           # One Handed Melee Crit Multi (15-18)
      # AffixConfig("Rupturing", [15], Operator.GE),          # Two Handed Melee Crit Multi (15-18)

      # AffixConfig("Vivid", [5], Operator.GE),               # Life (5-7)
      AffixConfig("Vivid", [7], Operator.GE),               # Life (5-7)
      # AffixConfig("Shimmering", [6], Operator.GE),          # ES (6-8)
      AffixConfig("Arming", [6], Operator.GE),              # Mine Throw Speed (6-8)
    ],
    "suffixes": [ 
      AffixConfig("Elements", [12], Operator.GE),           # Elemental Crit Multi (12-15)
      AffixConfig("Potency", [9], Operator.GE),             # Global Crit Multi (9-12)
      AffixConfig("Unmaking", [12], Operator.GE),           # Spell Crit Multi (12-15)
      # AffixConfig("Demolishing", [12], Operator.GE),        # Melee Crit Multi (12-15)
      
      AffixConfig("Zealousness", [6], Operator.GE),         # Fire DoT Multi (6-8)
      # AffixConfig("Combusting", [16], Operator.GE),          # Burning Damage
      # AffixConfig("Raiding", [None], Operator.ANY),          # Rarity
      # AffixConfig("Order", [None], Operator.ANY),            # Chaos Res
      # AffixConfig("Gelidity", [6], Operator.GE),            # Cold DoT Multi (6-8)
      AffixConfig("Atrophy", [6], Operator.GE),             # Chaos DoT Multi (6-8)
      AffixConfig("Entropy", [12], Operator.GE),             # Inc Damage Over Time
      AffixConfig("Blasting", [12], Operator.GE),             # Area Damage
      AffixConfig("Archery", [12], Operator.GE),             # Projectile Damage
      AffixConfig("Chaotic", [12], Operator.GE),             # Chaos Damage
      # AffixConfig("Exsanguinating", [6], Operator.GE),      # Phys DoT Multi (6-8)

      # AffixConfig("Intelligence", [12], Operator.GE),       # Int (12-16)
      # AffixConfig("Strength", [12], Operator.GE),           # Str (12-16)
      # AffixConfig("Spirit", [8], Operator.GE),              # Int/Str (8-10)

    ],
    "num_affixes_required": 2,
    "custom_is_valid": CustomIsValid.AdornedJewels,
  }

  # AdornedJewels: Config = {
  #   "name": "Adorned Jewels", 
  #   "prefixes": [
  #     AffixConfig("Vivid", [5], Operator.GE),               # Life (5-7)
  #   ],
  #   "suffixes": [ 
  #     # AffixConfig("Raiding", [None], Operator.ANY),          # Rarity
  #     # AffixConfig("Order", [None], Operator.ANY),            # Chaos Res
  #     AffixConfig("Zealousness", [6], Operator.GE),          # Fire DoT Multi (6-8)
  #     # AffixConfig("Infusion", [None], Operator.ANY),          # Recoup
  #     AffixConfig("Combusting", [16], Operator.GE),          # Burning Damage
  #   ],
  #   "num_affixes_required": 2,
  #   "custom_is_valid": CustomIsValid.AdornedJewels,
  # }

  AbyssJewel: Config = {
    "name": "Abyss Jewels", 
    "prefixes": [
      AffixConfig("Sanguine", [None], Operator.ANY),
      AffixConfig("Stalwart", [None], Operator.ANY),
      AffixConfig("Deleterious", [None], Operator.ANY),
    ],
    "suffixes": [ 
      AffixConfig("Lightning Rod", [None], Operator.ANY),
    ],
    "num_affixes_required": 2,
  }

  SadistGarb: Config = {
    "name": "Sadist Garb",
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
  LargeClusterSpellDamage: Config = {
    "name": "Large Cluster Jewel - Spell Damage",
    "prefixes": [
      AffixConfig("Potent", None, Operator.ANY),          # T2 Effect
      AffixConfig("Powerful", None, Operator.ANY),        # T1 Effect

      AffixConfig("Healthy", None, Operator.ANY),         # T2 Life
      AffixConfig("Sanguine", None, Operator.ANY),        # T1 Life
      
      AffixConfig("Glimmering", None, Operator.ANY),      # T2 ES
      AffixConfig("Glowing", None, Operator.ANY),         # T1 ES

      # AffixConfig("Hazardous", None, Operator.ANY),       # T2 % Damage
      AffixConfig("Dangerous", None, Operator.ANY),       # T1 % Damage
    ],
    "suffixes": [
      AffixConfig("Sky", None, Operator.ANY),             # T2 Attribute
      AffixConfig("Meteor", None, Operator.ANY),          # T1 Attribute

      # AffixConfig("Wrestler", None, Operator.ANY),        # T2 Str
      AffixConfig("Bear", None, Operator.ANY),            # T1 Str

      # AffixConfig("Student", None, Operator.ANY),         # T2 Int 
      AffixConfig("Prodigy", None, Operator.ANY),         # T1 Int 

      # AffixConfig("Drake", None, Operator.ANY),           # T1 Fire Res 
      # AffixConfig("Penguin", None, Operator.ANY),         # T1 Cold Res
      # AffixConfig("Storm", None, Operator.ANY),           # T1 Lightning Res
      # AffixConfig("Eviction", None, Operator.ANY),        # T1 Chaos Res
      # AffixConfig("Kaleidoscope", None, Operator.ANY),    # T1 All Ele Res

    ],
    "custom_should_regal": CustomShouldRegal.LargeClusterSpellDamage,
    "custom_should_exalt": CustomShouldExalt.LargeClusterSpellDamage, # We are exalting but leaving num_affixes_required as 3 because the 4th one is not strict
    "custom_is_valid": CustomIsValid.LargeClusterSpellDamage,
    "num_affixes_required": 3,
    "min_item_level": 84
  }

  # Large Cluster 12 Passives Bow Damage
  LargeClusterBow12: Config = {
    "name": "Large Cluster Jewel - Bow Damage 12",
    "prefixes": [
      # AffixConfig("Potent", None, Operator.ANY),          # T2 Effect
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

      # AffixConfig("Ease", None, Operator.ANY),            # T2 Attack Speed 
      AffixConfig("Mastery", None, Operator.ANY),         # T1 Attack Speed

      # AffixConfig("Drake", None, Operator.ANY),           # T1 Fire Res 
      AffixConfig("Penguin", None, Operator.ANY),         # T1 Cold Res
      # AffixConfig("Storm", None, Operator.ANY),           # T1 Lightning Res
      # AffixConfig("Lost", None, Operator.ANY),            # T3 Chaos Res
      AffixConfig("Banishment", None, Operator.ANY),      # T2 Chaos Res
      AffixConfig("Eviction", None, Operator.ANY),        # T1 Chaos Res
      AffixConfig("Kaleidoscope", None, Operator.ANY),    # T1 All Ele Res
    ],
    "custom_should_regal": CustomShouldRegal.LargeClusterBow,
    "custom_should_exalt": CustomShouldExalt.LargeClusterBow, # We are exalting but leaving num_affixes_required as 3 because the 4th one is not strict
    "custom_is_valid": CustomIsValid.LargeClusterBow,
    "num_affixes_required": 3,
    "min_item_level": 84
  }

  # Large Cluster 12 Passives Minion Damage
  LargeClusterMinion: Config = {
    "name": "Large Cluster Jewel - Minion Damage",
    "prefixes": [
      # AffixConfig("Potent", None, Operator.ANY),          # T2 Effect
      AffixConfig("Powerful", None, Operator.ANY),        # T1 Effect

      AffixConfig("Healthy", None, Operator.ANY),         # T2 Life
      AffixConfig("Sanguine", None, Operator.ANY),        # T1 Life
      
      AffixConfig("Glimmering", None, Operator.ANY),      # T2 ES
      AffixConfig("Glowing", None, Operator.ANY),         # T1 ES

      AffixConfig("Hazardous", None, Operator.ANY),       # T2 % Damage
      AffixConfig("Dangerous", None, Operator.ANY),       # T1 % Damage
    ],
    "suffixes": [
      # AffixConfig("Sky", None, Operator.ANY),             # T2 Attribute
      AffixConfig("Meteor", None, Operator.ANY),          # T1 Attribute

      # AffixConfig("Wrestler", None, Operator.ANY),        # T2 Str
      AffixConfig("Bear", None, Operator.ANY),            # T1 Str

      # AffixConfig("Lynx", None, Operator.ANY),            # T2 Dex 
      AffixConfig("Fox", None, Operator.ANY),             # T1 Dex

      # AffixConfig("Student", None, Operator.ANY),         # T2 Int 
      AffixConfig("Prodigy", None, Operator.ANY),         # T1 Int 

      AffixConfig("Ravaging", None, Operator.ANY),         # T2 Minion Attack Speed 
      AffixConfig("Razing", None, Operator.ANY),          # T1 Minion Attack Speed

      AffixConfig("Drake", None, Operator.ANY),           # T1 Fire Res 
      AffixConfig("Penguin", None, Operator.ANY),         # T1 Cold Res
      AffixConfig("Storm", None, Operator.ANY),           # T1 Lightning Res
      AffixConfig("Eviction", None, Operator.ANY),        # T1 Chaos Res
      AffixConfig("Kaleidoscope", None, Operator.ANY),    # T1 All Ele Res

    ],
    "custom_should_regal": CustomShouldRegal.LargeClusterMinion,
    "custom_should_exalt": CustomShouldExalt.LargeClusterMinion,
    "custom_is_valid": CustomIsValid.LargeClusterMinion,
    "num_affixes_required": 3,
    "min_item_level": 84
  }

  # Large Cluster 12 Passives Minion Damage
  Maps: Config = {
    "name": "Map",
    "prefixes": [
      AffixConfig("Splitting", [2], Operator.GE),
    ],
    "suffixes": [
    ],
    "custom_is_valid": CustomIsValid.Maps,
    "num_affixes_required": 1,
  }


  def get_config_by_base_name(item: Item) -> Config:
    ret = None
    item_base_name = item.base
    item_class = item.type
    item_level = item.ilvl
    item_rarity = item.rarity
    item_corrupted = item.is_corrupted
    item_num_prefixes = item.num_prefixes
    item_num_suffixes = item.num_suffixes
    name_arr = item_base_name.split()

    # if item_class == "Utility Flasks" and "Jade" in name_arr:
    #   ret = ConfigsModule.Jade
    # elif item_class == "Utility Flasks" and "Quicksilver" in name_arr:
    #   ret = ConfigsModule.Quicksilver
    # elif item_class == "Utility Flasks" and "Granite" in name_arr:
    #   ret = ConfigsModule.Granite
    # elif item_class == "Utility Flasks" and "Silver" in name_arr:
    #   ret = ConfigsModule.Silver
    if item_class == "Utility Flasks":
      ret = ConfigsModule.LeagueStartFlasks
    elif item_class == "Bows" and "Spine" in name_arr:
      ret = ConfigsModule.SpineBow
    elif item_class == "Amulets":
      ret = ConfigsModule.FocusedAmulet if item_base_name == "Focused Amulet" else ConfigsModule.Amulet
    elif item_class == "Boots":
      ret = ConfigsModule.Boots
    elif item_class == "Gloves":
      ret = ConfigsModule.Gloves
    elif item_class == "Helmets":
      ret = ConfigsModule.Helmet
    elif item_class == "Wands":
      ret = ConfigsModule.Wand
    elif item_class == "Quivers":
      ret = ConfigsModule.Quiver
    elif item_class == "Jewels" and "Large" in name_arr and "Cluster" in name_arr:
      if item.cluster_jewel_has("Bow"):
        ret = ConfigsModule.LargeClusterBow12
      elif item.cluster_jewel_has("Minion"):
        ret = ConfigsModule.LargeClusterMinion
      else:
        ret = ConfigsModule.LargeClusterSpellDamage
    elif item_class == "Jewels":
      ret = ConfigsModule.AdornedJewels
    elif item_class == "Abyss Jewels":
      ret = ConfigsModule.AbyssJewel
    elif item_class == "Body Armours" and "Sadist" in name_arr:
      ret = ConfigsModule.SadistGarb
    elif item_class == "Maps":
      ret = ConfigsModule.Maps
    else:
      raise ValueError(f"Unknown base name: {item_base_name}")
    
    if ret.get("min_item_level") is not None and int(item_level) < ret.get("min_item_level"):
      raise ValueError(f"Item level too low: {item_level} < {ret.get('min_item_level')}")
    
    print(f"💡 Using \"{ret.get('name')}\" config for \
          \n\titem base =\"{item_base_name}\" \
          \n\titem class=\"{item_class}\" \
          \n\titem level=\"{item_level}\" \
          \n\titem rarity=\"{item_rarity}\" \
          \n\titem corrupted=\"{item_corrupted}\" \
          \n\titem num_prefixes=\"{item_num_prefixes}\" \
          \n\titem num_suffixes=\"{item_num_suffixes}\"")
    return ret
  
  