# -*- coding: UTF-8 -*-

import argparse
from deal_bid_gov import DealBidGovDriver
from chrome_driver import ChromeDriver

parser = argparse.ArgumentParser(description='Crawl bidding information')


parser.add_argument('--dp', '--driver_path', default='/Users/peng_ji/codeHub/rookieCode/chromedriver', type=str,
                    help='path to chrome driver')
parser.add_argument('--url', default='http://deal.ggzy.gov.cn/ds/deal/dealList.jsp?HEADER_DEAL_TYPE=02', type=str,
                    help='target url')
parser.add_argument('-p', '--province', default='北京', type=str,
                    help='select province')
parser.add_argument('-c', '--city', default='不限', type=str,
                    help='select city')
parser.add_argument('--sp', '--save_path', default='.', type=str,
                    help='txt path of saving bid news')


def main():
    args = parser.parse_args()
    print(args)
    cd = ChromeDriver(args.dp)
    cd.get_response(args.url)

    dbgd = DealBidGovDriver(cd.driver, args.province, args.city)

    dbgd.select_time_range()
    dbgd.select_prov_and_city()
    dbgd.business_type()
    dbgd.search_submit()
    dbgd.save_records(args.sp)
    dbgd.quit()


if __name__ == "__main__":
    main()



