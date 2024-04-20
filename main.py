import asyncio
#from source.services import send_telegram
#from source.services import bot
from source.classes import Io_telebot, Task_base
from celery import Celery
from celery.schedules import crontab
app = Celery('main')
app.config_from_object('celeryconfig')


tsk = Task_base()
telebot = Io_telebot()

@app.task
def periodic_task():
    tsk.fill_db()

# async def run_periodically():
#     while True:
#         tsk.fill_db()
#         await asyncio.sleep(90)
#def main():
    # task1 = asyncio.create_task(tsk.fill_db())
    #task2 = asyncio.create_task(telebot())
    #task3 = asyncio.create_task(tsk.task_req())
    #task4 = asyncio.create_task(send_telegram())
    #await task1
    #await task2
    #await task3
    #await task4
if __name__ == '__main__':
    # event_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(event_loop)
    # event_loop.run_until_complete(main())
    periodic_task.delay()
    telebot()
