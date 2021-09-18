#%%
#!pip install aiohttp
#!pip install understat
#!pip install nest-asyncio
#%%
import asyncio
import json

import aiohttp

from understat import Understat

import nest_asyncio
nest_asyncio.apply()
#__import__('IPython').embed()

async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        fixtures = await understat.get_league_results(
            "epl",
            2018,
            {
                 "goals": {
            "h": "2",
            "a": "2"
        }
            }, 
           
        )
        return ([(x['id'], x['h']['short_title'], x['a']['short_title'], x['datetime']) for x in fixtures])

loop = asyncio.get_event_loop()
#loop.run_until_complete(main())
# %%
output = loop.run_until_complete(main())

# %%
for x in output: 
    print(x)
# %%
print(output)
# %%
