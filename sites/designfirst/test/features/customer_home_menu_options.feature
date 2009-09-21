Feature: customer home menu options
	
	As a dealer-customer
	I want to be able to easily access all of my available features
	So that I can use the system productively
	
	Scenario: dealer-customer menu options 
		Given I am a dealer-customer 
		And I am logged-in 
		Then I should see the following menu options: x, y, z
