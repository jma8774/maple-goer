from item_parser.line import Line
import regex as re

SEPERATOR = "--------"
RE_GET_BASE_NAME_WITHOUT_AFFIX = r'(?<=\'s\s|^)(.*?)(?=\sof|$)'
RE_GET_CONTENT_AFTER_COLON = r'(?<=:\s)(.*?)(?=$)'
RE_GET_CLUSTER_PASSIVES_NUM = r'(?<=Adds\s)(\d*?)(?=\sPassive)'
                                           
class Item:
  def __init__(self, raw_string: str):
    self._raw_string: str = raw_string
    self._item_affixes: list[str] = []
    self._item_affixes_parsed: dict = {}
    self._num_prefixes = 0
    self._num_suffixes = 0
    self._item_base = ""
    self._item_class = ""
    self._item_rarity = ""
    self._item_level = ""

    # Cluster Jewel Enchants
    self._cluster_jewel_enchants = []
    self._cluster_jewel_passives = 0

    lines = raw_string.splitlines()
    i = 0
    while i < len(lines):
      # Parse item class (always first line)
      if self._item_class == "":
        match = re.search(RE_GET_CONTENT_AFTER_COLON, lines[i])
        if match is None:
          raise ValueError(f"Could not parse item class: {lines[i]}, match={match}")
        self._item_class = match.group(0) if match else lines[i]
        i += 1
        continue

      # Parse item rarity (always second line)
      if self._item_rarity == "":
        match = re.search(RE_GET_CONTENT_AFTER_COLON, lines[i])
        if match is None:
          raise ValueError(f"Could not parse item rarity: {lines[i]}, match={match}")
        self._item_rarity = match.group(0) if match else lines[i]
        i += 1
        continue

      # Parse base (always at the end of the first section)
      if self._item_base == "" and lines[i] == SEPERATOR:
        # match = re.search(RE_GET_BASE_NAME_WITHOUT_AFFIX, lines[i-1])
        # self._item_base = match.group(0) if match else lines[i-1]
        self._item_base = lines[i-1]
        i += 1
        continue
      
      if self._item_level == "" and lines[i].startswith("Item Level: "):
        match = re.search(RE_GET_CONTENT_AFTER_COLON, lines[i])
        if match is None:
          raise ValueError(f"Could not parse item class: {lines[i]}, match={match}")
        self._item_level = match.group(0) if match else lines[i]
        i += 1
        continue

      if "Cluster" in self._item_base and lines[i].endswith("(enchant)"):
        if lines[i].startswith("Added"):
          self._cluster_jewel_enchants.append(lines[i])
          i += 1
          continue
        elif self._cluster_jewel_passives == 0:
          match = re.search(RE_GET_CLUSTER_PASSIVES_NUM, lines[i])
          if match is None:
            raise ValueError(f"Could not parse cluster jewel passives: {lines[i]}, match={match}")
          self._cluster_jewel_passives = int(match.group(0))
          i += 1
          continue
          
      # Parse affixes
      if lines[i] == SEPERATOR and (lines[i+1].startswith("{ Prefix") or lines[i+1].startswith("{ Suffix")):
        i += 1
        start = i
        while i < len(lines) and lines[i] != SEPERATOR:
          i += 1
        end = i
        self._item_affixes = lines[start:end]
        break       
      i += 1 
      
    i = 0
    while i < len(self._item_affixes):
      if self._item_affixes[i].startswith("{ Prefix"):
        self._num_prefixes += 1
      if self._item_affixes[i].startswith("{ Suffix"):
        self._num_suffixes += 1
      affix_type = self._item_affixes[i]
      affix_descriptions = []
      i += 1
      while i < len(self._item_affixes) and not self._item_affixes[i].startswith("{"):
        affix_descriptions.append(self._item_affixes[i])
        i += 1
      line = Line(affix_type, affix_descriptions[:])
      self._item_affixes_parsed[line.affix_name] = line

  @property
  def affixes(self):
    return self._item_affixes_parsed
  
  @property
  def base(self):
    return self._item_base
  
  @property
  def type(self):
    return self._item_class
  
  @property
  def ilvl(self):
    return self._item_level
  
  @property
  def rarity(self):
    return self._item_rarity
  
  @property
  def num_prefixes(self):
    return self._num_prefixes
  
  @property
  def num_suffixes(self):
    return self._num_suffixes
  
  @property
  def cluster_jewel_enchants(self):
    return self._cluster_jewel_enchants
  
  @property
  def cluster_jewel_passives(self):
    return self._cluster_jewel_passives
  
  def cluster_jewel_has(self, word: str):
    for line in self._cluster_jewel_enchants:
      if word in line:
        return True
    return False
  
  def __str__(self):
    return f"({self.num_prefixes}p {self.num_suffixes}s]) {([str(v) for k, v in self._item_affixes_parsed.items()])}"
    # return f"{self._item_base} {([str(v) for k, v in self._item_affixes_parsed.items()])}"
  
  def __eq__(self, other):
    if not isinstance(other, Item):
      return False
    if len(self.affixes) != len(other.affixes):
      return False
    for affix in self.affixes:
      if not other.affixes.get(affix) or (other.affixes.get(affix) != self.affixes.get(affix)):
        return False
    return True