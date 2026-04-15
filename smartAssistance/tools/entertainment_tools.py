from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from langchain_core.tools import tool

@tool
def open_youtube(search_title:str)->dict:
    """this function able to open youtube directly in browser
    for provided titile  """
    
    chrome_option = Options()
    chrome_option.add_experimental_option("detach",True)
    
    driver = webdriver.Chrome(options=chrome_option)

    driver.get("https://www.youtube.com")

    wait = WebDriverWait(driver, 10)

    search_box = wait.until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )

    search_box.send_keys(search_title)
    search_box.send_keys(Keys.RETURN)
    
    first_video = wait.until(
    EC.element_to_be_clickable((By.ID, "video-title"))
    )
    first_video.click()
    
    return { "success":"true","tittle":search_title}
  

@tool
def open_songhub(search_title: str):
    
    """this function can open a song in songhub.lk
    when search titile is provided"""
    
    chrome_option = Options()
    chrome_option.add_experimental_option("detach",True)
    
    driver = webdriver.Chrome(options=chrome_option)
    
    wait = WebDriverWait(driver, 10)

    driver.get("https://songhub.lk/")

    search_box = wait.until(
        EC.presence_of_element_located((By.NAME, "search"))
    )

    search_box.send_keys(search_title)
    search_box.send_keys(Keys.RETURN)

    # Wait for search results to load
    songs = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".gs-title a")  
        )
    )

    # Click first visible result
    for song in songs:
        if song.is_displayed():
            song.click()
            break
    
    #update state accordingly      