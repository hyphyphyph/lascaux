-- phpMyAdmin SQL Dump
-- version 3.3.7deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 24, 2010 at 02:09 AM
-- Server version: 5.1.49
-- PHP Version: 5.3.3-1ubuntu9.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `maxfind`
--

-- --------------------------------------------------------

--
-- Table structure for table `characteristic`
--

CREATE TABLE IF NOT EXISTS `characteristic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attr` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `characteristic`
--


-- --------------------------------------------------------

--
-- Table structure for table `characteristic_property`
--

CREATE TABLE IF NOT EXISTS `characteristic_property` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` text,
  `characteristic_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `characteristic_property`
--


-- --------------------------------------------------------

--
-- Table structure for table `item`
--

CREATE TABLE IF NOT EXISTS `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `kind` varchar(255) DEFAULT NULL,
  `created` int(11) DEFAULT NULL,
  `group_id` int(11) NOT NULL,
  `uuid_finder` varchar(255) DEFAULT NULL,
  `uuid_loser` varchar(45) DEFAULT NULL,
  `workflow_state_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=22 ;

--
-- Dumping data for table `item`
--


-- --------------------------------------------------------

--
-- Table structure for table `item_group`
--

CREATE TABLE IF NOT EXISTS `item_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `item_group`
--


-- --------------------------------------------------------

--
-- Table structure for table `item_x_characteristic`
--

CREATE TABLE IF NOT EXISTS `item_x_characteristic` (
  `item_id` int(11) NOT NULL,
  `characteristic_id` int(11) NOT NULL,
  PRIMARY KEY (`item_id`,`characteristic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `item_x_characteristic`
--


-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE IF NOT EXISTS `location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `place` varchar(255) DEFAULT NULL,
  `lat` varchar(255) DEFAULT NULL,
  `lng` varchar(255) DEFAULT NULL,
  `radius` float DEFAULT NULL,
  `date_start` int(11) DEFAULT NULL,
  `date_end` int(11) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `location`
--


-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE IF NOT EXISTS `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) DEFAULT NULL,
  `body` text,
  `date` int(11) DEFAULT NULL,
  `read` tinyint(1) DEFAULT NULL,
  `uuid_from` varchar(255) DEFAULT NULL,
  `uuid_to` varchar(255) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `message`
--


-- --------------------------------------------------------

--
-- Table structure for table `notification_setting`
--

CREATE TABLE IF NOT EXISTS `notification_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `notification_setting`
--


-- --------------------------------------------------------

--
-- Table structure for table `setting`
--

CREATE TABLE IF NOT EXISTS `setting` (
  `name` varchar(255) NOT NULL,
  `value` text,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `setting`
--

INSERT INTO `setting` (`name`, `value`) VALUES
('laf_item_workflow_set_id', '2');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `uuid` varchar(255) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `created` int(11) DEFAULT NULL,
  `lastlogin` int(11) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uuid`),
  KEY `username` (`username`),
  KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--


-- --------------------------------------------------------

--
-- Table structure for table `workflow_set`
--

CREATE TABLE IF NOT EXISTS `workflow_set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET latin1 NOT NULL,
  `desc` text CHARACTER SET latin1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `workflow_set`
--

INSERT INTO `workflow_set` (`id`, `title`, `desc`) VALUES
(2, 'Item', '');

-- --------------------------------------------------------

--
-- Table structure for table `workflow_state`
--

CREATE TABLE IF NOT EXISTS `workflow_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_set_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `desc` text,
  `next_id` int(11) DEFAULT NULL,
  `prev_id` int(11) DEFAULT NULL,
  `initial` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=18 ;

--
-- Dumping data for table `workflow_state`
--

INSERT INTO `workflow_state` (`id`, `workflow_set_id`, `name`, `title`, `desc`, `next_id`, `prev_id`, `initial`) VALUES
(16, 2, 'unverified', 'Unverified', '', 17, 0, 1),
(17, 2, 'verified', 'Verified', '', 0, 0, 0);
