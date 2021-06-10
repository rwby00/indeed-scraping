from selenium import webdriver
import pandas as pd 
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
driver = webdriver.Chrome("./chromedriver")


df = pd.DataFrame(columns=["Title","Location","Company","Salary","Sponsored","Description"])

for i in range(200,450,15):
	driver.get('https://jp.indeed.com/%E6%B1%82%E4%BA%BA?q=%E3%83%90%E3%82%A4%E3%83%88&l=%E6%B2%96%E7%B8%84%E7%9C%8C&start='+str(i))
	jobs = []
	driver.implicitly_wait(4)
	

	for job in driver.find_elements_by_class_name('result'):

		soup = BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
		
		try:
			title = soup.find("a",class_="jobtitle").text.replace("\n","").strip()
			
		except:
			title = 'None'

		try:
			location = soup.find(class_="location").text
		except:
			location = 'None'

		try:
			company = soup.find(class_="company").text.replace("\n","").strip()
		except:
			company = 'None'

		try:
			salary = soup.find(class_="salary").text.replace("\n","").strip()
		except:
			salary = 'None'

		try:
			sponsored = soup.find(class_="sponsoredGray").text
			sponsored = "Sponsored"
		except:
			sponsored = "Organic"				

		
		sum_div = job.find_element_by_xpath('./div[3]')
		try:
			sum_div.click()
		except:
			close_button = driver.find_elements_by_class_name('popover-x-button-close')[0]
			close_button.click()
			sum_div.click()	
		job_desc = driver.find_element_by_id('vjs-desc').text

		df = df.append({'Title':title,'Location':location,"Company":company,"Salary":salary,
						"Sponsored":sponsored,"Description":job_desc},ignore_index=True)

		print("Got these many results:",df.shape)


df.to_csv("Indeed_Okinawa_Baito_10_30.csv",index=False)	