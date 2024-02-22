communication_preference = {
  "jeemong": "dm"
}

def is_dm(user: str) -> bool:
  return communication_preference[user] == "dm" if user in communication_preference else False