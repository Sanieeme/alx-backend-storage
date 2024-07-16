#!/usr/bin/env python3
"""function that insert """


def insert_school(mongo_collection, **kwargs):
    """
    Python function that inserts a new document in a collection based on kwargs
    Args:
        mongo_collection: collection
        kwargs: parameter
    Returns:
        new documents
    """
    documents = mongo_collection.insert_one(kwargs)
    return documents.inserted_id
