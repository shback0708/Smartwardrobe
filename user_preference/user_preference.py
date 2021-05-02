import os
import webcolors

def setRating(p, inp):
  if not os.path.exists("fb.txt"):
    f = open("fb.txt", "w")
    f.close()
  f = open("fb.txt", "r")
  c = f.read()
  lines = c.split("\n")
  like = ""
  dislike = ""
  outfit = ""
  if(len(lines) >= 1):
    like = lines[0]
  if(len(lines) >= 2):
    dislike = lines[1]
  if(len(inp) == 2):
    outfit = inp[0][0] + " " + get_colour_name(inp[0][5]) + " "
    outfit += inp[1][0] + " " + get_colour_name(inp[1][5])
  else:
    outfit =  inp[0][0] + " " + get_colour_name(inp[0][5])
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
def getRating(inp):
  try:
    f = open("fb.txt", "r")
  except:
    return 0
  c = f.read()
  lines = c.split("\n")
  f.close()
  outfit = ""
  if(len(inp) == 2):
    outfit = inp[0][0] + " " + get_colour_name(inp[0][5]) + " "
    outfit += inp[1][0] + " " + get_colour_name(inp[1][5])
  else:
    outfit =  inp[0][0] + " " + get_colour_name(inp[0][5])

  if(len(lines) >= 1):
    good = lines[0].split(",")
    if outfit in good:
      return 1
  if(len(lines) >= 2):
    bad = lines[1].split(",")
    if outfit in bad:
      return -1
  return 0
def get_colour_name(rgb_triplet):
    min_colours = {}
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

if __name__ == '__main__':
    a = (("shirt","a","b","c","d",(0,0,0)), ("pants","a","b","c","d",(0,0,0)))
    b = (("dress","a","b","c","d",(100,0,0)),)
    c = (("shirt","a","b","c","d",(200,0,0)), ("pants","a","b","c","d",(100,0,0)))
    d = c = (("shirt","a","b","c","d",(300,0,0)), ("pants","a","b","c","d",(200,0,0)))
    setRating(1, a)
    setRating(-1,b)
    setRating(1, c)
    setRating(1,d)
    print(getRating(a))
    print(getRating(b))
    print(getRating(c))
    print(getRating(d))