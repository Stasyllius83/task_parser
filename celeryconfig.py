broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

beat_schedule = {
  'run-fill-db-every-hour': {
    'task': 'classes.fill_db',
    'schedule': 120, # каждый час (в секундах)
  },
}
