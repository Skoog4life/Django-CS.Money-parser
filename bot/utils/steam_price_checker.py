import aiohttp
import asyncio

from urllib.parse import quote

from asgiref.sync import sync_to_async

from bot.models import ItemPrice

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Chrome/67.0.3396.62 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

async def steam_hash_name(item_name):
    return quote(item_name).replace('/','-')

async def steam_request(item_name):
    url = f"https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name={await steam_hash_name(item_name)}" 
    steam_commission = 0.8697
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10, headers=headers) as response:
            data = await response.json()
            if data is not None:
                if "success" in data and data["success"] == True:
                    if "lowest_price" in data:
                        price = float(data["lowest_price"][1:].replace(",", ""))
                    elif "median_price" in data:                        
                        price = float(data["median_price"][1:].replace(",", ""))
                    return round(price * steam_commission, 3) # Formula for calculating profit
                else:
                    return -1
            else:
                await asyncio.sleep(5)
                print("Waiting for steam...")
                return await steam_request(item_name)


async def check_item_price(item_name, update=False):
    item = await ItemPrice.objects.filter(name=item_name).afirst() # Take the first item
    if item and not await sync_to_async(item.need_to_update)(24) and not update: # 
        return item.price
    else:
        await asyncio.sleep(3)
        item_price = await steam_request(item_name)
        if item_price == -1:
            return -1
        item, _ = await ItemPrice.objects.aupdate_or_create(name=item_name,defaults={'price':item_price})
        print(f'Updated item: {item_name}')
        return item.price
