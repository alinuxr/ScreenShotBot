'''
Screenshot making
input: url and data format for output
possible data formats: png,jpg and pdf

for pdf - firstly make screenshot in png and then convert to pdf

screenshot makes with Chrome webdriver manager
added verification to input string with exception

'''
import img2pdf
import regex as re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import InvalidArgumentException


def findurl(string: str):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

def screenshotmaker(url: str, format: str, filename: str) -> bool:
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        print("Making screenshot . . .")
    except InvalidArgumentException:
        print("InvalidArgumentException Message: invalid argument in url")
        logger = logging.getLogger('__screenshot_module_logging__')
        logger.exception("Exception occurred in InvalidArgumentException")
        return False
    driver.maximize_window()
    driver.get(url)
    string = 'screens/'+ filename +'.'
    screenshot = driver.save_screenshot(string + ('png' if format == 'pdf' else format))
    if format == 'pdf':
        imgFile = open('screens/' + filename + '.png', "rb") #ljltl
        pdfFile = open('screens/' + filename + '.pdf', "wb")#ljltk
        pdfFile.write(img2pdf.convert(imgFile))
        imgFile.close()
        pdfFile.close()
    driver.quit()
    print("Screenshot: success")
    return True

