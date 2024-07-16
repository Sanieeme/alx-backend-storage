#!/usr/bin/env python3
""" python function"""


def update_topics(mongo_collection, name, topics):
    filter = {"name": name}
    topic = {"$set": {"topics": name}}
    mongo_collection.update_one(filter, topic)
