from selenium import webdriver

topicsearch=input("enter search")
topicsearch=topicsearch.replace(' ',"")

browser=webdriver.Chrome('chromedriver')
for i in range(1):
    elements=browser.get("https://www.google.com/search?q="+
                         topicsearch+ "&start"+str(i))
