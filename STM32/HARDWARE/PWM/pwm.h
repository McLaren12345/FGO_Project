#ifndef _TIMER_H
#define _TIMER_H
#include "sys.h"
//////////////////////////////////////////////////////////////////////////////////	 
//本程序只供学习使用，未经作者许可，不得用于其它任何用途
//ALIENTEK STM32F407开发板
//定时器 驱动代码	   
//正点原子@ALIENTEK
//技术论坛:www.openedv.com
//创建日期:2014/6/16
//版本：V1.0
//版权所有，盗版必究。
//Copyright(C) 广州市星翼电子科技有限公司 2014-2024
//All rights reserved									  
////////////////////////////////////////////////////////////////////////////////// 	

void TIM1_PWM_Init(u32 arr,u32 psc);
void TIM8_PWM_Init(u32 arr,u32 psc);

void motor_x(u8 pluse_num);
void motor_y(u8 pluse_num);
void touch(void);

void motor_x_reversecontrol(u8 New_Postion);
void motor_y_reversecontrol(u8 New_Postion);

void move_xy(u8 x_position, u8 y_position);

//extern u16 x_Pluse_num;
//extern u16 y_Pluse_num;
//extern u8 x_completeFlag;
//extern u8 y_completeFlag;
#endif
