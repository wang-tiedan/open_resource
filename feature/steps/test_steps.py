# -- FILE: features/steps/test_steps.py

from behave import given, when, then, step

from open_resource.open_resource import app

def before_all(context):
  context.client = app.test_client()
  context.response = None

@given('I am on the index page')
def step_impl(context):
  context.response = context.client.get('/')

@then('I should see the title "{title}"')
def step_impl(context, title):
  assert title in context.response.data.decode('utf-8')
