#Need to install selenium, requests, pillow (for PIL)
from selenium import webdriver
import time
import requests
from PIL import Image
from io import BytesIO
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition/clothing_recognition'))
path = "chromedriver"
DRIVER_PATH = path
class WebScraper:
  
  def google(self, query):
    link = "https://images.google.com/?gws_rd=ssl"
    links = []
    ret = []
    limit = 10
    driver = webdriver.Chrome(path)
    driver.maximize_window()
    driver.get(link)
    driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input').send_keys(query)
    driver.find_element_by_xpath('//*[@id="sbtc"]/button').click()
    time.sleep(.5)
    images = driver.find_elements_by_class_name('rg_i')
    count = 0
    for image in images:
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
        links.append(link)
      if(count == limit):
        driver.close()
        break
    for l in links:
      response = requests.get(l)
      im = Image.open(BytesIO(response.content))
      ret.append(im)
    return ret
  
if __name__ == '__main__':
    ws = WebScraper()
    print("test completed.")
