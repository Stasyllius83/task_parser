from source.classes import Io_telebot, Task_base
from celery import Celery
app = Celery('main')
app.config_from_object('celeryconfig')


tsk = Task_base()
telebot = Io_telebot()

@app.task
def periodic_task():
    tsk.fill_db()


if __name__ == '__main__':

    periodic_task.delay()
    telebot()
