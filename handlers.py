import math
import time
from datetime import datetime
from aiogram.filters import Command
from aiogram import F, Router, types, Bot

import payments
from payments import (pending_payments, pending_payments_info, rub_custom,
                      stars_custom, CustomPaymentRubState, CustomPaymentStarsState, SendToFriend,
                      pending_sending_amount, pending_sending_id, pending_sending_message, send_to_user)
from aiogram.fsm.context import FSMContext
from aiogram.handlers import CallbackQueryHandler
from main import (users_data, users_payments, users_data_dict, users_payments_dict,
                  save_data, save_payments, total_values, save_total, id_generator)
from bot_buttons import (menu_keyboard, account_keyboard, payment_keyboard,
                         withdraw_keyboard, stars_keyboard, yk_payment_keyboard,
                         zero_transactions_keyboard, log_buttons, send_keyboard, try_again_amount_keyboard,
                         step_back_keyboard, try_again_id_keyboard, confirm_sending_keyboard, skip_message_keyboard)
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, PreCheckoutQuery


router = Router()



@router.message(Command('menu'))
async def command_menu(message: Message):
    user_id = message.from_user.id
    user_data = users_data_dict[user_id]
    print(f'Пользователь {user_id} оспользовался командой меню')
    if user_data['Is_verified']:
        await message.answer( '<strong>Выберите нужное действие:</strong>',
                         parse_mode='HTML', reply_markup=menu_keyboard)
    else:
        await confirm_phone(message)


@router.message(Command('account'))
async def command_account(message: Message):
    user_id = message.from_user.id
    user_data = users_data_dict[user_id]
    phone = int(user_data['Phone']) // 10**4
    balance = user_data['Balance']
    registration_date = user_data['Registration']
    volume = user_data['Funding_volume']
    days_count = (datetime.now() - datetime.strptime(registration_date, '%d.%m.%Y')).days
    if days_count % 10 == 1 and days_count % 100 != 11:
        days = 'день'
    elif days_count % 10 in [2, 3, 4] and not (11 <= days_count % 100 <= 19):
        days = 'дня'
    else:
        days = 'дней'
    print(f'Пользователь {user_id} оспользовался командой аккаунт')
    if user_data['Is_verified']:
        await message.answer(f'<strong>Мой аккаунт</strong>\n\n'
                             f'⚙️ <strong>ID:</strong> <code>{message.from_user.id}</code>\n'
                             f'🔒 <strong>Телефон:</strong> <code>{phone}****</code>\n'
                             f'🗓 <strong>Регистрация:</strong> <code>{registration_date} ({days_count} {days})</code>\n\n'
                             f'💵 <strong>Мой баланс: </strong><code>{balance}₽</code>\n'
                             f'💎 <strong>Мои пополнения за все время: </strong><code>{volume}₽</code>',
                             parse_mode='HTML', reply_markup=account_keyboard)
    else:
        await confirm_phone(message)


@router.message(Command('balance'))
async def command_balance(message: Message):
    user_id = message.from_user.id
    user_data = users_data_dict.get(user_id)
    print(f'Пользователь {user_id} оспользовался командой баланс')
    if user_data['Is_verified']:
        await message.answer('<strong>Выберите удобный способ пополнения баланса:</strong>',
                         parse_mode='HTML', reply_markup=payment_keyboard)
    else:
        await confirm_phone(message)


@router.message(Command('withdraw'))
async def command_withdraw(message: Message):
    user_id = message.from_user.id
    user_data = users_data_dict[user_id]
    print(f'Пользователь {user_id} оспользовался командой вывести')
    if user_data['Is_verified']:
        await message.answer('<strong>В разработке...</strong>',
                         parse_mode='HTML', reply_markup=withdraw_keyboard)
    else:
        await confirm_phone(message)


@router.message(Command('start'))
async def start(message: Message):
    user_id = message.from_user.id
    user = {'ID': user_id, 'Name': message.from_user.first_name,
            'Surname': message.from_user.last_name,
            'Username': message.from_user.username, 'Phone': None,
            'Is_verified': False, 'Registration': None, 'Balance': 0,
            'Funding_volume': 0}
    user_payments = {'ID': user_id,
                     'Transactions': {}
    }
    print(f'Пользователь {user_id} оспользовался командой старт')
    if user_id not in users_data_dict:
        total_values['Total_users'] += 1
        await message.answer('Привет! 🤖\nКак ты мог заметить, с сайта 5sim.biz '
                             'пропали все способы пополнения баланса, '
                             'кроме криптовалют.\nНе волнуйся, я создан, '
                             'чтобы помочь тебе с пополнением, в том случае, '
                             'если у тебя нет биржи или кошелька, с которых ты мог '
                             'бы пополнять баланс самостоятельно! 🤩')
        users_data.append(user)
        users_payments.append(user_payments)
        await save_data()
        await save_payments()
        await save_total()
        users_payments_dict[user_id] = user_payments
        users_data_dict[user_id] = user

    user_data = users_data_dict[user_id]

    if not user_data['Is_verified']:
        await confirm_phone(message)
    else:
        await command_menu(message)


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    user_id = message.from_user.id
    user_data = users_data_dict[user_id]
    user_payment = users_payments_dict[user_id]['Transactions']
    today = datetime.now().strftime('%d.%m.%Y')
    time_now = datetime.now().strftime('%H:%M:%S')
    print(pending_payments, 'я тут')
    await message.answer('<strong>Оплата успешная 🎉</strong>\n<i>Примечание: '
                         'не используйте одну и ту же ссылку на пополнение дважды, '
                         'ваша оплата не будет засчитана!</i>', parse_mode= 'HTML')
    if message.from_user.id in pending_payments:
        amount = pending_payments[user_id]
        trx_type = pending_payments_info[user_id]
        trx_id = await id_generator()
        total_values['Total_topups_count'] += 1
        total_values['Total_topups_volume'] += amount
        total_values['Total_transactions_count'] += 1
        trx_num = total_values['Total_transactions_count']
        user_data['Balance'] += amount
        user_data['Funding_volume'] += amount
        await save_total()
        await save_data()
        if today not in user_payment:
            user_payment[today] = {time_now: {'RUB': amount,
                                              'transaction_num': trx_num,
                                              'type': trx_type, 'trx_id': trx_id}}
            await save_payments()
        else:
            user_payment[today][time_now] = {'RUB': amount,
                                             'transaction_num': trx_num,
                                             'type': trx_type, 'trx_id': trx_id}
            await save_payments()
        del pending_payments_info[user_id]
        del pending_payments[user_id]
        print(pending_payments)


@router.message(F.contact)
async def check_contact(message: Message):
    user_id = message.from_user.id

    if message.contact is not None and message.contact.user_id == user_id:
        user_data = users_data_dict[user_id]
        user_data['Phone'] = message.contact.phone_number
        user_data['Is_verified'] = True
        user_data['Registration'] = time.strftime('%d.%m.%Y')
        total_values['Total_verified_users'] += 1
        await save_total()
        await save_data()
        remove_button = types.ReplyKeyboardRemove()
        await message.answer('<b>Номер телефона успешно подтвержден!</b> 🎉\n'
                             'Вы можете пользоваться ботом.', parse_mode='HTML',
                             reply_markup=remove_button)
        await command_menu(message)
    else:
        await confirm_phone(message)


@router.callback_query()
async def callback(call: CallbackQueryHandler, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_data_dict[user_id]

    phone = int(user_data['Phone']) // 10**4
    balance = user_data['Balance']
    registration_date = user_data['Registration']
    volume = user_data['Funding_volume']

    days_count = (datetime.now() - datetime.strptime(registration_date, '%d.%m.%Y')).days
    if days_count % 10 == 1 and days_count % 100 != 11:
        days = 'день'
    elif days_count % 10 in [2, 3, 4] and not (11 <= days_count % 100 <= 19):
        days = 'дня'
    else:
        days = 'дней'

    current_page = await state.get_data()
    current_page = current_page.get('current_page', 0)
    trx_log = await sorted_payments(call)
    total_pages = math.ceil((len(trx_log)-1) / 15)
    first_page_line = current_page * 15
    last_page_line = first_page_line + 15
    page_text = '\n'.join(trx_log[first_page_line:last_page_line])

    if call.data == 'account':
        print(f'Пользователь {user_id} вошел в аккаунт')
        await call.message.edit_text(f'<strong>Мой аккаунт</strong>\n\n'
                                     f'⚙️ <strong>ID:</strong> <code>{call.from_user.id}</code>\n'
                                     f'🔒 <strong>Телефон:</strong> <code>{phone}****</code>\n'
                                     f'🗓 <strong>Регистрация:</strong> <code>{registration_date} ({days_count} {days})</code>\n\n'
                                     f'💵 <strong>Мой баланс: </strong><code>{balance}₽</code>\n'
                                     f'💎 <strong>Мой объем пополнений: </strong><code>{volume}₽</code>',
                                     parse_mode='HTML', reply_markup=account_keyboard)
    elif call.data == 'transactions':
        print(f'Пользователь {user_id} вошел в транзакции')
        if users_data_dict[user_id]['Balance'] == 0:
            await call.message.edit_text('<strong>💔 Вы еще не совершили ни одной транзакции.</strong>',
                                         parse_mode='HTML', reply_markup=zero_transactions_keyboard)
        else:
            current_page = 0
            await state.update_data(current_page=current_page)
            await log_buttons(call, page_text, current_page, total_pages)
    elif call.data == 'next_page':
        current_page += 1
        await state.update_data(current_page=current_page)
        first_page_line = current_page * 15
        last_page_line = first_page_line + 15
        page_text = '\n'.join(trx_log[first_page_line:last_page_line])
        await log_buttons(call, page_text, current_page, total_pages)
    elif call.data == 'prev_page':
        current_page -= 1
        await state.update_data(current_page=current_page)
        first_page_line = current_page * 15
        last_page_line = first_page_line + 15
        page_text = '\n'.join(trx_log[first_page_line:last_page_line])
        await log_buttons(call, page_text, current_page, total_pages)
    elif call.data == 'send':
        print(f'Пользователь {user_id} вошел в перевод баланса')
        await call.message.edit_text('🎁 В этом разделе ты можешь <strong>отправить деньги</strong> со своего '
                                     'баланса другу, на свой второй аккаунт или любому другому пользователю, '
                                     'который <strong>уже пользуется ботом!</strong>\n\n<i>Просто введите сумму для '
                                     'отправки ниже:</i>', parse_mode='HTML', reply_markup=send_keyboard)
        await state.set_state(SendToFriend.amount_input)

    elif call.data == 'choose_id':
        await call.message.edit_text('<strong>👤 Введите ID пользователя для перевода.</strong>\n\n<i>Вам нужно ввести '
                                 'ID пользователя в числовом формате ниже:</i>', parse_mode='HTML', reply_markup=step_back_keyboard)
        await state.set_state(SendToFriend.id_input)
    elif call.data == 'confirm_sending':
        await state.clear()
        pending_sending_message[user_id] = None
        await call.message.answer(f'<strong>Вы переводите: <code>{pending_sending_amount[user_id]}₽</code>\nПользователю '
                             f'под ID: <code>{pending_sending_id[user_id]}</code>\n\nПодтверждаете?</strong>',
                             parse_mode='HTML', reply_markup=confirm_sending_keyboard)
    elif call.data == 'sending_confirmed':
        await send_to_user(call, bot, state)
        await call.message.edit_text('<strong>🎁 Перевод успешно отправлен!</strong>\n\n<i>Получателю придет уведомление с '
                                     'суммой перевода, вашим ID и сообщением, которое вы отправили.</i>', parse_mode='HTML', reply_markup=send_keyboard)
    elif call.data == 'topup':
        print(f'Пользователь {user_id} вошел в пополнение')
        await call.message.edit_text('<strong>Выберите удобный способ пополнения баланса:</strong>',
                                     parse_mode='HTML', reply_markup=payment_keyboard)
    elif call.data == 'withdraw':
        print(f'Пользователь {user_id} вошел в вывод')
        await call.message.edit_text('<strong>В разработке...</strong>',
                                     parse_mode='HTML', reply_markup=withdraw_keyboard)
    elif call.data == 'back':
        await call.message.edit_text('<strong>Выберите нужное действие:</strong>',
                                     parse_mode='HTML', reply_markup=menu_keyboard)
    elif call.data == 'YK':
        print(f'Пользователь {user_id} вошел в пополнение yk')
        if user_id in pending_payments:
            del pending_payments[user_id]
            del pending_payments_info[user_id]
        await call.message.edit_text('<strong>Выберите сумму для оплаты или введите ее вручную:</strong>\n'
                                     '<i>Минимальная сумма для пополнения через ЮKassa — 60₽</i>\n\n'
                                     '<i>⚠️ Обратите внимание, что на данный момент оплата через ЮKassa'
                                     ' происходит в тестовом режиме, любые депозиты до подключения'
                                     ' платежной системы будут обнулены!</i>',
                                     parse_mode='HTML', reply_markup=yk_payment_keyboard)
        await state.set_state(CustomPaymentRubState.waiting_for_custom_amount)
    elif call.data == 'stars':
        print(f'Пользователь {user_id} вошел в пополнение stars')
        if user_id in pending_payments:
            del pending_payments[user_id]
            del pending_payments_info[user_id]
        await call.message.edit_text('<strong>Выберите сумму для оплаты или введите ее вручную:</strong>',
                                     parse_mode='HTML', reply_markup=stars_keyboard)
        await state.set_state(CustomPaymentStarsState.waiting_for_custom_amount)
    elif call.data == '100_in_stars':
        await payments.stars_63(call, bot)
    elif call.data == '200_in_stars':
        await payments.stars_125(call, bot)
    elif call.data == '400_in_stars':
        await payments.stars_250(call, bot)
    elif call.data == '500_in_stars':
        await payments.stars_313(call, bot)
    elif call.data == '100_in_rub':
        await payments.rub_100(call, bot)
    elif call.data == '200_in_rub':
        await payments.rub_200(call, bot)
    elif call.data == '400_in_rub':
        await payments.rub_400(call, bot)
    elif call.data == '500_in_rub':
        await payments.rub_500(call, bot)


async def sorted_payments(call: CallbackQueryHandler):
    user_id = call.from_user.id
    user_transactions_info = users_payments_dict[user_id]['Transactions']
    sorted_dates = sorted(user_transactions_info.keys(), reverse=True)
    trx_log = []

    line_count = 0
    for date in sorted_dates:
        trx_log.append(f'✧<strong>{date}</strong>')
        line_count += 1
        trx_by_time = sorted(user_transactions_info[date].keys(), reverse=True)

        for count, time in enumerate(trx_by_time):
            trx = user_transactions_info[date][time]
            rub_amount = trx['RUB']
            trx_id = trx['trx_id']
            trx_type = trx['type']

            time_input = datetime.strptime(time, '%H:%M:%S')
            time_output = time_input.strftime('%H:%M')

            if count < len(trx_by_time)-1:
                line_count += 1
                if (line_count - 1) % 15 == 0:
                    trx_log.append(f'✧<strong>{date}</strong>')
                    line_count += 1
                trx_log.append(f'├ <i>{time_output}</i> - <code>{rub_amount}₽</code> -'
                               f'<i>{trx_type}</i> - (<code>№{trx_id}</code>)')
            else:
                line_count += 1
                if (line_count - 1) % 15 == 0:
                    trx_log.append(f'✧<strong>{date}</strong>')
                    line_count += 1
                trx_log.append(f'└ <i>{time_output}</i> - <code>{rub_amount}₽</code> - '
                               f'<i>{trx_type}</i> - (<code>№{trx_id}</code>)')
                trx_log.append('')
                line_count += 1
    return trx_log


@router.message(SendToFriend.amount_input)
async def send_money(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_amount = message.text.replace(',', '.')
    user_data = users_data_dict[user_id]
    balance = user_data['Balance']
    try:
        amount = float(user_amount)
        amount = int(amount)
        await message.delete()
        if amount <= 0:
            await message.answer('<strong>⚠️ Сумма введена некорректно.</strong>\n<i>Нельзя отправить сумму '
                                 'меньше или равную нулю.</i>', parse_mode='HTML', reply_markup=try_again_amount_keyboard)
        elif int(balance) < amount:
            await message.answer('<strong>⚠️ У вас не хватает средств для перевода.</strong>\n<i>Уменьшите сумму '
                                 'или пополните баланс.</i>', parse_mode='HTML', reply_markup=try_again_amount_keyboard)
        else:
            pending_sending_amount[user_id] = amount
            await message.answer('<strong>👤 Введите ID пользователя для перевода.</strong>\n\n<i>Вам нужно ввести '
                                 'ID пользователя в числовом формате ниже:</i>', parse_mode='HTML',
                                 reply_markup=step_back_keyboard)
            await state.set_state(SendToFriend.id_input)

    except ValueError:
        await message.delete()
        await message.answer('<strong>⚠️ Сумма введена некорректно, попробуйте еще раз.</strong>',
                             parse_mode='HTML', reply_markup=try_again_amount_keyboard)


@router.message(SendToFriend.id_input)
async def send_money(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_input = message.text

    try:
        send_to = int(user_input)
        await message.delete()
        if send_to == user_id:
            await message.answer(
                '<strong>❌ Вы не можете совершить перевод самому себе, попробуйте еще раз.</strong>',
                parse_mode='HTML', reply_markup=try_again_id_keyboard)
        elif send_to not in users_data_dict:
            await message.answer(
                '<strong>⚠️ Пользователь не найден.</strong>\n\n<i>Пригласите пользователя или проверьте '
                'корректность ID.</i>', parse_mode='HTML', reply_markup=try_again_id_keyboard)
        elif not users_data_dict[send_to]['Is_verified']:
            await message.answer('<strong>⚠️ Пользователь не авторизован.</strong>\n\n<i>Вы можете самостоятельно попросить '
                'пользователя пройти авторизацию.</i>', parse_mode='HTML', reply_markup=try_again_id_keyboard)
        else:
            pending_sending_id[user_id] = send_to
            await state.set_state(SendToFriend.message_input)
            await message.answer(f'📩 <strong>Вы можете ввести сообщение для пользователя.'
                                 f'</strong>\n<i>Обратите внимаение, что любые премиум-эмодзи, к сожалению, будут '
                                 f'преобразованы в обычные.</i>\n\n<i>Введите ваше текстовое сообщение ниже:</i>',
                                 parse_mode='HTML', reply_markup=skip_message_keyboard)
    except ValueError:
        await message.delete()
        await message.answer('<strong>⚠️ ID введен некорректно, попробуйте еще раз.</strong>',
                             parse_mode='HTML', reply_markup=try_again_id_keyboard)


@router.message(SendToFriend.message_input)
async def send_money(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_input = message.text
    try:
        send_message = str(user_input)
        pending_sending_message[user_id] = send_message
        await message.delete()
        await message.answer(f'<strong>Вы переводите: <code>{pending_sending_amount[user_id]}₽</code>\nПользователю '
                             f'под ID: <code>{pending_sending_id[user_id]}</code>\nВаше сообщение:</strong> '
                             f'{pending_sending_message[user_id]}\n\n<strong>Подтверждаете?</strong>',
                             parse_mode='HTML', reply_markup=confirm_sending_keyboard)
    except:
        await message.answer('<strong>❌ Некорректное сообщение, попробуйте еще раз!</strong>', parse_mode='HTML',
                             reply_markup=try_again_id_keyboard)
    await state.clear()


@router.message(CustomPaymentRubState.waiting_for_custom_amount)
async def process_custom_rub_amount(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    user_input = message.text.replace(',', '.')
    try:
        amount = float(user_input)
        amount = int(amount)
        if amount >= 60:
            pending_payments[user_id] = amount
            pending_payments_info[user_id] = 'Пополнение баланса — ЮKassa'
            await message.delete()
            await rub_custom(message, bot, state)
        else:
            await message.delete()
            await message.answer('<strong>Выберите удобный способ пополнения баланса:</strong>',
                                 parse_mode='HTML', reply_markup=payment_keyboard)
    except ValueError:
        await message.delete()
        await message.answer('<strong>Выберите удобный способ пополнения баланса:</strong>',
                                     parse_mode='HTML', reply_markup=payment_keyboard)
    await state.clear()


@router.message(CustomPaymentStarsState.waiting_for_custom_amount)
async def process_custom_stars_amount(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    user_input = message.text.replace(',', '.')
    try:
        amount = float(user_input)
        amount = int(amount)
        if amount > 0:
            pending_payments[user_id] = amount
            pending_payments_info[user_id] = 'Пополнение баланса — Stars'
            await message.delete()
            await stars_custom(message, bot, state)
        else:
            await message.delete()
            await message.answer('<strong>Выберите удобный способ пополнения баланса:</strong>',
                                 parse_mode='HTML', reply_markup=payment_keyboard)
    except ValueError:
        await message.delete()
        await message.answer('<strong>Выберите удобный способ пополнения баланса:</strong>',
                                     parse_mode='HTML', reply_markup=payment_keyboard)
    await state.clear()


@router.message()
async def any_message(message: Message, state: FSMContext):
    await command_menu(message)
    await state.clear()


@router.message()
async def confirm_phone(message: Message):
    user_id = message.from_user.id
    user_data = users_data_dict[user_id]

    if not user_data['Is_verified']:
        button_phone = [
            [KeyboardButton(text="✅ Подтвердить номер телефона", request_contact=True)]
            ]
        markup = ReplyKeyboardMarkup(keyboard=button_phone, resize_keyboard=True)
        await message.answer('☎️ <b>Номер телефона не подтвержден</b>\n\n'
                             'Вам необходимо подтвердить <b>номер телефона</b>'
                             ' для того, чтобы начать пользоваться ботом.\n\n'
                             'Для подтверждения нажмите кнопку ниже.',
                             parse_mode='HTML', reply_markup=markup)
    else:
        return

