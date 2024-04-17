import asyncio
from source.classes import Task_base
from source.services import send_telegram, telegram_bot



async def main():
    #queue = asyncio.Queue(100)

    tsk = Task_base()

    task1 = asyncio.create_task(tsk.fill_db())
    task2 = asyncio.create_task(telegram_bot())
    task3 = asyncio.create_task(tsk.task_req())
    task4 = asyncio.create_task(send_telegram(task3))

    await task1.delay()
    await task2
    await task3
    await task4

    print(task2)



if __name__ == '__main__':

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())
