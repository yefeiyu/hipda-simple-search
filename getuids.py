from requests_html import HTMLSession
import time
import json
import sqlite3
import re
import string

conn = sqlite3.connect('titles.db')
cur = conn.cursor()

useragent = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15'}
hpsession = HTMLSession()
hpsession.headers.update(useragent)




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'






def login():
    with open('pwd.json','r') as f:
        data = json.load(f)

    USERNAME = data['USERNAME']
    PWD = data['PWD']
    loginurl = 'https://www.hi-pda.com/forum/logging.php?action=login&loginsubmit=yes&inajax=1'
    data = {'loginfield': 'username', 'username': USERNAME, 'password': PWD}

    result = hpsession.post(loginurl, data=data)
    # print(result.text)



def get_title(page):
    # fid 2:D版, 6: BS版, 59: E版
    baseurl = 'https://www.hi-pda.com/forum//forumdisplay.php?fid=2&orderby=dateline&page='
    listurl = baseurl + str(page)
    listpage = hpsession.get(listurl)
    print(listpage.status_code)
    titletrs = listpage.html.find('table.datatable tbody tr')



    for titletr in titletrs:
        try:
            title = titletr.find('th.subject span a',first=True)

            if title == None:
                continue
            postdate = titletr.find('td em',first=True)

            print(postdate.text)
            if  not title.text.isnumeric():              
                href = title.attrs['href']
                tid = re.findall(r'\d+',href)[0]
                print(tid)
                print(title.text)

                # 插入数据库
                cur.execute('insert or ignore into titles(title,tid,postdate) values(?, ?,?)', (title.text, tid,postdate.text))  
                
        except:
            continue


def mainwork():
    login()
    for page in range(1,20):
        get_title(page)
        conn.commit()
        time.sleep(0.5)
    
    
    conn.close()

mainwork()
