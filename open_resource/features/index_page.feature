# -- FILE: features/index_page.feature

Feature: Show the Index page
  As a visitor
  I want to visit the index page
  So that I can see the list of ID_tables entries

  Scenario: Visiting the index page
    Given I am on the index page
    Then I should see the title "Index Page"
