# -*- coding: UTF-8 -*-

import os



def save_page(browser, save_dir, page_num):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    html_path = os.path.join(save_dir, "page_{}.html".format(page_num))
    # 打开文件，准备写入
    f = open(html_path, 'wb')

    f.write(browser.page_source.encode("utf8", "ignore"))  # 忽略非法字符
    print('写入page {}成功'.format(page_num))
    # 关闭文件
    f.close()

def create_save_dir(save_news_dir, prov,city,date_range):
    """

    :param save_news_dir: 保存招投标新闻的路径
    :param prov:
    :param city:
    :param date_range:
    :return:
    """
    save_news_dir = os.path.join(save_news_dir, prov, city, date_range)
    os.makedirs(save_news_dir, exist_ok=True)
    return save_news_dir

def make_dir(save_dir):
    os.makedirs(save_dir, exist_ok=True)

