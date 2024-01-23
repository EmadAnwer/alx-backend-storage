#!/usr/bin/env python3
""" 12-log_stats """
from pymongo import MongoClient
from pymongo.collection import Collection

if __name__ == "__main__":
    client: MongoClient = MongoClient("mongodb://127.0.0.1:27017")
    nginx_c: Collection = client.logs.nginx

    # nginx collection count
    print(f"{nginx_c.count_documents({})} logs")
    method: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for m in method:
        c: int = nginx_c.count_documents({"method": m})
        print(f"\tmethod {m}: {c}")

    count: int = nginx_c.count_documents({"method": "GET", "path": "/status"})
    print(f"{count} status check")
