# -- FILE: features/environment.py

from open_resource.open_resource import app

def before_all(context):
  context.client = app.test_client()
