-- MySQL dump 10.13  Distrib 5.7.18, for Win64 (x86_64)
--
-- Host: localhost    Database: vehicle_ads
-- ------------------------------------------------------
-- Server version	5.7.18-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `all_vehicles`
--

DROP TABLE IF EXISTS `all_vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `all_vehicles` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `link` varchar(255) NOT NULL,
  `title` text,
  `images` text,
  `description` text,
  `price` varchar(255) DEFAULT NULL,
  `year` varchar(255) DEFAULT NULL,
  `make` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `vehicle_condition` varchar(255) DEFAULT NULL,
  `fuel` varchar(255) DEFAULT NULL,
  `odometer` varchar(255) DEFAULT NULL,
  `paint_color` varchar(255) DEFAULT NULL,
  `vin` varchar(255) DEFAULT NULL,
  `cylinders` varchar(255) DEFAULT NULL,
  `transmission` varchar(255) DEFAULT NULL,
  `title_status` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `size` varchar(255) DEFAULT NULL,
  `drive` varchar(255) DEFAULT NULL,
  `html` text,
  `series` varchar(255) DEFAULT NULL,
  `vauto_link` text,
  `city` varchar(255) DEFAULT NULL,
  `series_type` varchar(255) DEFAULT NULL,
  `subtitle` varchar(255) DEFAULT NULL,
  `time_added` int(255) DEFAULT NULL,
  `last_modified` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `link_UNIQUE` (`link`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `all_vehicles`
--

LOCK TABLES `all_vehicles` WRITE;
/*!40000 ALTER TABLE `all_vehicles` DISABLE KEYS */;
/*!40000 ALTER TABLE `all_vehicles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `human_assistance`
--

DROP TABLE IF EXISTS `human_assistance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `human_assistance` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `link` varchar(255) NOT NULL,
  `title` text,
  `images` text,
  `description` text,
  `price` varchar(255) DEFAULT NULL,
  `year` varchar(255) DEFAULT NULL,
  `make` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `vehicle_condition` varchar(255) DEFAULT NULL,
  `fuel` varchar(255) DEFAULT NULL,
  `odometer` varchar(255) DEFAULT NULL,
  `paint_color` varchar(255) DEFAULT NULL,
  `vin` varchar(255) DEFAULT NULL,
  `cylinders` varchar(255) DEFAULT NULL,
  `transmission` varchar(255) DEFAULT NULL,
  `title_status` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `size` varchar(255) DEFAULT NULL,
  `drive` varchar(255) DEFAULT NULL,
  `html` text,
  `series` varchar(255) DEFAULT NULL,
  `vauto_link` text,
  `city` varchar(255) DEFAULT NULL,
  `series_type` varchar(255) DEFAULT NULL,
  `subtitle` varchar(255) DEFAULT NULL,
  `time_added` int(255) DEFAULT NULL,
  `last_modified` int(255) DEFAULT NULL,
  `original_link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `link_UNIQUE` (`link`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `human_assistance`
--

LOCK TABLES `human_assistance` WRITE;
/*!40000 ALTER TABLE `human_assistance` DISABLE KEYS */;
/*!40000 ALTER TABLE `human_assistance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicles_blacklisted`
--

DROP TABLE IF EXISTS `vehicles_blacklisted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicles_blacklisted` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `link` varchar(255) NOT NULL,
  `title` text,
  `images` text,
  `description` text,
  `price` varchar(255) DEFAULT NULL,
  `year` varchar(255) DEFAULT NULL,
  `make` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `vehicle_condition` varchar(255) DEFAULT NULL,
  `fuel` varchar(255) DEFAULT NULL,
  `odometer` varchar(255) DEFAULT NULL,
  `paint_color` varchar(255) DEFAULT NULL,
  `vin` varchar(255) DEFAULT NULL,
  `cylinders` varchar(255) DEFAULT NULL,
  `transmission` varchar(255) DEFAULT NULL,
  `title_status` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `size` varchar(255) DEFAULT NULL,
  `drive` varchar(255) DEFAULT NULL,
  `html` text,
  `series` varchar(255) DEFAULT NULL,
  `vauto_link` text,
  `city` varchar(255) DEFAULT NULL,
  `series_type` varchar(255) DEFAULT NULL,
  `subtitle` varchar(255) DEFAULT NULL,
  `last_modified` int(255) DEFAULT NULL,
  `time_added` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `link_UNIQUE` (`link`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicles_blacklisted`
--

LOCK TABLES `vehicles_blacklisted` WRITE;
/*!40000 ALTER TABLE `vehicles_blacklisted` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehicles_blacklisted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicles_whitelisted`
--

DROP TABLE IF EXISTS `vehicles_whitelisted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicles_whitelisted` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `link` varchar(255) NOT NULL,
  `title` text,
  `images` text,
  `description` text,
  `price` varchar(255) DEFAULT NULL,
  `year` varchar(255) DEFAULT NULL,
  `make` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `vehicle_condition` varchar(255) DEFAULT NULL,
  `fuel` varchar(255) DEFAULT NULL,
  `odometer` varchar(255) DEFAULT NULL,
  `paint_color` varchar(255) DEFAULT NULL,
  `vin` varchar(255) DEFAULT NULL,
  `cylinders` varchar(255) DEFAULT NULL,
  `transmission` varchar(255) DEFAULT NULL,
  `title_status` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `size` varchar(255) DEFAULT NULL,
  `drive` varchar(255) DEFAULT NULL,
  `html` text,
  `series` varchar(255) DEFAULT NULL,
  `vauto_link` text,
  `city` varchar(255) DEFAULT NULL,
  `series_type` varchar(255) DEFAULT NULL,
  `subtitle` varchar(255) DEFAULT NULL,
  `last_modified` int(255) DEFAULT NULL,
  `time_added` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `link_UNIQUE` (`link`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicles_whitelisted`
--

LOCK TABLES `vehicles_whitelisted` WRITE;
/*!40000 ALTER TABLE `vehicles_whitelisted` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehicles_whitelisted` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-19 17:51:40
