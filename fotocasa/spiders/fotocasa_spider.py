# -*- coding: utf-8 -*-
import requests
import scrapy

from lxml.html import fromstring
from os import getcwd
from os.path import join
from scrapy.utils.response import open_in_browser

import js2xml
import lxml.etree
from parsel import Selector

from fotocasa.items import PropertyItem
from scrapy_splash import SplashRequest


class FotocasaSpiderSpider(scrapy.Spider):
    name = 'fotocasa_spider'

    def __init__(self, page_url='', url_file=None, *args, **kwargs):
        # proxies = self.get_proxies() # get proxies from https://free-proxy-list.net/

        pages = 10
        self.start_urls = ['https://www.fotocasa.es/es/comprar/viviendas/barcelona-capital/todas-las-zonas/l/{}?latitude=41.3854&longitude=2.1775&combinedLocationIds=724,9,8,232,376,8019,0,0,0'.format(i + 1) for i in
                           range(pages)]

        if not page_url and url_file is None:
            TypeError('No page URL or URL file passed.')

        if url_file is not None:
            with open(url_file, 'r') as f:
                self.start_urls = f.readlines()
        if page_url:
            # Replaces the list of URLs if url_file is also provided
            self.start_urls = [page_url]

        super().__init__(*args, **kwargs)

    def start_requests(self):
        for page in self.start_urls:
            yield scrapy.Request(url=page, callback=self.crawl_page)

    def crawl_page(self, response):
        # response.xpath('//script/text()')[3].root -> this will get the variable for the json
        property_urls = ''
        for property in property_urls:
            yield scrapy.Request(url=property, callback=self.crawl_property)

    def crawl_property(self, response):
        property = PropertyItem()

        # Resource
        property["resource_url"] = "https://www.fotocasa.es/"
        property["resource_title"] = 'Fotocasa'
        property["resource_country"] = 'ES'

        # Property
        property["url"] = response.url
        property["title"] = response.xpath("//*[@class='re-DetailHeader-propertyTitle']/text()").get()
        property["subtitle"] = ''
        property["location"] = 'go back'
        property["extra_location"] = ''
        property["body"] = response.css('.fc-DetailDescription::text').get()

        # Price
        property["current_price"] = response.xpath('//*[@class="re-DetailHeader-price"]/text()').re_first('(.+) €')
        property["original_price"] = response.xpath('//*[@class="re-DetailHeader-price"]/text()').re_first('(.+) €')
        property["price_m2"] = ''
        property["area_market_price"] = ''
        property["square_meters"] = ''

        # Details
        property["area"] = ''
        property["tags"] = self.get_tags(response)
        property["bedrooms"] = response.xpath('//*[@class="re-DetailHeader-features"]//text()').getall()[0]
        property["bathrooms"] = response.xpath('//*[@class="re-DetailHeader-features"]//text()').getall()[2]
        property["last_update"] = ''
        consumption = self.get_consumption(response)
        emissions = self.get_emissions(response)
        property["certification_status"] = True if consumption and emissions else None
        property["consumption"] = consumption
        property["emissions"] = emissions

        # Multimedia
        property["main_image_url"] = 'go back'
        property["image_urls"] = 'go back'
        property["floor_plan"] = ''
        property["energy_certificate"] = ''
        property["video"] = ''

        # Agents
        property["seller_type"] = response.xpath('//*[@class="re-ContactDetail-inmoLogo"]//@src').get()
        property["agent"] = response.xpath('//*[@class="re-ContactDetail-inmoLogo"]//@src').get()
        property["ref_agent"] = response.xpath('//*[@class="re-ContactDetail-inmoContact"]//text()').re_first("Referencia: (.+)")
        property["source"] = 'fotocasa'
        property["ref_source"] = response.xpath('//*[@class="re-DetailReference"]//text()').re_first(": (.+)")
        property["phone_number"] = response.xpath('//*[@class="re-ContactDetail-phone"]//text()').get()

        # Additional
        property["additional_url"] = ''
        property["published"] = ''
        property["scraped_ts"] = ''

        yield property

    def get_tags(self, response):
        tags = ''
        top_tags_list = response.xpath('//*[@class="re-DetailFeaturesList-feature"]')  # upper tag block
        bottom_tags_list = response.xpath('//li[@class="re-DetailExtras-listItem"]/text()').getall()  # lower tag block

        for block in top_tags_list:
            label = block.css('::text').extract()[0]
            tag = block.css('::text').extract()[1]
            tags += "{}: {};".format(label, tag)

        bottom_tags = ';'.join(bottom_tags_list)
        tags += bottom_tags

        return tags

    def get_consumption(self, response):
        consumption = ''
        rating_list = response.css('.re-DetailEnergyCertificate-item::text').getall()
        units_list = response.css('.re-DetailEnergyCertificate-itemUnits::text').re('\w.+')
        if rating_list and units_list:
            consumption += "{};{} {}".format(rating_list[0], units_list[0], units_list[1])
            return consumption
        else:
            return None

    def get_emissions(self, response):
        emissions = ''
        rating_list = response.css('.re-DetailEnergyCertificate-item::text').getall()
        units_list = response.css('.re-DetailEnergyCertificate-itemUnits::text').re('\w.+')
        if len(units_list > 2):  # checking if emission is included in list
            emissions += "{};{} {}".format(rating_list[1], units_list[2], units_list[3])
            return emissions
        else:
            return None



