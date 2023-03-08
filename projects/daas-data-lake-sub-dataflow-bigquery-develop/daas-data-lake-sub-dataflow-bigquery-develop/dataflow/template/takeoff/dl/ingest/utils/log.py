import logging

import apache_beam as beam
from apache_beam.metrics import Metrics

from takeoff.dl.ingest.config import common


class LogMessage(beam.DoFn):
    """
    Log message element, count number of messages using counter metric
    :param subscription: PubSub subscription name
    """

    def __init__(self, subscription):
        super().__init__()
        self.subscription = subscription
        self.message_counter = Metrics.counter(self.__class__, f"message_counter__{subscription}")

    def process(self, element, *args, **kwargs):
        """
        Log each message
        :param element:
        :param args:
        :param kwargs:
        :return:
        """
        pubsub_message_id, message_json_data = element
        self.message_counter.inc()
        logging.info(
            f"PROCESSING MESSAGE (subscription='{self.subscription}'): "
            f"pubsub_message_id='{pubsub_message_id}', "
            f"event_ts='{message_json_data.get(common.EVENT_TIMESTAMP_FIELD, 'unknown')}', "
            f"client='{message_json_data.get(common.CLIENT_FIELD, 'unknown')}', "
            f"source='{message_json_data.get(common.SOURCE_FIELD, 'unknown')}'"
        )
        yield element


class CountError(beam.DoFn):
    """
    Count number of errors using counter metric
    :param subscription: PubSub subscription name
    """

    def __init__(self, subscription):
        super().__init__()
        self.subscription = subscription
        self.error_counter = Metrics.counter(self.__class__, f"error_counter__{subscription}")

    def process(self, element, *args, **kwargs):
        """
        Count each element
        :param element:
        :param args:
        :param kwargs:
        :return:
        """
        self.error_counter.inc()
        yield element
