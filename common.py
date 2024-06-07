def print_state(state: dict):
  print("State")
  for key, value in state.items():
    print('  {:<12}  {:<12}'.format(key+":", value))

def print_args(args):
  print("Arguments")
  for arg in args:
    print(f"  {arg}")

def print_scripts(scripts: dict):
  print("Scripts")
  for key, value in scripts.items():
    print('  {:<12}  {:<12}'.format(key+":", str(value)))