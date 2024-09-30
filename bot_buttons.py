from aiogram.handlers import CallbackQueryHandler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


menu_buttons = [
    [InlineKeyboardButton(text='👨‍💻 Мой аккаунт', callback_data='account'),
     InlineKeyboardButton(text='💳 Пополнить', callback_data='topup')],
    [InlineKeyboardButton(text='💸 Перевести на криптокошелек', callback_data='withdraw')]
        ]
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)

account_buttons = [
    [InlineKeyboardButton(text='📝 Мои операции', callback_data='transactions'),
    InlineKeyboardButton(text='🙋‍♂️ Перевод другу', callback_data='send')],
    [InlineKeyboardButton(text='← Назад', callback_data='back')]
]
account_keyboard = InlineKeyboardMarkup(inline_keyboard=account_buttons)


send_buttons = [
    [InlineKeyboardButton(text='← Назад', callback_data='account')]
]
send_keyboard = InlineKeyboardMarkup(inline_keyboard=send_buttons)

try_again_amount_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🙋‍♂️ Перевод другу', callback_data='send')]]
    )
try_again_id_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🥷 Ввести ID', callback_data='choose_id')]]
    )
step_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='← Изменить сумму', callback_data='send')]]
)
confirm_sending_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='❌ Нет', callback_data='send'),
                      InlineKeyboardButton(text='✅ Да', callback_data='sending_confirmed')]]
)
skip_message_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Пропустить →', callback_data='confirm_sending')]]
)


zero_transactions_buttons = [
    [InlineKeyboardButton(text='🤑 Перейти к пополнению', callback_data='topup')],
    [InlineKeyboardButton(text='← Назад', callback_data='account')]
]
zero_transactions_keyboard = InlineKeyboardMarkup(inline_keyboard=zero_transactions_buttons)


payment_buttons = [
    [InlineKeyboardButton(text='🟣 ЮKassa', callback_data='YK')],
    [InlineKeyboardButton(text='⭐️ Telegram Stars', callback_data='stars')],
    [InlineKeyboardButton(text='← Назад', callback_data='back')]
        ]
payment_keyboard = InlineKeyboardMarkup(inline_keyboard=payment_buttons)


withdraw_buttons = [
    [InlineKeyboardButton(text='← Назад', callback_data='back')]
]
withdraw_keyboard = InlineKeyboardMarkup(inline_keyboard=withdraw_buttons)


stars_buttons = [
        [InlineKeyboardButton(text='100₽ (63 ⭐️)', callback_data='100_in_stars'),
         InlineKeyboardButton(text='200₽ (125 ⭐️)', callback_data='200_in_stars')],
        [InlineKeyboardButton(text='400₽ (250 ⭐️)', callback_data='400_in_stars'),
         InlineKeyboardButton(text='500₽ (313 ⭐️)', callback_data='500_in_stars')],
        [InlineKeyboardButton(text='← Назад', callback_data='topup')]
    ]
stars_keyboard = InlineKeyboardMarkup(inline_keyboard=stars_buttons)


yk_payment_buttons = [
        [InlineKeyboardButton(text='100₽ 💵', callback_data='100_in_rub'),
         InlineKeyboardButton(text='200₽ 💵', callback_data='200_in_rub')],
        [InlineKeyboardButton(text='400₽ 💵', callback_data='400_in_rub'),
         InlineKeyboardButton(text='500₽ 💵', callback_data='500_in_rub')],
        [InlineKeyboardButton(text='← Назад', callback_data='topup')]
    ]
yk_payment_keyboard = InlineKeyboardMarkup(inline_keyboard=yk_payment_buttons)


async def log_buttons(call: CallbackQueryHandler, page_text, current_page: int, total_pages: int):
    trx_log_buttons = [[InlineKeyboardButton(text='← Назад', callback_data='account')]]
    if current_page == 0 and total_pages > 1:
        trx_log_buttons = [
            [InlineKeyboardButton(text=' ', callback_data='None'),
            InlineKeyboardButton(text='>', callback_data='next_page')],
            [InlineKeyboardButton(text='← Назад', callback_data='account')]
        ]
    elif 0 < current_page < total_pages - 1:
        trx_log_buttons = [
            [InlineKeyboardButton(text='<', callback_data='prev_page'),
             InlineKeyboardButton(text='>', callback_data='next_page')],
            [InlineKeyboardButton(text='← Назад', callback_data='account')]
        ]
    elif total_pages == 1:
        trx_log_buttons = [
            [InlineKeyboardButton(text='← Назад', callback_data='account')]
        ]
    elif current_page == total_pages - 1:
        trx_log_buttons = [
            [InlineKeyboardButton(text='<', callback_data='prev_page'),
            InlineKeyboardButton(text=' ', callback_data='None')],
            [InlineKeyboardButton(text='← Назад', callback_data='account')]
        ]

    trx_log_keyboard = InlineKeyboardMarkup(inline_keyboard=trx_log_buttons)
    await call.message.edit_text(text=page_text, parse_mode='HTML', reply_markup=trx_log_keyboard)