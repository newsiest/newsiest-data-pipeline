import logging
import pika
import os
import json
from pipeline.pipeline_stage import PipelineStage

class ExportManager(PipelineStage):
    def __init__(self):
        super().__init__()
        """
        Set up the RabbitMQ connection and channel
        """
        logging.getLogger('pika').setLevel(logging.WARNING)
        url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
        params = pika.URLParameters(url)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()

    def _process_one(self, to_process):
        """
        Declare the articles queue, and send the article JSON to it
        """
        self._channel.queue_declare(queue='articles')
        body = to_process.as_dict()
        self._channel.basic_publish(exchange='', routing_key='articles', body=json.dumps(body, sort_keys=True, default=str))
        return to_process

    def _post_process(self):
        """
        Close the RabbitMQ connection
        """
        self._connection.close()
