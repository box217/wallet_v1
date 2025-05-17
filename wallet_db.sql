/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 80405
 Source Host           : localhost:3306
 Source Schema         : wallet_db

 Target Server Type    : MySQL
 Target Server Version : 80405
 File Encoding         : 65001

 Date: 18/05/2025 00:23:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add merchant', 7, 'add_merchant');
INSERT INTO `auth_permission` VALUES (26, 'Can change merchant', 7, 'change_merchant');
INSERT INTO `auth_permission` VALUES (27, 'Can delete merchant', 7, 'delete_merchant');
INSERT INTO `auth_permission` VALUES (28, 'Can view merchant', 7, 'view_merchant');
INSERT INTO `auth_permission` VALUES (29, 'Can add platform user', 8, 'add_platformuser');
INSERT INTO `auth_permission` VALUES (30, 'Can change platform user', 8, 'change_platformuser');
INSERT INTO `auth_permission` VALUES (31, 'Can delete platform user', 8, 'delete_platformuser');
INSERT INTO `auth_permission` VALUES (32, 'Can view platform user', 8, 'view_platformuser');
INSERT INTO `auth_permission` VALUES (33, 'Can add wallet address', 9, 'add_walletaddress');
INSERT INTO `auth_permission` VALUES (34, 'Can change wallet address', 9, 'change_walletaddress');
INSERT INTO `auth_permission` VALUES (35, 'Can delete wallet address', 9, 'delete_walletaddress');
INSERT INTO `auth_permission` VALUES (36, 'Can view wallet address', 9, 'view_walletaddress');
INSERT INTO `auth_permission` VALUES (37, 'Can add recharge log', 10, 'add_rechargelog');
INSERT INTO `auth_permission` VALUES (38, 'Can change recharge log', 10, 'change_rechargelog');
INSERT INTO `auth_permission` VALUES (39, 'Can delete recharge log', 10, 'delete_rechargelog');
INSERT INTO `auth_permission` VALUES (40, 'Can view recharge log', 10, 'view_rechargelog');
INSERT INTO `auth_permission` VALUES (41, 'Can add merchant collection address', 11, 'add_merchantcollectionaddress');
INSERT INTO `auth_permission` VALUES (42, 'Can change merchant collection address', 11, 'change_merchantcollectionaddress');
INSERT INTO `auth_permission` VALUES (43, 'Can delete merchant collection address', 11, 'delete_merchantcollectionaddress');
INSERT INTO `auth_permission` VALUES (44, 'Can view merchant collection address', 11, 'view_merchantcollectionaddress');
INSERT INTO `auth_permission` VALUES (45, 'Can add collection log', 12, 'add_collectionlog');
INSERT INTO `auth_permission` VALUES (46, 'Can change collection log', 12, 'change_collectionlog');
INSERT INTO `auth_permission` VALUES (47, 'Can delete collection log', 12, 'delete_collectionlog');
INSERT INTO `auth_permission` VALUES (48, 'Can view collection log', 12, 'view_collectionlog');
INSERT INTO `auth_permission` VALUES (49, 'Can add telegram watch address', 13, 'add_telegramwatchaddress');
INSERT INTO `auth_permission` VALUES (50, 'Can change telegram watch address', 13, 'change_telegramwatchaddress');
INSERT INTO `auth_permission` VALUES (51, 'Can delete telegram watch address', 13, 'delete_telegramwatchaddress');
INSERT INTO `auth_permission` VALUES (52, 'Can view telegram watch address', 13, 'view_telegramwatchaddress');
COMMIT;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for core_collectionlog
-- ----------------------------
DROP TABLE IF EXISTS `core_collectionlog`;
CREATE TABLE `core_collectionlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `to_address` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(20,8) NOT NULL,
  `tx_hash` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `success` tinyint(1) NOT NULL,
  `chain_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `wallet_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tx_hash` (`tx_hash`),
  KEY `core_collectionlog_wallet_id_36d7487a_fk_core_walletaddress_id` (`wallet_id`),
  CONSTRAINT `core_collectionlog_wallet_id_36d7487a_fk_core_walletaddress_id` FOREIGN KEY (`wallet_id`) REFERENCES `core_walletaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of core_collectionlog
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for core_merchant
-- ----------------------------
DROP TABLE IF EXISTS `core_merchant`;
CREATE TABLE `core_merchant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `api_key` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `callback_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `api_key` (`api_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of core_merchant
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for core_merchantcollectionaddress
-- ----------------------------
DROP TABLE IF EXISTS `core_merchantcollectionaddress`;
CREATE TABLE `core_merchantcollectionaddress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `chain_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `collection_address` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `merchant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_merchantcollectiona_merchant_id_chain_type_t_bcd1d28c_uniq` (`merchant_id`,`chain_type`,`token_type`),
  CONSTRAINT `core_merchantcollect_merchant_id_a8a8e919_fk_core_merc` FOREIGN KEY (`merchant_id`) REFERENCES `core_merchant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of core_merchantcollectionaddress
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for core_platformuser
-- ----------------------------
DROP TABLE IF EXISTS `core_platformuser`;
CREATE TABLE `core_platformuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `merchant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_platformuser_merchant_id_user_id_278ae4b8_uniq` (`merchant_id`,`user_id`),
  CONSTRAINT `core_platformuser_merchant_id_d1de9a47_fk_core_merchant_id` FOREIGN KEY (`merchant_id`) REFERENCES `core_merchant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of core_platformuser
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for core_rechargelog
-- ----------------------------
DROP TABLE IF EXISTS `core_rechargelog`;
CREATE TABLE `core_rechargelog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tx_hash` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(20,8) NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `chain_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `wallet_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tx_hash` (`tx_hash`),
  KEY `core_rechargelog_wallet_id_f6839e02_fk_core_walletaddress_id` (`wallet_id`),
  CONSTRAINT `core_rechargelog_wallet_id_f6839e02_fk_core_walletaddress_id` FOREIGN KEY (`wallet_id`) REFERENCES `core_walletaddress` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of core_rechargelog
-- ----------------------------
BEGIN;
INSERT INTO `core_rechargelog` VALUES (1, '373e8f0b8f0fffcbb1a7dae5e25d626946f5d31cade5886550631842abf3c223', 1099.31300000, 1, 'TRC20', 'USDT', '2025-05-11 17:25:49.655881', NULL);
INSERT INTO `core_rechargelog` VALUES (2, '9fef150e1f9cb0fecd7bf690c4a3036b5aaeef09142ba4a6492e212f0c074696', 9.67211500, 1, 'TRC20', 'USDT', '2025-05-11 17:25:51.057509', NULL);
INSERT INTO `core_rechargelog` VALUES (3, '90d92c48b37d4278b4b8a4db2e382146d5935cb976e9f17ce56215faf37e0934', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-11 17:25:51.848467', NULL);
INSERT INTO `core_rechargelog` VALUES (4, '873ba7542f3fddcbd6a96678f338fd92ff86abb4e876c8b4e4693b16ffb38f8d', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-11 17:25:52.662452', NULL);
INSERT INTO `core_rechargelog` VALUES (5, 'b88fab5a15ed074cb6779bc2e00773040301a30dc86e1d3c2773308645681d0b', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-11 17:25:53.479014', NULL);
INSERT INTO `core_rechargelog` VALUES (6, '677fe50d50631577ad945833284b9eacb41c7d7e0788d68b40233cd52c800709', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-11 17:25:54.301959', NULL);
INSERT INTO `core_rechargelog` VALUES (7, '844f34646a0f8d20902ffb062511a40dce9ad32468b13b69e19d8bb5402e1992', 901.54000000, 1, 'TRC20', 'USDT', '2025-05-11 19:19:28.775629', NULL);
INSERT INTO `core_rechargelog` VALUES (8, 'ae8031a85d24f5e62e6c1e0dd5cb70848c463bc73408820dafe3233d30d15234', 0.04999100, 1, 'TRC20', 'USDT', '2025-05-12 00:45:52.778130', NULL);
INSERT INTO `core_rechargelog` VALUES (9, '3461d3291236a46fbfdc3e1157e816a777f35d3cf4844d268d6379f0dab74f56', 0.01000100, 1, 'TRC20', 'USDT', '2025-05-12 00:45:53.859205', NULL);
INSERT INTO `core_rechargelog` VALUES (10, 'd05efc9150f07d738aa2d9c8e0dc2cc727fe6b247bcd3329d826643e25804e88', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-12 06:28:51.614656', NULL);
INSERT INTO `core_rechargelog` VALUES (11, '20e9152254ca8d86c066d1a6ea15f0096913910a8b7453b2d5ce02c3fbe2d9f9', 1436.82000000, 1, 'TRC20', 'USDT', '2025-05-12 09:07:23.581896', NULL);
INSERT INTO `core_rechargelog` VALUES (12, 'e65893f1f7d31ab987d1016fbdfa6d4b58da247381efe70d0320f5138d261c72', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-12 09:07:24.932722', NULL);
INSERT INTO `core_rechargelog` VALUES (13, 'd02c2382648db5b4f4f948c7f972258bdeb69ad5743e4aa9d413f4bb2f84c8bf', 2.00010000, 1, 'TRC20', 'USDT', '2025-05-12 09:07:26.264182', NULL);
INSERT INTO `core_rechargelog` VALUES (14, '8f64cd4b9b0217e3eab7b51659c9c0a7bf2971d0804fd0482c4802de7faa3e86', 11600.00000000, 1, 'TRC20', 'USDT', '2025-05-12 09:07:27.123931', NULL);
INSERT INTO `core_rechargelog` VALUES (15, '0c3d63a362301f12cc67c9b0b09b8176f8849fd73dcd6b4249603dea43ad6381', 7.00000000, 1, 'TRC20', 'USDT', '2025-05-12 11:47:44.122908', NULL);
INSERT INTO `core_rechargelog` VALUES (16, '5321f863290786af908ad5f9deba2dfcb33905e96172a693ea4f250532f34457', 30286.00000000, 1, 'TRC20', 'USDT', '2025-05-12 12:05:15.339786', NULL);
INSERT INTO `core_rechargelog` VALUES (17, '5c18ea7d6e14951e86fe1aa9ee2e75771e2ad42eb0b452c3a12e85ac52cc7523', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-12 14:09:03.617940', NULL);
INSERT INTO `core_rechargelog` VALUES (18, 'bcf634c58e6d8b188806ac92d1d2d5f90cf3be7a6792d01f192edd9cec3cab01', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-12 14:09:08.931498', NULL);
INSERT INTO `core_rechargelog` VALUES (19, 'a7bdc5f9d3edfd15feb15134abd1382143223915bbff765545ad5cb1775f1fd3', 12094.00000000, 1, 'TRC20', 'USDT', '2025-05-12 14:59:12.006264', NULL);
INSERT INTO `core_rechargelog` VALUES (20, 'b990eb871c707bb74a26a9364fa66a33f9164973a51c5e0117a5da11cfa1041d', 391.05000000, 1, 'TRC20', 'USDT', '2025-05-12 16:59:07.911163', NULL);
INSERT INTO `core_rechargelog` VALUES (21, '87540da9852b424c64bf5a82297c751750cc74868bc60bfd1681cb00c3afe090', 8.29049900, 1, 'TRC20', 'USDT', '2025-05-12 18:44:41.415867', NULL);
INSERT INTO `core_rechargelog` VALUES (22, '396e819093de505084bbc52704e277b4139c5f86bb1282c9c6bf14fe65506a80', 0.03000100, 1, 'TRC20', 'USDT', '2025-05-13 04:22:14.915950', NULL);
INSERT INTO `core_rechargelog` VALUES (23, '6e54399f599852f322004e4c2dba64b4457d52e9485bec1dbed6c0b97aaa0c01', 34756.00000000, 1, 'TRC20', 'USDT', '2025-05-13 05:59:44.115709', NULL);
INSERT INTO `core_rechargelog` VALUES (24, '5dbab03645df272f6379ffbd0771797411706b3f67544f0f187ac4062ec86cf2', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-13 07:34:00.481693', NULL);
INSERT INTO `core_rechargelog` VALUES (25, 'dc8c867c5476ebb82840b7f8d876fa50689806f00a7a31dc13812cb0854f9ec8', 266.00000000, 1, 'TRC20', 'USDT', '2025-05-13 08:11:56.581168', NULL);
INSERT INTO `core_rechargelog` VALUES (26, '3e5f92f1e38438e350dd0d6764ec10f2bfacef13bb3eae5a2b3e87cc9133646f', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-13 09:21:50.512902', NULL);
INSERT INTO `core_rechargelog` VALUES (27, '4be86e7a1c445e84552be2257ca036b409d388ead5d2c5709e676f3cf92c11cf', 9.00000000, 1, 'TRC20', 'USDT', '2025-05-13 09:21:51.485309', NULL);
INSERT INTO `core_rechargelog` VALUES (28, 'a185dd1215f18df97e6ff052a5b4867914c59c7a411f5c8619eb9018c04339ad', 0.01000100, 1, 'TRC20', 'USDT', '2025-05-13 10:19:59.258188', NULL);
INSERT INTO `core_rechargelog` VALUES (29, '32b3fb24e98ea2de9ab84e8fc31766524a7e0306f52e31f5e3c0e96f1b3bbf94', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-13 11:31:00.014092', NULL);
INSERT INTO `core_rechargelog` VALUES (30, '17d6b14c2b941ad50df57495da3d0442a832a77b97b075fa36092e1517149434', 5.00000000, 1, 'TRC20', 'USDT', '2025-05-13 12:12:13.794184', NULL);
INSERT INTO `core_rechargelog` VALUES (31, '159b7ccf946d244a41233a49a495bb8ee3e0d5c174e48b0b656dd97da2f2ef9e', 14492.00000000, 1, 'TRC20', 'USDT', '2025-05-13 13:16:55.176900', NULL);
INSERT INTO `core_rechargelog` VALUES (32, '6d75c0ced321b5a0401f09f33dab8cf48a200536fb04815dcfc529ab7c6d9f6c', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-13 14:41:22.567123', NULL);
INSERT INTO `core_rechargelog` VALUES (33, 'ce4648c69de50c9653352532fcaf4914a8b4ad9153637bf9afcd697eb6407282', 4.00000000, 1, 'TRC20', 'USDT', '2025-05-13 14:57:44.138182', NULL);
INSERT INTO `core_rechargelog` VALUES (34, '63792d38b13f52ca8fdd720064631e710e063759a6106de893784f6fab054d7d', 89.00000000, 1, 'TRC20', 'USDT', '2025-05-13 16:26:13.926732', NULL);
INSERT INTO `core_rechargelog` VALUES (35, '5ee92255b7d4eb1745c9cb18fae13872019528c3f4d20427181491e452b5bde8', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-13 16:26:36.879158', NULL);
INSERT INTO `core_rechargelog` VALUES (36, '763af1e75a0a1fe352fc9881c87cf3718079f92c221fb7b146b1dd8cf89bfa1d', 478.05000000, 1, 'TRC20', 'USDT', '2025-05-13 18:53:54.564555', NULL);
INSERT INTO `core_rechargelog` VALUES (37, 'f38e0c2cee9827b276e1b2454dc4bc80df501d0625e4f942ea65d93dc4cfe0d1', 6.93981700, 1, 'TRC20', 'USDT', '2025-05-13 18:53:56.412857', NULL);
INSERT INTO `core_rechargelog` VALUES (38, 'f7ddcea89d20c751aa182a143137ce117fe94782a01667be89936ccae162035d', 3000.00000000, 1, 'TRC20', 'USDT', '2025-05-13 18:53:58.166442', NULL);
INSERT INTO `core_rechargelog` VALUES (39, '439840670a630df04a565c996fc7a6449717c1ee2cd7b669871c112ab783df04', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 00:29:30.272639', NULL);
INSERT INTO `core_rechargelog` VALUES (40, '5c8aaed843e8462797978c634985a8352bc0e37a87d1e45723675005df2e05fe', 30286.00000000, 1, 'TRC20', 'USDT', '2025-05-14 03:06:31.857169', NULL);
INSERT INTO `core_rechargelog` VALUES (41, 'd59af6c52873422189610091cd681915e194989f95a952126e74254421af49b5', 0.01000100, 1, 'TRC20', 'USDT', '2025-05-14 03:46:13.284827', NULL);
INSERT INTO `core_rechargelog` VALUES (42, 'a7a0162dc4c31af4c69a4da5a70eb6c3f9b004fd3637f59dcfc5c4061579c073', 12090.00000000, 1, 'TRC20', 'USDT', '2025-05-14 03:56:26.254875', NULL);
INSERT INTO `core_rechargelog` VALUES (43, '0ccebabd2781797f0fda7ac1b6dcba81452dd69d5c2e7240a549afbdabe18e32', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 04:01:39.017744', NULL);
INSERT INTO `core_rechargelog` VALUES (44, '30d061f363721280ddf94192d14d0d82501e3ffde60a4caf1c42bac33172cdf5', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 07:45:27.659338', NULL);
INSERT INTO `core_rechargelog` VALUES (45, '4017769cfe7263f00d3d8dc1dd2ddb81e33cce06f913f6a8d3859392889d701a', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 07:46:13.258070', NULL);
INSERT INTO `core_rechargelog` VALUES (46, 'b18bcdf3166e41b4a5acfa3ca8ba159858a1c0f283e36061d3675b2066d6d377', 9.00000000, 1, 'TRC20', 'USDT', '2025-05-14 07:51:05.103898', NULL);
INSERT INTO `core_rechargelog` VALUES (47, '9b1ec05f5e4a157fc66091f896db38d851c04493eb3d8acba8d553e13acbcd4d', 1013.45000000, 1, 'TRC20', 'USDT', '2025-05-14 07:52:12.550670', NULL);
INSERT INTO `core_rechargelog` VALUES (48, '5ac1a617341a3872323de1645171195d9fdf3b7bce5a1bb5ed1f03661dee3b02', 24227.00000000, 1, 'TRC20', 'USDT', '2025-05-14 08:00:02.754329', NULL);
INSERT INTO `core_rechargelog` VALUES (49, '02e15dd8380a8f81c9f4cd64554095d56cfd9aa4bfc6a4ed49eb74a5157da810', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-14 08:28:58.244463', NULL);
INSERT INTO `core_rechargelog` VALUES (50, '2f05cf59b51ea97fb99fb63541cd24c7b840ff2e06f5be2f0ce3a086b5712c19', 1052.71000000, 1, 'TRC20', 'USDT', '2025-05-14 09:16:17.329960', NULL);
INSERT INTO `core_rechargelog` VALUES (51, '1e26a8abdd5b3ec06cabdb47932d5028638e61e31e0879ef7c906db082ccc430', 1.00000000, 1, 'TRC20', 'USDT', '2025-05-14 09:50:05.322881', NULL);
INSERT INTO `core_rechargelog` VALUES (52, '042d8fa8ab880313589b9ae092a01f4a0f91e11a04f59dd1082ce9a597d781a2', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-14 09:54:22.139748', NULL);
INSERT INTO `core_rechargelog` VALUES (53, 'c3884fb1361319fc570e6c512be40e3c0604b6f6beae9d884f9a442ba621919a', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 11:24:34.615386', NULL);
INSERT INTO `core_rechargelog` VALUES (54, '0d708f43d6f2d7716e9494c0811b74393b026e02de4900c14655e2982e28a18e', 8.00000000, 1, 'TRC20', 'USDT', '2025-05-14 11:33:49.785513', NULL);
INSERT INTO `core_rechargelog` VALUES (55, '98dee4bb0947ea0bc7d4b0148dc73a217657402707386d0481f75c44d5992ed5', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 12:38:59.765228', NULL);
INSERT INTO `core_rechargelog` VALUES (56, 'ecf5fe1627684dba75f007ac2180dd448d594ad6c2c030890ff0ddea0ab27c13', 3348.00000000, 1, 'TRC20', 'USDT', '2025-05-14 14:53:05.245921', NULL);
INSERT INTO `core_rechargelog` VALUES (57, 'b0a195de3f04b36c909b3acb4e56956ddc0c94b1ccd3e32dba430598ca937f44', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 15:15:28.566933', NULL);
INSERT INTO `core_rechargelog` VALUES (58, 'a9caeb81ea797121c68129bf2b1d7499297ad3bcd0a09aa77db131b4ea9ebd50', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 17:25:18.089458', NULL);
INSERT INTO `core_rechargelog` VALUES (59, '52995f908e20e6665c16939ec43a617e01e99944df3fbe43209ce4d71c99baa6', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 19:39:42.303114', NULL);
INSERT INTO `core_rechargelog` VALUES (60, '86030fd7352fd7377aa2dfab49f0e344e6eef0234b7329c7cc9f6496e23583da', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-14 20:02:43.652215', NULL);
INSERT INTO `core_rechargelog` VALUES (61, 'a746f3a34264a1abce424011f1fb6ee4722adf876798d7b2c5cfaa0b725e98ce', 1251.15000000, 1, 'TRC20', 'USDT', '2025-05-14 21:43:30.529887', NULL);
INSERT INTO `core_rechargelog` VALUES (62, '542fa433b432cdc8ff2140f3fd60785bc3cd252986a8fabe93125ee3c659fc15', 8.00000000, 1, 'TRC20', 'USDT', '2025-05-15 00:04:21.450120', NULL);
INSERT INTO `core_rechargelog` VALUES (63, 'd187fe56b19db0a425bfd058521d5827effadf99b775ed656aa161937d382de4', 14547.00000000, 1, 'TRC20', 'USDT', '2025-05-15 02:44:39.708381', NULL);
INSERT INTO `core_rechargelog` VALUES (64, 'effdef59e421e3632acbabb132a55c1312a35f85873ff831448a1dafeb9693dd', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-15 21:00:25.985265', NULL);
INSERT INTO `core_rechargelog` VALUES (65, '34c2b03de77ef347164c94033892cd214d76d8f5ab375b1fa22ed34856d62d1d', 7.00000000, 1, 'TRC20', 'USDT', '2025-05-15 21:00:27.238183', NULL);
INSERT INTO `core_rechargelog` VALUES (66, '26a3c1a050ce40d71fef8afeb296036c03cb65ed42046ed31d83b8189b1c8e40', 18.94000000, 1, 'TRC20', 'USDT', '2025-05-15 21:00:29.162108', NULL);
INSERT INTO `core_rechargelog` VALUES (67, '60e77bcda5b413fdd2f8a5900b8447718d4461c2f2fd9d9d356fc4da268dcbd5', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-15 21:00:30.005075', NULL);
INSERT INTO `core_rechargelog` VALUES (68, '8f859d0c9c79f6c4d372a84a06e2b216c7f8ef1f8cb54b929ac12af9f9c1881c', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-15 21:00:30.853948', NULL);
INSERT INTO `core_rechargelog` VALUES (69, 'd8a79d82210e44e62567a3f0f5af5697001a442504ccb49260ee5b498c139964', 11668.00000000, 1, 'TRC20', 'USDT', '2025-05-15 21:00:32.121094', NULL);
INSERT INTO `core_rechargelog` VALUES (70, '965f177a719caf7d43498ac810db3897d273706602470e62c899e1bb05359e26', 1.00010000, 1, 'TRC20', 'USDT', '2025-05-15 21:00:32.967206', NULL);
INSERT INTO `core_rechargelog` VALUES (71, '2cc89c130f42000f551a4c3f155cd46774f7266a0768c6d5333bb6239e0b156c', 9.00000000, 1, 'TRC20', 'USDT', '2025-05-16 00:26:21.168990', NULL);
INSERT INTO `core_rechargelog` VALUES (72, '6ed93f400707d75aae34bf2d061bea5eae870905f6a7ebc83016049bfd8227c0', 86928.00000000, 1, 'TRC20', 'USDT', '2025-05-16 09:42:48.120043', NULL);
INSERT INTO `core_rechargelog` VALUES (73, 'ac2557faf60a3e034467b89f96a91c9eed1ef3ed958723459b57e8e8d69d6c38', 0.01000100, 1, 'TRC20', 'USDT', '2025-05-16 09:47:08.260425', NULL);
INSERT INTO `core_rechargelog` VALUES (74, '455c7edf61466df16f23d1c619c5cffa38b87e58ee65c6c5a596e5a995597287', 12110.00000000, 1, 'TRC20', 'USDT', '2025-05-16 09:53:06.852181', NULL);
INSERT INTO `core_rechargelog` VALUES (75, '29a01653f6a23d90ac20eac779f59b618f3d8afcb7f6a349a68e29892d89b1f3', 1230.00000000, 1, 'TRC20', 'USDT', '2025-05-16 13:15:45.007779', NULL);
INSERT INTO `core_rechargelog` VALUES (76, '6d196ac49f0a67767ab09289c7466a7340236f2f20550197be4f322f07b79c05', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-16 13:15:46.534950', NULL);
INSERT INTO `core_rechargelog` VALUES (77, '87032a3b113fb0481b49b5167be764fdb7776fe25298ad9565a1c93fa3a4f9c4', 4826.00000000, 1, 'TRC20', 'USDT', '2025-05-16 15:08:03.824920', NULL);
INSERT INTO `core_rechargelog` VALUES (78, 'b62ab2d6512775d5d085fa4b8c8bbaf781defd7c2d6eb3449d29bd3e175366e2', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-16 16:36:16.903649', NULL);
INSERT INTO `core_rechargelog` VALUES (79, '7957ffdf761b0405c7f7c2a3f03e8ddbef1385ed19c8e114d30e58e25f6a15d2', 15949.00000000, 1, 'TRC20', 'USDT', '2025-05-16 17:16:18.178063', NULL);
INSERT INTO `core_rechargelog` VALUES (80, 'cdccb88b490fb5162aa10e670098246178ec73a1cd987c5a9530f35bd2a7751c', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-16 17:51:49.044228', NULL);
INSERT INTO `core_rechargelog` VALUES (81, '91e692f2125f02045079e0e19e3ae8f0e2425acbac6d31c25ff65e2402e04fa1', 2.00000000, 1, 'TRC20', 'USDT', '2025-05-16 18:31:28.609014', NULL);
INSERT INTO `core_rechargelog` VALUES (82, '0dc7abb7143f3cf15fb448c372da07ba467156ef6c1d9efc20bb798c578d59cb', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-16 20:27:56.350214', NULL);
INSERT INTO `core_rechargelog` VALUES (83, 'fa05605b2876678a699b10019125262cd1f11684aeaa2f7554fccc5a5d8f8051', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-17 03:26:33.016200', NULL);
INSERT INTO `core_rechargelog` VALUES (84, 'b428d7a27b8979f53aaf5a7c247264514d28bb01078064f92326a9144f2af627', 14705.00000000, 1, 'TRC20', 'USDT', '2025-05-17 04:50:44.300222', NULL);
INSERT INTO `core_rechargelog` VALUES (85, 'b78d53a11f88a7b52b5c065e899dc51762babe16ca7c0af3d2306c2c4c848cb0', 0.03333300, 1, 'TRC20', 'USDT', '2025-05-17 05:46:35.200227', NULL);
INSERT INTO `core_rechargelog` VALUES (86, 'bb64bb6cb714217445c46be2f8dac294c5edbced0c553cc29935b20109ddf738', 9.00000000, 1, 'TRC20', 'USDT', '2025-05-17 07:38:59.227280', NULL);
INSERT INTO `core_rechargelog` VALUES (87, 'b8fa88e6ecc0536b243641576a10ed2764126d43ff9ae0b12f3fe9007601c9b0', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-17 09:06:58.853031', NULL);
INSERT INTO `core_rechargelog` VALUES (88, 'a157e6e9ef686fc1c0efa4f3865476561c211aae425e3578056640d678badae9', 1.00100000, 1, 'TRC20', 'USDT', '2025-05-17 09:30:31.894452', NULL);
INSERT INTO `core_rechargelog` VALUES (89, 'a52b143057ec74179fb8fd2a4f2933b11b3a3d3a869ae95057704e55986934a8', 0.01000100, 1, 'TRC20', 'USDT', '2025-05-17 11:08:09.415701', NULL);
INSERT INTO `core_rechargelog` VALUES (90, '9d3be993fa2da233cfb34f08115c8a284b4a091ef6bcb3a0090e893e64fad01d', 1.00100000, 1, 'TRC20', 'USDT', '2025-05-17 11:08:10.357223', NULL);
INSERT INTO `core_rechargelog` VALUES (91, '7a14cab53d6d928adf760fecfabe21dc5254056887e5b54a39174a4f09a38e79', 5.00000000, 1, 'TRC20', 'USDT', '2025-05-17 12:18:25.586796', NULL);
INSERT INTO `core_rechargelog` VALUES (92, '2398d455924c4b613b5e325af5aa99e984656597b9dba6ffacb07254946397bf', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-17 12:51:36.858541', NULL);
INSERT INTO `core_rechargelog` VALUES (93, '5ecbf1421d5737dc76ed8502d8683d8034553527bffb9ba27fce61d676e72313', 10.00000000, 1, 'TRC20', 'USDT', '2025-05-17 13:01:08.837377', NULL);
INSERT INTO `core_rechargelog` VALUES (94, 'd8463aba369c56e282c92598980c42d61dae7879182ff39ba1f9fb94604a3a81', 0.01000100, 1, 'TRC20', 'USDT', '2025-05-17 13:02:29.209880', NULL);
INSERT INTO `core_rechargelog` VALUES (95, '70e3f6be41429400197108e3301b2bf734eaeb4719dcaf7e904237244a90777c', 1.00000000, 1, 'TRC20', 'USDT', '2025-05-17 13:19:50.093735', NULL);
COMMIT;

-- ----------------------------
-- Table structure for core_telegramwatchaddress
-- ----------------------------
DROP TABLE IF EXISTS `core_telegramwatchaddress`;
CREATE TABLE `core_telegramwatchaddress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `chain_type` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_type` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `added_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_telegramwatchaddres_chat_id_address_chain_ty_b3c22c4a_uniq` (`chat_id`,`address`,`chain_type`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of core_telegramwatchaddress
-- ----------------------------
BEGIN;
INSERT INTO `core_telegramwatchaddress` VALUES (2, '6676637728', 'TAuovTf8MmV7jpNkPTsmDosnSLtdZDH8jC', 'trc20', 'USDT', '2025-05-11 16:32:05.487560');
INSERT INTO `core_telegramwatchaddress` VALUES (4, '893032849', 'TUrw4GNUUXBALhd8PMEXQChZrKsGbSnT9k', 'trc20', 'USDT', '2025-05-11 17:21:46.058723');
INSERT INTO `core_telegramwatchaddress` VALUES (5, '893032849', 'TAbRJ5n7XCMEVVYSv51MkpHSdyvj555555', 'trc20', 'USDT', '2025-05-11 17:22:46.974468');
INSERT INTO `core_telegramwatchaddress` VALUES (6, '6676637728', '0x742d35cc6634c0532925a3b844bc454e4438f44e', 'erc20', 'USDT', '2025-05-11 17:44:49.856721');
INSERT INTO `core_telegramwatchaddress` VALUES (7, '6676637728', '0x9f2d2c0e852fe940b2f9d37df063ea9b779326b7', 'erc20', NULL, '2025-05-11 17:51:55.679402');
INSERT INTO `core_telegramwatchaddress` VALUES (8, '6676637728', '0x73f7b1184b5cd361cc0f7654998953e2a251dd58', 'erc20', NULL, '2025-05-11 17:52:27.914707');
INSERT INTO `core_telegramwatchaddress` VALUES (9, '6676637728', '0xe58F13D7Abd63b4C6Ac83691c95e41e00A997c0E', 'erc20', NULL, '2025-05-11 18:00:29.269622');
INSERT INTO `core_telegramwatchaddress` VALUES (10, '6430173041', 'TTXq5yha4EX6pa2E3AmaLhkLgs9iVZShep', 'trc20', NULL, '2025-05-12 00:45:40.932725');
INSERT INTO `core_telegramwatchaddress` VALUES (11, '893032849', '0xa76af40062da3cee57c2a832a2741b1d4769d059', 'erc20', '', '2025-05-12 09:12:25.832748');
INSERT INTO `core_telegramwatchaddress` VALUES (12, '893032849', '0x95222290dd7278aa3ddd389cc1e1d165cc4bafe5', 'erc20', '', '2025-05-12 09:13:23.639006');
INSERT INTO `core_telegramwatchaddress` VALUES (13, '893032849', '0x7e2a2fa2a064f693f0a55c5639476d913ff12d05', 'erc20', '', '2025-05-12 09:13:49.524145');
INSERT INTO `core_telegramwatchaddress` VALUES (14, '893032849', 'TVpej6nnzURQ41gLi2aZhKbNrRmNX1yLpt', 'trc20', '', '2025-05-13 18:51:42.883235');
COMMIT;

-- ----------------------------
-- Table structure for core_walletaddress
-- ----------------------------
DROP TABLE IF EXISTS `core_walletaddress`;
CREATE TABLE `core_walletaddress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `private_key_encrypted` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `chain_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `address` (`address`),
  UNIQUE KEY `core_walletaddress_user_id_chain_type_token_type_42277bf5_uniq` (`user_id`,`chain_type`,`token_type`),
  CONSTRAINT `core_walletaddress_user_id_86cddcda_fk_core_platformuser_id` FOREIGN KEY (`user_id`) REFERENCES `core_platformuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of core_walletaddress
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (12, 'core', 'collectionlog');
INSERT INTO `django_content_type` VALUES (7, 'core', 'merchant');
INSERT INTO `django_content_type` VALUES (11, 'core', 'merchantcollectionaddress');
INSERT INTO `django_content_type` VALUES (8, 'core', 'platformuser');
INSERT INTO `django_content_type` VALUES (10, 'core', 'rechargelog');
INSERT INTO `django_content_type` VALUES (13, 'core', 'telegramwatchaddress');
INSERT INTO `django_content_type` VALUES (9, 'core', 'walletaddress');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-05-11 16:28:37.511211');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2025-05-11 16:28:37.662400');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2025-05-11 16:28:37.702189');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-05-11 16:28:37.707890');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-11 16:28:37.711984');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2025-05-11 16:28:37.741857');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2025-05-11 16:28:37.757231');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2025-05-11 16:28:37.766585');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2025-05-11 16:28:37.770669');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2025-05-11 16:28:37.784254');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2025-05-11 16:28:37.784760');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2025-05-11 16:28:37.788936');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2025-05-11 16:28:37.805226');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2025-05-11 16:28:37.818227');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2025-05-11 16:28:37.825966');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2025-05-11 16:28:37.829658');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2025-05-11 16:28:37.842885');
INSERT INTO `django_migrations` VALUES (18, 'core', '0001_initial', '2025-05-11 16:28:37.914913');
INSERT INTO `django_migrations` VALUES (19, 'core', '0002_collectionlog', '2025-05-11 16:28:37.929835');
INSERT INTO `django_migrations` VALUES (20, 'core', '0003_telegramwatchaddress', '2025-05-11 16:28:37.934567');
INSERT INTO `django_migrations` VALUES (21, 'core', '0004_rename_created_at_telegramwatchaddress_added_at_and_more', '2025-05-11 16:28:37.944859');
INSERT INTO `django_migrations` VALUES (22, 'sessions', '0001_initial', '2025-05-11 16:28:37.950720');
INSERT INTO `django_migrations` VALUES (23, 'core', '0005_alter_rechargelog_wallet', '2025-05-11 17:25:44.402262');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
