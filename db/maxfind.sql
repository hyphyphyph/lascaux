-- phpMyAdmin SQL Dump
-- version 3.3.7deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 24, 2010 at 05:04 AM
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
  `attr` text NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=104 ;

--
-- Dumping data for table `characteristic`
--

INSERT INTO `characteristic` (`id`, `attr`, `value`) VALUES
(1, 'color', 'black'),
(2, 'brand', 'hp'),
(3, 'model', 'dv2'),
(4, '0', ''),
(5, '1', ''),
(6, '2', ''),
(7, '3', ''),
(8, '4', ''),
(9, '5', ''),
(10, '6', ''),
(11, '7', ''),
(12, '8', ''),
(13, '9', ''),
(14, '10', ''),
(15, '11', ''),
(16, '12', ''),
(17, '13', ''),
(18, '14', ''),
(19, '15', ''),
(20, '16', ''),
(21, '17', ''),
(22, '18', ''),
(23, '19', ''),
(24, '20', ''),
(25, '21', ''),
(26, '22', ''),
(27, '23', ''),
(28, '24', ''),
(29, '25', ''),
(30, '26', ''),
(31, '27', ''),
(32, '28', ''),
(33, '29', ''),
(34, '30', ''),
(35, '31', ''),
(36, '32', ''),
(37, '33', ''),
(38, '34', ''),
(39, '35', ''),
(40, '36', ''),
(41, '37', ''),
(42, '38', ''),
(43, '39', ''),
(44, '40', ''),
(45, '41', ''),
(46, '42', ''),
(47, '43', ''),
(48, '44', ''),
(49, '45', ''),
(50, '46', ''),
(51, '47', ''),
(52, '48', ''),
(53, '49', ''),
(54, '50', ''),
(55, '51', ''),
(56, '52', ''),
(57, '53', ''),
(58, '54', ''),
(59, '55', ''),
(60, '56', ''),
(61, '57', ''),
(62, '58', ''),
(63, '59', ''),
(64, '60', ''),
(65, '61', ''),
(66, '62', ''),
(67, '63', ''),
(68, '64', ''),
(69, '65', ''),
(70, '66', ''),
(71, '67', ''),
(72, '68', ''),
(73, '69', ''),
(74, '70', ''),
(75, '71', ''),
(76, '72', ''),
(77, '73', ''),
(78, '74', ''),
(79, '75', ''),
(80, '76', ''),
(81, '77', ''),
(82, '78', ''),
(83, '79', ''),
(84, '80', ''),
(85, '81', ''),
(86, '82', ''),
(87, '83', ''),
(88, '84', ''),
(89, '85', ''),
(90, '86', ''),
(91, '87', ''),
(92, '88', ''),
(93, '89', ''),
(94, '90', ''),
(95, '91', ''),
(96, '92', ''),
(97, '93', ''),
(98, '94', ''),
(99, '95', ''),
(100, '96', ''),
(101, '97', ''),
(102, '98', ''),
(103, '99', '');

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=38 ;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`id`, `title`, `kind`, `created`, `group_id`, `uuid_finder`, `uuid_loser`, `workflow_state_id`) VALUES
(37, '123', 'found', 1287906927, 15, NULL, '17078700df4411dfbf2100265e50c061', 17);

-- --------------------------------------------------------

--
-- Table structure for table `item_group`
--

CREATE TABLE IF NOT EXISTS `item_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `item_group`
--

INSERT INTO `item_group` (`id`, `name`) VALUES
(15, 'laptop');

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

INSERT INTO `item_x_characteristic` (`item_id`, `characteristic_id`) VALUES
(37, 1),
(37, 2),
(37, 3),
(37, 4),
(37, 5),
(37, 6),
(37, 7),
(37, 8),
(37, 9),
(37, 10),
(37, 11),
(37, 12),
(37, 13),
(37, 14),
(37, 15),
(37, 16),
(37, 17),
(37, 18),
(37, 19),
(37, 20),
(37, 21),
(37, 22),
(37, 23),
(37, 24),
(37, 25),
(37, 26),
(37, 27),
(37, 28),
(37, 29),
(37, 30),
(37, 31),
(37, 32),
(37, 33),
(37, 34),
(37, 35),
(37, 36),
(37, 37),
(37, 38),
(37, 39),
(37, 40),
(37, 41),
(37, 42),
(37, 43),
(37, 44),
(37, 45),
(37, 46),
(37, 47),
(37, 48),
(37, 49),
(37, 50),
(37, 51),
(37, 52),
(37, 53),
(37, 54),
(37, 55),
(37, 56),
(37, 57),
(37, 58),
(37, 59),
(37, 60),
(37, 61),
(37, 62),
(37, 63),
(37, 64),
(37, 65),
(37, 66),
(37, 67),
(37, 68),
(37, 69),
(37, 70),
(37, 71),
(37, 72),
(37, 73),
(37, 74),
(37, 75),
(37, 76),
(37, 77),
(37, 78),
(37, 79),
(37, 80),
(37, 81),
(37, 82),
(37, 83),
(37, 84),
(37, 85),
(37, 86),
(37, 87),
(37, 88),
(37, 89),
(37, 90),
(37, 91),
(37, 92),
(37, 93),
(37, 94),
(37, 95),
(37, 96),
(37, 97),
(37, 98),
(37, 99),
(37, 100),
(37, 101),
(37, 102),
(37, 103);

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`id`, `place`, `lat`, `lng`, `radius`, `date_start`, `date_end`, `item_id`) VALUES
(7, 'Montréal, Québec', NULL, NULL, NULL, 123, 123, 37);

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

INSERT INTO `user` (`uuid`, `username`, `email`, `password`, `created`, `lastlogin`, `active`) VALUES
('17078700df4411dfbf2100265e50c061', 'd.mounce', 'd.mounce@silkseed.com', 'e4a13a5744d69adad891c034b290cfc8942fb9fa', 1287906938, NULL, 0);

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
