#!/usr/bin/env python3
"""python function"""


def list_all(mongo_collection):
    """
    Python function that lists all documents in a collection

    Args:
        mongo_collection: collection
    Returns:
        list
    """
    cursor = mongo_collection.find({})
    documents = list(cursor)
    return documents
