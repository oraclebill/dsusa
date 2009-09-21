Feature: customer home page 
	
	As a dealer-customer
	I want to be able to easily review my transactions
	So that I can understand the status of my orders
	
	Scenario: customer home page 
		Given I am on the customer-home page 
		Then I should see an order status list
		And I should see a diagram archive
		And I should see a recent purchase list
		And I should see my account credit balance
		And I should see my subscription status
		And I should see my name and join date
