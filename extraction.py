# In this restaurants name is extracted form zomato using beautiful soup and then saved that data into pickle file
# pickle file save data in binary form. 

import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
l=[]
driver=webdriver.Firefox()
for i in range(1,200):
    driver.get("https://www.zomato.com/ahmedabad/restaurants?page="+str(i))
    page = driver.page_source
    soup=BeautifulSoup(page,'lxml')
    code=soup.find_all("a",attrs={"data-result-type":"ResCard_Name"})
    for j in code:
        l.append(j.get_text().strip())
print(l)

pickle_out=open("zomatorestodata.pickle","wb")
pickle.dump(l,pickle_out,-1)
pickle_out.close()
