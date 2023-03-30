
import scrapy
from scrapy.utils.log import configure_logging
import re
import asyncio
from twisted.internet import asyncioreactor
scrapy.utils.reactor.install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
from twisted.internet import reactor
from scrapy_playwright.page import PageMethod
from playwright.async_api import Dialog, Response as PlaywrightResponse, Request as PlaywrightRequest
from euscrapy.items import JobItem
from scrapy.http import FormRequest
from euscrapy.proxies import proxies
import random
from datetime import datetime
import json

# print(proxies)
URL = "https://ec.europa.eu/eures/portal/jv-se/search?page=1&resultsPerPage=50&orderBy=MOST_RECENT&publicationPeriod=LAST_DAY&lang=en"
ORIGIN = "https://ec.europa.eu"
PER_PAGE = 50
TOTAL_PAGE = 0
ORDER_BY = "MOST_RECENT"
proxy = random.choice(proxies)
# print(proxy)
COUNTRY_CODES = [
    # {'name':'Austria','code':'at'},
    # {'name':'Belgium','code':'be'},
    # {'name':'Bulgaria','code':'bg'}, 
    # {'name':'Croatia','code':'hr'}, 
    # {'name':'Cyprus', 'code': 'cy'}, 
    # {'name':'Czechia','code':'cz'}, 
    # {'name':'Denmark','code':'dk'}, 
    # {'name':'Estonia', 'code':'ee'},

    # {'name':'Finland', 'code':'fi'}, 
    # {'name':'France', 'code':'fr'}, 
    # {'name':'Germany', 'code':'de'}, 
    # {'name':'Greece', 'code':'el'}, 
    # {'name':'Hungary','code':'hu'}, 
    # {'name':'Iceland', 'code':'is'}, 
    # {'name':'Ireland', 'code':'ie'}, 
    # {'name':'Italy', 'code':'it'}, 
    # {'name':'Latvia','code':'lv'}, 

    {'name':'Liechtenstein', 'code':'li'}, 
    {'name':'Lithuania','code':'lt'}, 
    {'name':'Luxembourg','code':'lu'}, 
    {'name':'Malta','code':'mt'}, 
    # {'name':'Netherlands','code':'nl'}, 
    # {'name':'Norway','code':'no'}, 
    # {'name':'Poland','code':'pl'}, 
    
    # {'name':'Portugal','code':'pt'}, 
    # {'name':'Romania','code':'ro'}, 
    # {'name':'Slovakia','code':'sk'}, 
    # {'name':'Slovenia','code':'si'}, 
    # {'name':'Spain','code':'es'}, 
    # {'name':'Sweden','code':'se'}, 
    # {'name':'Switzerland','code':'ch'}
]
# post_data = {}
# headers = {}
class EuSpider(scrapy.Spider):
    name="Liechtenstein_Lithuania_Luxembourg_Malta"

    custom_settings=dict(
        DOWNLOAD_HANDLERS = {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        PLAYWRIGHT_BROWSER_TYPE = "chromium",
        TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        CONCURRENT_REQUESTS =1,
        SCRAPEOPS_API_KEY = 'a671c735-5d18-4516-be30-8ba6b3daef18',

        # Add In The ScrapeOps Extension
        EXTENSIONS = {
             'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
        },

        # Update The Download Middlewares
        DOWNLOADER_MIDDLEWARES = { 
            'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550, 
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        },
        PLAYWRIGHT_LAUNCH_OPTIONS = {
            "headless": True,
            "proxy": {
                    "server": f"http://{proxy.split(':')[0]+':'+proxy.split(':')[1]}",
                    "username": proxy.split(':')[2],
                    "password": proxy.split(':')[3],
                },
        },
        # PLAYWRIGHT_CONTEXTS = {
        #     "default": {
        #         "proxy": {
        #             "server": "http://default-proxy.com:3128",
        #             "username": "user1",
        #             "password": "pass1",
        #         },
        #     },
        # },
        DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter',
        LOG_ENABLED = False,
        # LOG_FILE = 'log.txt',
        # PLAYWRIGHT_MAX_CONTEXTS = 32
    )

    def start_requests(self):

        yield scrapy.Request(url=URL,callback=self.parse_total_page, meta=dict(
            playwright = True,
            # playwright_include_page = True,
            playwright_page_methods =[
                PageMethod('wait_for_selector', 'css=jv-result-summary'),
                PageMethod('wait_for_timeout', 2000),
                PageMethod('click', '//*[@id="undefined-show-more-show-less"]')
            ]
        ))

    # Scrape Total Page Number
    async def parse_total_page(self,response):
        for country_data in COUNTRY_CODES:
            
            country_code = country_data['code']
            country_name = country_data['name']
            avaialable_job_desc = response.xpath(f'//*[@id="{country_code}"]/text()').get(default="")
            try:
                total_jobs = re.findall(r'\d+', avaialable_job_desc)[0]
                total_jobs = int(total_jobs)
            except:
                total_jobs = 0

            if total_jobs > 0:
                if total_jobs > 10000:
                    total_jobs = 10000

                total_page = int(total_jobs/PER_PAGE)

                if PER_PAGE * total_page < total_jobs:
                    total_page = total_page+1
                for page_num in range(total_page):

                    page_num = page_num + 1
                    page_url = f"https://ec.europa.eu/eures/portal/jv-se/search?page={page_num}&resultsPerPage={PER_PAGE}&orderBy={ORDER_BY}&locationCodes={country_code}&publicationPeriod=LAST_DAY&lang=en"
                    yield scrapy.Request(url=page_url,callback=self.parse_job_links, meta=dict(
                            playwright = True,
                            playwright_page_methods =[
                                PageMethod('wait_for_selector', 'jv-result-summary'),
                            ]), cb_kwargs={'country':country_name})

    # Scrape Job Links
    def parse_job_links(self, response, country):
        job_links = response.xpath('//jv-result-summary//a[contains(@class,"jv-result-summary-title")]/@href').getall()

        for job_link in job_links:
            handle = job_link.split('/')[-1]
            job_link = f'https://ec.europa.eu/eures/eures-apps/searchengine/page/jv/id/{handle}?lang=en'

            yield scrapy.Request(url=job_link,callback=self.parse_job_details, cb_kwargs = {'country':country}) 

    # Scrape Job details
    def parse_job_details(self, response, country):
        data = response.json()

        jvProfile = data['jvProfiles']
        preferredLanguage = data['preferredLanguage']


        
        item = jvProfile[preferredLanguage]
        item['preferredLanguage'] = preferredLanguage

        item['creationDate'] = int(data['creationDate']/1000)
 
        item['lastModificationDate'] = int(data['lastModificationDate']/1000)

        item['handle']  = data['id']
        item['vacancy']  = data['reference']
        item['source']  = data['source']
        item['documentId']  = data['documentId']
        item['connectionPointId']  = data['connectionPointId']

        print(country)
        item['country'] = country
        item['link'] = "https://ec.europa.eu/eures/portal/jv-se/jv-details/" + item['handle']

        application_instruction_data = '\n'.join(item['applicationInstructions'])

        linkToApply = re.search(r'href="(.*?)"', application_instruction_data)
        if linkToApply != None:
            item['linkToAppy'] = linkToApply.group(1)
        else:
            item['linkToAppy'] = ""
        email = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', application_instruction_data)
        if email != None:
            item['email'] = email.group(0)
        else:
            item['email'] = ""
        phone = re.search(r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}', application_instruction_data)
        if phone != None:
            item["phone"] = phone.group(0)
        else:
            item['phone'] = ""

        job_item = JobItem()
        job_item['data'] = item
        yield job_item
        