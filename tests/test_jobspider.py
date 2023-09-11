import pytest
import scrapy

from scrapy.exceptions import IgnoreRequest, DropItem
from scrapy.selector import Selector
from app.spiders.jobspider import JobspiderSpider
from app.items import JobItem


@pytest.fixture
def spider():
    spoder = JobspiderSpider()
    return spoder

class TestJobSpider:

    def test_parse_no_response(self, spider):
        response = None
        with pytest.raises(IgnoreRequest, match="Request ignored due to None response"):   
            next(spider.parse(response))
    

    def test_parse_no_jobs(self, spider):
        body = "<html><body><span>good</span></body></html>"
        response = Selector(text=body)
        with pytest.raises(IgnoreRequest, match="No jobs to scrape"):  
            next(spider.parse(response))
    

    def test_parse_successful(self, spider):
        body = '''
        <table>
            <tbody>
                <tr>
                    <td><a href="/o/database-engineer" class="sc-18rtkup-2 fuWRmp">Database Engineer</a></td>
                    <td><span><span class="custom-css-style-job-location"><span class="custom-css-style-job-location-city">Amsterdam</span><span class="custom-css-style-job-location-city-separator">, </span><span class="custom-css-style-job-location-region">Noord-Holland</span><span class="custom-css-style-job-location-region-separator">, </span><span class="custom-css-style-job-location-country">Netherlands</span></span></span></td>
                    <td aria-label="No department">IT Operations</td>
                    <td style="text-align:right"><a aria-live="off" href="/o/database-engineer" style="white-space:nowrap" class="s03za1-0 keQdpD">View job</a></td>
                </tr>
                <tr>
                    <td><a href="/o/presales-solution-consultant-nl" class="sc-18rtkup-2 fuWRmp">PreSales Solution Consultant</a></td>
                    <td><span><span class="custom-css-style-job-location"><span class="custom-css-style-job-location-city">Amsterdam</span><span class="custom-css-style-job-location-city-separator">, </span><span class="custom-css-style-job-location-region">Noord-Holland</span><span class="custom-css-style-job-location-region-separator">, </span><span class="custom-css-style-job-location-country">Netherlands</span></span></span></td>
                    <td aria-label="No department">Customer Engagement</td>
                    <td style="text-align:right"><a aria-live="off" href="/o/presales-solution-consultant-nl" style="white-space:nowrap" class="s03za1-0 keQdpD">View job</a></td>
                </tr>
                <tr>
                    <td><a href="/o/senior-linux-systems-engineer-onpremise-and-cloud" class="sc-18rtkup-2 fuWRmp">Senior Linux Systems Engineer (On-Premise and Cloud)</a></td>
                    <td><span><span class="custom-css-style-job-location"><span class="custom-css-style-job-location-city">Amsterdam</span><span class="custom-css-style-job-location-city-separator">, </span><span class="custom-css-style-job-location-region">Noord-Holland</span><span class="custom-css-style-job-location-region-separator">, </span><span class="custom-css-style-job-location-country">Netherlands</span></span></span></td>
                    <td aria-label="No department">IT Operations</td>
                    <td style="text-align:right"><a aria-live="off" href="/o/senior-linux-systems-engineer-onpremise-and-cloud" style="white-space:nowrap" class="s03za1-0 keQdpD">View job</a></td>
                </tr>
            </tbody>
        </table>'''
        response = Selector(text=body)
        for item in spider.parse(response):
            assert isinstance(item, JobItem)


    def test_hash_url_fail(self, spider):
        url = None
        with pytest.raises(DropItem, match="Job url is not valid"):   
            spider.hash_url(url)
    
    def test_hash_url(self, spider):
        link = 'https://default/position'
        hashed_url = spider.hash_url(link)
        assert type(hashed_url) is str 