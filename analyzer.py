# THIS IS FINAL ANALYZER

import time
import pickle
import json
from bs4 import BeautifulSoup
#USE OF SELENIUM
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#USE OF FUZZYWUZZY
from fuzzywuzzy import process
#USE OF NLTK
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
#USE OF MATPLOTLIB
import matplotlib.pyplot as plt
import os 
import shutil


#this function is use to create word form input
def create_words():
	words = []
	for x in l:
		words.extend(x.split())
	words = list(set(words))
	words.sort() 
	words = [x.lower() for x in words]
	return words


def y(k,a,w):
	x = process.extractOne(a,w)
	k.append(x[0])
	return k
		
#this function check the splling of word
def spell_checker(words):
	s = temp_name.split()
	k = []
	for a in s:
		 k = y(k,a,words)
	return k

#this function matches the created word from original list
def find_match(x,s):
	flag = 0
	for q in s:
		if q in x:
			flag = 1
		else:
			flag = 0
			break
	if ( flag == 1):
		return True
	else:
		return False

#finds restaurant name 
def find_res_name(s,k):
	z=[]
	for x in l:
		if find_match(x.lower(),s):
			z.append(x)
	user_input=process.extractOne(k,z)[0]
	return user_input

#function do the scrapping of links
def link_scrapping(user_input):
	browser.get("https://www.zomato.com/ahmedabad")
	page=None
	soup=None
	search = browser.find_element_by_id("keywords_input")
	search.send_keys(user_input)
	time.sleep(5)
	search.send_keys(Keys.RETURN)
	time.sleep(5)
	try:
		browser.find_element_by_xpath("//a[@class='ui ta-right pt10 fontsize3 zred pb10 pr10']").click()
	except:
		pass
	page = browser.page_source
	soup = BeautifulSoup(page,"lxml")
	name_dict={}
	count=0
	new = soup.find_all("a",attrs={'data-result-type':'ResCard_Name'})
	if(len(new) == 0 ):
		new = soup.find_all("a",attrs={'class':'ui large header left'}) 	
	for tag in new:
		count +=1
		if(tag.get_text().strip() == user_input):	
			name_dict.update({count:{"name":tag.text.strip(),"link":tag['href'].strip()}})
	return name_dict

#function do reviews scrapping 
def review_scrapping(name_dict):
	review_dict= {}                                                                       
	count = 0
	for x in name_dict:
		count += 1
		browser.get(name_dict[x]['link'])
		browser.find_element_by_xpath("//a[@data-sort='reviews-dd']").click()
		while True:
			try:
				browser.find_element_by_xpath("//div[@class='load-more bold ttupper tac cursor-pointer fontsize2']").click()
			except:
				break
		page = browser.page_source
		soup = BeautifulSoup(page,"lxml")
		review = []
		for tag in soup.find_all("div", attrs= {"class":"rev-text mbot0 "}):
			review.append(tag.get_text().strip())
		review_dict.update({count:{"name":soup.find("a",{"class":"ui large header left"}).text.strip(),"area":soup.find("a",{"class":"left grey-text fontsize3"}).text.strip(),"review":review}})
	return review_dict

#review is analyzed
def analyzie_review(review_dict):
	if os.path.exists('images'):
		shutil.rmtree('images')
	os.makedirs('images')
	for x in review_dict:
		reviews=[]
		for i in review_dict[x]["review"]:
			reviews.append(i.strip("Rated\xa0\n                               "))
			stop=stopwords.words("english")
			stop.extend(["\n","\xa0","/"])
			filter_data=[]
			temp=[]
			for j in reviews:
				for w in j.split():
					if w not in stop:
						temp.append(w)
				filter_data.append((" ").join(temp))
		
		filter_sentence=[]
		for m in filter_data:
			filter_sentence.extend(sent_tokenize(m))
		negative,positive,neutral=0,0,0
		for n in filter_sentence:
			if TextBlob(n).sentiment.polarity < 0:
				negative+=1
			elif TextBlob(n).sentiment.polarity==0:
				neutral+=1
			elif TextBlob(n).sentiment.polarity > 0:
				positive+=1
		labels = 'Negative','Positive','Neutral'
		sizes = [negative,positive,neutral]
		colors = ['red', 'green','lightskyblue']
		explode = ( 0, 0.1, 0)
		plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
		plt.axis('equal')
		plt.savefig('images/' + review_dict[x]["area"] + '.png') 
		plt.clf()
	print("Analyzing done all images have been saved ")


temp_name = input("Enter the restarunts to be searched : ")
with open("zomatorestodata.pickle","rb") as name:
	l= pickle.load(name)


words=create_words()
k = spell_checker(words)
user_input = find_res_name(k," ".join(k))
print(user_input)

print("Opening browser")

browser=webdriver.Firefox()

print("Scrapping for links ")

name_dict=link_scrapping(user_input)

print("Scrapping for Reviews ")

review_dict = review_scrapping(name_dict)

print("Analyzing Reviews ")

analyzie_review(review_dict)

browser.close()
