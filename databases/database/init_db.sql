SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

DROP DATABASE IF EXISTS `database`;
CREATE DATABASE `database`;
USE `database`;

CREATE TABLE IF NOT EXISTS `employee` (
       `IRSNumber` int(10) NOT NULL,
       `FirstName` varchar(25) NOT NULL,
       `LastName` varchar(25) NOT NULL,
       `SocialSecurityNo` int(11) NOT NULL,
       `DriverLicense` int(10) NOT NULL,
       `City` varchar(25) NOT NULL,
       `Street` varchar(25) NOT NULL,
       `StreetNo` int(3) NOT NULL,
       `PostalCode` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `store` (
       `StoreID` int(10) NOT NULL,
       `City` varchar(25) NOT NULL,
       `Street` varchar(25) NOT NULL,
       `StreetNo` int(3) NOT NULL,
       `PostalCode` int(5) NOT NULL,
       `PhoneNumber` int(10) NOT NULL,
       `Email` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `vehicle` (
       `LicensePlate` varchar(8) NOT NULL,
       `StoreID` int(10) NOT NULL,
       `CarType` varchar(15) NOT NULL,
       `Model` varchar(15) NOT NULL,
       `Make` varchar(15) NOT NULL,
       `CC` int(5) NOT NULL,
       `HorsePower` int(5) NOT NULL,
       `CarYear` int(4) NOT NULL,
       `Km` int(6) NOT NULL,
       `LastService` date NOT NULL,
       `NextService` date NOT NULL,
       `InsuranceExpdate` date NOT NULL,
       `Damages` varchar(25) NOT NULL,
       `Malfunction` varchar(25) NOT NULL,
       `FuelType` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `customer` (
       `CustomerID` int(10) NOT NULL,
       `IRSNumber` int(10) NOT NULL,
       `FirstName` varchar(25) NOT NULL,
       `LastName` varchar(25) NOT NULL,
       `SocialSecurityNo` varchar(11) NOT NULL,
       `DriverLicense` int(10) NOT NULL,
       `FirstRegistration` date NOT NULL,
       `City` varchar(25) NOT NULL,
       `Street` varchar(25) NOT NULL,
       `StreetNo` int(3) NOT NULL,
       `PostalCode` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `works` (
       `IRSNumber` int(10) NOT NULL,
       `StoreID` int(10) NOT NULL,
       `StartDate` date NOT NULL,
       `FinishDate` date NOT NULL,
       `WorkerPosition` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `reserves` (
       `LicensePlate` varchar(8) NOT NULL,
       `StartDate` date NOT NULL,
       `FinishDate` date NOT NULL,
       `StartLocation` varchar(15) NOT NULL,
       `FinishLocation` varchar(15) NOT NULL,
       `Paid` varchar(3) NOT NULL,
       `CustomerID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `rents` (
       `LicensePlate` varchar(8) NOT NULL,
       `StartDate` date NOT NULL,
       `FinishDate` date NOT NULL,
       `StartLocation` varchar(25) NOT NULL,
       `FinishLocation` varchar(25) NOT NULL,
       `CustomerID` int(10) NOT NULL,
       `ReturnState` varchar(15) NOT NULL,
       `IRSNumber` int(10) NOT NULL,
       `PaymentAmount` int(5) NOT NULL,
       `PaymentMethod` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*** evretiria ***/

ALTER TABLE `employee`
  ADD PRIMARY KEY (`IRSNumber`);

ALTER TABLE `store`
    ADD PRIMARY KEY (`StoreID`);

ALTER TABLE `customer`
    ADD PRIMARY KEY (`CustomerID`);
      
ALTER TABLE `vehicle`
      ADD PRIMARY KEY (`LicensePlate`),
      ADD KEY `fk_Vehicle_store_idx` (`StoreID`);
      
ALTER TABLE `works`
      ADD PRIMARY KEY (`IRSNumber`,`StoreId`,`StartDate`),
      ADD KEY `fk_Works_store_idx` (`StoreID`),
       ADD KEY `fk_Works_irs_number` (`IRSNumber`);
   
ALTER TABLE `reserves`
     ADD PRIMARY KEY (`LicensePlate`,`StartDate`),
     ADD KEY `fk_Reserves_customer_idx` (`CustomerID`),
     ADD KEY `fk_Reserves_license_plate` (`LicensePlate`);

ALTER TABLE `rents`
      ADD PRIMARY KEY (`LicensePlate`,`StartDate`),
      ADD KEY `fk_Rents_irs` (`IRSNumber`),
      ADD KEY `fk_Rents_customer_idx` (`CustomerID`),
      ADD KEY `fk_Rents_license_plate` (`LicensePlate`);

/* * * * * * AUTO INCREMENTS * * * * * */

ALTER TABLE `customer`
MODIFY `CustomerID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

ALTER TABLE `store`
MODIFY `StoreID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;


/*** periorismoi - eksartiseis ***/

ALTER TABLE `vehicle`
      ADD CONSTRAINT  `fk_Vehicle_store_idx` FOREIGN KEY (`StoreID`) REFERENCES `store`(`StoreID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE `works`
  ADD CONSTRAINT `fk_Works_irs` FOREIGN KEY (`IRSNumber`) REFERENCES `employee` (`IRSNumber`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Works_store` FOREIGN KEY (`StoreID`) REFERENCES `store` (`StoreID`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;
      
ALTER TABLE `reserves`
      ADD CONSTRAINT `fk_Reserves_customer_idx` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
      ADD CONSTRAINT `fk_Reserves_license_plate` FOREIGN KEY (`LicensePlate`) REFERENCES `vehicle` (`LicensePlate`) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE `rents`
       ADD CONSTRAINT `fk_Rents_customer_idx` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
      ADD CONSTRAINT `fk_Rents_irs` FOREIGN KEY (`IRSNumber`) REFERENCES `employee` (`IRSNumber`) ON DELETE NO ACTION ON UPDATE NO ACTION,
      ADD CONSTRAINT `fk_Rents_license_plate` FOREIGN KEY (`LicensePlate`) REFERENCES `vehicle` (`LicensePlate`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/* * * * * * VIEWS * * * * * */
 
/* * * * * * view1 * * * * * * 
/* ClientsPerEmployee - 
/* Apeikonizei to plithos ton aftokiniton 
/* ta opoia exei kanei rent o kahe customer
/* stoixeio aparaitito gia tin anagnorisi
/* ton agapimenon mas pelaton <3
/* einai mi enimerosimi efoson
/* xrisimopoieitai i sunathroistiki sunartisi count
**/

DROP TABLE IF EXISTS `CustomersRents`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY
DEFINER VIEW `CustomersRents` as
  select `CustomerID` as `ID`,
  count(`CustomerID`) as `Total`
  from `rents`
  group by `CustomerID`;

/* * * * * * view2 * * * * * * 
/* EmployeeInfo - 
/* O pinakas customer periexei polla stoixeia
/* arketa apo ta opoia den einai xrisima se kathimerini vasi
/* opote dimiourgoume mia provoli me ta simantikotera ex afton
/* einai enimerosimi efoson
/* de xrisimopoieitai kamia sunathroistiki sunartisi
**/

DROP TABLE IF EXISTS `Fleet`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY
DEFINER VIEW `Fleet` AS
  select  `LicensePlate` AS `Plate`,
      `CarType` AS `CarType`,
      `Make`,
      `Model`,
      `CarYear` AS `CarYear`,
      `FuelType` AS `Fuel`
      from `vehicle`;


/* * * * * * * INSERTS * * * * * * */
INSERT INTO `store` (`City`, `Street`, `StreetNo`, `PostalCode`,`PhoneNumber`,`Email`) VALUES
('Athens', 'Maikina', 59, 15772, 2135678234,'car_rentoulis_ath@protonmail.com'),
('Herakleion', 'Karystou', 9, 45672, 2510895623, 'car_rentoulis_her@protonmail.com'),
('Thessaloniki', 'Kamvounion', 6, 23772, 2310536677, 'car_rentoulis_thes@protonmail.com'),
('Patra', 'Masalas', 2, 11201, 2610533981, 'car_rentoulis_pat@protonmail.com'),
('Rodos', 'Evelpidon', 39, 11241, 2710258963, 'car_rentoulis_rod@protonmail.com');

INSERT INTO `employee` (`IRSNumber`, `FirstName`, `LastName`, `SocialSecurityNo`, `DriverLicense`, `City`, `Street`, `StreetNo`, `PostalCode`) VALUES
(854623589,'Eudoksia','Loukianou',01129602902,9872535666,'Athens','Alber Kami',2,41222),
(888885623,'Xrusa', 'Nanou', 30119602903, 9663696369, 'Athens', 'Iras', 3, 15882),
(998885623,'Thomi', 'Ntintoka', 16129602903, 6663696369, 'Athens', 'Iras', 3, 15882),
(888886369,'Vaso', 'Palentza', 05059602903, 9663363369, 'Athens', 'Iras', 3, 15882),
(888887812,'Eva', 'Sarafianou', 12129302903, 8333696369, 'Herakleion', 'Ermou', 4, 78882),
(666885623,'Stefanos', 'Koutoupis', 30119302903, 7773696369, 'Herakleion', 'Iras', 3, 15882),
(754683589,'Magdalini','Tsoureka',11039609802,6685792316,'Herakleion','Katseli',23,78222),
(561298745,'Karolos','Markou',01129202891,7894565666,'Patra','Oreinis Taksiarxias',2,12456),
(661298745,'David','Harvey',01128102891,9994565666,'Patra','Oreinis Taksiarxias',12,12456),
(771298745,'Gilles','Dauve',03057902891,4594565666,'Patra','Kalatrava',2,12456),
(444624565,'Kostis','Papagiorgis',15038902902,9685741425,'Rodos','Manis',2,31222),
(554624565,'Kostis','Xrusostomou',05068902902,9685741425,'Rodos','Manis',2,31222),
(444689565,'Manolis','Anagnostakis',14048802945,1234541425,'Thessaloniki','Kamvounion',6,51222),
(444339565,'Giannis','Ritsos',14046502945,1235441425,'Thessaloniki','Skoufa',6,51222),
(422689565,'Arthouros','Rimbaud',14047002945,1234541425,'Thessaloniki','Tsimiski',6,51222);

INSERT INTO `customer` (`IRSNumber`, `FirstName`, `LastName`, `SocialSecurityNo`, `DriverLicense`, `FirstRegistration`, `City`, `Street`, `StreetNo`, `PostalCode`) VALUES
(123456789,'Makis','Atzemoglou',28029636902,1232535666,'2015-03-08','Athens','Soutsou',3,31422),
(453256789,'Giannis','Atzemoglou',27029636902,2132535666,'2015-03-18','Athens','Kolokotroni',3,31422),
(383456789,'Ioustinianos','Atzemoglou',28039636902,2232535666,'2015-05-08','Athens','Xarilaou',3,31422),
(114589967,'Aliki','Likka',11048609802,6645692316,'2015-05-18','Athens','Travlantoni',51,15772),
(324589637,'Silvia','Federikou',15058509802,6666692316,'2016-06-16','Herakleion','Skra',1,14872),
(114522967,'Maria','Gogou',13059709802,7745696666,'2016-06-18','Thessaloniki','Ntourouti',11,14772),
(123444967,'Kristalis','Lountemis',11048719802,1145697777,'2016-06-19','Patra','Kokkinaki',5,21772),
(664577637,'Silvia','Manolatou',21058509802,6677692316,'2016-07-16','Herakleion','Ermou',1,14872),
(884589637,'Maya','Katseli',15058508856,8866692316,'2016-09-17','Herakleion','Skra',1,14872),
(123489967,'Nikos','Karouzos',16058719802,6345697777,'2016-12-19','Rodos','Afroditis',5,11772),
(114589967,'Katerina','Gogou',12059709802,6645696666,'2017-01-18','Thessaloniki','Ntourouti',11,14772),
(663489967,'Menelaos','Lountemis',11048719802,6645697777,'2017-05-19','Patra','Kokkinaki',5,21772),
(553489967,'Stathis','Karouzos',16058919802,6344697777,'2017-06-19','Rodos','Afroditis',5,11772),
(114581167,'Sofia','Likka',11048609802,7745692316,'2017-08-18','Athens','Travlantoni',51,15772),
(114581167,'Aliki','Markou',12129009802,1115692316,'2017-10-18','Athens','Travelou',15,15772);


INSERT INTO `vehicle` (`LicensePlate`, `StoreID`, `CarType`, `Model`, `Make`, `CC`, `HorsePower`, `CarYear`, `Km`, `LastService`, `NextService`, `InsuranceExpdate`, `Damages`, `Malfunction`, `FuelType`) VALUES
('PIA 2317', 1, 'Car', 'Yaris', 'Toyota', 1000, 69, '2007-00-00', 130000, '2017-10-11', '2018-03-11', '2018-04-12','No', 'No', 'Gas'),
('AKA 1312', 1, 'Motorcycle', 'Vespa', 'Piagio', 60, 500, '2014-00-01', 15000, '2017-10-11', '2018-03-11', '2018-04-12','No', 'No', 'Gasoline'),
('MIH 2315', 1, 'Mini Van', 'Cube', 'Renault', 1300, 72, '2013-00-01', 110000, '2017-11-11', '2018-04-11', '2018-05-12','No', 'No', 'Oil'),
('MIH 2415', 1, 'Truck', 'PR3000', 'Man', 4000, 400, '2013-00-01', 110000, '2017-11-11', '2018-04-11', '2018-05-12','No', 'No', 'Oil'),
('PIH 2313', 1, 'Car', 'Golf', 'Wolks Wagen', 1200, 70, '2012-00-01', 120000, '2017-11-13', '2018-04-13', '2019-05-13','No', 'No', 'Gas'),
('XIA 3117', 2, 'Car', 'Yaris', 'Toyota', 1000, 69, '2007-00-01', 50000, '2017-12-11', '2018-12-11', '2018-04-12','No', 'No', 'Gas'),
('MIO 2517', 2, 'Motorcycle', 'Mpla', 'Suzuki', 1000, 50, '2015-00-01', 100000, '2017-11-11', '2018-04-11', '2018-05-12','No', 'No', 'Gasoline'),
('MIH 6618', 2, 'Mini Van', 'Cube', 'Renault', 1300, 72, '2013-00-01', 60000, '2017-12-12', '2018-04-12', '2018-05-12','No', 'No', 'Oil'),
('MIH 3334', 3, 'Car', 'Mito', 'Alfa Romeo', 1000, 69, '2015-00-01', 50000, '2017-11-11', '2018-04-11', '2018-05-12','No', 'No', 'Gas'),
('MIH 6678', 3, 'Truck', 'PR4000', 'Man', 4000, 400, '2007-00-01', 200000, '2017-11-11', '2018-04-11', '2018-05-12','No', 'No', 'Oil'),
('MIH 3335', 4, 'Car', 'Mito', 'Alfa Romeo', 1000, 69, '2015-00-01', 50000, '2018-01-03', '2018-06-11', '2018-12-12','No', 'No', 'Gas'),
('MIH 1256', 4, 'Motorcycle', 'GT40', 'Kawasaki', 60, 1000, '2014-00-01', 20000, '2017-11-11', '2018-04-11', '2018-05-12','No', 'No', 'Gasoline'),
('MIH 3336', 5, 'Car', 'Mito', 'Alfa Romeo', 1000, 69, '2015-00-01', 50000, '2018-02-03', '2018-07-11', '2019-02-12','No', 'No', 'Gas'),
('PIH 2317', 5, 'Car', 'Golf', 'Wolks Wagen', 1200, 70, '2012-00-01', 120000, '2017-11-12', '2018-04-12', '2019-05-12','No', 'No', 'Gas'),
('KAB 1312', 5, 'Motorcycle', 'Vespa', 'Piagio', 60, 500, '2014-00-01', 15000, '2017-12-11', '2018-04-11', '2018-07-12','No', 'No', 'Gasoline');

INSERT INTO `works`(`IRSNumber`,`StoreID`, `StartDate`, `FinishDate`, `WorkerPosition`) VALUES
(854623589, 1, '2015-01-07', '2018-07-07', 'Manager'),
(888885623, 1, '2015-01-07', '2018-07-07', 'Grammateia'),
(998885623, 1, '2015-01-07', '2018-07-07', 'DeliveryGirl'),
(888886369, 1, '2015-01-07', '2018-07-07', 'DeliveryGirl'),
(888887812, 2, '2016-01-07', '2019-07-07', 'Manager'),
(666885623, 2, '2016-01-07', '2019-07-07', 'Grammateia'),
(754683589, 2, '2016-01-07', '2019-07-07', 'DeliveryGirl'),
(444689565, 3, '2016-01-09', '2019-07-09', 'Manager'),
(444339565, 3, '2016-01-09', '2019-07-09', 'DeliveryBoy'),
(422689565, 3, '2016-01-09', '2019-07-09', 'DeliveryBoy'),
(561298745, 4, '2016-01-09', '2019-07-09', 'Manager'),
(661298745, 4, '2016-01-09', '2019-07-09', 'DeliveryBoy'),
(771298745, 4, '2016-01-09', '2019-07-09', 'DeliveryBoy'),
(444624565, 5, '2016-01-09', '2019-07-09', 'Manager'),
(554624565, 5, '2016-01-09', '2019-07-09', 'DeliveryBoy');


INSERT INTO `rents` (`LicensePlate`, `CustomerID`, `IRSNumber`, `StartDate`, `FinishDate`, `StartLocation`, `FinishLocation`, `ReturnState`, `PaymentAmount`, `PaymentMethod`) VALUES
('PIA 2317', 10, 998885623, '2015-03-08', '2015-03-23', 'Athens', 'Athens', 'No', 763, 'metrita'),
('MIH 2315', 11, 998885623, '2015-03-18', '2015-03-28', 'Athens', 'Athens', 'No', 200, 'metrita'),
('PIA 2317', 12, 888886369, '2015-05-08', '2015-05-20', 'Athens', 'Athens', 'No', 420, 'metrita'),
('AKA 1312', 13, 998885623, '2015-05-18', '2015-05-28', 'Athens', 'Patra', 'No', 500, 'metrita'),
('MIO 2517', 14, 754683589, '2016-03-28', '2016-02-12', 'Herakleion', 'Herakleion', 'No', 500, 'metrita'),
('MIH 6678', 15, 444689565, '2016-05-02', '2016-06-02', 'Thessaloniki', 'Thessaloniki', 'No', 1000, 'metrita'),
('AKA 1312', 13, 888886369, '2016-08-02', '2016-08-12', 'Athens', 'Athens', 'No', 250, 'metrita'),
('MIH 1256', 16, 561298745, '2016-09-02', '2016-09-09', 'Patra', 'Patra', 'Damaged', 300, 'metrita'),
('XIA 3117', 17, 754683589, '2016-10-28', '2016-11-05', 'Herakleion', 'Herakleion', 'No', 500, 'metrita'),
('PIA 2317', 10, 998885623, '2016-12-08', '2016-12-23', 'Athens', 'Athens', 'No', 763, 'metrita'),
('MIH 6618', 18, 754683589, '2017-01-28', '2017-02-05', 'Herakleion', 'Herakleion', 'No', 500, 'metrita'),
('XIA 3117', 18, 754683589, '2017-02-28', '2017-03-05', 'Herakleion', 'Herakleion', 'No', 400, 'metrita'),
('MIH 3336', 19, 554624565, '2017-03-10', '2017-03-16', 'Rodos', 'Rodos', 'No', 400, 'metrita'),
('MIH 3334', 20, 444689565, '2017-05-02', '2017-05-04', 'Thessaloniki', 'Thessaloniki', 'No', 100, 'metrita'),
('MIH 3335', 21, 561298745, '2017-05-02', '2017-05-09', 'Patra', 'Patra', 'No', 300, 'metrita'),
('MIH 3336', 22, 554624565, '2017-06-10', '2017-06-16', 'Rodos', 'Rodos', 'No', 400, 'metrita'),
('AKA 1312', 23, 998885623, '2017-08-28', '2016-08-07', 'Athens', 'Athens', 'No', 500, 'metrita'),
('PIA 2317', 24, 998885623, '2017-09-01', '2017-09-10', 'Athens', 'Athens', 'No', 500, 'metrita');

INSERT INTO `reserves` (`LicensePlate`, `CustomerID`, `StartDate`, `FinishDate`, `StartLocation`, `FinishLocation`, `Paid`) VALUES
('PIA 2317', 10, '2015-03-08', '2015-03-23', 'Athens', 'Athens', 'YES'),
('PIA 2317', 12, '2015-12-12', '2015-12-20', 'Athens', 'Athens', 'YES'),
('AKA 1312', 13, '2015-05-18', '2015-05-28', 'Athens', 'Patra', 'YES'),
('AKA 1312', 13, '2016-08-02', '2016-08-12', 'Athens', 'Athens', 'YES'),
('MIH 1256', 16, '2016-09-02', '2016-09-09', 'Patra', 'Patra', 'YES'),
('XIA 3117', 17, '2016-10-28', '2016-11-05', 'Herakleion', 'Herakleion', 'YES'),
('PIA 2317', 10, '2016-12-08', '2016-12-23', 'Athens', 'Athens', 'YES'),
('MIH 6618', 18, '2017-01-28', '2017-02-05', 'Herakleion', 'Herakleion', 'YES'),
('XIA 3117', 18, '2017-02-28', '2017-03-05', 'Herakleion', 'Herakleion', 'YES'),
('MIH 3336', 19, '2017-03-10', '2017-03-16', 'Rodos', 'Rodos', 'YES'),
('MIH 3334', 20, '2017-05-02', '2017-05-04', 'Thessaloniki', 'Thessaloniki', 'YES'),
('MIH 3335', 21, '2017-05-02', '2017-05-09', 'Patra', 'Patra', 'YES'),
('MIH 3336', 22, '2017-06-10', '2017-06-16', 'Rodos', 'Rodos', 'YES'),
('AKA 1312', 23, '2017-08-28', '2016-08-07', 'Athens', 'Athens', 'YES'),
('PIA 2317', 24, '2017-09-01', '2017-09-10', 'Athens', 'Athens', 'NO');

/* * * * * * * TRIGGERS * * * * * */

/* * * * * * * trigger1 * * * * * */
DELIMITER $$
CREATE TRIGGER trigger_check_if_reserved BEFORE INSERT ON reserves
FOR EACH ROW
BEGIN
  IF (EXISTS (SELECT LicensePlate FROM reserves WHERE
  LicensePlate =new.LicensePlate AND
  new.StartDate <= DATE_ADD(FinishDate, INTERVAL 1 DAY) AND
  new.FinishDate >= DATE_SUB(StartDate, INTERVAL 1 DAY)))
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'I am sorry, this vehicle is already reserved for the selected dates';
  END IF;
END
$$
DELIMITER ;

-- /* * * * * * * trigger2 * * * * * */
DELIMITER $$
CREATE TRIGGER trigger_car_condition AFTER INSERT ON rents
FOR EACH ROW
BEGIN
  UPDATE vehicle set vehicle.damages=CONCAT(new.ReturnState)
  WHERE new.licenseplate=vehicle.licenseplate;
END
$$
DELIMITER ;