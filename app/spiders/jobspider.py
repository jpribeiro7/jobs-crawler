import scrapy
from app.items import JobItem
from scrapy_redis.spiders import RedisSpider
from scrapy.exceptions import IgnoreRequest, DropItem, CloseSpider
import hashlib

class JobspiderSpider(RedisSpider):
    ''' 
        This spider consumes from Redis 1 url at a time (redis_batch_size) and performs the job-postings parsing (parse)
    '''
    name = "jobspider"
    redis_key = 'jobs_queue:start_urls'
    # Number of urls to fech at a time
    redis_batch_size = 1
    # Max time before the spider stops checking redis
    max_idle = 7

    def parse(self, response):
        ''' Retrieves job postings from the three tables in the website '''
        if response is None:
            raise IgnoreRequest("Request ignored due to None response")
        elif response.css("table tbody tr").get() is None:
            raise IgnoreRequest("No jobs to scrape")
        
        if self.state.get('jobs') is None:
            self.state['jobs'] = self.state.get('jobs', {})
            
        for table in response.css("table"):
            for row in table.css('tbody tr'):
                # Used JobItem to ensure that all jobs have the same structure
                job = JobItem()
                job['id'] = self.hash_url(row.css('td a').attrib['href'])
                
                if job['id'] in self.state.get('jobs', {}):
                    continue
                    
                job['name'] = row.css('td a::text').get()
                job['location'] = row.css('td .custom-css-style-job-location-city::text, td .custom-css-style-job-location-region::text, td .custom-css-style-job-location-country::text').get()
                job['department'] = row.css('td a::text').get()

                self.state['jobs'][job['id']] = job
                yield job

    def hash_url(self, url: str) -> str:
        ''' Returns md5 hash based on url that identifies job postings '''
        if url is None or url == '':
            raise DropItem("Job url is not valid")
        m = hashlib.md5()
        m.update(str.encode(url))
        return str(int(m.hexdigest(), 16))[0:12]

        