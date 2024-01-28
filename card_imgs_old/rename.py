import os

d = {"clubs" : "c",
     "diamonds" : "d",
     "hearts" : "h",
     "spades" : "s",
     "clubs2" : "c",
     "diamonds2" : "d",
     "hearts2" : "h",
     "spades2" : "s"}

for old_name in os.listdir():
    if ".png" in old_name:
     old = old_name.split("_of_")
     if "ace" in old[0]: old[0] = "A"
     if "king" in old[0]: old[0] = "K"
     if "queen" in old[0]: old[0] = "Q"
     if "jack" in old[0]: old[0] = "J"
     new_name = old[0] + d[old[1].strip(".png")] + ".png"
     # print(new_name)
     os.rename(old_name, new_name)