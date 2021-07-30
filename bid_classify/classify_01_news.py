
import time, os


def get_news_content(driver, url):
    driver.get(url)
    eles = driver.find_elements_by_xpath("//*[@id=\"div_0104\"]/ul/li/a")
    if len(eles) < 1:
        return None
    ele = eles[0]
    show_detail = ele.get_attribute('onclick')
    new_url = show_detail.split('\'')[-2]

    driver.get('http://www.ggzy.gov.cn/information' + new_url)
    time.sleep(3)
    html = driver.find_element_by_class_name('detail_content')
    news_content = html.get_attribute('innerText')
    return news_content

def save_bid_news(driver, txt_path, save_news_dir):
    tfp = open(txt_path, 'r')

    for line in tfp.readlines():
        if '\t' not in line:
            continue

        title, url = line.strip().split('\t')

        news = get_news_content(driver, url)

        if news is None:
            print("the url {} is invalid".format(url))
            continue
        name = url.split('/')[-1].replace('.shtml', '')

        fp = open(os.path.join(save_news_dir, name + ".txt"), 'w')
        fp.write(line)
        fp.write(news)
        fp.close()


