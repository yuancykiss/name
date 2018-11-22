import re
import threading

import pymysql
import requests
from lxml import etree


def conn_db():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8', database='da')
    cur = db.cursor()
    return db, cur


def insert_db(**kwargs):
    pass


def get_page(url):
    """
    发起请求并返回网页text
    :param url:
    :return:
    """
    html = requests.get(url).text
    return html


def get_surname(url):
    """
    第一层：爬取姓氏
    :param url: 首页
    :return: 姓氏和url列表
    """
    html = get_page(url)
    etree_html = etree.HTML(html)

    # surnames
    surnames = []
    surname = etree_html.xpath('//div[@class="col-xs-12"]/a/text()')
    for item in surname:
        if len(item) == 6:
            surnames.append(item[0])
        else:
            surnames.append(item[:2])

    # surnames_urls
    surnames_urls = []
    surnames_url = etree_html.xpath('//div[@class="col-xs-12"]/a/@href')
    for surnames_url in surnames_url:
        surnames_urls.append('http://' + surnames_url[2:])
        # surnames_urls.append(re.findall(r'(\w+.resgain.net/)name_list.html', surnames_url)[0])
    return surnames, surnames_urls


def get_name(surname_url):
    """
    第二层：爬取姓名
    :param surname_url:
    :return:
    """
    for i in range(10):
        print('正在抓取第%s页' % i)
        url = re.findall(r'(.*?).html', surname_url)[0] + '_' + str(i+1) + '.html'
        html = get_page(url)
        etree_html = etree.HTML(html)
        names = etree_html.xpath('//div[@class="col-xs-12"]/a/text()')
        surname = re.findall(r'http://(\w+)\..*?', url)[0]
        print(url)
        # print(names)
        get_info(names, surname)


def get_info(names_list, surname):
    """
    第三层：解析各个字段，并插入数据库
    :param names_list:
    :param surname:
    :return:
    """
    db, cur = conn_db()
    for item in names_list:
        url = 'http://' + surname + '.resgain.net/name/' + item + '.html'
        html = get_page(url)
        etree_html = etree.HTML(html)
        # name
        name = item
        print(name)
        # nums
        nums = etree_html.xpath('//div[@class="navbar-brand"]/text()')[0]
        nums = re.findall(r'(\d+)', nums)[0]
        # print(nums)
        # sex_boy
        sex_boy = etree_html.xpath('//div[@class="container"]/div[2]//div[@class="progress"]/div[1]/text()')[0]
        sex_boy = re.findall(r'(\d+\.\d+).*?男孩.*?', sex_boy)[0]
        # sex_girl
        sex_girl = etree_html.xpath('//div[@class="container"]/div[2]//div[@class="progress"]/div[2]/text()')[0]
        sex_girl = re.findall(r'(\d+\.\d+).*?女孩.*?', sex_girl)[0]
        # print(sex_boy, sex_girl)
        wuxing = etree_html.xpath('//div[@class="container"]/div[4]/div[2]//div[@class="col-xs-6"]/blockquote/text()')
        # five_lines
        five_lines = wuxing[0]
        # three_talents
        three_talents = wuxing[1]
        # print(five_lines, three_talents)
        # five_ge
        five_ge = []
        old_five_ge = etree_html.xpath('//div[@class="container"]/div[4]/div[2]//div[@class="col-xs-12"][1]/blockquote/text()')
        for item in old_five_ge:
            item = item.strip()
            if len(item) != 0:
                five_ge.append(item[1:])
        # print(five_ge)

        # five_ge_parse
        five_ge_parse = []
        old_five_ge_parse = etree_html.xpath('//div[@class="container"]/div[4]/div[2]//div[@class="col-xs-12"][2]/blockquote/div/text()')
        for item in old_five_ge_parse:
            five_ge_parse.append(item[1:])
        # print(five_ge_parse)

        sql = 'insert into name_copy(name,sex_girl,sex_boy,five_lines,three_talents,nums,sky,earth,human,total,wai,sky_parse,earth_parse,human_parse,total_parse,wai_parse) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
              (name, sex_girl, sex_boy, five_lines, three_talents, nums, five_ge[0], five_ge[1], five_ge[2], five_ge[3], five_ge[4],
               five_ge_parse[0], five_ge_parse[2], five_ge_parse[1], five_ge_parse[4], five_ge_parse[3])
        try:
            cur.execute(sql)

            db.commit()
        except:
            pass


def main():
    url = 'http://www.resgain.net/xmdq.html'
    surnames, surnames_urls = get_surname(url)
    print(surnames_urls)
    for i in range(0, 50):
        t1 = threading.Thread(target=thread_work, args=[surnames_urls, (len(surnames_urls)//50)*i, (len(surnames_urls)//50)*(i+1), i])
        t1.start()
        # thread_work(surnames_urls, (len(surnames_urls)//10)*i, (len(surnames_urls)//10)*(i+1))


def thread_work(surnames_urls, start_len, end_len, i):
    for index in range(start_len, end_len):
        print(i)
        get_name(surnames_urls[index])


if __name__ == '__main__':
    main()