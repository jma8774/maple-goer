import regex as re
from item_parser.constants import Operator
from item_parser.item import Item
from item_parser.line import Line

class AffixConfig:
  def __init__(self, affix_name: str, values: list[int], operator: int):
    self._affix_name = affix_name
    self._values = values
    self._operator = operator

  def pass_check(self, line: Line):
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

  @property
  def affix_name(self):
    return self._affix_name
  
  def __str__(self):
    return f"{self._affix_name}: {self._values} {self._operator}"