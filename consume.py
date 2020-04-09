#!/usr/bin/env python

import logging
from multiprocessing import Process
import string
import json
import time
import random
from kafka import KafkaConsumer
import argparse


logging.basicConfig(level=logging.WARNING)


def run_consumer(topic, group_id, consumer_id):
    print(
        f"Consuming on topic {topic} with group {group_id} from consumer {consumer_id}"
    )
    consumer = KafkaConsumer(
        topic,
        group_id=group_id,
        bootstrap_servers=["kafka:9092"],
        value_deserializer=lambda v: json.loads(v.decode("utf8")),
    )

    for msg in consumer:
        print(
            f"consumer_id: {consumer_id}, topic: {msg.topic}, partition: {msg.partition}, offset: {msg.offset}, key: {msg.key} message: {msg.value}"
        )


class ConsumerThread(Process):
    def __init__(self, consumer_id, topic, group_id=None):
        Process.__init__(self)
        self.daemon = True

        self.consumer_id = consumer_id
        self.topic = topic = topic
        self.group_id = group_id

    def run(self):
        if self.group_id is None:
            # Pick a random group id
            group_id = self.random_group_id()
        else:
            group_id = self.group_id

        run_consumer(self.topic, group_id, self.consumer_id)

    def random_group_id(self, n=16):
        return "".join(random.choice(string.ascii_lowercase) for _ in range(n))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--topic", required=True)
    parser.add_argument("-g", "--group-id")
    parser.add_argument("-n", "--n-consumers", required=True, type=int)
    args = parser.parse_args()

    for i in range(args.n_consumers):
        consumer = ConsumerThread(
            consumer_id=i, topic=args.topic, group_id=args.group_id
        )
        consumer.start()

    time.sleep(86400)
