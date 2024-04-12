import asyncio
import os

from twscrape import API, gather
from twscrape.logger import set_log_level
import json

async def main():
    api = API()

    #Account adding removed for commi

    # await api.pool.login_all()

    set_log_level("TRACE")
    # repids = open("republicans", "r").read().split("\n")
    # for i in range(len(repids)):
    #     repids[i] = repids[i].split(".com/")[1]

    # print(repids)

    total_searches = 0

    following_dmc = []
    following_dmc.extend(await gather(api.following("722793491059769344", limit=1600)))
    following_dmc.extend(await gather(api.following("73754019", limit=1600)))
    following_dmc.extend(await gather(api.following("14377605", limit=1600)))
    following_dmc.extend(await gather(api.following("939091", limit=1600)))
    following_dmc.extend(await gather(api.following("409486555", limit=1600)))
    following_dmc.extend(await gather(api.following("216776631", limit=1600)))
    following_dmc.extend(await gather(api.following("1349154719386775552", limit=1600)))

    followers_following_ids = []
    following_dmc_ids = []
    i = 0
    for follower in following_dmc:
        following_dmc_ids.append(follower.id)
        follower = await gather(api.following(follower.id, limit=10))
        print(i)
        for fol in follower:
            followers_following_ids.append(fol.id)
        i += 1

    print(followers_following_ids)
    print(following_dmc_ids)
    print(len(followers_following_ids))
    print(len(following_dmc_ids))

    with open("DMC", "w") as f:
        for id in following_dmc_ids:
            f.write("%s\n" % id)
        for id in followers_following_ids:
            f.write("%s\n" % id)



    # for user_id in repids:
    #     print(user_id + " starting")
    #     tweets = await gather(api.search(user_id, limit=100))
    #
    #     for tweet in tweets:
    #         filename = f"rep/{user_id}/tweet_{tweet.id}.json"
    #         os.makedirs(os.path.dirname(filename), exist_ok=True)
    #         f = open(filename, "w")
    #         f.write(json.dumps(tweet.dict(), indent = 4, default=str))
    #     total_searches += 1
    #     print(f"{user_id} finished total searches is {total_searches}")
    #
    # demids = open("democrats", "r").read().split("\n")
    # for i in range(len(demids)):
    #     demids[i] = demids[i].split(".com/")[1]
    #
    # print(demids)
    #
    # for user_id in demids:
    #     print(user_id + " starting")
    #     tweets = await gather(api.search(user_id, limit=100))
    #
    #     for tweet in tweets:
    #         filename = f"dem/{user_id}/tweet_{tweet.id}.json"
    #         os.makedirs(os.path.dirname(filename), exist_ok=True)
    #         f = open(filename, "w")
    #         f.write(json.dumps(tweet.dict(), indent=4, default=str))
    #     total_searches += 1
    #     print(f"{user_id} finished total searches is {total_searches}")

if __name__ == "__main__":
    asyncio.run(main())