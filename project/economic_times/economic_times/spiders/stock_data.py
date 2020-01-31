# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import re
from parsel import Selector




class StockDataSpider(scrapy.Spider):
    name = 'stock_data'
    base_url = 'https://economictimes.indiatimes.com/'

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome('/home/nandagopal/hti/scrapy/chromedriver',
                                       chrome_options=options)

    def start_requests(self):
        for stock in ['hdfc bank', 'sbin']:
            driver = self.driver
            driver.get(self.base_url)
            search_box = driver.find_element_by_xpath('//input[@class="inputBox"]')
            search_box.click()
            search_box.send_keys(stock)
            search_box.send_keys(Keys.ENTER)
            time.sleep(1)
            yield scrapy.Request(driver.current_url)

    def parse(self, response):
        urls = dict()
        content = Selector(response.text)
        urls['cash_flow_url'] = content.xpath("//a[text()='Cash Flow Statement']/@href").extract_first()
        urls['half_yearly_results_url'] = content.xpath("//a[text()='Half Yearly Results']/@href").extract_first()
        urls['capital_structure'] = content.xpath("//a[text()='Capital Structure']/@href").extract_first()
        urls['dividends'] = content.xpath("//a[text()='Dividends']/@href").extract_first()
        urls['profit_loss_account'] = content.xpath("//a[text()='Profit and Loss Account']/@href").extract_first()
        urls['quarterly_results'] = content.xpath("//a[text()='Quarterly Results']/@href").extract_first()
        urls['yearly_results'] = content.xpath("//a[text()='Yearly Results']/@href").extract_first()
        urls['balance_sheets'] = content.xpath("//a[text()='Balance Sheet']/@href").extract_first()
        urls['nine_months_results'] = content.xpath("//a[text()='Nine Monthly Results']/@href").extract_first()
        urls['share_holding_pattern'] = content.xpath("//a[text()='Shareholding Pattern']/@href").extract_first()
        for k, v in urls.items():
            print(k, "---->" ,v)
        yield urls

    def get_stock_url(self, url, stock):
        driver = self.driver
        driver.get(url)
        search_box = driver.find_element_by_xpath('//input[@class="inputBox"]')
        search_box.click()
        search_box.send_keys(stock)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
        # company_id = re.findall(r'companyid-(.*).cms', str(driver.current_url))[0]
        return driver.current_url
