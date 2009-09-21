Core functionality consists of :

Customer

1. login and purchase design package
2. create order from customer home
2.5 enter minimum necessary order info
3. login and upload diagram for incomplete order
4. submit order from customer home
5. completed order generates email notification
6. login and review completed order 

Designer
 
7. designer registration 
8. submitted order generates email status notification for designer
9. designer logs in an retrieves design order
10. designer logs in and uploads completed order


Customer - 1

0. setup database with demo/demo user, demoaccount account and demoprofile[demo, demoaccount]

1. login using demo/demo, validate customer home displayed

2. create order from home, validate order-detail page displayed
	- account information is displayed
	- order status / payment information is displayed
	- section status is displayed
	-- 
	- displayed order status : new
	- displayed order payment is 'none'
	- displayed order sections are all 'incomplete'
		[ design, cabinetry, hardware, moulding, cabinet box, corner cabinet, 
		  island, other, organization ('space management'), miscellaneous, 
		  appliances, diagrams 
		]
		
2.5. enter minimum necessary order info
	- enter design info
		- job name 'jones kitchen'
	- enter cabinetry info
	- skip hardware info
	- skip moulding info
	- enter box info
	- enter 3 appliances
		- dishwasher, refrigerator, microwave
	- download floorplan template
	- save
	- logout

3. login and upload diagram for incomplete order
	- from marketing page login as demo
	- open order associated with 'jones kitchen'
	- upload 2 pages
	- logout
	- confirm customer email notification
	
4. submit order from customer home.