# -- FILE: features/environment.py
def before_all(context):
  context.client = app.test_client()
