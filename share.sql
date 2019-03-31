/*
 Navicat Premium Data Transfer

 Source Server         : 腾讯云
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : 193.112.43.41:3306
 Source Schema         : share

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 31/03/2019 15:26:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pwd` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_super` smallint(6) NULL DEFAULT NULL,
  `role_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  INDEX `ix_admin_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 'admin', 'pbkdf2:sha256:50000$0gSDR3pY$b8187a3b2fb6efcaf1a7d89cf2c0b2dfa3e827113e063b31841e2552af2ffbcb', 0, 1, '2018-02-04 12:10:57');
INSERT INTO `admin` VALUES (2, 'Devil', 'pbkdf2:sha256:50000$c2l8Hv51$2bc027ba6924b8e18e691ad6549ba086b3bd3b056ab4ebe669e3d3753fe67ad6', 0, 1, '2018-02-04 12:12:40');
INSERT INTO `admin` VALUES (3, 'JS_chen', 'pbkdf2:sha256:50000$yrdGTlUN$55e987e662a254beb735c776b787706f39bc3ed9ba3ef5d0903f5408e5c92a85', 1, 2, '2018-02-05 15:00:37');

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `admin_id`(`admin_id`) USING BTREE,
  INDEX `ix_adminlog_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of adminlog
-- ----------------------------
INSERT INTO `adminlog` VALUES (1, 1, '127.0.0.1', '2018-02-04 12:27:56');
INSERT INTO `adminlog` VALUES (2, 1, '127.0.0.1', '2018-02-04 16:28:22');
INSERT INTO `adminlog` VALUES (3, 1, '127.0.0.1', '2018-02-04 16:48:53');
INSERT INTO `adminlog` VALUES (4, 1, '127.0.0.1', '2018-02-04 16:49:45');
INSERT INTO `adminlog` VALUES (5, 1, '127.0.0.1', '2018-02-04 16:50:38');
INSERT INTO `adminlog` VALUES (6, 1, '127.0.0.1', '2018-02-08 14:52:11');
INSERT INTO `adminlog` VALUES (7, 2, '127.0.0.1', '2018-02-09 15:16:52');
INSERT INTO `adminlog` VALUES (8, 1, '127.0.0.1', '2018-02-28 15:19:35');
INSERT INTO `adminlog` VALUES (9, 1, '127.0.0.1', '2018-03-06 15:32:15');
INSERT INTO `adminlog` VALUES (10, 1, '127.0.0.1', '2018-06-24 14:58:35');
INSERT INTO `adminlog` VALUES (11, 2, '127.0.0.1', '2018-06-24 17:36:09');

-- ----------------------------
-- Table structure for adminoplog
-- ----------------------------
DROP TABLE IF EXISTS `adminoplog`;
CREATE TABLE `adminoplog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `reason` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `admin_id`(`admin_id`) USING BTREE,
  INDEX `ix_adminoplog_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `adminoplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of adminoplog
-- ----------------------------
INSERT INTO `adminoplog` VALUES (1, 1, '127.0.0.1', '修改了密码', '2018-02-04 16:50:23');
INSERT INTO `adminoplog` VALUES (2, 1, '127.0.0.1', '添加了一个角色：admin→系统维护员', '2018-02-05 15:17:27');
INSERT INTO `adminoplog` VALUES (3, 1, '127.0.0.1', '修改了权限：admin→超级管理员→/admin/：超级管理员→/admin/', '2018-02-05 15:41:17');
INSERT INTO `adminoplog` VALUES (4, 1, '127.0.0.1', '修改了权限：admin→超级管理员→/admin/：超级管理员→/admin/', '2018-02-05 15:55:56');
INSERT INTO `adminoplog` VALUES (5, 1, '127.0.0.1', '修改了权限：admin→超级管理员→/admin/：超级管理员→/admin/', '2018-02-05 15:56:21');
INSERT INTO `adminoplog` VALUES (6, 1, '127.0.0.1', '修改了权限：admin→超级管理员→/admin/auth/list/1：超级管理员→/admin/auth/list/1', '2018-02-05 15:56:51');
INSERT INTO `adminoplog` VALUES (7, 1, '127.0.0.1', '修改了权限：admin→超级管理员→/admin/：超级管理员→/admin/', '2018-02-05 15:57:07');
INSERT INTO `adminoplog` VALUES (8, 1, '127.0.0.1', '添加了权限：admin→添加管理员→/admin/admin/add/', '2018-02-05 15:58:27');
INSERT INTO `adminoplog` VALUES (9, 1, '127.0.0.1', '添加了权限：admin→添加角色→/admin/role/add/', '2018-02-05 15:59:18');
INSERT INTO `adminoplog` VALUES (10, 1, '127.0.0.1', '删除了一个权限：admin→添加角色', '2018-02-05 15:59:23');
INSERT INTO `adminoplog` VALUES (11, 1, '127.0.0.1', '冻结了一个会员：Devil', '2018-02-08 15:33:02');
INSERT INTO `adminoplog` VALUES (12, 1, '127.0.0.1', '解冻了一个会员：Devil', '2018-02-08 15:33:07');
INSERT INTO `adminoplog` VALUES (13, 1, '127.0.0.1', '解冻了一个会员：Devil', '2018-02-08 15:33:33');
INSERT INTO `adminoplog` VALUES (14, 2, '127.0.0.1', '删除了一个会员：share', '2018-02-09 15:51:09');
INSERT INTO `adminoplog` VALUES (15, 2, '127.0.0.1', '删除了一个会员：share', '2018-02-09 15:53:50');
INSERT INTO `adminoplog` VALUES (16, 2, '127.0.0.1', '删除了一个会员：home', '2018-02-09 16:21:02');
INSERT INTO `adminoplog` VALUES (17, 1, '127.0.0.1', '添加了一个链接类型：迅雷磁力', '2018-03-06 15:36:34');
INSERT INTO `adminoplog` VALUES (18, 1, '127.0.0.1', '添加了一个链接类型：百度网盘', '2018-03-06 15:37:39');
INSERT INTO `adminoplog` VALUES (19, 1, '127.0.0.1', '添加了一个链接类型：腾讯微盘', '2018-03-06 15:37:51');
INSERT INTO `adminoplog` VALUES (20, 1, '127.0.0.1', '添加了一个链接类型：新浪微盘', '2018-03-06 15:38:04');
INSERT INTO `adminoplog` VALUES (21, 1, '127.0.0.1', '添加了一个标签：- -选择- -', '2018-03-06 15:59:41');
INSERT INTO `adminoplog` VALUES (22, 1, '127.0.0.1', '添加了一个标签：电影', '2018-03-06 15:59:51');
INSERT INTO `adminoplog` VALUES (23, 1, '127.0.0.1', '添加了一个标签：IT资源', '2018-03-06 15:59:59');

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('4a846569cd01');

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `ix_auth_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES (1, '超级管理员', '/admin/', '2018-02-05 15:05:10');
INSERT INTO `auth` VALUES (2, '添加管理员', '/admin/admin/add/', '2018-02-05 15:58:27');

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `resource_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `resource_id`(`resource_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_comment_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`resource_id`) REFERENCES `resource` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for followers
-- ----------------------------
DROP TABLE IF EXISTS `followers`;
CREATE TABLE `followers`  (
  `follower_id` int(11) NULL DEFAULT NULL,
  `followed_id` int(11) NULL DEFAULT NULL,
  INDEX `followed_id`(`followed_id`) USING BTREE,
  INDEX `follower_id`(`follower_id`) USING BTREE,
  CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of followers
-- ----------------------------
INSERT INTO `followers` VALUES (2, 1);
INSERT INTO `followers` VALUES (1, 2);
INSERT INTO `followers` VALUES (5, 1);

-- ----------------------------
-- Table structure for link
-- ----------------------------
DROP TABLE IF EXISTS `link`;
CREATE TABLE `link`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_link_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of link
-- ----------------------------
INSERT INTO `link` VALUES (1, '- -选择- -', '2018-03-06 15:51:09');
INSERT INTO `link` VALUES (2, '迅雷磁力', '2018-03-06 15:36:34');
INSERT INTO `link` VALUES (3, '百度网盘', '2018-03-06 15:37:39');
INSERT INTO `link` VALUES (4, '腾讯微盘', '2018-03-06 15:37:51');
INSERT INTO `link` VALUES (5, '新浪微盘', '2018-03-06 15:38:04');

-- ----------------------------
-- Table structure for resource
-- ----------------------------
DROP TABLE IF EXISTS `resource`;
CREATE TABLE `resource`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `tag_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  `link_id` int(11) NULL DEFAULT NULL,
  `img_url` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url_info` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE,
  UNIQUE INDEX `url`(`url`) USING BTREE,
  INDEX `tag_id`(`tag_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_resource_addtime`(`addtime`) USING BTREE,
  INDEX `link_id`(`link_id`) USING BTREE,
  CONSTRAINT `resource_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `resource_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `resource_ibfk_3` FOREIGN KEY (`link_id`) REFERENCES `link` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resource
-- ----------------------------
INSERT INTO `resource` VALUES (4, '红海行动[DVD版]', 'http://dl102.80s.com.co:999/1802/红h行动[DVD版]/红h行动[DVD版]_bd.mp4', 2, 1, '2018-03-07 16:35:17', 2, '2018-03/201803071635163dabc28a34a44c0495761f103566d235.jpg', '');
INSERT INTO `resource` VALUES (5, '抓妖记2[DVD版]', 'http://dl105.80s.com.co:999/1803/zyj2[DVD版]v2/zyj2[DVD版]v2_bd.mp4', 2, 1, '2018-03-07 16:50:26', 2, '2018-03/20180307165025b74d7e77c2304d1f85c29466a4ef1aeb.jpg', '');
INSERT INTO `resource` VALUES (6, '唐人街探案2[高清DVD版]', 'http://dl106.80s.com.co:999/1803/唐rjt案2[高清DVD版]/唐rjt案2[高清DVD版]_bd.mp4', 2, 1, '2018-03-09 14:38:25', 2, '2018-03/201803091438254cec76969c214b51a1f6c78aa23a20ff.jpg,2018-03/2018030914382587507b5947234a199ce62b63dea7c3e6.jpg', '');
INSERT INTO `resource` VALUES (7, '西游记女儿国[DVD版]', 'http://dl102.80s.com.co:999/1802/西y记n儿国[DVD版]/西y记n儿国[DVD版].mp4', 2, 2, '2018-03-10 20:07:41', 2, '2018-03/20180310200740a7614d0155fc47ebabc133e94172ef3f.jpg', '');
INSERT INTO `resource` VALUES (8, '勇敢者游戏：决战丛林', 'http://dl105.80s.com.co:999/1803/勇gz游x：决zc林/勇gz游x：决zc林.mp4', 2, 1, '2018-03-16 18:06:13', 2, '2018-03/2018031819441247ad0cb3b94e4f269a2b377ee5faa94e.jpg,2018-03/2018031819480742ba7b31f72a42438b669caf03fb720a.jpg,2018-03/20180318194832c1054d92834b495fa84ec66e1e3db598.jpg', '');
INSERT INTO `resource` VALUES (9, '移动迷宫3：死亡解药[DVD版]', 'http://dl107.80s.com.co:999/1803/移dmg3：sw解y[DVD版]v2/移dmg3：sw解y[DVD版]v2_bd.mp4', 2, 1, '2018-03-16 18:08:28', 2, '2018-03/201803161808275698cd040fca4fcaa2690f8a275e1278.jpg,2018-03/201803201522248798ef4848e34ba2a326d046bc951f4b.jpg', '');
INSERT INTO `resource` VALUES (10, '湮灭', 'http://dl174.80s.im:920/1803/湮灭/湮灭.mp4', 2, 1, '2018-03-18 16:09:23', 2, '2018-03/20180318193810fd6dab59ffde495c9b867d7374d9ab39.jpg,2018-03/20180318193810e3b5b229ca7f4f67adeb7005bcd464e9.jpg', '');
INSERT INTO `resource` VALUES (11, '齐天大圣·万妖之城', 'http://dl177.80s.im:920/1803/齐天大圣·万妖之城/齐天大圣·万妖之城.mp4', 2, 1, '2018-03-20 16:09:48', 2, '2018-03/2018032016121414336f5fede641f3af60ad29570d71ce.jpg', '');
INSERT INTO `resource` VALUES (12, '水形物语', 'http://dl175.80s.im:920/1803/[水形物语]BD中英双字/[水形物语]BD中英双字.mp4', 2, 1, '2018-03-20 16:16:15', 2, '2018-03/20180320162536bc8d9d2a4ced43dc8c39f9bb473315fc.jpg', '');
INSERT INTO `resource` VALUES (13, '星球大战8：最后的绝地武士', 'http://dl174.80s.im:920/1803/星球大战8：最后的绝地武士/星球大战8：最后的绝地武士.mp4', 2, 1, '2018-03-20 16:28:09', 2, '2018-03/20180320162942bfbbbb340e984233b0bee2b98531e289.jpg', '');
INSERT INTO `resource` VALUES (14, '环太平洋2：雷霆再起', 'http://dl167.80s.im:920/1801/[环太平洋2：雷霆再起]预告片/[环太平洋2：雷霆再起]预告片_hd.mp4', 2, 1, '2018-03-20 16:31:09', 2, '2018-03/201803201645394ab96bd99fe44b2fbbcbbda322bb1719.jpg', '');
INSERT INTO `resource` VALUES (15, '古墓丽影：源起之战', 'http://dl171.80s.im:920/1802/[古墓丽影：源起之战]中文版正式预告/[古墓丽影：源起之战]中文版正式预告_hd.mp4', 2, 1, '2018-03-20 16:47:14', 2, '2018-03/201803201651068315a9421b474d2e812fe0d5ad635e1f.jpg', '');
INSERT INTO `resource` VALUES (16, '公牛历险记', 'http://dl176.80s.im:920/1803/[公牛历险记]BD国语/[公牛历险记]BD国语.mp4', 2, 1, '2018-03-20 16:53:51', 2, '2018-03/20180320165441c53ce1a7cf284aad94a7ac97400b87f4.jpg', '');

-- ----------------------------
-- Table structure for resourcecol
-- ----------------------------
DROP TABLE IF EXISTS `resourcecol`;
CREATE TABLE `resourcecol`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resource_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `resource_id`(`resource_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_resourcecol_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `resourcecol_ibfk_1` FOREIGN KEY (`resource_id`) REFERENCES `resource` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `resourcecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `auths` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `ix_role_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, '超级管理员', '1', '2018-02-04 12:11:35');
INSERT INTO `role` VALUES (2, '普通管理员', '1', '2018-02-05 14:57:19');
INSERT INTO `role` VALUES (3, '系统维护员', '1', '2018-02-05 15:17:27');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_tag_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES (1, '- -选择- -', '2018-03-06 15:59:40');
INSERT INTO `tag` VALUES (2, '电影', '2018-03-06 15:59:51');
INSERT INTO `tag` VALUES (3, 'IT资源', '2018-03-06 15:59:59');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pwd` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `info` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `face` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  `uuid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE,
  UNIQUE INDEX `face`(`face`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  UNIQUE INDEX `phone`(`phone`) USING BTREE,
  UNIQUE INDEX `uuid`(`uuid`) USING BTREE,
  INDEX `ix_user_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'Devil', 'pbkdf2:sha256:50000$HgxoTbpr$e4defa2a7f68e5f85b535fc9c243a9d07d17c819b44d3cceb068808837b7be25', '1062933783@qq.com', '13126051483', '哈哈', '20180210145935651814261af14c48901c6cb23169a6c8.jpg', '2018-02-08 14:53:36', '93f0011e63db4287be290379d3e1b320', 1);
INSERT INTO `user` VALUES (2, 'JS_chen', 'pbkdf2:sha256:50000$KQ0UG0ta$dd84f411436b98a5267712158bf91556ae58ef0a0499b1b8609f7b8a4640e460', '123456@qq.com', '13126051488', 'hahah', '2018031020061592771c83daf14818a65bce5f86e5e94f.jpg', '2018-02-08 15:27:48', 'aab0dd8f841b46f59dfe6bdedc94cde1', 1);
INSERT INTO `user` VALUES (5, 'share', 'pbkdf2:sha256:50000$k7lmn50I$4f30a83323bf200e45b6cd77ee18f745db7763fd5ea5bc39dc19d6587dd3d88e', '106394@qq.com', '13126051678', NULL, NULL, '2018-02-09 15:54:47', 'a15987e27f07427f9e46ae6109a1767a', 1);
INSERT INTO `user` VALUES (6, 'share_1', 'pbkdf2:sha256:50000$6mpnIwzS$dedc9dded6bc51120b37bc99eb06a71535263087fb249181bcb333466989f688', '1234375637@qq.com', '13126051975', NULL, NULL, '2018-02-09 16:01:11', 'c3412a8677994e19adf1c403aa63dcaf', 1);
INSERT INTO `user` VALUES (7, 'share_2', 'pbkdf2:sha256:50000$isZCQ0Ad$3e94744812799ed13768d821e5319348464e2fbd494598b6a68efbfdde1bfc09', '642324@qq.com', '13126052456', NULL, NULL, '2018-02-09 16:03:51', 'ef5cb2f9133a437e89f3e4eb8f24a337', 1);
INSERT INTO `user` VALUES (8, 'share_3', 'pbkdf2:sha256:50000$lyA13nBP$2039da8f85e1ae1c24534abab93a4a78c550280d2fe29b872568737ccb06f688', '2435456464@qq.com', '13122051483', NULL, NULL, '2018-02-09 16:05:50', 'ff105047378b4a77a4f6c1f280c41b96', 1);
INSERT INTO `user` VALUES (9, 'share_4', 'pbkdf2:sha256:50000$bUyXMnpt$7d7082a92fbc775bbf761d05e482fc7a3fb8aeabc5dc06906d9c8fc0d703a00c', '123754@qq.com', '13126051443', NULL, NULL, '2018-02-09 16:08:11', '2e4283f371524436a0dc22d731d241d9', 1);
INSERT INTO `user` VALUES (10, 'share_5', 'pbkdf2:sha256:50000$fu8dbxEf$a5ef7ba830819f452454f3f0d70843e8ccce829dcad5960b157165849915af3e', '123535@qq.com', '13126341483', NULL, NULL, '2018-02-09 16:10:10', '464540a073d14783a9dc803c46b22abb', 1);
INSERT INTO `user` VALUES (12, 'home', 'pbkdf2:sha256:50000$bWb90qfr$c2864af08551108a2a4c3f83f176f3451daaa4be1e2441057babe2647f7e9cec', '4573857@163.com', '13126951483', NULL, NULL, '2018-02-09 16:35:37', '521fabbd394644ef9a260ffca60e4c77', 1);

-- ----------------------------
-- Table structure for userlog
-- ----------------------------
DROP TABLE IF EXISTS `userlog`;
CREATE TABLE `userlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_userlog_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userlog
-- ----------------------------
INSERT INTO `userlog` VALUES (1, 1, '127.0.0.1', '2018-02-08 15:36:45');
INSERT INTO `userlog` VALUES (2, 2, '127.0.0.1', '2018-02-08 15:38:50');
INSERT INTO `userlog` VALUES (3, 1, '127.0.0.1', '2018-02-08 16:02:44');
INSERT INTO `userlog` VALUES (4, 1, '127.0.0.1', '2018-02-09 15:16:17');
INSERT INTO `userlog` VALUES (5, 1, '127.0.0.1', '2018-02-09 16:11:03');
INSERT INTO `userlog` VALUES (6, 1, '127.0.0.1', '2018-02-09 16:12:46');
INSERT INTO `userlog` VALUES (7, 1, '127.0.0.1', '2018-02-09 16:32:13');
INSERT INTO `userlog` VALUES (8, 1, '127.0.0.1', '2018-02-09 16:32:38');
INSERT INTO `userlog` VALUES (9, 12, '127.0.0.1', '2018-02-09 16:35:59');
INSERT INTO `userlog` VALUES (10, 1, '127.0.0.1', '2018-02-09 17:47:33');
INSERT INTO `userlog` VALUES (11, 6, '127.0.0.1', '2018-02-09 17:47:52');
INSERT INTO `userlog` VALUES (12, 1, '127.0.0.1', '2018-02-10 14:31:26');
INSERT INTO `userlog` VALUES (13, 1, '127.0.0.1', '2018-02-23 13:29:55');
INSERT INTO `userlog` VALUES (14, 1, '127.0.0.1', '2018-03-07 15:53:45');
INSERT INTO `userlog` VALUES (15, 1, '127.0.0.1', '2018-03-09 14:25:46');
INSERT INTO `userlog` VALUES (16, 2, '127.0.0.1', '2018-03-10 15:45:58');
INSERT INTO `userlog` VALUES (17, 1, '127.0.0.1', '2018-03-13 15:58:02');
INSERT INTO `userlog` VALUES (18, 1, '127.0.0.1', '2018-03-15 15:05:12');
INSERT INTO `userlog` VALUES (19, 1, '127.0.0.1', '2018-03-16 15:06:02');
INSERT INTO `userlog` VALUES (20, 1, '127.0.0.1', '2018-03-17 15:01:43');
INSERT INTO `userlog` VALUES (21, 1, '127.0.0.1', '2018-03-18 15:55:08');
INSERT INTO `userlog` VALUES (22, 1, '127.0.0.1', '2018-03-20 15:09:56');
INSERT INTO `userlog` VALUES (23, 1, '127.0.0.1', '2018-03-24 16:02:26');
INSERT INTO `userlog` VALUES (24, 1, '127.0.0.1', '2018-06-24 14:50:09');
INSERT INTO `userlog` VALUES (25, 1, '127.0.0.1', '2018-06-24 14:54:24');
INSERT INTO `userlog` VALUES (26, 1, '127.0.0.1', '2018-06-24 14:57:39');
INSERT INTO `userlog` VALUES (27, 1, '127.0.0.1', '2018-06-24 14:59:28');
INSERT INTO `userlog` VALUES (28, 1, '127.0.0.1', '2018-06-24 15:02:11');
INSERT INTO `userlog` VALUES (29, 5, '127.0.0.1', '2018-06-24 15:03:57');
INSERT INTO `userlog` VALUES (30, 5, '127.0.0.1', '2018-06-24 15:04:27');
INSERT INTO `userlog` VALUES (31, 5, '127.0.0.1', '2018-06-24 17:37:05');
INSERT INTO `userlog` VALUES (32, 5, '127.0.0.1', '2018-06-25 09:06:55');
INSERT INTO `userlog` VALUES (33, 5, '127.0.0.1', '2018-06-29 17:57:38');

-- ----------------------------
-- Table structure for useroplog
-- ----------------------------
DROP TABLE IF EXISTS `useroplog`;
CREATE TABLE `useroplog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `reason` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_useroplog_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `useroplog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
