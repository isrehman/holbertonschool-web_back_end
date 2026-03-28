#!/usr/bin/env python3
"""Module that returns all students sorted by average score"""


def top_students(mongo_collection):
    """Returns all students sorted by average score.

    Args:
        mongo_collection: pymongo collection object

    Returns:
        List of students sorted by average score with averageScore key
    """
    return list(mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]))
