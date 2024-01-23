#!/usr/bin/env python3
"""
    10-update_topics.py
"""

from pymongo.collection import Collection


def update_topics(mongo_collection: Collection, name, topics):
    """changes all topics of a school document based on the name"""

    mongo_collection.update_one({"name": name}, {"$set": {"topics": topics}})
