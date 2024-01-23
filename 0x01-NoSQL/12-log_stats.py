#!/usr/bin/env python3
""" provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient


if __name__ == "__main__":
    """provides some stats about Nginx logs stored in MongoDB"""

    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_c = client.logs.nginx

    n_logs = nginx_c.count_documents({})
    print(f"{n_logs} logs")
    methods: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for m in methods:
        c: int = nginx_c.count_documents({"method": m})
        print(f"\tmethod {m}: {c}")

    status_check: int = nginx_c.count_documents(
        {"method": "GET", "path": "/status"}
        )
    print(f"{status_check} status check")
