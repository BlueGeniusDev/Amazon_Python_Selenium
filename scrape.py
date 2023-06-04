from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import xlsxwriter
import time
import json


def get_products(url, driver):

    # navigate to the webpage
    driver.get(url)
    time.sleep(5)

    title = driver.find_element(
        "xpath", '//h1[@id="title"]').text
    videoCount = 0
    try:

        btn_video = driver.find_element(
            "xpath", '//li[@data-csa-c-action="image-block-alt-image-clickToImmersiveVideos"]')

        driver.execute_script('arguments[0].click();', btn_video)
        time.sleep(5)

        try:
            videoCount = int(driver.find_element(
                "xpath", '//span[@id="videoCount"]').text[:-7])
            data = []
            temp = driver.find_elements(
                'xpath', '//ol[@class="a-carousel"]//li')
            for x in range(videoCount):
                video_url = temp[x].find_elements(
                    'xpath', '//a[@class="a-link-normal"]')[x].get_attribute('href')
                title = temp[x].find_elements(
                    'xpath', '//h4[@class="vse-video-title-text"]')[x].text
                content = temp[x].find_elements(
                    'xpath', '//div[@class="vse-video-labels "]')[x].text

                data.append({
                    "video_url": video_url,
                    "title": title,
                    "content": content
                })
        except:
            videoCount = 1
            data = driver.find_element(
                "xpath", '//div[@id="main-video-container"]//video').get_attribute('src')

    except:
        data = None

    return title, videoCount, data


with xlsxwriter.Workbook('bestseller.xlsx') as workbook:
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['Product Title', 'Video Count'])
    # initialize the webdriver
    driver = webdriver.Chrome()

    with open("urls.txt", 'r') as urllist, open('bestseller.jsonl', 'w') as outfile:
        i = 0
        for url in urllist.read().splitlines():
            title, videoCount, data = get_products(url, driver)

            # Convert data to JSON string and write to file
            json_data = json.dumps([title, videoCount, data])
            outfile.write(json_data + "\n")

            i += 1
            worksheet.write_row(i, 0, [title, videoCount])
            outfile.write("\n")
        time.sleep(3)
    driver.quit()
