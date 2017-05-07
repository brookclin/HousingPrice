import scrapy

class walkscoreSpider(scrapy.Spider):
	name='walkscore'

	def start_requests(self):
		f=open('missing_score.txt')
		# self.log('11111111111')
		# for i in f:
		# 	# self.log('11111111111')
		# 	yield scrapy.Request(url='https://www.walkscore.com/score/'+i,callback=self.parse)	
		yield scrapy.Request(url='https://www.walkscore.com/score/1-w-century-dr-unit-25a-los-angeles-ca-90067',callback=self.parse)	


	def parse(self,response):
		score=response.xpath("//div[@data-eventsrc='score page walk badge']/img/@src").extract()[0]
		ss=score.encode("utf-8")
		outputscore=ss.split('/')[-1].split('.')[0]
		# self.log(type(ss))
		# self.log(ss)
		# self.log('1111111111111111111111111111111111111111	')
		yield{'url':response.request.meta['redirect_urls'],
		'score':outputscore}