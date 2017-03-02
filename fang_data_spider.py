import re
import xlrd
import requests
import  xlsxwriter
from bs4 import BeautifulSoup

# 获取房源详细页的URL并去重
fname = 'room_url.xlsx'
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
sh = bk.sheet_by_name('Sheet1')
nrows = sh.nrows
ncols = sh.ncols
room_url_list = []
for i in range(1, nrows):
    room_url = sh.row_values(i)[1]
    # print(row_data_url)
    room_url_list.append(room_url)
room_url_set = set(room_url_list)
# print(len(room_url_set))
# print(room_url_set)
def get_room_data(room_url):

    data = requests.get(room_url).text
    soup = BeautifulSoup(data, 'lxml')
    try:
        #获取名称
        name = soup.find('div',{"class":"title"}).get_text()
        na_p = re.compile('\s+')
        name = re.sub(na_p,'',name)
        # print(name)
        worksheet.write(i,0,name)
        #获取房价
        price = soup.find('dt', {'class':"gray6 zongjia1"}).find('span',{'class':'red20b'}).get_text()
        # print(price)
        worksheet.write(i,1,price)
        #获取户型
        house_type = soup.find('dd',{'class':"gray6"}).get_text()[3:]
        # print(house_type)
        worksheet.write(i,2,house_type)
        #获取面积
        area = soup.find_all('dd',{'class':"gray6"})[1].get_text()[5:][:-2]
        # print(area)
        worksheet.write(i,3,area)
    except:
        pass
    try:

    #获取手机号码
        phone = soup.find("div",{"class":"phone_top"}).find('p').find("label", {"id":"mobilecode"}).get_text()
        # print(phone)
        worksheet.write(i,4,phone)
        #获取年代
        age = soup.find('div',{'class':"inforTxt"}).find_all('dl')[1].find('dd').get_text()[4:]
        # print(age)
        worksheet.write(i,5,age)
        #朝向
        toward = soup.find('div',{'class':"inforTxt"}).find_all('dl')[1].find_all('dd')[1].get_text()[4:]
        # print(toward)
        worksheet.write(i,6,toward)
        #楼层
        floor = soup.find('div',{'class':"inforTxt"}).find_all('dl')[1].find_all('dd')[2].get_text()[4:]
        # print(floor)
        worksheet.write(i,7,floor)
        #结构
        structure = soup.find('div',{'class':"inforTxt"}).find_all('dl')[1].find_all('dd')[3].get_text()[4:]
        # print(structure)
        worksheet.write(i,8,structure)
    except:
        pass
    try:

        #楼盘名称
        name_p = soup.find('div',{'class':"inforTxt"}).find_all('dl')[1].find('dt').get_text()
        # name_p = name_p.replace(' ','').strip('\n')
        p=re.compile('\s+')
        name_p = re.sub(p,'',name_p)[5:][:-6]
        # print(name_p)
        worksheet.write(i,9,name_p)
        #学校
        school = soup.find('div',{'class':"inforTxt"}).find_all('dl')[1].find_all('dt')[1].get_text()[4:]
        # print(school)
        worksheet.write(i,10,school)
        #配套设施
        fac = soup.find('div',{'class':"inforTxt"}).find_all('dl')[1].find_all('dt')[2].get_text()[5:]
        # print(fac)
        worksheet.write(i,11,fac)
    except:
        pass
    i += 1
    global i

workbook = xlsxwriter.Workbook('room_data.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:A', 100)#name
worksheet.set_column('B:B', 10)#price
worksheet.set_column('C:C', 20)#type
worksheet.set_column('D:D', 10)#area
worksheet.set_column('E:E', 20)#phone
worksheet.set_column('F:F', 10)#age
worksheet.set_column('G:G', 10)#toward
worksheet.set_column('H:H', 10)#floor
worksheet.set_column('I:I', 10)#structure
worksheet.set_column('J:J', 50)#name_p
worksheet.set_column('K:K', 20)#school
worksheet.set_column('L:L', 20)#fac
i = 0

# room_url_set = {'http://esf.hf.fang.com/chushou/3_226885831.htm'}
for room_url in room_url_set:
    try:
        # print(i)
        get_room_data(room_url)
        print("success-->"+str(room_url))
    except:
        print("fail..."+str(room_url))
        pass

workbook.close()
