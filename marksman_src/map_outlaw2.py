from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mail import Marksman

def outlaw2_macro(marksman: 'Marksman'):
  print("Started Outlaw Infested Wastes 2 macro")
  while not marksman.should_exit():
    marksman.buff_setup()
    marksman.q_and_surgebolt(afterDelay=0.55)
    marksman.jump_down_attack_turn(delayAfter=0.5, turn='right')
    marksman.q_and_surgebolt(afterDelay=0.55)
    marksman.bot.press_release('left')
    marksman.jump_attack(attackDelay=0.05, delayAfter=0.55)
    marksman.jump_attack(attackDelay=0.05, delayAfter=0.55)
    marksman.teleport_reset()
  print("Paused Outlaw Infested Wastes 2 macro")