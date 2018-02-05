create database hospital DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

use hospital;

CREATE TABLE IF NOT EXISTS `hospital_history_user` (
  `hospital_user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `hospital_user` varchar(50) COMMENT '用户帐号',
  `hospital_name` varchar(50) COMMENT '用户姓名',
  `hospital_user_tired` varchar(10) COMMENT '用户疲劳感',
  `hospital_user_temperature` varchar(10) COMMENT '用户体温',  
  `hospital_user_respire` varchar(10) COMMENT '用户呼吸',  
  `hospital_user_heart` varchar(10) COMMENT '用户心跳', 
  `hospital_user_stomach` varchar(10) COMMENT '用户胃部', 
  `hospital_user_shit` varchar(10) COMMENT '用户大便', 
  PRIMARY KEY (`hospital_user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='历史用户表' AUTO_INCREMENT=1;

CREATE TABLE IF NOT EXISTS `hospital_current_user` (  
  `hospital_user` varchar(50) NOT NULL COMMENT '用户帐号',
  `hospital_name` varchar(50) COMMENT '用户姓名',
  `hospital_user_tired` varchar(10) COMMENT '用户疲劳感',
  `hospital_user_temperature` varchar(10) COMMENT '用户体温',  
  `hospital_user_respire` varchar(10) COMMENT '用户呼吸',  
  `hospital_user_heart` varchar(10) COMMENT '用户心跳', 
  `hospital_user_stomach` varchar(10) COMMENT '用户胃部', 
  `hospital_user_shit` varchar(10) COMMENT '用户大便', 
  `hospital_user_prevAsk` varchar(50) COMMENT '用户之前提的问题', 
  PRIMARY KEY (`hospital_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='当前用户表';

insert into hospital_current_user(hospital_user, hospital_name, hospital_user_tired, hospital_user_temperature, hospital_user_respire, hospital_user_heart, hospital_user_stomach, hospital_user_shit, hospital_user_prevAsk) values('currentUser', '临时用户', '-1', '-1', '-1', '-1', '-1', '-1', '-1');
