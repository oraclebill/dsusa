Feature: add appliance info 
	
	As a customer
	I need to be able to pay for my designs
	So that the company can make money
	
	Scenario: add payment info 
		Given I am on the order details page 
		When I select 'payment'
		Then I am redirected to google checkout to complete the order.
