import asyncio
from aioconsole import ainput
import datetime

def parse_absolute_time(local_time: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.strptime(local_time, '%d-%m-%Y %H:%M')
    except ValueError:
        print("Некорректный формат времени. Используйте формат ДД-ММ-ГГГГ ЧЧ:ММ (например, 26-04-2025 14:30)")
        return None

async def single_reminder(text: str, delay_seconds: float):
    await asyncio.sleep(delay_seconds)
    print(f'\n Напоминание {text}!')

async def display_time():
    tasks = []

    while True:
        text = await ainput("\nО чём вам напомнить? (Или 'exit' для выхода): ")
        if text.lower() == 'exit':
            print('\nСпасибо за использование таймера. Будем ждать вас еще!')
            break

        while True:
            local_time = await ainput("Введите время (ДД-ММ-ГГГГ ЧЧ:ММ): ")
            reminder_time = parse_absolute_time(local_time)
            if not reminder_time:
                continue

            now = datetime.datetime.now()
            if reminder_time <= now:
                print('Ошибка: Указанное время уже прошло')
                continue

            delay_seconds = (reminder_time - now).total_seconds()
            tasks.append(asyncio.create_task(single_reminder(text, delay_seconds)))
            print(f"Напоминание '{text}' установлено на {reminder_time.strftime('%d-%m-%Y %H:%M')}")
            break

        while True:
            count_reminders = await ainput('\nХотите добавить еще напоминаний? (y/n): ')
            if count_reminders.lower() == 'no' or count_reminders.lower() == 'n':
                print('Хорошо. Мы напомним вам о ваших задачах, ожидайте...')
                break
            elif count_reminders.lower() == 'y' or count_reminders.lower() == 'yes':
                break
            else:
                print("Пожалуйста, введите 'y' или 'n'")

    if tasks:
        await asyncio.gather(*tasks)
    return 'Все напоминания установлены!'

if __name__ == '__main__':
    asyncio.run(display_time())