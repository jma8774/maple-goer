from PIL import Image

def openImage(file):
  return Image.open(f"images/{file}")

# Images
class Images:
  CRAFT           = openImage('craft.png')
  OK_START        = openImage('ok_start.png')
  OK_END          = openImage('ok_end.png')
  CANCEL          = openImage("cancel.png")
  TAB_RESET       = openImage("tab_reset.png")
  EXTRACT_UP      = openImage("extract_up.png")
  CONFIRM         = openImage("confirm.png")
  BAG             = openImage("bag.png")
  SORT            = openImage("sort.png")
  ENHANCE_STAR    = openImage("star.png")
  ENHANCE_ENHANCE = openImage("enhance.png")
  ENHANCE_OK      = openImage("e_ok.png")

  FOREBERION      = openImage("foreberion.png")
  ASCENDION       = openImage("mob.png")
  LIMINIA_ICON    = openImage("liminia_icon.png")
  RUNE_MINIMAP    = openImage("rune_minimap.png")
  RUNE_MSG        = openImage("rune_msg.png")
  MINIMAP         = openImage("minimap.png")

  # Boss
  LUCID           = openImage("lucid.png")
  WILL            = openImage("will.png")

  def get(key, suffix):
    return getattr(Images, f"{key}{suffix}")