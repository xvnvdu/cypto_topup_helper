from hiden import yookassa_test_token
from aiogram import Bot, Router, F
from aiogram.handlers import CallbackQueryHandler
from aiogram.types import LabeledPrice, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime
from main import id_generator, total_values, save_total, save_data, save_payments, users_payments_dict, users_data, \
    users_data_dict

router = Router()
pending_payments = {}
pending_payments_info = {}
pending_sending_amount = {}
pending_sending_id = {}
pending_sending_message = {}
pending_sending_info = {}
pending_recieving_info = {}

class CustomPaymentStarsState(StatesGroup):
    waiting_for_custom_amount = State()

class CustomPaymentRubState(StatesGroup):
    waiting_for_custom_amount = State()

class SendToFriend(StatesGroup):
    amount_input = State()
    id_input = State()
    message_input = State()


@router.callback_query()
async def stars_63(call: CallbackQueryHandler, bot: Bot):
    user_id = call.from_user.id
    link_63 = await bot.create_invoice_link(
        title='пополнение на 100₽',
        description='description',
        provider_token='',
        currency='XTR',
        prices=[LabeledPrice(label='Оплата', amount=63)],
        payload='invoice'
    )
    pending_payments[user_id] = 100
    pending_payments_info[user_id] = 'Пополнение баланса — Stars'
    stars_payment_100 = [
        [InlineKeyboardButton(text='Пополнить на 100₽ (63 ⭐️)', url=link_63)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='stars')]
    ]
    stars_payment_100_keyboard = InlineKeyboardMarkup(inline_keyboard=stars_payment_100)
    await call.message.edit_text('<strong>⭐️ Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=stars_payment_100_keyboard)

@router.callback_query()
async def stars_125(call: CallbackQueryHandler, bot: Bot):
    user_id = call.from_user.id
    link_125 = await bot.create_invoice_link(
        title='пополнение на 200₽',
        description='description',
        provider_token='',
        currency='XTR',
        prices=[LabeledPrice(label='Оплата', amount=125)],
        payload='invoice'
    )
    pending_payments[user_id] = 200
    pending_payments_info[user_id] = 'Пополнение баланса — Stars'
    stars_payment_200 = [
        [InlineKeyboardButton(text='Пополнить на 200₽ (125 ⭐️)', url=link_125)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='stars')]
    ]
    stars_payment_200_keyboard = InlineKeyboardMarkup(inline_keyboard=stars_payment_200)
    await call.message.edit_text('<strong>⭐️ Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=stars_payment_200_keyboard)

@router.callback_query()
async def stars_250(call: CallbackQueryHandler, bot: Bot):
    user_id = call.from_user.id
    link_250 = await bot.create_invoice_link(
        title='пополнение на 400₽',
        description='description',
        provider_token='',
        currency='XTR',
        prices=[LabeledPrice(label='Оплата', amount=250)],
        payload='invoice'
    )
    pending_payments[user_id] = 400
    pending_payments_info[user_id] = 'Пополнение баланса — Stars'
    stars_payment_400 = [
        [InlineKeyboardButton(text='Пополнить на 400₽ (250 ⭐️)', url=link_250)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='stars')]
    ]
    stars_payment_400_keyboard = InlineKeyboardMarkup(inline_keyboard=stars_payment_400)
    await call.message.edit_text('<strong>⭐️ Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=stars_payment_400_keyboard)

@router.callback_query()
async def stars_313(call: CallbackQueryHandler, bot: Bot):
    user_id = call.from_user.id
    link_313 = await bot.create_invoice_link(
        title='пополнение на 500₽',
        description='description',
        provider_token='',
        currency='XTR',
        prices=[LabeledPrice(label='Оплата', amount=313)],
        payload='invoice'
    )
    pending_payments[user_id] = 500
    pending_payments_info[user_id] = 'Пополнение баланса — Stars'
    stars_payment_500 = [
        [InlineKeyboardButton(text='Пополнить на 500₽ (313 ⭐️)', url=link_313)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='stars')]
    ]
    stars_payment_500_keyboard = InlineKeyboardMarkup(inline_keyboard=stars_payment_500)
    await call.message.edit_text('<strong>⭐️ Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=stars_payment_500_keyboard)



@router.callback_query()
async def rub_100(call: CallbackQueryHandler, bot: Bot):
    user_id = call.from_user.id
    link_100 = await bot.create_invoice_link(
        title='Пополнение баланса на 100₽',
        description=' ',
        provider_token=yookassa_test_token,
        currency='RUB',
        prices=[LabeledPrice(label='Оплата', amount=100*100)],
        payload='invoice'
    )
    pending_payments[user_id] = 100
    pending_payments_info[user_id] = 'Пополнение баланса — ЮKassa'
    rub_payment_100 = [
        [InlineKeyboardButton(text='Пополнить на 100₽ 💵', url=link_100)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='YK')]
    ]
    rub_payment_100_keyboard = InlineKeyboardMarkup(inline_keyboard=rub_payment_100)
    print(pending_payments)
    await call.message.edit_text('<strong>💳 Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=rub_payment_100_keyboard)

@router.callback_query()
async def rub_200(call: CallbackQueryHandler, bot: Bot):
    user_id = call.from_user.id
    link_200 = await bot.create_invoice_link(
        title='Пополнение баланса на 200₽',
        description=' ',
        provider_token=yookassa_test_token,
        currency='RUB',
        prices=[LabeledPrice(label='Оплата', amount=200*100)],
        payload='invoice'
    )
    pending_payments[user_id] = 200
    pending_payments_info[user_id] = 'Пополнение баланса — ЮKassa'
    rub_payment_200 = [
        [InlineKeyboardButton(text='Пополнить на 200₽ 💵', url=link_200)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='YK')]
    ]
    rub_payment_200_keyboard = InlineKeyboardMarkup(inline_keyboard=rub_payment_200)
    await call.message.edit_text('<strong>💳 Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=rub_payment_200_keyboard)

@router.callback_query()
async def rub_400(call: CallbackQueryHandler, bot: Bot):
    user_id = call.from_user.id
    link_400 = await bot.create_invoice_link(
        title='Пополнение баланса на 400₽',
        description=' ',
        provider_token=yookassa_test_token,
        currency='RUB',
        prices=[LabeledPrice(label='Оплата', amount=400*100)],
        payload='invoice'
    )
    pending_payments[user_id] = 400
    pending_payments_info[user_id] = 'Пополнение баланса — ЮKassa'
    rub_payment_400 = [
        [InlineKeyboardButton(text='Пополнить на 400₽ 💵', url=link_400)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='YK')]
    ]
    rub_payment_400_keyboard = InlineKeyboardMarkup(inline_keyboard=rub_payment_400)
    await call.message.edit_text('<strong>💳 Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=rub_payment_400_keyboard)

@router.callback_query()
async def rub_500(call: CallbackQueryHandler, bot: Bot):
    user_id = call.from_user.id
    link_500 = await bot.create_invoice_link(
        title='Пополнение баланса на 500₽',
        description=' ',
        provider_token=yookassa_test_token,
        currency='RUB',
        prices=[LabeledPrice(label='Оплата', amount=500*100)],
        payload='invoice'
    )
    pending_payments[user_id] = 500
    pending_payments_info[user_id] = 'Пополнение баланса — ЮKassa'
    rub_payment_500 = [
        [InlineKeyboardButton(text='Пополнить на 500₽ 💵', url=link_500)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='YK')]
    ]
    rub_payment_500_keyboard = InlineKeyboardMarkup(inline_keyboard=rub_payment_500)
    await call.message.edit_text('<strong>💳 Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=rub_payment_500_keyboard)


@router.message()
async def rub_custom(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    pending_payments[user_id] = int(pending_payments[user_id])
    amount = pending_payments[user_id]
    pending_payments_info[user_id] = 'Пополнение баланса — ЮKassa'
    custom_rub_link = await bot.create_invoice_link(
        title=f'Пополнение баланса на {amount}₽',
        description=' ',
        provider_token=yookassa_test_token,
        currency='RUB',
        prices=[LabeledPrice(label='Оплата', amount=amount*100)],
        payload='invoice'
    )
    custom_rub_payment = [
        [InlineKeyboardButton(text=f'Пополнить на {amount}₽ 💵', url=custom_rub_link)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='YK')]
    ]
    custom_rub_keyboard = InlineKeyboardMarkup(inline_keyboard=custom_rub_payment)
    await message.answer('<strong>💳 Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=custom_rub_keyboard)


@router.message()
async def stars_custom(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    pending_payments[user_id] = int(pending_payments[user_id])
    amount = pending_payments[user_id]
    pending_payments_info[user_id] = 'Пополнение баланса — Stars'
    stars_amount = round(amount/1.7)
    custom_stars_link = await bot.create_invoice_link(
        title=f'Пополнение баланса на {amount}₽',
        description=' ',
        provider_token=yookassa_test_token,
        currency='XTR',
        prices=[LabeledPrice(label='Оплата', amount=stars_amount)],
        payload='invoice'
    )
    custom_stars_payment = [
        [InlineKeyboardButton(text=f'Пополнить на {amount}₽ ({stars_amount} ⭐️)', url=custom_stars_link)],
        [InlineKeyboardButton(text='Изменить сумму', callback_data='stars')]
    ]
    custom_stars_keyboard = InlineKeyboardMarkup(inline_keyboard=custom_stars_payment)
    await message.answer('<strong>⭐️ Для пополнения баланса нажмите кнопку ниже:</strong>',
                                 parse_mode='HTML', reply_markup=custom_stars_keyboard)


@router.message()
async def send_to_user(call: CallbackQueryHandler, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_data_dict[user_id]
    reciever_id = pending_sending_id[user_id]
    reciever_data = users_data_dict[reciever_id]
    user_data['Balance'] = int(user_data['Balance'])
    reciever_data['Balance'] = int(reciever_data['Balance'])

    amount = pending_sending_amount[user_id]
    amount = int(amount)

    pending_sending_info[user_id] = f' Перевод баланса — ID: <code>{reciever_id}</code>'
    pending_recieving_info[reciever_id] = f' Пополнение баланса — ID: <code>{user_id}</code>'
    sender_info = pending_sending_info[user_id]
    reciever_info = pending_recieving_info[reciever_id]

    sender_payments = users_payments_dict[user_id]['Transactions']
    reciever_payments = users_payments_dict[reciever_id]['Transactions']

    today = datetime.now().strftime('%d.%m.%Y')
    time_now = datetime.now().strftime('%H:%M:%S')

    if call.from_user.id in pending_sending_amount:
        trx_sender_id = await id_generator()
        trx_reciever_id = await id_generator()
        total_values['Total_transactions_count'] += 1
        trx_num = total_values['Total_transactions_count']
        user_data['Balance'] -= amount
        reciever_data['Balance'] += amount

        await save_total()
        await save_data()

        if today not in sender_payments:
            sender_payments[today] = {time_now: {'RUB': amount,
                                                 'transaction_num': trx_num,
                                                 'type': sender_info, 'trx_id': trx_sender_id}}
            await save_payments()
        else:
            sender_payments[today][time_now] = {'RUB': amount,
                                                 'transaction_num': trx_num,
                                                 'type': sender_info, 'trx_id': trx_sender_id}
            await save_payments()
        if today not in reciever_payments:
            reciever_payments[today] = {time_now: {'RUB': amount,
                                                 'transaction_num': trx_num,
                                                 'type': reciever_info, 'trx_id': trx_reciever_id}}
            await save_payments()
        else:
            reciever_payments[today][time_now] = {'RUB': amount,
                                                 'transaction_num': trx_num,
                                                 'type': reciever_info, 'trx_id': trx_reciever_id}
            await save_payments()

        if pending_sending_message[user_id] is not None:
            await bot.send_message(chat_id=reciever_id,
                                   text=f'<strong>🎉 Пополнение баланса от другого пользователя!</strong>\n\n'
                                        f'<i>🥷 Перевод от пользователя под ID: <code>{user_id}</code>\n💰 Сумма перевода: '
                                        f'<code>{amount}₽</code>\n📨 Сообщение от пользователя:</i>\n\n{pending_sending_message[user_id]}',
                                   parse_mode='HTML')
        else:
            await bot.send_message(chat_id=reciever_id,
                                   text=f'<strong>🎉 Пополнение баланса от другого пользователя!</strong>\n\n'
                                        f'<i>🥷 Перевод от пользователя под ID: <code>{user_id}</code>\n💰 Сумма перевода: '
                                        f'<code>{amount}₽</code></i>', parse_mode='HTML')

    del (pending_sending_amount[user_id], pending_sending_message[user_id], pending_sending_id[user_id],
         pending_sending_info[user_id], pending_recieving_info[reciever_id])