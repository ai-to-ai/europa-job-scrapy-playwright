# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EuscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobItem(scrapy.Item):
    data = scrapy.Field()
    # link = scrapy.Field()
    # country = scrapy.Field()
    # creation_date = scrapy.Field()
    # location = scrapy.Field()
    # immidate_start_indicator = scrapy.Field()

    # header = scrapy.Field()
    # sub_header = scrapy.Field()
    # vacancy_id = scrapy.Field()
    # handle = scrapy.Field()

    # job_language = scrapy.Field()
    # job_sector = scrapy.Field()
    # position_schedule = scrapy.Field()
    # position_type = scrapy.Field()
    # last_application_date = scrapy.Field()
    # start_application_date = scrapy.Field()
    # occupation = scrapy.Field()
    # start_date = scrapy.Field()

    # job_description = scrapy.Field()
    # job_location = scrapy.Field()

    # employer_name = scrapy.Field()
    # employer_description = scrapy.Field()
    # employer_sector = scrapy.Field()
    # employer_legal_id = scrapy.Field()
    # employer_type = scrapy.Field()
    # employer_size = scrapy.Field()

    # job_requirements_experience = scrapy.Field()
    # job_requirements_education = scrapy.Field()
    # remuneration_benefit = scrapy.Field()

    # link_to_apply = scrapy.Field()
    # email = scrapy.Field()
    # phone = scrapy.Field()
