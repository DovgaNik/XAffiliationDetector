import asyncio
import os
import random
import time

from twscrape import API, gather
from twscrape.logger import set_log_level
import json

async def main():
    api = API()

    #Account adding removed for commi

    await api.pool.login_all()

    set_log_level("TRACE")

    repids = open("republicans", "r").read().split("\n")
    for i in range(len(repids)):
        repids[i] = repids[i].split(".com/")[1]

    print(repids)

    total_searches = 0

    for user_id in repids:
        print(user_id + " starting")
        tweets = await gather(api.search(user_id, limit=100))

        for tweet in tweets:
            filename = f"rep/{user_id}/tweet_{tweet.id}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            f = open(filename, "w")
            f.write(json.dumps(tweet.dict(), indent = 4, default=str))
        total_searches += 1
        print(f"{user_id} finished total searches is {total_searches}")

    demids = open("democrats", "r").read().split("\n")
    for i in range(len(demids)):
        demids[i] = demids[i].split(".com/")[1]

    print(demids)

    for user_id in demids:
        print(user_id + " starting")
        tweets = await gather(api.search(user_id, limit=100))

        for tweet in tweets:
            filename = f"dem/{user_id}/tweet_{tweet.id}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            f = open(filename, "w")
            f.write(json.dumps(tweet.dict(), indent=4, default=str))
        total_searches += 1
        print(f"{user_id} finished total searches is {total_searches}")

if __name__ == "__main__":
    asyncio.run(main())