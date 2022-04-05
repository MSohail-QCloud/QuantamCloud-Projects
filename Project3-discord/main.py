import time
import urllib.request
import zipfile
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from anticaptchaofficial.hcaptchaproxyless import *

'''solver = hCaptchaProxyless()
solver.set_verbose(1)
solver.set_key("611ef0077216bf9c0ff1f66171d3c8cb")
# solver.set_website_url("https://website.com")
# solver.set_website_key("SITE_KEY")

g_response = solver.solve_and_return_solution()
if g_response != 0:
    print("g-response: "+g_response)
else:
    print("task finished with error "+solver.error_code)'''

url = 'https://antcpt.com/anticaptcha-plugin.zip'
filehandle, _ = urllib.request.urlretrieve(url)
# unzip it
with zipfile.ZipFile(filehandle, "r") as f:
    f.extractall("plugin")

# set API key in configuration file
api_key = "611ef0077216bf9c0ff1f66171d3c8cb"
file = Path('./plugin/js/config_ac_api_key.js')
file.write_text(
    file.read_text().replace("antiCapthaPredefinedApiKey = ''", "antiCapthaPredefinedApiKey = '{}'".format(api_key)))

# zip plugin directory back to plugin.zip
zip_file = zipfile.ZipFile('./plugin.zip', 'w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk("./plugin"):
    for file in files:
        path = os.path.join(root, file)
        zip_file.write(path, arcname=path.replace("./plugin/", ""))
zip_file.close()

# set browser launch options
options = Options()
# options.add_argument("--incognito")
options.add_argument("start-maximized")
options.add_argument('--load-extension={}'.format(str(Path.cwd()) + '\plugin'))

# set browser launch options
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

fil = "orderfile.txt"

f = open(fil, "r")
for l in f:
    lst = l.split(':')
    print(lst[0])
    print(lst[2])

    # navigate to the target page
    browser.get('https://discord.com/register')
    email = str(lst[0])
    username = "MyOutlook"
    password = str(lst[2])
    # fill register form
    time.sleep(1)
    # browser.find_element_by_name('email').send_keys('orlo5jva22uqey9@bc.ru')
    browser.find_element(by=By.NAME, value='email').send_keys(email)
    time.sleep(1)
    # browser.find_element_by_name('username').send_keys(username)
    browser.find_element(by=By.NAME, value='username').send_keys(username)
    time.sleep(1)
    # browser.find_element_by_name('password').send_keys(password+Keys.TAB+'1'+Keys.TAB+'1'+Keys.TAB+'1980'+Keys.TAB+Keys.TAB)
    browser.find_element(by=By.NAME, value='password').send_keys(
        password + Keys.TAB + '1' + Keys.TAB + '1' + Keys.TAB + '1980' + Keys.TAB + Keys.TAB)
    time.sleep(1)
    # browser.find_element_by_css_selector('.contents-3ca1mk').click()
    browser.find_element(by=By.CSS_SELECTOR, value='.contents-3ca1mk').click()
    time.sleep(5)
    #kk = browser.find_element(By.CSS_SELECTOR("#errorMessage-1kMqS5")).text
    #print(kk)
    time.sleep(120)
    # wait = WebDriverWait(browser, 120)
    # wait.until(lambda x: x.find_element_by_css_selector('.antigate_solver.solved'))
    geturl=browser.current_url
    if geturl=="https://discord.com/register":
        continue
    else:
        input("span")
    input("next row \n")

input(" enter key to exit")
