from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
browser=webdriver.Firefox(executable_path = 'D:\软件（exe文件）\geckodriver.exe')
userinfo={}
for idh in range(2010000,2011000):
	userinfo['id']=idh
	browser.get('https://www.renrendai.com/loan-'+str(idh)+'.html')
	html = BeautifulSoup(browser.page_source,'html.parser')
	info = html.find('div',class_="loan-content")
	vartag= info.find('em',class_="con-font")
	userinfo['标的金额']=vartag.string
	vartag=info.find('p',class_="w205")
	userinfo['年利率']=vartag.em.string
	vartag=info.find('p',class_="w150")
	userinfo['还款期限']=vartag.em.string
	vartag=info.find_all('i',class_="loan-li-desc")
	vartag=vartag[2]
	userinfo['风险等级']=vartag.next_sibling.string
	vartag=info.find_all('i',class_="loan-li-desc")
	vartag=vartag[4]
	userinfo[vartag.string]=vartag.next_sibling.string
	vartag=info.find('div',class_="loan-box-top")
	userinfo['剩余期数']=vartag.p.span.string
	vartag=info.find('div',class_="loan-user-info")
	vartag=html.find('div',class_="loan-user-info")
	vartag=vartag.ul.find_all("li")
	size=len(vartag)
	for i in range(3,size):
		 	    userinfo[vartag[i].span.string]=vartag[i].em.string
	vartag=html.find("ul",class_='my-credit-info')	 
	vartag=vartag.find_all("li")
	vartag1=vartag[0].em.find_all("span")
	userinfo[vartag[0].span.string]=vartag1[0].string
	vartag=html.find_all("ul",class_='my-credit-info')
	vartag=vartag[0].find_all("li")
	for i in range(1,9):
			     vartag1=vartag[i].find_all("span")
			     vartag2=vartag1[1].find_all("span")
			     userinfo[vartag1[0].string]=vartag2[0].string
	vartag=html.find("table",class_='borrower-table')
	vartag=vartag.tbody
	vartag=vartag.find_all("tr")
	for item in vartag:
		vartag1=item.find_all("td")
		if vartag1[1].string=="已完成":
			userinfo[vartag1[0].string]=1
	df=pd.DataFrame(userinfo,index=[0])
	df.to_csv('data.csv',mode='a',header=False)
