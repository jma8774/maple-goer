from item_parser.configs.affix_config import AffixConfig
from item_parser.constants import Operator
from item_parser.item import Item
from item_parser.line import Line
from item_parser.configs.item_base_config import ConfigsModule

class CraftingWorkItem:
  def __init__(self, positions: list):
    self._positions = positions

  @property
  def positions(self):
    return self._positions
  
