import json, random, string


try:
    with open('users_data.txt', 'r', encoding='utf-8') as file:
        users_data = json.load(file)
except Exception as e:
    print(f"Ошибка при загрузке данных: {e}")
    users_data = []

try:
    with open('users_payments.txt', 'r', encoding='utf-8') as up:
        users_payments = json.load(up)
except Exception as e:
    print(f"Ошибка при загрузке данных: {e}")
    users_payments = []

try:
    with open('total_values.txt', 'r', encoding='utf-8') as total:
        total_data = json.load(total)
        total_values = total_data[0]
except Exception as e:
    print(f"Ошибка при загрузке данных: {e}")
    total_values = {}

users_data_dict = {person['ID']: person for person in users_data}
users_payments_dict = {person['ID']: person for person in users_payments}


async def save_data():
    try:
        with open('users_data.txt', 'w', encoding='utf-8') as file:
            json.dump(users_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

async def save_payments():
    try:
        with open('users_payments.txt', 'w', encoding='utf-8') as up:
            json.dump(users_payments, up, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

async def save_total():
    try:
        with open('total_values.txt', 'w', encoding='utf-8') as total:
            json.dump([total_values], total, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")


async def id_generator():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=9))
