--
-- CREATE TABLE "product_product" (
--     "id" integer NOT NULL PRIMARY KEY,
--     "name" varchar(20) NOT NULL,
--     "verbose_name" varchar(120) NOT NULL,
--     "description" text NOT NULL,
--     "sort_order" integer NOT NULL,
--     "base_price" decimal NOT NULL,
--     "credit_value" smallint NOT NULL,
--     "purchaseable" bool NOT NULL,
--     "debitable" bool NOT NULL
-- )

--
-- BASE PRODUCTS
--
insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 1, 'Base', 'Base 20/20 Design File', 'A complete 20/20 .kit file with completed design. For professional designers only.', 
           100, 85, 85, 1, 1 );

insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 2, 'Full', 'Full PDF Design Layout', 'A package containing PDF floorplans, elevations, and color persepective views. Optionally includes 20/20 .kit file.', 
           120, 120, 120, 1, 1 );

insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 3, 'Base Plus', 'Base 20/20 Design plus one free revision', 'A complete 20/20 .kit file with completed design. Includes one revision and the ability to purchase additional revisions. For professional designers.', 
           140, 140, 140, 1, 1 );

insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 4, 'Full', 'Full PDF Design Layout', 'A package containing PDF floorplans, elevations, and color persepective views. Includes one revision and the ability to purchase additional revisions. Optionally includes 20/20 .kit file.', 
           160, 140, 140, 1, 1 );

--
-- REVISIONS
--
insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 5, 'Base Rev', 'A 20/20 only revision', 'A new 20/20 design produced by incorporating feedback on a previous, revisable design. Optionally includes 20/20 .kit file.', 
           200, 30, 30, 1, 1 );

insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 6, 'Full Rev', 'Revision of a Full PDF Design Layout package.', 'A revsison package containing PDF floorplans, elevations, and color persepective views. Includes one revision and the ability to purchase additional revisions. Optionally includes 20/20 .kit file.', 
           220, 40, 40, 1, 1 );
           
-- 
-- PACKAGES
--
insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 7, 'Base 5-Pack', '5 Base Designs', 'A package containing PDF floorplans, elevations, and color persepective views. Includes one revision and the ability to purchase additional revisions. Optionally includes 20/20 .kit file.', 
           400, 500, 600, 1, 0 );
       
insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 8, 'Full 5-Pack', '5 Full Designs', 'A package containing PDF floorplans, elevations, and color persepective views. Includes one revision and the ability to purchase additional revisions. Optionally includes 20/20 .kit file.', 
           420, 600, 700, 1, 0 );
       
insert into product_product ( id, name, verbose_name, description, sort_order, base_price, credit_value, purchaseable, debitable )
       values ( 9, 'Full Plus 5-Pack', '5 Full Designs w/5 revisions', 'A package containing PDF floorplans, elevations, and color persepective views. Includes one revision and the ability to purchase additional revisions. Optionally includes 20/20 .kit file.', 
           440, 700, 800, 1, 0 );
       
