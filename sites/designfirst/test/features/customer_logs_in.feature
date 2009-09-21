Feature: customer logs in
	
	As a dealer-customer
	I want to login
	So that I can access my account
	
	Scenario: log in 
		Given I am not logged in 
		And I am on the public website
		When I log in
		Then my customer dashboard is displayed
		