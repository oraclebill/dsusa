Feature: add floorplan info 
	
	As a customer
	I need to be able to specify my floorplan dimensions
	So that the the designers can design a kitchen that fits
	
	Scenario: add floorplan info 
		Given I am on the order details page 
		When I select 'add floorplan'
		Then a floorplan template is generated and made available for download
		And a fax number and measuring instructions are displayed 
