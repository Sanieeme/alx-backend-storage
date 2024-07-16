#!/usr/bin/env python3
""" python function"""


def update_topics(mongo_collection, name, topics):
    """
    update topics
    Args:
        mongo_collection: collection
        name: string
        topics: list of strings
    Returns:
         list of trings
    """
    filter = {"name": name}
    topic = {"$set": {"topics": name}}
    mongo_collection.update_one(filter, topic)
