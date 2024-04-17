import asyncio
import os
from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Numeric, UniqueConstraint
from source.services import task_parser
Base = declarative_base()
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
DATABASE = os.getenv('DB_CONNECT')
from celery import Celery
app = Celery('classes')



class Task(Base):
    """

    """
    __tablename__ = 'task'
    # __table_args__ = (UniqueConstraint('name_number'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column('topic', String)
    quantity_solved = Column('quantity_solved', Numeric)
    name_number = Column('name_number', String)
    difficulty = Column('difficulty', Numeric)
    UniqueConstraint('name_number', name='idx_name_number')

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Task_base:
    """

    """

    def __init__(self) -> None:
        """

        """
        self.engine = create_engine(DATABASE)
        self.session = self.create_session(self.engine)
        self.create_table('task_parser')

    def create_table(self, table_name):
        """

        """
        if not self.engine.dialect.has_table(self.engine.connect(), table_name):
            Base.metadata.create_all(self.engine)

    @staticmethod
    def create_session(engine):
        """

        """
        Session = sessionmaker(bind=engine)
        return Session()

    async def fill_db(self):
        """

        """
        try:
            all_tasks = await task_parser()

            for task in all_tasks:

                session = self.create_session(self.engine)

                task = Task(
                    topic=task[1],
                    quantity_solved=task[3],
                    name_number=task[0],
                    difficulty=task[2],
                )

                session.add(task)
                session.commit()
            session.close()

        except Exception as e:
            print(f"Произошла ошибка {e}")
            await asyncio.sleep(10)

    @app.task
    async def task_req(self):
        """

        """
        session = self.create_session(self.engine)

        tasks_req = session.query(Task).filter(Task.topic == 'math', Task.difficulty == '800',).order_by(Task.id.desc()).limit(10).all()

        all_task_list = []
        for obj in tasks_req:
            task_list = []
            task_list.append(obj.topic)
            task_list.append(int(obj.quantity_solved))
            task_list.append(obj.name_number)
            task_list.append(int(obj.difficulty))
            all_task_list.append(task_list)
        return all_task_list
