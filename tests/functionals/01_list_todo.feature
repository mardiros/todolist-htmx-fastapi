Feature: As a user, I can view my todo list

  Scenario: View the todolist
    Given anonymous user on the index page
    Then I see the heading "My TODO List"
