import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import MySQLdb

now = datetime.datetime.now()

# 获取网页数据，并解析网页
def get_save_url(url, headers):
	html = requests.get(url, headers=headers)
	if html.status_code == 200:
		print("网页" + url + "已经打开")
	soup = BeautifulSoup(html.text, 'lxml')
	global soup
	html = html.text
	global html
	get_post_fact_city_num(soup,html)
	print("正在抓取第"+pagenum+"页的职位信息")
	



def get_post_fact_city_num(soupx,htmlx):

	l_post_name = []
	l_fact_name = []
	l_city_name = []
	l_num = []
	l_lab = []
	l_post_time = []
	l_now_time = []
	regex = "__ga__fullResult(.*)postname_clicksfullresult(.*)postnames_001"
	posts = soup.findAll("a", {"class":re.compile(regex)}) 
	for post in posts[::2]:		
		post = post.get_text()
		#print(post)
		l_post_name.append(post)
	facts = soup.findAll("p", {"class":"searchResultCompanyname"})

	for fact in facts[::2]:
		fact = fact.get_text()
		l_fact_name.append(fact)

	cities = soup.findAll("em", {"class":"searchResultJobCityval"})
	for city in cities[::2]:

		city = city.get_text()
		l_city_name.append(city)
	
	nums = soup.findAll("em", {"class":"searchResultJobPeopnum"})
	for num in nums:
		num = num.get_text()
		l_num.append(num)
	#print("nums: "+str(inums))
	labs = soup.findAll("p", {"class":"searchResultCompanyIndustry"})

	for lab in labs:
		lab = lab.get_text()
		l_lab.append(lab)

	time_regex = "<span>发布时间\：<em></em>(.*)</span>"
	time_pa = re.compile(time_regex)
	times = re.findall(time_pa,html) 
	itimes = 1
	for time in times:
		l_post_time.append(time)

	save_to_sql(l_post_name,l_fact_name,l_city_name,l_num,l_lab,l_post_time)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"}

# 这里页数可以在搜索结果包含的范围内任意设置
urls = ["http://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_%E7%BB%9F%E8%AE%A1_{}_0".format(str(x)) for x in range(2, 920)]
#url = "http://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_%E7%BB%9F%E8%AE%A1_2_0"
db = MySQLdb.connect(host="localhost", user="root", passwd="数据库密码",db="test",use_unicode=True,charset="utf8")
cursor = db.cursor()

# 这里注意字符的大小尽量大，有些公司介绍比较长。。。
sqlxx = """CREATE TABLE zhilian_tongjix(
		post_name VARCHAR(100),
		fact_name VARCHAR(100),
		city_name VARCHAR(20),
		num VARCHAR(50),
		lab VARCHAR(200),
		post_time VARCHAR(50),
		now_time VARCHAR(50)
		) """

cursor.execute(sqlxx)

def save_to_sql(l_post_name,l_fact_name,l_city_name,l_num,l_lab,l_post_time):
	now_time = datetime.datetime.now()
	sql = """INSERT INTO zhilian_tongjix\
	   SET post_name=%s, fact_name=%s, city_name=%s, num=%s, lab=%s, post_time=%s, now_time=%s"""
	for x in range(0,len(l_post_name)):
		#print(len(l_post_name))
		#print(x)
		#print(l_fact_name)
		cursor.execute(sql,(l_post_name[x],l_fact_name[x],l_city_name[x],l_num[x],l_lab[x],l_post_time[x],now_time))
		db.commit()
	print("抓取成功，已存入数据库！")

for url in urls:
	try:
		time.sleep(1)
		pagenum = url.split("_")[-2]
		get_save_url(url=url,headers=headers)
	except:
		print("第 "+str(pagenum)+" 失败...")
		pass
db.close()
print("大功告成！！！")

