# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
import selenium
import urllib.request
import urllib3
import os
import time

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # init
    cwd = os.getcwd()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={cwd}/environment/")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)
    # Get already downloaded episodes
    downloaded_episodes = os.listdir(f"{cwd}/futurama/")

    # get list

    driver.get("https://www.wcofun.com/anime/futurama-season-1")
    url_elements = driver.find_elements_by_class_name("cat-eps")

    urls = {}
    for element in url_elements:
        tag = element.find_element_by_tag_name("a")
        urls[tag.get_attribute("innerText")] = tag.get_attribute("href")
    print(f"Extracted urls {urls}")
    for name in urls.keys():
        name_wo_questions = name.replace("?", "").replace(":", "")  # does not work well with file names
        if f"{name_wo_questions}.mp4" in downloaded_episodes:
            print(f"Skipping {name} because it is already present in the dir")
            continue
        print(f"Downloading video {name}")
        driver.get(urls[name])
        for iframe_name in ["cartoon-js-0", "anime-js-0", "cizgi-js-0"]:
            try:
                driver.switch_to.frame(iframe_name)
                print(f"It was {iframe_name} wohoo")
                break
            except selenium.common.exceptions.NoSuchFrameException:
                print(f"It is not a {iframe_name}")

        driver.implicitly_wait(10)
        video_url = driver.find_element_by_id("video-js_html5_api").get_attribute("src")
        # Prepare request # User agent has to be the same or it will not download
        req = urllib.request.Request(
            video_url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
            }
        ) # User agent has to be the same as the one from the browser or else one gets an 404, probably download protection
        # Execute request
        response = None
        for attempt in range(10):
            try:
                response = urllib.request.urlopen(req)
                break
            except urllib.error.HTTPError:
                print(f"Failed to download at attempt {attempt}. Trying again after a few secs....")
                time.sleep(2)
        if not response:
            raise Exception("Could not download")
        with open(f'{cwd}/futurama/{name_wo_questions}.mp4', 'wb') as out:
            while True:
                data = response.read(8192)  # block size 8192
                if not data:
                    break
                out.write(data)
        # urllib.request.urlretrieve(video_url, f'{cwd}/regular_show/{name}.mp4')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/



