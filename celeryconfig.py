broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

beat_schedule = {
  'run-periodic-task-every-hour': {
    'task': 'main.periodic_task',
    'schedule': 120, # каждый час (в секундах)
  },
}
