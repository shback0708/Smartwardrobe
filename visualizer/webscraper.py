#Need to install selenium, requests, pillow (for PIL), webcolors
#pip install selnium
#pip install webcolors==1.3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from PIL import Image
from io import BytesIO
import sys
import os
import webcolors

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition/clothing_recognition'))
path = "chromedriver"
DRIVER_PATH = path
class WebScraper:
  
  def scrapeOutfits(self, labels, num, offset = 0):
    link = "https://images.google.com/?gws_rd=ssl"
    links = []
    ret = []
    limit = num
    query = ""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(path, options = chrome_options)
    driver.maximize_window()
    driver.get(link)
    if(len(labels) == 2):
      color = self.get_colour_name(labels[0][5])
      color1 = self.get_colour_name(labels[1][5])
      label = labels[0][0]
      label1 = labels[1][0]
      query = color + " " + label + " " + color1 + " " + label1
      
    else:
      color = self.get_colour_name(labels[0][5])
      label = labels[0][0]
      query = color + " " + label
    driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input').send_keys(query)
    driver.find_element_by_xpath('//*[@id="sbtc"]/button').click()
    time.sleep(.5)
    images = driver.find_elements_by_class_name('rg_i')
    while (len(images) < limit + offset):
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      images = driver.find_elements_by_class_name('rg_i')
    count = 0
    for image in images:
      try:
        image.click()
        time.sleep(.3)
        element = driver.find_elements_by_class_name("v4dQwb")
        if(count == 0):
          img = element[0].find_element_by_class_name("n3VNCb")
        else:
          img = element[1].find_element_by_class_name("n3VNCb")
        link = img.get_attribute("src")
        if(link[0:4] == "http"):
          count += 1
          if (count >= offset):
            links.append(link)
        if(count == limit + offset):
          break
      except:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.close()
    for l in links:
      print(l)
      response = requests.get(l)
      try:
        im = Image.open(BytesIO(response.content)).convert('RGB')
        ret.append(im)
      except:
        pass
    return ret
  #used from https://stackoverflow.com/questions/9694165/convert-rgb-color-to-
  #english-color-name-like-green-with-python#:~:text=To%20find%20the%20closest
  #%20colour%20name%3A&text=There%20is%20a%20program%20called,can%20do%20what%20you%20want.
  def get_colour_name(self, rgb_triplet):
    min_colours = {}
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]
  
if __name__ == '__main__':
    ws = WebScraper()
    ws.scrapeOutfits((("shirt", "flannel", "a", "b", "c", (0,0,0)), ("jeans", "long", "a", "b", "c", (0,0,255))), 100)
    #ws.scrapeOutfits((("dress", "a", "b", "c", "d", (200,0,0)), 80),)
    print("test completed.")
