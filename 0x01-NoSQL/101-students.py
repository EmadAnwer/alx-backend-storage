#!/usr/bin/env python3
"""Module for 101-students"""

from pymongo.collection import Collection


def top_students(mongo_collection:Collection):
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
