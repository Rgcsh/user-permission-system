/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : userpermission

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2018-10-25 16:49:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for acticle
-- ----------------------------
DROP TABLE IF EXISTS `acticle`;
CREATE TABLE `acticle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL COMMENT '外键,指向user.id',
  `role_type` int(11) NOT NULL COMMENT '用户权限,冗余字段',
  `content` varchar(256) NOT NULL COMMENT '文章内容',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `status` tinyint(4) DEFAULT '1' COMMENT '文章状态',
  PRIMARY KEY (`id`),
  KEY `index_uid` (`uid`),
  KEY `index_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of acticle
-- ----------------------------
INSERT INTO `acticle` VALUES ('1', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 13:48:26', null, '2');
INSERT INTO `acticle` VALUES ('2', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 13:50:26', null, '2');
INSERT INTO `acticle` VALUES ('3', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 13:51:19', null, '1');
INSERT INTO `acticle` VALUES ('4', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 13:52:36', null, '1');
INSERT INTO `acticle` VALUES ('5', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 13:53:12', null, '1');
INSERT INTO `acticle` VALUES ('6', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 13:53:27', null, '1');
INSERT INTO `acticle` VALUES ('7', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 13:55:13', null, '1');
INSERT INTO `acticle` VALUES ('8', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 13:56:57', null, '1');
INSERT INTO `acticle` VALUES ('9', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 14:02:05', '2018-10-25 14:02:07', '1');
INSERT INTO `acticle` VALUES ('10', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 15:11:10', null, '1');
INSERT INTO `acticle` VALUES ('11', '1', '2', '你好啊啊啊 啊啊！！！！！！', '2018-10-25 15:17:24', null, '1');
INSERT INTO `acticle` VALUES ('12', '1', '2', '您好，面试官，非常感谢您给我这次机会', '2018-10-25 15:17:24', null, '1');
INSERT INTO `acticle` VALUES ('13', '2', '1', '如果有幸进入贵公司，我会努力工作，为公司创造尽可能多的价值', '2018-10-25 15:25:34', null, '1');
INSERT INTO `acticle` VALUES ('14', '2', '1', '我所居住的地方离贵公司只有半小时的距离', '2018-10-25 15:25:34', null, '1');
INSERT INTO `acticle` VALUES ('15', '2', '1', '管理员发布的文章12', '2018-10-25 15:25:34', null, '1');
INSERT INTO `acticle` VALUES ('16', '2', '1', '管理员发布的文章123', '2018-10-25 15:25:34', null, '1');
INSERT INTO `acticle` VALUES ('17', '2', '1', '管理员发布的文章1234', '2018-10-25 15:25:34', null, '1');
INSERT INTO `acticle` VALUES ('18', '2', '1', '管理员发布的文章123453', '2018-10-25 15:25:34', null, '1');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(256) NOT NULL COMMENT '密码',
  `mobile` varchar(64) DEFAULT NULL COMMENT '手机号',
  `role_type` int(11) NOT NULL COMMENT '用户权限1:admin 2:user',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'e10adc3949ba59abbe56e057f20f883e', '17621032219', '2', '2018-10-25 13:00:11');
INSERT INTO `user` VALUES ('2', 'e10adc3949ba59abbe56e057f20f883e', '17621032218', '1', '2018-10-25 13:02:53');
INSERT INTO `user` VALUES ('3', 'e10adc3949ba59abbe56e057f20f883e', '17621032211', '1', '2018-10-25 15:11:10');
INSERT INTO `user` VALUES ('4', 'e10adc3949ba59abbe56e057f20f883e', '17621032217', '2', '2018-10-25 15:17:24');
