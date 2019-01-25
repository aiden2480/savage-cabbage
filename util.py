# Other long lists and variables #
message_colours = [
  0x7FFF00, # Green
  0x0000ff, # Blue
  0xFFFF00, # Yellow
  0x8A2BE2, # Purple
  0xffa500, # Orange
  0xbff442, # Lime
  0x00ffa5] # Light aqua

roasts = [
  #"Oof!",
  "Hecc off!",
  "You are a dirt puddle!",
  "Go commit **neck-rope**",
  "Go commit **bullet-face**",
  "You're fatter than big smoke",
  "Go commit **choke-on-water**",
  "You are smelly and not very smart",
  "You have a face made for **radio**",
  "Go commit **oxygen-not-reach-lung**",
  "Go commit **food-not-reach-stomach**",
  "You're so ugly that Hello Kitty said **goodbye** to you",
  #"I've seen some pricks in my life, but **you're a cactus!**",
  "You're as useless as **ejection seats** on a **helicopter**",
  "You bring everyone a lot of joy, when you **leave the room**",
  "If what you don't know can't hurt you, you must be **invunreble!**",
  "Somebody once told me that you aren't the sharpest tool in the shed",
  "You've got a photographic memory but **with the lens cover glued on**",
  "Roses are red, Violets are blue, God made me pretty, **What happened to you**?",
  "There are several people in this world that I find obnoxious and you are **all of them**",
  "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. **I think you owe it an apology**"
  #"You're as straight as the pole your mum dances on"
]

one_in_what = 15
greetings = ['Hey','Yo','Wassup','Oi']
roasts_no_bold = [i.replace('**','') for i in roasts] 
roasts_str = ''
for i in roasts_no_bold: roasts_str += i + '\n'