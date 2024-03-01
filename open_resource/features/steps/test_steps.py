# -- FILE: features/steps/test_steps.py

from behave import given, when, then, step
# Import Flask app
from open_resource.open_resource_service import app
# Give a test client
def before_all(context):
  context.client = app.test_client()
  context.response = None

@given('I am on the index page')
def step_impl(context):
  context.response = context.client.get('/')

@then('I should see the title "{title}"')
def step_impl(context, title):
  assert title in context.response.data.decode('utf-8')
