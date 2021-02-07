import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from datetime import datetime

def get_images(driver, distination, query):
    total_downloaded_images = 0
    
    if not os.path.exists(distination):
        os.mkdir(distination)
    
    if not os.path.exists(os.path.join(distination, query)):
        os.mkdir(os.path.join(distination, query))

    search_url="https://www.google.com/search?q={q}&tbm=isch&tbs=sur%3Afc&hl=en&ved=0CAIQpwVqFwoTCKCa1c6s4-oCFQAAAAAdAAAAABAC&biw=1251&bih=568" 
    for o in range(5):
        print('[!] Start New Round:', o+1)
        driver.get(search_url.format(q=query))

        #Scroll to the end of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)#sleep_between_interactions

        #Locate the images to be scraped from the current page 
        imgResults = driver.find_elements_by_xpath("//img[contains(@class,'Q4LuWd')]")
    
        totalResults = len(imgResults)
        print('[+] Found results:', totalResults)

        #Click on each Image to extract its corresponding link to download
        img_urls = set()
        for i in  range(0,len(imgResults)):
            img=imgResults[i]
            try:
                img.click()
                time.sleep(2)
                actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'https' in actual_image.get_attribute('src'):
                        i_url = actual_image.get_attribute('src')
                        if i_url not in img_urls:
                            if download_from_link(i_url, os.path.join(distination, query)):
                                total_downloaded_images+=1
                                print("[+] downloads till now:", total_downloaded_images)
                        img_urls.add(i_url)
                driver.execute_script("window.history.go(-1)")
                
            except ElementClickInterceptedException or ElementNotInteractableException as err:
                print(err)
    return total_downloaded_images

def download_from_link(url, path):
    image_content = ""
    file_name = f"{query + '_' + str(datetime.timestamp(datetime.now()))}.jpg"    
    try:
        image_content = requests.get(url).content

    except Exception as e:
            print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        
        file_path = os.path.join(path, file_name)
        
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        # print(f"SAVED - {url} - AT: {file_path}")
        return True
    except Exception as e:
        # print(f"ERROR - COULD NOT SAVE {url} - {e}")
        return False

if __name__ == '__main__':
    opts=webdriver.ChromeOptions()
    opts.headless=True

    #Install Driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    # queries = ['electric suv', 'audi suv', 'mercides suv', 'porche suv']
    # queries = ['fast suv', 'nissan suv', 'citreon suv']
    queries = ['mg suv', 'kia suv', 'subaru suv']
    # huyndai
    # jeep
    # ford
    # gmc
    distination = '7-2-2021'
    total_downloaded_images = 0
    #Specify Search URL 
    for query in queries:
        total_downloads_per_round = get_images(driver, distination, query)
        print('[+] Images downloaded in this round:', total_downloads_per_round)
        total_downloaded_images += total_downloads_per_round
    print('Total Downloaded Images:', total_downloaded_images)
    