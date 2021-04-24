import os
def setRating(p, outfit):
  if not os.path.exists("fb.txt"):
    f = open("fb.txt", "w")
    f.close()
  f = open("fb.txt", "r")
  c = f.read()
  lines = c.split("\n")
  like = ""
  dislike = ""
  if(len(lines) >= 1):
    like = lines[0]
  if(len(lines) >= 2):
    dislike = lines[1]
  if(p == 1):
    outfits = like.split(",")
    if outfit not in outfits:
      if(len(like) != 0):
        like += ("," + outfit)
      else:
        like += (outfit)
    if(dislike != ""):
      o = dislike.split(",")
      if outfit in o or outfit == o:
        o.remove(outfit)
        dislike = ",".join(o)
  elif(p == -1):
    outfits = dislike.split(",")
    if outfit not in outfits:
      if(len(dislike) != 0):
        dislike += ("," + outfit)
      else:
        dislike += (outfit)
    if(like != ""):
      o = like.split(",")
      if outfit in o:
        o.remove(outfit)
        like = ",".join(o)
  f.close()
  f = open("fb.txt", "w")
  f.seek(0)
  f.truncate()
  f.write(like)
  f.write("\n")
  f.write(dislike)
  f.close()
def getRating(outfit):
  try:
    f = open("fb.txt", "r")
  except:
    return 0
  c = f.read()
  lines = c.split("\n")
  f.close()
  if(len(lines) >= 1):
    good = lines[0].split(",")
    if outfit in good:
      return 1
  if(len(lines) >= 2):
    bad = lines[1].split(",")
    if outfit in bad:
      return -1
  return 0
