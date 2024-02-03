import requests
import json
import urllib.parse
import time
import asyncio
import aiohttp
import aiofiles
from .steam_price_checker import check_item_price

from bot.models import FoundItem


async def parser():
    page_count = 180
    csmoney_allowed_discount = 0.25
    steam_allowed_profit = 1.25
    try:
        async with aiohttp.ClientSession() as session:
            for page in range(0, page_count, 60):
                stop_loop = False
                async with session.get(
                    f"https://cs.money/1.0/market/sell-orders?limit=60&minPrice=0.25&offset={page}&order=desc&sort=discount&type=12",
                    timeout=10,
                ) as response:
                    src = await response.text()
                    try:
                        data = json.loads(src)
                    except json.JSONDecodeError as e:
                        data = {"items": []}
                        stop_loop = True
                        print("CSMONEY ERROR")

                    async with aiofiles.open(f"items{page}.json", "w", encoding="utf-8") as file:
                        await file.write(json.dumps(data, indent=4, ensure_ascii=False))

                    item_list = []
                    for item in data["items"]:
                        if item["pricing"]["discount"] >= csmoney_allowed_discount:
                            item_id = item["id"]
                            full_name_of_item = item["asset"]["names"]["full"]
                            item_link = (
                                f"https://steamcommunity.com/market/listings/730/{urllib.parse.quote(full_name_of_item)}"
                            )
                            csmoney_computed_price = item["pricing"]["computed"]
                            csmoney_discount = item["pricing"]["discount"]

                            item_list.append(
                                {
                                    "Item ID": item_id,
                                    "Name": full_name_of_item,
                                    "Link": item_link,
                                    "Price": csmoney_computed_price,
                                    "Discount": csmoney_discount,
                                }
                            )

                            steam_price = await check_item_price(item_name=full_name_of_item)
                            if steam_price == -1:
                                continue

                            profit = float(steam_price / csmoney_computed_price)

                            if profit >= steam_allowed_profit:
                                await FoundItem.objects.aget_or_create(
                                    item_id=item_id,
                                    name=full_name_of_item,
                                    link=item_link,
                                    csmoney_price=csmoney_computed_price,
                                    steam_price=steam_price,
                                    profit=profit,
                                )
                                # print(f"PROFIT {full_name_of_item} {profit}")

                        else:
                            stop_loop = True
                            break

                    async with aiofiles.open(f"items_discount{page}.json", "w", encoding="utf-8") as file:
                        await file.write(json.dumps(item_list, indent=4, ensure_ascii=False))

                if stop_loop:
                    break
        print("code")
    except TimeoutError:
        print('Sleep (10)')
        await asyncio.sleep(10)

