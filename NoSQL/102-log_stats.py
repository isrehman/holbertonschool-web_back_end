#!/usr/bin/env python3
"""Module that provides stats about Nginx logs stored in MongoDB
with top 10 IPs"""
from pymongo import MongoClient


def log_stats():
    """Provides stats about Nginx logs stored in MongoDB
    with top 10 most present IPs"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    print("{} logs".format(collection.count_documents({})))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))
    status = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status))

    print("IPs:")
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in top_ips:
        print("\t{}: {}".format(ip.get('_id'), ip.get('count')))


if __name__ == "__main__":
    log_stats()
