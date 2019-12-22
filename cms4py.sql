-- Adminer 4.7.4 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role` varchar(512) DEFAULT NULL,
  `description` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `auth_group` (`id`, `role`, `description`) VALUES
(1,	'normal',	NULL),
(2,	'editor',	NULL),
(3,	'admin',	NULL),
(4,	'blocked',	NULL);

DROP TABLE IF EXISTS `auth_membership`;
CREATE TABLE `auth_membership` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `auth_membership` (`id`, `group_id`, `user_id`) VALUES
(1,	3,	1);

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `login_name` varchar(512) DEFAULT NULL,
  `nickname` varchar(512) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `phone` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `openid` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `auth_user` (`id`, `login_name`, `nickname`, `email`, `phone`, `password`, `openid`) VALUES
(1,	'admin',	'peter',	'admin@admin.com',	'12345678901',	'pbkdf2(1000,20,sha512)$a86455de126ff290$759cda1eafd4cbc856839052a4ffed2276f9cd86',	NULL),
(2,	'plter',	'nick',	'a@a.a',	'12',	'pbkdf2(1000,20,sha512)$ae298e5a1172df02$8316fe004c219e703dc044b7166c55805e5a5147',	NULL);

DROP TABLE IF EXISTS `cms4py_session`;
CREATE TABLE `cms4py_session` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `session_id` varchar(512) DEFAULT NULL,
  `session_content` longtext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `cms4py_session` (`id`, `session_id`, `session_content`) VALUES
(1,	'a3d4e002e51442b9988a3eaae8cbaf64',	'{\"current_user\": {\"id\": 1, \"login_name\": \"admin\", \"email\": \"admin@admin.com\", \"phone\": \"12345678901\", \"nickname\": \"peter\"}}'),
(2,	'7aeb7788d2dc4fe0a50af67a12a22813',	'{\"current_user\": {\"id\": 1, \"login_name\": \"admin\", \"email\": \"admin@admin.com\", \"phone\": \"12345678901\", \"nickname\": \"peter\"}}'),
(3,	'4f748486c2344b64a7084326da452bd9',	'{\"current_user\": {\"id\": 1, \"login_name\": \"admin\", \"email\": \"admin@admin.com\", \"phone\": \"12345678901\", \"nickname\": \"peter\"}}');

-- 2019-12-22 08:01:32
