# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #Resource
    resource_url = scrapy.Field()
    resource_title = scrapy.Field()
    resource_country = scrapy.Field()

    # Property
    url = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    location = scrapy.Field()
    extra_location = scrapy.Field()
    body = scrapy.Field()

    # Price
    current_price = scrapy.Field()
    original_price = scrapy.Field()
    price_m2 = scrapy.Field()
    area_market_price = scrapy.Field()
    square_meters = scrapy.Field()

    # Details
    area = scrapy.Field()
    tags = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    last_update = scrapy.Field()
    certification_status = scrapy.Field()
    consumption = scrapy.Field()
    emissions = scrapy.Field()

    # Multimedia
    main_image_url = scrapy.Field()
    image_urls = scrapy.Field()
    floor_plan = scrapy.Field()
    energy_certificate = scrapy.Field()
    video = scrapy.Field()

    # Agents
    seller_type = scrapy.Field()
    agent = scrapy.Field()
    ref_agent = scrapy.Field()
    source = scrapy.Field()
    ref_source = scrapy.Field()
    phone_number = scrapy.Field()

    # Additional
    additional_url = scrapy.Field()
    published = scrapy.Field()
    scraped_ts = scrapy.Field()