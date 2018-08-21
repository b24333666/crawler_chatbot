import logging
import re
import webbrowser

import MySQLdb
import pymongo
import requests
from bs4 import BeautifulSoup
from gensim import models
from gensim.models import word2vec
from pymongo import MongoClient

uri = "mongodb://localhost/" 
client = MongoClient(uri)
print(client)
db = client['text_dict_keyword']
collection = db.dict_zh_tw
zhtw_dict = collection.find()


# import chatbot_3_1

def get_combinations(string):
    combs = []
    for i in range(1, 2**len(string)):
        pat = "{0:b}".format(i).zfill(len(string))
        combs.append(''.join(c for c, b in zip(string, pat) if int(b)))
    return combs

def get_permutations2(clst):
    if len(clst)==1:
        return [clst[0]]
    results = []
    for idx, c in enumerate(clst):
        results += [c+substr for substr in get_permutations2(clst[:idx] + clst[idx+1:])]
    return results

# def option_pass(self):
#     option = self
#     user_account = input('請輸入帳戶: ')
#     user_password = input('請輸入密碼: ')
#     password = sql.confirm_account(user_account)
#     return option


class wiki_project:
    def wiki_key(self):
        keyword = self
        url = "https://zh.wikipedia.org/wiki/"

        res = requests.get(url+keyword)
        soup = BeautifulSoup(res.text,'lxml')
        article = soup.select_one(".mw-parser-output p").text
        if len(article) > 30:
            # print(article)
            return article
        elif len(article) <= 30:
            for i in range(0,len(soup)):
                article = soup.select(".mw-parser-output")[i].get_text()
                # print(article)
                return article
        else:
            return article


class google:

    def google_choice(self):
        gi = self
        # print(gi)
        # print(type(gi))
        choice = input("請選擇: ")
        user_choice = gi[int(choice)]
        # print(user_choice)
        # print(type(user_choice))
        u_link = user_choice['link']
        webbrowser.open(u_link, new=0, autoraise=True) 
        #new=0, url會在同一個 瀏覽器視窗中開啟 ; new=1，新的瀏覽器視窗會被開啟 ; new=2  新的瀏覽器tab會被開啟
        # webbrowser.open_new(u_link) 
        # webbrowser.open_new_tab(u_link)
        return u_link

    def google_search(self):
        keyword = self
        url = "https://www.google.com.tw/search?q="
        res = requests.get(url+keyword)
        soup = BeautifulSoup(res.text,'lxml')
        g_info = {}
        gs = input("搜尋連結數量:")
        for i in range(0,int(gs)):
            a_title = soup.select(".r a")[i].text
            o_link = soup.select('.r a')[i]
            a_link0 = o_link.get('href')
            a_link = re.search (r'([https].*?:\/\/\w.*\/)',a_link0)
            if a_link:
                # return a_title,a_link.group(0)
                # print(a_link.group(0)) #連結取得
                # print(a_title)
                a_link = a_link.group(0)
                google_i = {i+1:{"title":a_title,"link":a_link}}
                print(google_i) #列出選項
            g_info[i+1] = {"title":a_title,"link":a_link}

        return g_info


    def youtube_choice(self):
        y_info = self
        choice = input("請選擇: ")
        user_choice = y_info[int(choice)]
        # print(type(user_choice))
        u_link = user_choice['link']
        webbrowser.open(u_link, new=0, autoraise=True) #new=0, url會在同一個 瀏覽器視窗中開啟 ; new=1，新的瀏覽器視窗會被開啟 ; new=2  新的瀏覽器tab會被開啟
        # webbrowser.open_new(u_link) 
        # webbrowser.open_new_tab(u_link)
        # print(u_link)
        # print(type(u_link))
        return u_link

    def youtube_serach(self):
        keyword = self
        url = "https://www.youtube.com/results?search_query="
        res = requests.get(url+keyword)
        soup = BeautifulSoup(res.text,'html.parser')
        y_info = {}
        gi = input('搜尋多少影片')
        
        for i in range(0,int(gi)):
            a_title_1 = soup.select(".yt-uix-tile-link")[i].text
            a_link = soup.select(".yt-uix-tile-link")[i]
            ylink = a_link.get('href')
            youlink = 'https://www.youtube.com' + ylink 
            youtube_i = {i+1:{"title":a_title_1,"link":youlink}}
            print(youtube_i) #列出選項
            y_info[i+1] = {"title":a_title_1,"link":youlink}
        return y_info
        # print(y_info)
       

class yahoo:
    def yahoo_choice(self):
        yahoo_info = self
        choice = input("請選擇: ")
        user_choice = yahoo_info[int(choice)]
        # print(user_choice)
        # print(type(user_choice))
        u_link = user_choice['yahoo_title_link']
        webbrowser.open(u_link, new=0, autoraise=True) 


    def yahoo_news(self):
        url = self
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'html.parser')
        yahoo_news_title_info = {}
        title_lenth = soup.select(".nr-applet-main-nav-item") 
        for i in range(0,len(title_lenth)):
            yahoo_title_1 = soup.select(".nr-applet-nav-item")[i].text
            a_link = soup.select(".nr-applet-nav-item")[i]
            yahoo_title_link = a_link.get('href')
            # print(yahoo_title_1)
            # print(yahoo_link) 
            if yahoo_title_link :
                yahoo_news = {i+1:{'class_title':yahoo_title_1,'yahoo_title_link':yahoo_title_link}}
                print(yahoo_news)# 列選項
            yahoo_news_title_info[i+1] = {'class_title':yahoo_title_1,'yahoo_title_link':yahoo_title_link}
        return yahoo_news_title_info


class money:
    def exchange(self):
        exchange = str(self)
        exchange = exchange.upper()
        url = "http://www.taiwanrate.org/exchange_rate.php?c=" + exchange
        res = requests.get(url)
        res.encoding = 'utf-8'
        # soup = BeautifulSoup(res.text,'lxml')
        soup = BeautifulSoup(res.text,'html.parser')
        # print(soup)
        ch = input('請問要即期還是現金: ')
        if ch == "即期" or ch == "即期匯率":
            for i in range(0,19):
                bank_name = soup.select("#accounts a")[i].text
                print(bank_name)
                for i in range(0,57,1):
                    bank_buy_sale = soup.select("#accounts td")[i].text
                    print(bank_buy_sale)
        elif ch == "現金" or ch == "現金匯率":
            for i in range(0,19): #19間銀行
                bank_name = soup.select("#accounts2 a")[i].text
                print(bank_name)
                for i in range(0,57,1):
                    bank_buy_sale = soup.select("#accounts2 td")[i].text
                    print(bank_buy_sale)
        
        else:
            pass


class sql:

    def sales_sql(self):
        productsname = self
        productset = {}
        db = MySQLdb.connect(host="localhost",user="root", passwd="root", db="unmannedstore",charset='utf8')
        cursor = db.cursor()
        sql = "SELECT * FROM unmannedstore.products where ProductName like '" + productsname + "';"
        cursor.execute(sql)
        rc = cursor.fetchone()        
        rc = list(rc)
        productset = {'title':rc[1],'price':rc[2]}
        for i in range(0,len(productset)):
            productset_totle = {i:rc[2]}
            return productset,productset_totle 
    
    def mysql_user_banlance(self):
        accounts = self
        db = MySQLdb.connect(host="localhost",user="root", passwd="root", db="unmannedstore",charset='utf8')
        cursor = db.cursor()
        sql = "SELECT * FROM unmannedstore.member where Account like '" + accounts + "'; "
        cursor.execute(sql)
        user_balance = cursor.fetchone()
        return user_balance[0],user_balance[1],user_balance[4]

    def mysql_create_user(self):
        accounts = self
        db = MySQLdb.connect(host="localhost",user="root", passwd="root", db="unmannedstore",charset='utf8')
        cursor = db.cursor()
        sql = "INSERT INTO unmannedstore.member (member.Account,member.Password,member.UserName,member.Balance,member.PhoneNumber,member.Address) values ('" + accounts + "'); "
        print(sql)
        cursor.execute(sql)
        db.commit()
        db.close()
        # return cursor

    def confirm_account(self):
        accounts = self
        db = MySQLdb.connect(host="localhost",user="root", passwd="root", db="unmannedstore",charset='utf8')
        cursor = db.cursor()
        sql = "SELECT * FROM unmannedstore.member where Account like '" + accounts + "'; "
        cursor.execute(sql)
        user = cursor.fetchone()
        return user[2]


class op:
    def balance():
        try:
            user_account = input('請輸入帳戶: ')
            user_password = input('請輸入密碼: ')
            password = sql.confirm_account(user_account)
            while password == user_password:
                user_balance = sql.mysql_user_banlance(user_account)
                # totle = sql.sales_sql(name[i]) #要放購買紀錄
                # user_b = user_balance[2] - totle[1][0]
                # account = "ID: " + str(user_balance[0]) +  " 會員帳戶: " + str(user_balance[1]) + " 目前餘額: " + str(user_b)
                account = "ID: " + str(user_balance[0]) +  " 會員帳戶: " + str(user_balance[1]) + " 目前餘額: " + str(user_balance[2])
                return account
            
            else :
                # pass
                keyword = input('密碼錯誤!!請再嘗試一次 按 "q" 離開 或 按Enter繼續\n')
                while keyword =="離開" or keyword.lower() == "exit" or keyword.lower() == "q":
                    break
                else:
                    op.balance()

            
        except TypeError:
            print('找不到此帳戶!!請再重新輸入一次<(=_=)>')
            op.balance()

    def Checkout():
        totle_p = []
        allp = []
        name = ["雪碧","茶裏王","衛生紙"]
        Quantity = [2,1,2]
        for i in range(0,len(name)):
            productsprice =  sql.sales_sql(name[i])
            products_info = productsprice[0]
            products_p = int(productsprice[1][0])
            totle_p.append(products_p)
            all_p = products_p * Quantity[i]
            allp.append(all_p)
            print("本次購買品項為: 品名: "+str(products_info['title']) +"\t單價: " + str(products_info['price']) + " 數量: " + str(Quantity[i]) + "\t小計: " + str(all_p) )
        print("==========================================================")
        at = sum(allp)
        t = "總計: " + str(sum(allp)) + "元整"
        return t,at

    def account_updata(self): #要與帳戶作連結
        updata = self
        db = MySQLdb.connect(host="localhost",user="root", passwd="root", db="unmannedstore",charset='utf8')
        cursor = db.cursor()
        sql = "SELECT * FROM unmannedstore.member where Account like '" + updata + "'; "
        ce = cursor.execute(sql)
        user_b = ce[4] - op.Checkout[1]
        sql = "UPDATA unmannedstore.member SET Balance = " + user_b + "; "
        ce = cursor.execute(sql)
        return user_b

class weather:
    def city_weather(url):
        city = {}
        index = "/V7/index.htm"
        n_url = url + index
        html = requests.get(n_url)
        html.encoding = "utf-8"
        soup = BeautifulSoup(html.text,"lxml")
        county = soup.select("#divTitle a")
        for i in range(0,len(county)):
            city_weather = county[i]
            city_name = city_weather.text
            city_link = city_weather.get("href")
            # if city_link:
            #     city1 = {'county':city_name,"city_link":city_link}
                # print(city1)
            city[city_name] = city_link
        # print(city["基隆市"])
        # search = input("查詢縣市名:")
        print("查詢縣市名:")
        # search = speech_input()
        # search = "臺北市"
        if search in city.keys():
            new_url = url + city[search]
            # print("錯誤"+new_url)
            # print("正確"+"https://www.cwb.gov.tw/V7/forecast/taiwan/Taipei_City.htm")
            return new_url
        else:
            print("查詢失敗!!沒有此縣市")
            city_weather()


    def c_status(city_link):
        # print(type(city_link))
        html = requests.get(city_link)
        html.encoding = "utf-8"
        soup = BeautifulSoup(html.text,"lxml")
        # print(soup)
        html_table = soup.select(".FcstBoxTable01")
        # print(type(html_table))
        th_title = []
        status = []
        c_status =[]
        for table in html_table:
            for tb_img_title in table.find_all("th"):
                th_text = tb_img_title.text
                # print(th_text)
                th_title.append(th_text)
            for td_tr in table.find_all("td"):
                td_text = td_tr.text
                # print(td_text)
                status.append(td_text)
            for td_tr in table.find_all("img"):
                td_img = td_tr.get("alt")
                # print(td_img)
                c_status.append(td_img)
        status.remove("\n")
        status.remove("\n")
        status.remove("\n")
        status.insert(0," ")
        
        th_title[1] = "溫度"
        th_title[4] = "降雨機率"
        th_title[5] = "今日白天"
        th_title[6] = "今晚至明晨"
        th_title[7] = "明天白天"
        th_title[9] = "最高溫"
        th_title[10] = "最低溫"
        th_title[11] = "降雨量"
        # print(th_title)
        # print("========================")
        # print(status)
        # print("=========================")
        # print(c_status)
        county = th_title[0]
        am_county = {th_title[5]:{th_title[1]:status[1],th_title[2]:c_status[0],th_title[3]:status[2],th_title[4]:status[3]}}
        pm_county = {th_title[6]:{th_title[1]:status[4],th_title[2]:c_status[1],th_title[3]:status[5],th_title[4]:status[6]}}
        tm_county = {th_title[7]:{th_title[1]:status[7],th_title[2]:c_status[2],th_title[3]:status[8],th_title[4]:status[9]}}
        m = {th_title[8]:{th_title[9]:status[10],th_title[10]:status[11],th_title[11]:status[12]}}
        
        # print(am_county)
        # print(pm_county)
        # print(tm_county)
        # print(m)
        return am_county,pm_county,tm_county,m,county

wi_ki_zh_name = ["維基"]
wi_ki_zh_key  = get_permutations2(wi_ki_zh_name)
wi_ki_en_name = ['wiki']
wi_ki_en_key = get_permutations2(wi_ki_en_name)
wi_ki_key = wi_ki_en_key + wi_ki_zh_key


google_zh_name = ["谷歌"]
google_zh_key  = get_permutations2(google_zh_name)
google_en_name = ['google']
google_en_key = get_permutations2(google_en_name)
google_key = google_en_key+ google_zh_key

weather_zh_key = ['查','查詢','天氣']
weather_zh_key = get_permutations2(weather_zh_key)+get_combinations(weather_zh_key)
weather_en_key = ["weather"]
weather_en_key = get_permutations2(weather_en_key)+get_combinations(weather_en_key)
weather_key = weather_en_key+weather_zh_key

dict_zh_name = ["字典"]
dict_zh_key  = get_permutations2(dict_zh_name)
dict_en_name = ['dictionary'] 
dict_en_key = get_permutations2(dict_en_name)
dict_key = dict_en_key + dict_zh_key + ['dict']
# print(dict_key)
    


exchange_zh_name = ["匯率"]
exchange_zh_key  = get_permutations2(exchange_zh_name)
exchange_en_name = ['exchange']
exchange_en_key = get_permutations2(exchange_en_name)
exchange_key = exchange_en_key + exchange_zh_key


yahoo_news_zh_name = ['新聞','奇摩']
yahoo_news_zh_key = get_permutations2(yahoo_news_zh_name)
yahoo_news_en_name = ["news",'yahoo']
yahoo_news_en_key = get_permutations2(yahoo_news_en_name)
yahoo_news_key = yahoo_news_en_key+yahoo_news_zh_key
# print(yahoo_news_key)


def search(i):
    try:
        while i =="離開" or i.lower() == "exit" or i.lower() == "q":
            print("歡迎下次再來")
            break
        else: 
            # print(dict_en_key)
            # print(dict_zh_key)
            # if i == "維基" or i.lower() =='wiki' or i == "維基百科":
            if i.lower() in wi_ki_key:
                print("歡迎來到維基百科")
                keyword = input("你想要找的{}: ".format('事物')) # 要實現搜尋特定資料Function
                while keyword =="離開" or keyword.lower() == "exit" or keyword.lower() == "q":
                    print("歡迎下次再來")
                    break
                else:
                    i = wiki_project.wiki_key(keyword)
                    # print(i)
                    return i

            elif i.lower() in google_key:
                print("Google 歡迎您")
                keyword = input("你想要找的{}: ".format('事物')) # 要實現輸入於mongodb上的搜尋紀錄
                while keyword =="離開" or keyword.lower() == "exit" or keyword.lower() == "q":
                    print("歡迎下次再來")
                    break
                else:
                    i = google.google_search(keyword)
                    g_choice = google.google_choice(i)
                    # print(i)
                    return g_choice
            
            elif i.lower() == "youtube":
                print("YouTube 歡迎您")
                keyword = input("你想要找的{}: ".format('影片')) # 要實現把youtube加入我的最愛 紀錄於mongodb上
                while keyword =="離開" or keyword.lower() == "exit" or keyword.lower() == "q":
                    print("歡迎下次再來")
                    break
                else:
                    i = google.youtube_serach(keyword)
                    user_choice = google.youtube_choice(i)
                    # print(type(user_choice))
                    return user_choice
                

            elif i.lower() in weather_key:
                print("Welcome weather")
                url = "https://www.cwb.gov.tw"
                city_link = weather.city_weather(url)
                status = weather.c_status(city_link)
                try:
                    # q = input("請問要查詢 '今日白天' '今晚至明晨' 還是 '明天白天' 的天氣:")
                    print("請問要查詢 '今日白天' '今晚至明晨' 還是 '明天白天' 的天氣:")
                    # q = speech_input()
                    d = {"今日白天":0,"今晚至明晨":1,"明天白天":2}
                    bot_say ="您查詢的縣市為" + str(status[4]) + "溫度範圍為" + str(status[d[q]][q]["溫度"]) + "℃ " + ",天氣狀況大概是" + str(status[d[q]][q]["天氣狀況"]) + ",感覺" + str(status[d[q]][q]["舒適度"]) + ',降雨機率大約有 ' + str(status[d[q]][q]["降雨機率"]+"左右。")
                    return bot_say   
                
                except KeyError:
                    print("輸入錯誤!!請再重新輸入")

            elif i.lower() in exchange_key:
                print("歡迎光臨 Bank~!")
                keyword = input("請輸入{}: ".format('幣別')) # 要實現圖片輸出並記錄每天價格
                while keyword =="離開" or keyword.lower() == "exit" or keyword.lower() == "q":
                    print("歡迎下次再來")
                    break
                else:
                    i = money.exchange(keyword)
                    # print(i)
                    return i

            elif i.lower() in dict_key:
                st = input("查詢字(成語): ")
                zd = collection.find({"text":st})
                print(type(zd))
                return zd

            elif i == "結帳" or i.lower() == "Checkout":
                r = op.Checkout()
                return r[0]


            elif i == "餘額" or i.lower() == "Balance":
                op.balance()


            elif i == "新增會員" or i.lower() == "createuser":
                user_account1 = input('帳號: ')
                user_account2 = input('密碼: ')
                user_account3 = input('姓名: ')
                user_account4 = input('額度: ')
                user_account5 = input('行動電話: ')
                user_account6 = input('聯絡地址: ')
                user_account = str(user_account1) + "','" + str(user_account2) + "','" +  str(user_account3) + "','" + str(user_account4) + "','" +  str(user_account5) + "','" +  str(user_account6)              
                # print(user_account)
                sql.mysql_create_user(user_account)
                # print(user_info)
                create = "新增會員完成!!"
                return create

            # elif i == "購買紀錄" or i.lower() == "hitstory":
            #     user_account = input('請輸入查詢帳戶: ')
            #     user_balance = sql.mysql_user_banlance(user_account)



            elif i.lower() in yahoo_news_key:
                print("歡迎 Yahoo_News")
                # keyword = input("請輸入{}: ".format('新聞類別')) # 要實現圖片輸出並記錄每天價格
                while keyword =="離開" or keyword.lower() == "exit" or keyword.lower() == "q":
                    print("歡迎下次再來")
                    continue
                else:
                    url = "https://tw.news.yahoo.com/"
                    y = yahoo.yahoo_news(url)
                    i = yahoo.yahoo_choice(y)
                    # print(i)
                    return i


    except AttributeError :
        print("請重新輸入你要查的事物")
        search(i)
    except ValueError :
        pass





# i = input("Test請輸入: ")
# print(search(i))
