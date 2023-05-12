Feature: As a user, I can view my todo list

  Scenario: View the todolist
    Given anonymous user on the index page
    Then I see the heading "My TODO List"
    And I see the text "Congrats, you have nothing to do"
    And I see the input "Farm some gems"

  Scenario: Add item the todolist
    Given anonymous user on the index page
    When I fill the field "Farm some gems" with "Write some code"
    And I click on the "Add" button
    Then I see the text "Write some code"
    When I fill the field "Farm some gems" with "Package that code"
    And I click on the "Add" button
    Then I see the text "Write some code"
    Then I see the text "Package that code"
