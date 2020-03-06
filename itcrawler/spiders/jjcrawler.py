# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import time 

class JjcrawlerSpider(scrapy.Spider):
		name = 'jjcrawler'
		SCROLL_PAUSE_TIME = 0.5

		def start_requests(self): 
			yield SeleniumRequest(
				url = "https://justjoin.it/",
				wait_time = 3,
				callback = self.parse
				)


		def parse_position(self,content):
			#Content in form: 'position: absolute; left: 0px; top: 0px; height: 89px; width: 100%;'
			return int(content.split(";")[2].split(':')[1][:-2])

		def fetch_html(self,driver):
			html = driver.page_source
			return Selector(text=html)

		def parse(self, response):

			driver = response.meta['driver']
			driver.maximize_window()
			
			search_input = driver.find_element_by_xpath("//div[@class='css-40k5xv']")
												

			last_height = driver.execute_script("return arguments[0].scrollHeight",search_input)
			
			
			#--------------------- FIND LAST ELEMENT TOP POSITION --------------------------------------
			driver.execute_script("arguments[0].scrollTo(0,arguments[0].scrollHeight)",search_input)
			
			time.sleep(self.SCROLL_PAUSE_TIME)

			response_obj = self.fetch_html(driver)
			
			offer_list = response_obj.xpath("//div[@class='css-40k5xv']/div")
			
			last_element = offer_list.xpath(".//div[starts-with(@style,'position:')]")[-1]
			last_element_top_position = self.parse_position(last_element.xpath(".//@style").get())

			#Get back to top
			driver.execute_script("arguments[0].scrollTo(0,0)",search_input)

			last_top_position_seen = -1

			print(last_element_top_position)

			while last_top_position_seen < last_element_top_position:
				response_obj = self.fetch_html(driver)
				offer_list = response_obj.xpath("//div[@class='css-40k5xv']/div")
			
				for item in offer_list.xpath(".//div[starts-with(@style,'position:')]"):
					item_pos = self.parse_position(item.xpath(".//@style").get())
					if item_pos <= last_top_position_seen:
						continue
					else:
						yield{
						'title':item.xpath("normalize-space(.//a[@class='css-18rtd1e']/div[@class='css-1djzjwc']/div[@class='css-4vtr3h']/div[@class='css-dcciyt']/div[@class='css-rm26dz']/text())").get(),
						'top position':item_pos
						}


				#Get current view last element position 
				last_element_seen = offer_list.xpath(".//div[starts-with(@style,'position:')]")[-1]
				last_top_position_seen = self.parse_position(last_element_seen.xpath(".//@style").get())
				

				search_input.send_keys(Keys.PAGE_DOWN)
				time.sleep(self.SCROLL_PAUSE_TIME)





			