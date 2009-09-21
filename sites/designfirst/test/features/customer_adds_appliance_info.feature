Feature: add appliance info 
	
	As a customer
	I need to be able to specify my appliance information
	So that the designers understand the constraints of the design
	  and I can indicate things that are not easy to indicate legibly
	  in the floorplan drawing
	
	Scenario: add appliance info 
		Given I am on the order details page 
		When I select 'add appliance'
		Then the appliance edit page is displayed
