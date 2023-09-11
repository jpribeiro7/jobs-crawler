# jobs-crawler


### Design Choices:
My system design consists in three main components:
 - url seed - Redis Publisher that handles which websites we want to scrape.
 - url frontier - Redis that stores websites to scrape and is accessed by several redis-spiders.
 - spiders - downloads html, parses their jobs, checks for duplicates and sends them to an external service via RabbitMQ


### Why use Redis and Scrapy-Redis? 
Scrapy-redis spiders can access redis as distributed workers. This means that for if there is more than one page of job postings, you can process each page in a separate spider.

### Why use RabbitMQ? 
RabbitMQ can handle assure that millions of job-postings are handled while also providing fault tolerance. The ability to establish retries and the usage of Dead-letter-queue can help to monitor and decrease the number of errors in the system.

### Setup Redis:
    ```docker
        docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
    ```

### Setup RabbitMQ with docker: 
    ```docker
        docker run -d -p 15672:15672 --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
    ```

### Run url seed
    ```python
        python url_seed.py
    ```

### Build TextKernel Crawler
    ```docker
        docker build -t textkernel .
    ```

Current limitations and bottlenecks:
1. The current architecture provides duplication handling for job postings via spider.state. This means that if we run several scrappers of the same type, it won't guarantee duplcation handling.
2. Links can currently be scrapped more than once. This means that different jobs of the same spider might process a link again.
3. We might run into anti-scraping techniques.
4. Only one spider was built.

To solve #1 and #2 we could build a separate shared cache (like Redis) as the following diagram shows:


To solve #3 we might need to timeout requests or implement proxies.



How do we handle Continuous Delivery for different crawlers?
- Create a repos for a different crawler?
- Always deploy all the crawlers?