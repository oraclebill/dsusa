--
-- CREATE TABLE "product_product" (
--     "id" integer NOT NULL PRIMARY KEY,
--     "name" varchar(20) NOT NULL,
--     "description" text NOT NULL,
--     "sort_order" integer NOT NULL,
--     "base_price" decimal NOT NULL,
--     "credit_value" smallint NOT NULL,
--     "purchaseable" bool NOT NULL,
--     "debitable" bool NOT NULL
--     "is_revision" bool NOT NULL default 0,
-- )

--
-- BASE PRODUCTS
--
insert into product_product ( id, name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 1, 'Pro Design', 'A professional design in 20/20 KIT file form, with Cabinet Price Report detailing retail cost of all cabinetry.', 
           100, 85, 85, 1, 1 );

insert into product_product ( id, name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 2, 'Presentation Pack', 'A presentation ready package containing PDF floorplans, elevations, and color persepective views in addition to 20/20 KIT file and Cabinet Price Report.', 
           120, 125, 125, 1, 1 );

insert into product_product ( id, name, description, sort_order, base_price, credit_value, purchaseable, debitable, is_revision )
       values ( 4, 'Presentation Pack Revision', 'A Presentation Pack Revision gives you the ability to purchase a revision to a previous design for a discounted price. Presentation Pack revisions can not be purchsed individually - they must be purchased with a Presentation Pack.', 
           140, 80, 80, 1, 1, 1 );           
-- 
-- PACKAGES
--
insert into product_product ( id, name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 7, 'Pro Design 6-4-5', 'Six Pro Designs for the price of five.', 1000, 425, 510, 1, 0 );
       
insert into product_product ( id, name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 8, 'Presentation Pack 6-4-5 Special', 'Six Presentation Pack Design Packages for the price of five.', 1010, 625, 750, 1, 0 );
       
insert into product_product ( id, name, description, sort_order, base_price, credit_value, purchaseable, debitable, is_revision )
       values ( 9, 'Presentation Pack Revision 6-4-5 Special', 'Six Presentation Pack Design Revisions for the price of five', 1020, 400, 480, 1, 0, 1 );
       
