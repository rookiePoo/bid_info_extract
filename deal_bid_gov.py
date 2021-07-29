# -*- coding: UTF-8 -*-
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import re, os

from selenium.webdriver.common.by import By

import datetime


class DealBidGovDriver:
    """
        driver: chrome的自动化句柄
        province: 目标省
        city: 目标市
        start_date: 时间开始节点，格式%Y-%m-%d，如2021-07-26
        months: 时间长度（月），start_date + months = end_date
    """

    def __init__(self, driver, province, city,
                 end_date='today', months=1, **kwargs):
        self.driver = driver
        self.province = province
        self.city = city
        if end_date == 'today':
            end_date = datetime.datetime.today()
        else:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        months = min(3, months)
        start_date = end_date - datetime.timedelta(days=months*30)

        self.start_date = start_date.strftime("%Y-%m-%d")
        self.end_date = end_date.strftime("%Y-%m-%d")

        print(self.start_date, self.end_date)





    def select_time_range(self):
        """
            时间范围最大为3个月
        """
        time_range = self.driver.find_element_by_id('choose_time_06')
        time_range.click()

        time_begin = self.driver.find_element_by_id('TIMEBEGIN_SHOW')
        time_begin.clear()
        time_begin.send_keys(self.start_date)

        time_end = self.driver.find_element_by_id('TIMEEND_SHOW')
        time_end.clear()
        time_end.send_keys(self.end_date)


    def select_prov_and_city(self):
        """
            选择省份和市
        """
        region_prov = self.driver.find_element_by_id("provinceId")
        select_prov = Select(region_prov)
        options_prov = [option.text for option in select_prov.options]
        print(options_prov)
        assert self.province in set(options_prov), '省份输入有误'
        select_prov.select_by_visible_text(self.province)

        region_city = self.driver.find_element_by_id("cityId")
        select_city = Select(region_city)
        options_city = [option.text for option in select_city.options]
        print(options_city)
        assert self.city in set(options_city), '城市输入有误'
        select_city.select_by_visible_text(self.city)


    def business_type(self):
        """
            不限: choose_classify_00
            工程建设: choose_classify_01
            政府采购: choose_classify_02
            土地使用权: choose_classify_03
            矿业权: choose_classify_04
            国有产权: choose_classify_05
            碳排放权: choose_classify_21
            排污权: choose_classify_22
            药品采购: choose_classify_23
            二类疫苗: choose_classify_24
            林权: choose_classify_25
            其他: choose_classify_90

            下面细分项目阶段
            工程建设:
                不限: choose_stage_0100
                招标/资审公告: choose_stage_0101
                开标记录: choose_stage_0102
                交易结果公示: choose_stage_0104
                招标/资审文件澄清: choose_stage_0105
            :return:
        """

        project_type = self.driver.find_element_by_id('choose_classify_01')
        project_type.click()

        project_stage = self.driver.find_element_by_id('choose_stage_0104')
        project_stage.click()

    def search_submit(self):
        # 提交，搜索
        search = self.driver.find_element_by_id('searchButton')
        search.click()
        time.sleep(5)

    def get_page_num(self):

        page_num= self.driver.find_element(By.XPATH, '//*[@id="paging"]/span[3]').text
        print("搜索记录总共{}页".format(page_num))

        page_num = re.findall('\d+', page_num)[0]

        return page_num

    def write_title_herf(self, writer):
        for link in self.driver.find_elements_by_xpath("//*[@id=\"toview\"]/div/div/h4/a"):
            print(link.get_attribute('title'))
            print(link.get_attribute('href'))
            writer.write(link.get_attribute('title') + '\t' + link.get_attribute('href') + '\n')

    def save_records(self, save_dir):

        txt_name = self.province + "_" + self.city + "_" + self.start_date.replace("-","") + "-" + self.end_date.replace("-","")+'.txt'
        save_path = os.path.join(save_dir, txt_name)

        record_writer = open(save_path, 'w')
        page_num = self.get_page_num()
        self.write_title_herf(record_writer)

        for i in range(2, int(page_num)+1):

            self.driver.execute_script("javascript:getList({})".format(i))
            try:
                WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "a_hover"), str(i)))
            except:
                print("page {} time out!!!".format(i))
                time.sleep(10)
                self.driver.execute_script("javascript:getList({})".format(i))
            time.sleep(1)
            self.write_title_herf(record_writer)

        record_writer.close()

    def quit(self):
        self.driver.quit()

# if __name__ == "__main__":
#     driver_path = '/Users/peng_ji/codeHub/rookieCode/chromedriver'
#     url = 'http://deal.ggzy.gov.cn/ds/deal/dealList.jsp?HEADER_DEAL_TYPE=02'
#     cd = ChromeDriver(driver_path)
#     cd.get_response(url)
#
#     dbgd = DealBidGovDriver(cd.driver, '北京', '不限')
#     dbgd.select_time_range()
#     dbgd.select_prov_and_city()
#     dbgd.business_type()
#     dbgd.search_submit()
#     dbgd.save_records('.')
#     dbgd.quit()
