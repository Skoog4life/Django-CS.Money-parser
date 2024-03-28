from aiogram import types

from bot.utils.loader import bot, dp, memory_storage, loop
from bot.models import TelegramUser, ItemPrice
from asgiref.sync import sync_to_async
from bot.handlers import logic

from django.contrib.auth.models import User
from django.db import IntegrityError

from bot.utils.steam_price_checker import check_item_price

from aiogram.utils.exceptions import MessageTextIsEmpty

from aiogram.dispatcher import FSMContext

from bot.keyboards import keyboard


@dp.message_handler(commands=['notify_on'])
async def notify_on(message: types.Message):
    await TelegramUser.objects.filter(pk=message.from_user.id).aupdate(notify=True)

@dp.message_handler(commands=['notify_off'])
async def notify_off(message: types.Message):
    await TelegramUser.objects.filter(pk=message.from_user.id).aupdate(notify=False)

@dp.message_handler(commands=['profit'])
@dp.message_handler(state=logic.FiniteStateMachine.profit)
async def change_profit(message: types.Message, state: FSMContext): 
    current_state = await state.get_state()
    if current_state is None:
        profit = message.get_args()
    else:
        profit = message.text
        await state.finish()
    try:
        user = await TelegramUser.objects.aget(pk=message.from_user.id)
        await sync_to_async(user.set_desired_profit)(int(profit))
    except MessageTextIsEmpty:
        await message.reply('You need to provide the desired profit. Use the command like this: /profite <profit>')
    except:
        await message.reply('Try again')

@dp.message_handler(commands=['check'])
@dp.message_handler(state=logic.FiniteStateMachine.check)
async def check_price(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    try:
        if current_state is None:
            item_name = " ".join(message.get_args().split())
        else:
            item_name = message.text
            await state.finish()
        await message.reply(f'{item_name}')       
        if await ItemPrice.objects.filter(name=item_name).aexists(): 
            price = await check_item_price(item_name=item_name)
            await message.reply(f'Price of {item_name} is {price}')
        else:
            await message.reply('Item not found')    
    except MessageTextIsEmpty:
        await message.reply('You need to provide an item name. Use the command like this: /check <item_name>')
    except:
        await message.reply('Try again')


@dp.message_handler(commands=['create_user'])
@dp.message_handler(state=logic.FiniteStateMachine.create_user)
async def create_user(message: types.Message, state: FSMContext):    
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    current_state = await state.get_state()

    if current_state is None:
        username, password = message.get_args().split()   
    else:
        username, password = message.text.split()
        await state.finish()    
    user_request_user = await sync_to_async(lambda: user_request.user)() 
    if not user_request_user:
        try:
            user = await sync_to_async(User.objects.create_user)(username=username, password=password)
            await sync_to_async(user.save)()            
            await sync_to_async(user_request.set_user)(user)
            await message.reply('User created')
        except IntegrityError:
            await message.reply('User with this username already exists')         
    else:
        await message.reply('User already exists')
