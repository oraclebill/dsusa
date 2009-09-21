Feature: create order 
	
	As a dealer-customer
	I need to be able to create new orders
	So that I can describe my requirements and request services
	
	Scenario: create order 
		Given I am on the customer home page 
		When I select the 'create order' button
		Then a new order number is generated
		And the order details page is displayed for the new order
