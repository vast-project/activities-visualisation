CREATE USER 'tasksuser'@'localhost' IDENTIFIED BY 'HemoGels3!@#';
grant all privileges on *.* to 'tasksuser'@'localhost';
CREATE DATABASE `tasks` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE tasks;
CREATE TABLE `adminusers` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `organization` int NOT NULL,
  `active` int NOT NULL,
  `resetlink` varchar(100),
  `resetlinkexpdate` datetime,
  `fullname` varchar(30) NOT NULL,
  `phone` int,
  `typeid` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `educationlevel` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `level` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `events` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL,
  `visitor` varchar(50) NOT NULL,
  `noofvisitors` int NOT NULL,
  `educationlevel` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `organizations` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `phone` int,
  `address` varchar(50),
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `usertypes` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
INSERT INTO `tasks`.`adminusers` (`email`, `password`, `organization`, `active`, `fullname`,`typeid`) VALUES ('adminuser@vast.org', 'Abc@12345', 1, 1, 'VAST Admin User',1);
INSERT INTO `tasks`.`educationlevel` (`level`) VALUES ('PRIMARY SCHOOL');
INSERT INTO `tasks`.`educationlevel` (`level`) VALUES ('HIGH SCHOOL');
INSERT INTO `tasks`.`organizations` (`name`) VALUES ('VAST');
INSERT INTO `tasks`.`usertypes` (`type`) VALUES ('VAST User');
INSERT INTO `tasks`.`usertypes` (`type`) VALUES ('Organization User');
