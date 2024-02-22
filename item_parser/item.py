from item_parser.line import Line
import regex as re

SEPERATOR = "--------"
RE_GET_BASE_NAME_WITHOUT_AFFIX = r'(?<=\'s\s|^)(.*?)(?=\sof|$)'
RE_GET_CONTENT_AFTER_COLON = r'(?<=:\s)(.*?)(?=$)'
                                           
class Item:
  def __init__(self, raw_string: str):
    self._raw_string: str = raw_string
    self._item_affixes: list[str] = []
    self._item_affixes_parsed: dict = {}
    self._item_base = ""
    self._item_class = ""
    self._item_level = ""

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
  def item_base(self):
    return self._item_base
  
  @property
  def item_class(self):
    return self._item_class
  
  @property
  def item_level(self):
    return self._item_level

  def __str__(self):
    return f"{([str(v) for k, v in self._item_affixes_parsed.items()])}"
    # return f"{self._item_base} {([str(v) for k, v in self._item_affixes_parsed.items()])}"
  
  def __eq__(self, other):
    if isinstance(other, Item):
      if len(self.affixes) != len(other.affixes):
        return False
      for affix in self.affixes:
        if not other.affixes.get(affix):
          return False
    return True