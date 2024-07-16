#!/usr/bin/env python3
""" function"""


def schools_by_topic(mongo_collection, topic):
    """
    function that returns the list of school having a specific topic

    Args:
        mongo_collection: collection
        topic: topic
    Returns:
        list of school
    """
    new_topic = list(mongo_collection.find({"topics": topic}))
    return new_topic
