import asyncio
import os
import threading
from random import shuffle

from twscrape import API, gather
from twscrape.logger import set_log_level
import json

async def main():
    api = API()

    #Account adding removed for commi

    # await api.pool.login_all()

    set_log_level("TRACE")

    repids = open("republicans", "r").read().split("\n")
    shuffle(repids)
    repids = repids[:9000]

    demids = open("democrats", "r").read().split("\n")
    shuffle(demids)
    demids = demids[:9000]



    following_dmc = []
    following_dmc.extend(await gather(api.following("11134252", limit=1600)))
    following_dmc.extend(await gather(api.following("15207668", limit=1600)))
    following_dmc.extend(await gather(api.following("14344823", limit=1600)))
    following_dmc.extend(await gather(api.following("1249982359", limit=1600)))

    print(len(following_dmc))

    followers_following_ids = []
    following_dmc_ids = []
    i = 0
    with open("GOP2", "w") as f:
        for follower in following_dmc:
            following_dmc_ids.append(follower.id)
            f.write("%s\n" % follower.id)
            follower = await gather(api.following(follower.id, limit=10))
            print(i)
            for fol in follower:
                followers_following_ids.append(fol.id)
                f.write("%s\n" % fol.id)
            i += 1

    print(followers_following_ids)
    print(following_dmc_ids)
    print(len(followers_following_ids))
    print(len(following_dmc_ids))

    total_searches = 0
    for user_id in repids:
        try:
            print(user_id + " starting republican")
            tweets = await gather(api.user_tweets(user_id, limit=10))

            for tweet in tweets:
                filename = f"rep/{user_id}/tweet_{tweet.id}.json"
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                f = open(filename, "w")
                f.write(json.dumps(tweet.dict(), indent = 4, default=str))
            total_searches += 1
            print(f"{user_id} finished total searches is {total_searches}")
        except:
            print(f"Error with {user_id}")

    total_searches = 0
    for user_id in demids:
        print(user_id + " starting democrat")
        tweets = await gather(api.user_tweets(user_id, limit=10))

        for tweet in tweets:
            filename = f"dem/{user_id}/tweet_{tweet.id}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            f = open(filename, "w")
            f.write(json.dumps(tweet.dict(), indent=4, default=str))
        total_searches += 1
        print(f"{user_id} finished total searches is {total_searches}")

if __name__ == "__main__":
    asyncio.run(main())