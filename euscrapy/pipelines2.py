# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import JobItem
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from datetime import datetime, timezone, date
import json
from lxml import etree

class MongoDBPipeline:

    def open_spider(self, spider):
        settings = get_project_settings()

        # get db instance.
        self.client = MongoClient(settings.get('MONGODB_URI'))
        self.db = self.client[settings.get('DB_NAME')]
        # self.job_collection = self.db[settings.get('COLLECTION_NAME')]
        # date_str = date.today().isoformat()
        # now_utc = datetime.now(timezone.utc)
        # date_str = now_utc.strftime("%Y_%m_%d_%H_%M_%S")
        # file_name = spider.name +"_"+ date_str + '.xml'
        # self.xml_file = open(file_name, 'w')
        # headerTemplate = f"""<?xml version="1.0" encoding="UTF-8"?>
        #                         <root>
        #                             <company>
        #                                 <jobBoardID></jobBoardID>
        #                                 <linkFiller><![CDATA[1]]></linkFiller>
        #                                 <jobBoardUrl><![CDATA[]]></jobBoardUrl>
        #                                 <country></country>
        #                                 <lastCrawlDate>{date_str}</lastCrawlDate>
        #                                 <companies>"""
        # self.xml_file.write(headerTemplate)
    def close_spider(self, spider):
        self.client.close()
        # footerTemplate = """        </companies>
        #                         </company>
        #                     </root>"""
        # self.xml_file.write(footerTemplate)
        # self.xml_file.close()
    def process_item(self, item, spider):

        # job object contains all data that filled and transfer from spider to pipeline for process and save to db.
        if isinstance(item, JobItem):
            job_item = ItemAdapter(item).asdict()
            job = job_item['data']
            country = job['country']

            self.job_collection = self.db[country]
            self.report_collection = self.db['report']

            now_utc = datetime.now(timezone.utc)
            date_ = now_utc.strftime("%d/%m/%Y")

            # job['crawlDate'] = date_

            print('######### Saving item to db #########')
            handle = self.job_collection.find_one({"handle": job["handle"]})
            if handle is None:

                # # create XML 
                # company = etree.Element('company')
                # # another child with text
                # companyID = etree.Element('companyID')
                # companyID.text = ""

                # companyName = etree.Element('companyName')
                # companyName.text = self.CDATA(job['employer']['name'])

                # companyUrl = etree.Element('companyUrl')
                # companyUrl.text = self.CDATA(job['employer']['website'])

                # companyJobOffersUrl = etree.Element('companyJobOffersUrl')
                # companyJobOffersUrl.text = self.CDATA(job['link'])

                # companyJobSampleUrl = etree.Element('companyJobSampleUrl')
                # companyJobSampleUrl.text = self.CDATA(job['link'])

                # country = etree.Element('country')
                # country.text = self.CDATA(job['country'])

                # companyContactFirstName = etree.Element('companyContactFirstName')
                # companyContactFirstName.text = self.CDATA("")

                # companyContactLastName = etree.Element('companyContactLastName')
                # companyContactLastName.text = self.CDATA("")

                # companyContactGender = etree.Element('companyContactGender')
                # companyContactGender.text = self.CDATA("")

                # companyAddress = etree.Element('companyAddress')
                # if len(job["locations"][0]["addressLines"]) > 0:
                #     companyAddress.text = self.CDATA(job["locations"][0]["addressLines"][0])
                # else:
                #     companyAddress.text = self.CDATA("")

                # companyZip = etree.Element('companyZip')
                # companyZip.text = self.CDATA(job["locations"][0]["postalCode"])

                # companyCity = etree.Element('companyCity')
                # companyCity.text = self.CDATA(job['locations'][0]['cityName'])

                # companyPhone = etree.Element('companyPhone')
                # companyPhone.text = self.CDATA(job['phone'])

                # companyEmail = etree.Element('companyEmail')
                # companyEmail.text = self.CDATA(job['email'])

                # companyJobOffersNumber = etree.Element('companyJobOffersNumber')
                # companyJobOffersNumber.text = self.CDATA(job['numberOfPosts'])

                # lastCrawlDate = etree.Element('lastCrawlDate')
                # lastCrawlDate.text = self.CDATA(job['crawlDate'])

                # jobs = etree.Element('jobs')
                # _job = etree.Element('job')
                # _id = etree.Element('id')
                # _id.text = self.CDATA(job['handle'])

                # title = etree.Element('title')
                # title.text = self.CDATA(job['title'])

                # url = etree.Element('url')
                # url.text = self.CDATA(job['link'])

                # _date = etree.Element('date')
                # _date.text = self.CDATA(job['creationDate'])

                # address = etree.Element('address')
                # address.text = companyAddress.text

                # city = etree.Element('city')
                # city.text = self.CDATA(job['locations'][0]['cityName'])

                # _country = etree.Element('country')
                # _country.text = self.CDATA(job['country'])

                # _zip = etree.Element('zip')
                # _zip.text = self.CDATA(job['locations'][0]['postalCode'])

                # email = etree.Element('email')
                # email.text = self.CDATA(job['email'])

                # reference = etree.Element('reference')
                # reference.text = self.CDATA(job['vacancy'])

                # isco = etree.Element('isco')
                # isco.text = self.CDATA("")

                # website = etree.Element('website')
                # website.text = self.CDATA(job['employer']['website'])

                # company.append(companyID)
                # company.append(companyName)
                # company.append(companyUrl)
                # company.append(companyJobOffersUrl)
                # company.append(companyJobSampleUrl)
                # company.append(country)
                # company.append(companyContactFirstName)
                # company.append(companyContactLastName)
                # company.append(companyContactGender)
                # company.append(companyAddress)
                # company.append(companyZip)
                # company.append(companyCity)
                # company.append(companyPhone)
                # company.append(companyEmail)
                # company.append(companyJobOffersNumber)
                # company.append(lastCrawlDate)
                # _job.append(_id)
                # _job.append(title)
                # _job.append(url)
                # _job.append(_date)
                # _job.append(address)
                # _job.append(city)
                # _job.append(_country)
                # _job.append(_zip)
                # _job.append(email)
                # _job.append(reference)
                # _job.append(isco)
                # _job.append(website)
                # jobs.append(_job)
                # company.append(jobs)
                # # pretty string
                # s = etree.tostring(company, pretty_print=True)
                # company_str = s.decode('utf-8')
                # # print(company_str)

                # companyTemplate = f"""<company>
                #                             <companyID></companyID>
                #                             <companyName><![CDATA[{job['employer']['name']}]]></companyName>
                #                             <companyUrl><![CDATA[{job['employer']['website']}]]></companyUrl>
                #                             <companyJobOffersUrl><![CDATA[{job['link']}]]></companyJobOffersUrl>
                #                             <companyJobSampleUrl><![CDATA[{job['link']}]]></companyJobSampleUrl>
                #                             <country><![CDATA[{job['country']}]]></country>
                #                             <companyContactFirstName><![CDATA[]]></companyContactFirstName>
                #                             <companyContactLastName><![CDATA[]]></companyContactLastName>
                #                             <companyContactGender><![CDATA[]]></companyContactGender>
                #                             <companyAddress><![CDATA[{''.join(job['locations'][0]['addressLines'])}]]></companyAddress>
                #                             <companyZip><![CDATA[{job['locations'][0]['postalCode']}]]></companyZip>
                #                             <companyCity><![CDATA[{job['locations'][0]['cityName']}]]></companyCity>
                #                             <companyPhone><![CDATA[{job['phone']}]]></companyPhone>
                #                             <companyEmail><![CDATA[{job['email']}]]></companyEmail>
                #                             <companyJobOffersNumber>{job['numberOfPosts']}</companyJobOffersNumber>
                #                             <lastCrawlDate>![CDATA[{job['crawlDate']}]]</lastCrawlDate>
                #                                 <jobs>
                #                                     <job>
                #                                         <id>{job['handle']}</id>
                #                                         <title><![CDATA[{job['title']}]]></title>
                #                                         <description><![CDATA[{job['description']}]]></description>
                #                                         <url><![CDATA[{job['link']}]]></url>
                #                                         <date>{job['creationDate']}</date>
                #                                         <address><![CDATA[{''.join(job['locations'][0]['addressLines'])}]]></address>
                #                                         <city><![CDATA[{job['locations'][0]['cityName']}]]></city>
                #                                         <country><![CDATA[{job['country']}]]></country>
                #                                         <zip><![CDATA[{job['locations'][0]['postalCode']}]]></zip>
                #                                         <email><![CDATA[{job['email']}]]></email>
                #                                         <reference><![CDATA[{job['vacancy']}]]></reference>
                #                                         <isco><![CDATA[]]></isco>
                #                                         <website><![CDATA[{job['employer']['website']}]]></website>
                #                                     </job>
                #                                 </jobs>
                #                         </company>"""

                # self.xml_file.write(companyTemplate)
                self.job_collection.insert_one(job)
                print('######### Item saved #########')

                print('######### Saving report to db #########')
                # Write Report Data
                report_data = self.report_collection.find_one({'country': job['country'], 'date': date_})
                obj = {}
                if report_data is None:
                    
                    obj['date'] = date_
                    obj['country'] = job['country']
                    obj['numberOfJobs'] = 1
                    self.report_collection.insert_one(obj)
                    print('######### Report saved #########')
                else:
                    obj['numberOfJobs'] = report_data['numberOfJobs'] + 1
                    self.report_collection.update_one({'country': job['country'], 'date':date_},{"$set": obj})
                    print('######### Report updated #########')

                
            else:
                print('######### Duplicated item #########')

        return item
    def CDATA(self,data):
        return f"<![CDATA[{data}]]>"