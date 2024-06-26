class Operator:
  EQ = 0
  GT = 1
  LT = 2
  GE = 3
  LE = 4
  NE = 5
  ANY = 6
  PASS = 7

  ENDS_WITH = 100
  STARTS_WITH = 101

  def parse(operator: int):
    if operator == Operator.EQ:
      return "="
    if operator == Operator.GT:
      return ">"
    if operator == Operator.LT:
      return "<"
    if operator == Operator.GE:
      return ">="
    if operator == Operator.LE:
      return "<="
    if operator == Operator.NE:
      return "!="
    if operator == Operator.ANY:
      return "ANY"
    return "UNKNOWN"