-- Adminer 5.3.0 MariaDB 11.1.2-MariaDB-1:11.1.2+maria~ubu2204 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE DATABASE `cms4py` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `cms4py`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `login_name` varchar(128) DEFAULT NULL,
  `nicename` varchar(512) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `avatar` varchar(512) DEFAULT NULL,
  `gender` varchar(128) DEFAULT NULL,
  `is_super` tinyint(4) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `login_name` (`login_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `user` (`id`, `login_name`, `nicename`, `password`, `email`, `phone`, `avatar`, `gender`, `is_super`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1,	'a',	NULL,	'pbkdf2(1000,20,sha512)$8696c93cdb1058ba$dd6ec6ea92a0ca0d7296d91892cb92e7f029e0cd',	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL),
(2,	NULL,	NULL,	'pbkdf2(1000,20,sha512)$89a96cdb7f695569$80636c115a1c4b1d6506dfdac260f59cf0d796bf',	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL),
(25,	'a1',	NULL,	'pbkdf2(1000,20,sha512)$b2667f46acc02f41$372d6b6fc6cbe5f6877c26fc7ac5c5c8a570c6d4',	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL),
(26,	'a2',	NULL,	'pbkdf2(1000,20,sha512)$91ac228427ffb1e5$933782915cd5b0e1b9686df21369d5eba03b08a2',	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL),
(38,	'a3',	NULL,	'pbkdf2(1000,20,sha512)$89fa5a440bc35795$4ccee080b45b227cfcffc910a10ea6986c545c05',	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL),
(39,	'a4',	NULL,	'pbkdf2(1000,20,sha512)$a09a8c6fae320334$12aa0464487a8566d2fe5493221a66fb1f435be7',	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL),
(41,	'a5',	NULL,	'pbkdf2(1000,20,sha512)$8b37199ee305415f$f5d2fb78ffcca0955a4cd54722568ac0e5d12d18',	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL),
(42,	'a6',	NULL,	'pbkdf2(1000,20,sha512)$8d3c836b1932d2bc$1b2dd9647fef6c087d99327e8c0dd63c0862dc1d',	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL,	NULL);

-- 2025-07-19 14:03:37 UTC
