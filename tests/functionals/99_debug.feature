Feature: As a developper, I want a browser open with a session

  @dev
  Scenario: start an initialized session and wait
    Given anonymous user on the index page
    When I fill the field "Farm some gems" with "Take a bowl"
    And I click on the "Add" button
    And I fill the field "Farm some gems" with "Add 3 ripe bananas"
    And I click on the "Add" button
    And I fill the field "Farm some gems" with "Add 2 cups of fun flour"
    And I click on the "Add" button
    And I fill the field "Farm some gems" with "Add 1 cup of magic"
    And I click on the "Add" button
    And I fill the field "Farm some gems" with "Add 1 teaspoon of giggles"
    And I click on the "Add" button
    And I fill the field "Farm some gems" with "Add A pinch of happiness"
    And I click on the "Add" button
    And I fill the field "Farm some gems" with "Have fun"
    And I click on the "Add" button
    Then I wait
