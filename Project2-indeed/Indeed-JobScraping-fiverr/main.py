from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from sys import exit as sysExit
from googlesearch import search
import re
from requests_html import HTMLSession
from PyQt5.QtWidgets import QApplication
from  PyQt5.QtCore import *
from  PyQt5.QtGui import *
from  PyQt5.QtWidgets import *
import os
import subprocess
from PyQt5.QtWidgets import QMessageBox
import threading


from PyQt5.QtWidgets import QMessageBox
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from time import sleep
from lxml import etree
from csv import DictWriter
from config import web_config
import uuid
## ---------------Libraries

queue_count=[]
webs=[]
queue=[]
count=0
all_jobs = []
status=False
keywordd=""


class JobScraper:
    jobs_data = []

    def __init__(self, url, keyword, config, email=None, password=None):
        self.url = url
        self.config = config
        self.email = email
        self.password = password
        self.keyword = keyword

    def main(self):
        global all_jobs
        global webs
        global queue
        global count
        global status
        status = True
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            self.page = browser.new_page()
            # self.page.set_viewport_size({"width": 1920, "height": 1080})
            self.page.goto(self.url, timeout=0)
            sleep(5)
            self._accept_cookies()
            if 'login' in self.config:
                self.login()
            self._search_job()

            self._close_noti()
            urls = self._parse_html()
            if urls:
                new_url = []
                for u in range(len(urls)):
                    if 'javascript:;' in urls[u]:
                        pass
                    else:
                        new_url.append(urls[u])
                urls = new_url
                self._goto_job(urls)
                sleep(3)
                # print(self.jobs_data)
                # self.write_csv()
            count -= 1
            print(urls)
            print('closing browser')
            browser.close()

    def create_csv_file(self):
        filename = self.config['name'] + '_' + str(uuid.uuid4()) + '.csv'
        self.filepath = f'./{filename}'
        with open(self.filepath, 'w') as f:
            headers = ['job_title', 'company_name', 'email', 'city', 'posted_by']
            csv_writer = DictWriter(f, fieldnames=headers)
            csv_writer.writeheader()

    def write_csv(self, data):
        with open(self.filepath, 'a') as f:
            headers = ['job_title', 'company_name', 'email', 'city', 'posted_by']
            csv_writer = DictWriter(f, fieldnames=headers)
            csv_writer.writerow(data)
        print(f'new data job to {self.filepath}')

    def _goto_job(self, urls):
        if urls:
            for url in urls:
                sleep(3)
                try:
                    if 'compare_url' in self.config:
                        self.page.goto(url)
                        self._read_job()
                    else:
                        if self.config['web_url'] in url:
                            self.page.goto(url)
                            self._read_job()
                        else:
                            if ("https" in url) or ("www." in url):
                                print("yes")
                                self.page.goto(url.replace("//", "").replace("www.", "https://").replace('https//', ''))
                                print(url.replace("//", "").replace("www.", "https://"))
                            else:
                                if 'base_url' in self.config:
                                    self.page.goto(self.config['base_url'] + url)
                                    print(self.config['base_url'] + url)
                                else:
                                    self.page.goto(self.url + url)
                                    print(self.url + url)
                            self._read_job()
                except Exception as e:
                    print(e)
                    print('timeout')
                    sleep(3)
                sleep(3)
                # self.page.goto(self.url+urls[0])
            # self._read_job()
        return 'urls not found'

    def _read_job(self):
        global all_jobs
        global webs
        global queue
        global count
        global status
        sleep(3)
        print('read job')
        selector_job_title = self.config['job_page']['job_title']
        selector_company_name = self.config['job_page']['company_name']
        selector_email = self.config['job_page']['email']
        selector_city = self.config['job_page']['city']
        selector_posted_by = self.config['job_page']['posted_by']

        html = self.page.inner_html('html')
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        soup2 = etree.HTML(str(soup))
        try:
            job_title = soup.select_one(selector_job_title)
        except Exception as e:
            job_title = soup2.xpath(selector_job_title)[0]

        try:
            company_name = soup.select_one(selector_company_name)
        except:
            company_name = soup2.xpath(selector_company_name)[0]
        email = soup.select_one(selector_email)
        city = soup.select_one(selector_city)
        posted_by = soup.select_one(selector_posted_by)

        data = {
            'job_title': job_title,
            'company_name': company_name,
            'email': email,
            'posted_by': posted_by,
            'city': city
        }
        # print(data)
        for k, v in data.items():
            if v is not None:
                value = v.text.replace('\n', ' ')
                value = ' '.join(value.split())
                # print(value)
                data[k] = value.replace(',', ' ')
            else:
                data[k] = 'None'
        # self.jobs_data.append(data)
        print(data)
        if data not in all_jobs:
            queue.append(data)

            all_jobs.append(data)

    def _close_noti(self):
        if 'noti' in self.config:
            print('close notifiation')
            selector_button = self.config['noti']['button']
            try:
                self.page.click(selector_button, delay=5.0)
            except:
                print('no noti')

    def login(self):
        print('login to the account')
        email_field = self.config['login']['email_field']
        password_filed = self.config['login']['password_field']
        login_button = self.config['login']['login_button']

        print('entering email')
        self.page.fill(email_field, self.email)
        print('entering password')
        self.page.fill(password_filed, self.password)
        self.page.click(login_button)
        sleep(5)

    def _search_job(self):
        print('search for job')
        job_title = self.keyword
        print(self.config['search_page'])
        try:
            if self.config['search_page']['url_search'] == True:
                job_title2 = self.keyword.replace(" ", "+")
                self.page.goto(self.url + "/jobs/suche?q=" + job_title2 + "&where=")
                return
        except:
            pass
        selector_input = self.config['search_page']['input_field']
        selector_job = ''
        if 'select_job' in self.config['search_page']:
            selector_job = self.config['search_page']['select_job']

        if 'search_button' in self.config['search_page']:
            selector_button = self.config['search_page']['search_button']

        if 'goto_job' in self.config['search_page']:
            print('click on job')
            self.page.goto(self.config['search_page']['goto_job'])
            self.page.wait_for_load_state()

        sleep(5)
        print('inputing jobtitle')
        self.page.fill(selector_input, job_title)
        sleep(3)
        if 'press_enter' in self.config['search_page']:
            print('press enter')
            self.page.keyboard.press('Enter')
        else:
            self.page.click(selector_button)
        if selector_job:
            print('click job')
            sleep(5)
            self.page.click(selector_job, delay=5)
        sleep(5)

    def _accept_cookies(self):
        print(self.config['name'])
        if self.config['name'] == 'arbeitsagentur':
            self.page.keyboard.press('Enter')
        if self.config['name'] == 'karriere':
            self.page.click('body', delay=3)
            sleep(3)
            self.page.keyboard.press('Tab')
            sleep(1)
            self.page.keyboard.press('Tab')
            self.page.keyboard.press('Enter')
            return
        if 'accept_cookies' in self.config:
            print('acceept cookies')
            selector_input = self.config['accept_cookies']['accept']
            try:
                self.page.click(selector_input, delay=1)
                return
            except:
                print('no cookies')
                return
            try:
                self.page.keyboard.press('Tab')
                sleep(4)
                self.page.keyboard.press('Enter')
                # sleep(4)
            except Exception as e:
                print(e)
                print("no cookies")

    def click_on_more2(self, button):
        selector_results = self.config['result_page']['results_container']
        selector_links = self.config['result_page']['links']

        print('parsing jobs links')
        urls = []
        self.page.wait_for_load_state()
        is_buttion_exist = self.page.query_selector(button)
        print('clicking on more button')
        cc = self.config['next_page_button_1']['max_clicks']
        while cc != 0:
            try:
                self.page.click(button)
                self.page.wait_for_load_state()
                html = self.page.inner_html(selector_results)
                soup = BeautifulSoup(html, 'html.parser')
                pre_html = ''

                d = soup.select(selector_links)
                for el in d:
                    try:
                        if not el.attrs['href'] == 'javascript:void(0)':
                            href = el.attrs['href']
                            urls.append(href)
                    except:
                        print('href not found')
                cc -= 1
                print(urls)
            except Exception as e:
                print(e)
                break
            sleep(5)
            is_buttion_exist = self.page.query_selector(button)
        if urls:
            print(len(urls), 'jobs found')
            print(urls)
        else:
            print('no jobs found')
        return urls

    def click_on_more(self, button):
        urls = []
        selector_results = self.config['result_page']['results_container']
        selector_links = self.config['result_page']['links']
        is_buttion_exist = self.page.query_selector(button)
        print('clicking on more button')
        cc = self.config['next_page_button']['max_clicks']
        for i in range(0, 100):
            self.page.keyboard.press("ArrowDown")
        while cc != 0:
            try:
                self.page.click(button)
                self.page.wait_for_load_state()
                cc -= 1
            except Exception as e:
                print(e)
                break
            sleep(5)
            is_buttion_exist = self.page.query_selector(button)

    def scroll(self):
        self.page.evaluate(
            """
            var intervalID = setInterval(function () {
                var scrollingElement = (document.scrollingElement || document.body);
                scrollingElement.scrollTop = scrollingElement.scrollHeight;
            }, 200);

            """
        )
        prev_height = None
        while True:
            curr_height = self.page.evaluate('(window.innerHeight + window.scrollY)')
            if not prev_height:
                prev_height = curr_height
                sleep(1)
            elif prev_height == curr_height:
                self.page.evaluate('clearInterval(intervalID)')
                break
            else:
                prev_height = curr_height
                sleep(1)

    def _parse_html(self):
        selector_results = self.config['result_page']['results_container']
        selector_links = self.config['result_page']['links']

        print('parsing jobs links')
        urls = []
        self.page.wait_for_load_state()
        sleep(10)
        if 'next_page_button_1' in self.config:
            if 'scroll' in self.config:
                px = 0
                click = 0
                self.page.keyboard.press("PageDown")
                while px < 100:
                    self.page.click(self.config['scroll']['scroll_container'])
                    self.page.keyboard.press("ArrowDown")
                    print('scroling')
                    px += 1
                if True:
                    sleep(3)
                    button = self.config['next_page_button']['next_button']
                    self.click_on_more(button)
                    click += 1

            else:
                print('press more button')
                button = self.config['next_page_button_1']['next_button']
                urls = self.click_on_more2(button)
                return urls
        if 'next_page_button' in self.config:
            if 'scroll' in self.config:
                px = 0
                click = 0
                self.page.keyboard.press("PageDown")
                while px < 200:
                    self.page.click(self.config['scroll']['scroll_container'])
                    self.page.keyboard.press("ArrowDown")
                    print('scroling')
                    px += 1
                if True:
                    sleep(3)
                    button = self.config['next_page_button']['next_button']
                    self.click_on_more(button)
                    click += 1

            else:
                print('press more button')
                button = self.config['next_page_button']['next_button']
                urls = self.click_on_more(button)
                return urls
        if 'next_page_url' in self.config:
            page_num = 25
            print('here')
            while True:
                sleep(5)
                self.page.wait_for_load_state()
                html = self.page.inner_html(selector_results)
                soup = BeautifulSoup(html, 'html.parser')
                d = soup.select(selector_links)
                if not d:
                    break
                i = 0
                while i < len(d):
                    try:
                        href = d[i].attrs['href']
                        if href in urls:
                            break
                        urls.append(href)
                    except:
                        print('href not found')
                    i += 1
                sleep(2)
                next_url = f"{self.config['next_page_url']}+{self.keyword}&start={page_num}"
                self.page.goto(next_url)
                self.page.wait_for_load_state()
                page_num += 25

        self.page.wait_for_load_state()
        html = self.page.inner_html(selector_results)
        soup = BeautifulSoup(html, 'html.parser')
        pre_html = ''
        if 'next_page' in self.config['result_page']:
            selector_next_page = self.config['result_page']['next_page']
            next_page = soup.select(selector_next_page)
            print(next_page)
            next_count = 0
            while True:
                if not next_page:
                    break
                next_count += 1
                if next_count == 20:
                    break
                sleep(5)
                html = self.page.inner_html(selector_results)
                soup = BeautifulSoup(html, 'html.parser')
                next_page = soup.select(selector_next_page)
                print('extracing links')
                d = soup.select(selector_links)
                for el in d:
                    try:
                        href = el.attrs['href']
                        urls.append(href)
                    except:
                        print('href not found')
                print('click on next button')
                sleep(1)
                try:
                    if not self.page.is_disabled(selector_next_page):
                        print('clicking on next page')
                        self.page.click(selector_next_page)
                        sleep(2)
                        if html == pre_html:
                            break
                    else:
                        break
                except Exception as e:
                    print(e)
                    break
                pre_html = html
        else:
            print('i am running')
            # print(selector_links)
            d = soup.select(selector_links)
            for el in d:
                try:
                    if not el.attrs['href'] == 'javascript:void(0)':
                        href = el.attrs['href']
                        urls.append(href)
                except:
                    print('href not found')
        if urls:
            print(len(urls), 'jobs found')
            print(urls)
        else:
            print('no jobs found')
        return urls


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        # self.ui = Ui_MainWindow()
        self.setWindowTitle('Scraper')

        # self.ui.setupUi(self)
        # self.ui.pushButton.clicked.connect(self.start)

        # self.show()

    def create_csv_file(self):
        filename = 'DATA SCRAPED.csv'
        # self.filepath = f'./{filename}'
        with open(filename, 'w', encoding='utf-8') as f:
            headers = ['job_title', 'company_name', 'email', 'city', 'posted_by']
            csv_writer = DictWriter(f, fieldnames=headers)
            csv_writer.writeheader()
            f.close()

    def write_csv(self, data):
        strr = ""
        filename = 'DATA SCRAPED.csv'
        with open(filename, 'a', encoding='utf-8') as f:
            headers = ['job_title', 'company_name', 'email', 'city', 'posted_by']
            csv_writer = DictWriter(f, fieldnames=headers)
            if data['job_title'] != "None":
                print("writing data")
                print(data)
                if data["email"] == "None":
                    query = data["company_name"] + " email"
                    print(query)
                    links = []
                    for j in search(query):
                        links.append(j)

                    EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
                    session = HTMLSession()
                    email_count = 0
                    for url in links:
                        if email_count == 6:
                            break
                        r = session.get(url)

                        for re_match in re.finditer(EMAIL_REGEX, r.text):
                            # print(re_match.group())
                            strr += re_match.group() + "\n"
                        email_count += 1
                    data["email"] = strr
                    print("email donee")
                try:
                    csv_writer.writerow(data)
                except Exception as e:
                    print(e)
                print("row writted")
                f.close()
        print(f'new data job to {filename}')

    def manage_queue(self):
        global webs
        global queue
        global count
        global status
        global queue_count
        print("queue started")

        while True:

            if status == True:
                if True:
                    try:
                        data = queue[0]
                        queue_count.append(0)
                        queue.pop(0)
                        self.write_csv(data)
                        # print(data)
                        # queue_count.pop(0)
                    except Exception as e:
                        # print(e)
                        pass

            if status == False:
                break

    def start(self):
        global webs
        global queue
        global count
        global status
        obj = scraper = JobScraper(url=web_config['job_indeed']['web_url'], keyword=keywordd,
                                 config=web_config['job_indeed'])
        webs.append(obj)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    keywordd=input(print("Enter key word to search on indeed/n"))

    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
    breakk = True

