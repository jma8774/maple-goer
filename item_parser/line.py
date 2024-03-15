import regex as re

AFFIX_NAME_REGEX = r'(?<=")(.*?)(?=")'

class Line:
  def __init__(self, affix_type: str, affix_descriptions: list[str]):
    self._affix_type = affix_type
    self._affix_descriptions_raw = affix_descriptions
    self._affix_description_values: list[int] = []

    # Parse affix name
    self._affix_name = re.search(AFFIX_NAME_REGEX, affix_type)
    if self._affix_name is not None:
      self._affix_name = self._affix_name.group(0)
      self._affix_name = re.sub(r'^of the ', "", self._affix_name)
      self._affix_name = re.sub(r'^of ', "", self._affix_name)
      self._affix_name = re.sub(r'\'s$', "", self._affix_name)

    # Parse affix values
    for d in affix_descriptions:
      if re.search("Unscalable", d) or re.search("crafted", d):
        self._affix_description_values.append(None)
        continue
      for value in re.findall(r'(?<=\s|^)[-+]*\d*\.?\d+(?=\(|\s|%)', d): # Capture all numbers, except those inside of parenthesis
        self._affix_description_values.append(float(value) if '.' in value else int(value))

  @property
  def is_valid(self):
    return self._affix_name is not None and len(self._affix_description_values) > 0
  
  @property
  def affix_name(self):
    if self._affix_name is None:
      raise ValueError(f"[affix_name] Attempting to use an invalid line: {self._affix_descriptions_raw}")
    return self._affix_name
  
  @property
  def affix_values(self):
    return self._affix_description_values
  
  @property
  def affix_raw(self):
    return self._affix_descriptions_raw
  
  def __str__(self):
    if not self.is_valid:
      if self._affix_name is not None:
        return f'[❌] {self.affix_name}: {self._affix_descriptions_raw}'
      elif len(self._affix_description_values) != 0:
        return f'[❌] {self._affix_type}: {self._affix_description_values}'
      else:
        return f'[❌] {self._affix_type} - {self._affix_descriptions_raw}'
    return f'[✅] {self.affix_name}: {self.affix_values}'
  
  def __eq__(self, other):
    if not isinstance(other, Line):
      return False
    if self.affix_name != other.affix_name:
      return False
    if len(self.affix_values) != len(other.affix_values):
      return False
    for i in range(len(self.affix_values)):
      if self.affix_values[i] != other.affix_values[i]:
        return False
    # Will do a string comparison against raw descrption if affix values are the same (For items with same affix names but they represent different values eg. Cluster jewels "Notable" and "Significance")
    for i in range(len(self._affix_descriptions_raw)):
      if self._affix_descriptions_raw[i] != other._affix_descriptions_raw[i]:
        return False
    return True
