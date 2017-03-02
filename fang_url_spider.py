#coding:utf-8
import time
import requests
import xlsxwriter
from bs4 import BeautifulSoup

#获取网页源码
def get_data(url):
    data = requests.get(url)
    print(data.status_code)
    data = data.text
    # print(data)
    return data

#获取一页的房源列表，获取房源详细页面的URL
def get_roomlist(data):

    soup = BeautifulSoup(data, 'lxml')
    room_list = soup.find_all('dl', {'class':"list rel"})
    print(len(room_list))
    # print(room_list[0])
    # room_url_list = []

    for room in room_list:
        room_name = room.find('dd').find('p').find('a')['title']
        worksheet.write(i,0,room_name)
        room_url_r = room.find('dd').find('p').find('a')['href']
        room_url = "http://esf.hf.fang.com/"+str(room_url_r)
        # room_url_list.append(room_url)
        worksheet.write(i,1,room_url)
        post_time = room.find('dd').find_all('p')[3].find('span').get_text()
        # print(post_time)
        worksheet.write(i,2,post_time)
        print(str(room_name)+': '+str(room_url))
        i += 1
        global i
    #获取下一列表页的url
    next_page_r = soup.select("#PageControl1_hlk_next")
    next_page = "http://esf.hf.fang.com/"+str(next_page_r[0]["href"])
    print(next_page)
    try:
        print("------------------new page-----------------")
        new_data = get_data(next_page)
        get_roomlist(new_data)
    except:
        try:
            time.sleep(3)
            get_roomlist(new_data)
        except:
            pass


    # return room_url_list
i = 0
workbook = xlsxwriter.Workbook('room_url.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:A', 50)#name
worksheet.set_column('B:B', 50)#url
worksheet.set_column('C:C', 10)#time

data = get_data('http://esf.hf.fang.com/house-a0875/')
get_roomlist(data)
workbook.close()