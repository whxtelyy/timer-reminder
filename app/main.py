import asyncio
from aioconsole import ainput

def counting_time(time: float) -> float:
    return time * 60

async def async_input(promt: str) -> str:
    return await ainput(promt)

async def single_reminder(text: str, delay_seconds: float):
    await asyncio.sleep(delay_seconds)
    print(f'\n Напоминание {text}. (Прошло {delay_seconds/60:.1f} минут)')

async def display_time():
    tasks = []

    while True:
        try:
            text = await ainput("О чём вам напомнить? (Или 'exit' для выхода): ")
            if text.lower() == 'exit':
                print('Спасибо за использование таймера. Будем ждать вас еще!')
                break

            local_time = float(await ainput("Через сколько минут? "))
            if local_time <= 0:
                print('Ошибка: Время должно быть положительным')
                continue

            tasks.append(asyncio.create_task(single_reminder(text, counting_time(local_time))))

            count_reminders = await ainput('Хотите добавить еще напоминаний? (y,yes/n,no): ')
            if count_reminders == 'no' or count_reminders == 'n':
                print('Хорошо. Мы напомним вам о ваших задачах, ожидайте...')
                break

        except ValueError:
            print('Ошибка: Введите корректное число')
            continue

    if tasks:
        await asyncio.gather(*tasks)
    return 'Все напоминания установлены!'

if __name__ == '__main__':
    asyncio.run(display_time())