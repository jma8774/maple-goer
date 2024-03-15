import regex as re
from item_parser.constants import Operator
from item_parser.item import Item
from item_parser.line import Line

class ExtraStringConfig:
  def __init__(self, s: str, operator: Operator):
    self._s = s
    self._operator = operator
    
  def pass_check(self, line: Line):
    for d in line.affix_raw:
      if self._operator == Operator.STARTS_WITH and d.startswith(self._s):
        return True
      if self._operator == Operator.ENDS_WITH and d.endswith(self._s):
        return True
      if self._operator == Operator.EQ and self._s in d:
        return True
    return False
  
class AffixConfig:
  def __init__(self, affix_name: str, values: list[int], operator: Operator, extra_configs: list[ExtraStringConfig] = []):
    self._affix_name = affix_name
    self._values = values
    self._operator = operator
    self._extra_configs = extra_configs

  def pass_check(self, line: Line):
    def check1():
      if self._affix_name != line.affix_name:
        print(f"Affix name mismatch: {self._affix_name} != {line.affix_name}")
        return False
      if self._operator == Operator.ANY:
        return True
      if len(self._values) != len(line.affix_values):
        print(f"Value length mismatch: {self._values} != {line.affix_values}")
        return False
      # print(f"Checking {self._affix_name}: {line.affix_values} {Operator.parse(self._operator)} {self._values}")
      for i, config_value in enumerate(self._values):
        if line.affix_values[i] is None and config_value is None:
          continue
        elif line.affix_values[i] is None or config_value is None:
          return False
        if self._operator == Operator.EQ and config_value != line.affix_values[i]:
          return False
        if self._operator == Operator.GT and config_value >= line.affix_values[i]:
          return False
        if self._operator == Operator.GE and config_value > line.affix_values[i]:
          return False
        if self._operator == Operator.LT and config_value <= line.affix_values[i]:
          return False
        if self._operator == Operator.LE and config_value < line.affix_values[i]:
          return False
        if self._operator == Operator.NE and config_value == line.affix_values[i]:
          return False
      return True
    
    def check2():
      for config in self._extra_configs:
        if not config.pass_check(line):
          return False
      return True
    
    c1 = check1()
    c2 = check2()
    print(f"c1={c1}, c2={c2}")
    return c1 and c2

  @property
  def affix_name(self):
    return self._affix_name
  
  def __str__(self):
    return f"{self._affix_name}: {self._values} {self._operator}"
  