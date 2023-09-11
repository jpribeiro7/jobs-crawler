# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

import pika
from scrapy.utils.serialize import ScrapyJSONEncoder


class RabbitMQPipeline(object):
    ''' This pipeline is responsible for sending job postings to an external service '''
    def __init__(self, host, port, user, password, queue):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.queue = queue
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host,
                                               port=self.port,
                                               credentials=credentials)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        self.encoder = ScrapyJSONEncoder()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("RABBITMQ_HOST"),
            port=crawler.settings.get("RABBITMQ_PORT"),
            user=crawler.settings.get("RABBITMQ_DEFAULT_USER"),
            password=crawler.settings.get("RABBITMQ_DEFAULT_PASS"),
            queue=crawler.settings.get("RABBITMQ_QUEUE"),
        )

    def close_spider(self, spider):
        self.channel.close()
        self.connection.close()

    def process_item(self, item, spider):
        data = self.encoder.encode(item)

        #I realize that routing key and queue are not the same, however for testing purposes it should be enough
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=data,
        )

        return item

   