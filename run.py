# -*- coding: UTF-8 -*-

import argparse
from deal_bid_gov import DealBidGovDriver
from chrome_driver import ChromeDriver
from bid_classify.classify_01_news import save_bid_news
from data_helper import create_save_dir

parser = argparse.ArgumentParser(description='Crawl bidding information')


parser.add_argument('--dp', '--driver-path', default='/Users/peng_ji/codeHub/rookieCode/chromedriver', type=str,
                    help='path to chrome driver')
parser.add_argument('--url', default='http://deal.ggzy.gov.cn/ds/deal/dealList.jsp?HEADER_DEAL_TYPE=02', type=str,
                    help='target url')
parser.add_argument('-p', '--province', default='北京', type=str,
                    help='select province')
parser.add_argument('-c', '--city', default='不限', type=str,
                    help='select city')
parser.add_argument('--ed', '--end-date', default=None, type=str,
                    help='the last day of bidding news')
parser.add_argument('--dr', '--data-range', default=1, type=int,
                    help='data range of news')
parser.add_argument('--sp', '--save-path', default='.', type=str,
                    help='txt path of saving bid news')
parser.add_argument('--nd', '--news-dir', default='./news', type=str,
                    help='txt path of saving bid news')


def main():
    args = parser.parse_args()
    print(args)
    cd = ChromeDriver(args.dp)
    cd.get_response(args.url)

    dbgd = DealBidGovDriver(cd.driver, args.province, args.city, months=args.dr)

    dbgd.select_time_range()
    dbgd.select_prov_and_city()
    dbgd.business_type()
    dbgd.search_submit()
    save_path, data_range = dbgd.save_records(args.sp)
    save_news_dir = create_save_dir(args.nd, args.province, args.city, data_range)
    save_bid_news(cd.driver, save_path, save_news_dir)
    dbgd.quit()


if __name__ == "__main__":
    main()



