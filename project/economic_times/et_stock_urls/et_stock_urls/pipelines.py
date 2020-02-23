# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class EconomicTimesPipeline(object):

    def open_spider(self, spider):
        self.file = open('stock_urls.csv', 'w+')
        self.file.write('stock,cash_flow_url,half_yearly_results_url,capital_structure,dividends,profit_loss_account,'
                        'quarterly_results,yearly_results,balance_sheets,nine_months_results,share_holding_pattern \n')

    def process_item(self, item, spider):
        urls_string = ",".join(item.values())
        self.file.write(item['cash_flow_url'].split('/')[1]+ ","+ urls_string + '\n')

    def close_spider(self, spider):
        pass

