import scrapy

class zillowSpider(scrapy.Spider):
	name = "zillow"

	def start_requests(self):
		# urls=[
		# 'https://www.zillow.com/homes/recently_sold/Los-Angeles-CA/12447_rid/globalrelevanceex_sort/34.602693,-117.191163,33.437171,-119.632874_rect/8_zm/']

		urls = [
		
		]
		for i in range(104):
			urls.append('https://www.zillow.com/homes/recently_sold/'+str(90000+i)+'/300001-600000_price/')
			urls.append('https://www.zillow.com/homes/recently_sold/'+str(90000+i)+'/0-300000_price/')
			urls.append('https://www.zillow.com/homes/recently_sold/'+str(90000+i)+'/600001-900000_price/')
			urls.append('https://www.zillow.com/homes/recently_sold/'+str(90000+i)+'/900001-_price/')
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
			for i in range(2,21):
				yield scrapy.Request(url=(url+str(i)+'_p/'), callback=self.parse)

	def parseHomeDetial(self,response):

		price=response.xpath("//div[@class='main-row status-icon-row recently-sold-row home-summary-row']/span/text()").extract()
		if price==[]:
			price=response.xpath("//div[@class='main-row  home-summary-row']/span/text()").extract()
		houseType=response.xpath("//div[@class='zsg-media-bd' and p/text()='Type']/div/text()").extract()
		yearBuilt=response.xpath("//div[@class='zsg-media-bd' and p/text()='Year Built']/div/text()").extract()
		bedrooms=response.xpath("//div[div/text()='Bedrooms']//span[@class='hdp-fact-value']/text()").extract()
		flooring=response.xpath("//li[span/text()='Floor size: ']/span[@class='hdp-fact-value']/text()").extract()
		lot=response.xpath("//li[span/text()='Lot: ']/span[@class='hdp-fact-value']/text()").extract()
		propertyCondition=response.xpath("//li[span/text()='Property Condition: ']/span[@class='hdp-fact-value']/text()").extract()
		neighborhood=response.xpath("//h2[@data-module='neighborhood']/text()").extract()


		# Price=response.xpath("//div[@class='zsg-content-component null'][1]/table/tbody/tr[1]/td").extract()
		# Price.append(response.xpath("//section[@class='zsg-content-section null'][1]/table/tbody/tr[1]/td").extract())


		yield {'url':response.url.split('/')[-3],'price':price,
		'type':houseType,
		'Year Built':yearBuilt,
		'bedrooms':bedrooms,
		'flooring':flooring,
		'lot':lot,
		'propertyCondition':propertyCondition,
		'neighborhood':neighborhood


		}

	def parseWalkscore(self,response):
		score=response.xpath("//div[@data-eventsrc='score page walk badge']/img/@src").extract()[0]
		ss=score.encode("utf-8")
		outputscore=ss.split('/')[-1].split('.')[0]
		# self.log(type(ss))
		# self.log(ss)
		# self.log('1111111111111111111111111111111111111111	')
		yield{'url':response.url.split('/')[-1],
		'score':outputscore}



	def parse(self, response):
		# a=response.xpath("//div[@id='map-result-count-message']")
		# self.log(type(a))
		# self.log(a.extract())
		# resultCount=response.xpath("//div[@id='map-result-count-message']/h2/text()").extract()[0].split(' ')[0]
		# resc=resultCount.split(',')
		# if len(resc)>1:
		# 	count=int(resc[0])*1000+int(resc[1])
		# else:
		# 	count=int(resc[0])
		# if count>500:
		# 	self.log(response.url)
		# else:
		res=response.xpath('//div[@class="zsg-photo-card-content zsg-aspect-ratio-content"]/a/@href').extract()
		for u in res:

			yield scrapy.Request(url='https://www.zillow.com'+u,callback=self.parseHomeDetial)
			yield scrapy.Request(url='https://www.walkscore.com/score/'+u.split('/')[2],callback=self.parseWalkscore)
		# self.log(res)
	
	


    	