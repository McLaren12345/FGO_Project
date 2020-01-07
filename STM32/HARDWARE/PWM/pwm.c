#include "pwm.h"
//#include "led.h"
#include "usart.h"
#include "delay.h"
#include "rs485.h"
//////////////////////////////////////////////////////////////////////////////////	 
//本程序只供学习使用，未经作者许可，不得用于其它任何用途
//ALIENTEK STM32F407开发板
//定时器PWM 驱动代码	   
//正点原子@ALIENTEK
//技术论坛:www.openedv.com
//创建日期:2014/5/4
//版本：V1.0
//版权所有，盗版必究。
//Copyright(C) 广州市星翼电子科技有限公司 2014-2024
//All rights reserved									  
////////////////////////////////////////////////////////////////////////////////// 	 


//TIM1 PWM部分初始化 
//PWM输出初始化
//arr：自动重装值
//psc：时钟预分频数
void TIM1_PWM_Init(u32 arr,u32 psc)
{		 					 
	//此部分需手动修改IO口设置
	
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	TIM_OCInitTypeDef  TIM_OCInitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM1,ENABLE);  	//TIM1时钟使能    
	//RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE); 	//使能PORTA时钟，使用PA8，TIM1通道1	
	
	GPIO_PinAFConfig(GPIOA,GPIO_PinSource8,GPIO_AF_TIM1); //GPIOF9复用为定时器1
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_8;           //GPIOA8
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;        //复用功能
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;	//速度100MHz
	GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;      //推挽复用输出
	GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;        //上拉
	GPIO_Init(GPIOA,&GPIO_InitStructure);              //初始化PA8
	  
	TIM_TimeBaseStructure.TIM_Prescaler=psc;  //定时器分频
	TIM_TimeBaseStructure.TIM_CounterMode=TIM_CounterMode_Up; //向上计数模式
	TIM_TimeBaseStructure.TIM_Period=arr;   //自动重装载值
	TIM_TimeBaseStructure.TIM_ClockDivision=TIM_CKD_DIV1;
  TIM_TimeBaseStructure.TIM_RepetitionCounter=0;	
	
	TIM_TimeBaseInit(TIM1,&TIM_TimeBaseStructure);//初始化定时器1
	
	TIM_ClearFlag(TIM1, TIM_FLAG_Update);//清中断标志位
	TIM_ITConfig(TIM1,TIM_IT_Update|TIM_IT_Trigger,ENABLE);
	
	NVIC_InitStructure.NVIC_IRQChannel=TIM1_UP_TIM10_IRQn; //定时器3中断
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=0x00; //抢占优先级0
	NVIC_InitStructure.NVIC_IRQChannelSubPriority=0x01; //子优先级1
	NVIC_InitStructure.NVIC_IRQChannelCmd=ENABLE;
	NVIC_Init(&NVIC_InitStructure);
	
	//初始化TIM1 Channel1 PWM模式	 
	TIM_SelectOnePulseMode(TIM1,TIM_OPMode_Single);//单脉冲模式，每次更新自动清计数器
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM2; //选择定时器模式:TIM脉冲宽度调制模式2
 	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable; //比较输出使能
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_Low; //输出极性:TIM输出比较极性低
	TIM_OCInitStructure.TIM_Pulse = 400;//占空比20%
	TIM_OCInitStructure.TIM_OCIdleState = TIM_OCIdleState_Reset;
	TIM_OC1Init(TIM1, &TIM_OCInitStructure);  //根据T指定的参数初始化外设TIM1OC1
	
	TIM_CtrlPWMOutputs(TIM1,ENABLE);//使能TIM1PWM输出

	TIM_OC1PreloadConfig(TIM1, TIM_OCPreload_Enable);  //使能TIM1在CCR1上的预装载寄存器
 
  TIM_ARRPreloadConfig(TIM1,ENABLE);//ARPE使能 
	
	//TIM_Cmd(TIM1, ENABLE);  //使能TIM1 
										  
}  



//TIM8 PWM部分初始化 
//PWM输出初始化
//arr：自动重装值
//psc：时钟预分频数
void TIM8_PWM_Init(u32 arr,u32 psc)
{		 					 
	//此部分需手动修改IO口设置
	
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	TIM_OCInitTypeDef  TIM_OCInitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM8,ENABLE);  	//TIM8时钟使能    
	RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC, ENABLE); 	//使能PORTE时钟，使用PC6，TIM8通道1	
	
	GPIO_PinAFConfig(GPIOC,GPIO_PinSource6,GPIO_AF_TIM8); //GPIOC6复用为定时器14
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6;           //GPIOC6
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;        //复用功能
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;	//速度100MHz
	GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;      //推挽复用输出
	GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;        //上拉
	GPIO_Init(GPIOC,&GPIO_InitStructure);              //初始化PF9
	  
	TIM_TimeBaseStructure.TIM_Prescaler=psc;  //定时器分频
	TIM_TimeBaseStructure.TIM_CounterMode=TIM_CounterMode_Up; //向上计数模式
	TIM_TimeBaseStructure.TIM_Period=arr;   //自动重装载值
	TIM_TimeBaseStructure.TIM_ClockDivision=TIM_CKD_DIV1;
  TIM_TimeBaseStructure.TIM_RepetitionCounter=0;	
	
	TIM_TimeBaseInit(TIM8,&TIM_TimeBaseStructure);//初始化定时器8
	
	TIM_ClearFlag(TIM8, TIM_FLAG_Update);//清中断标志位
	TIM_ITConfig(TIM8,TIM_IT_Update|TIM_IT_Trigger,ENABLE);
	
	NVIC_InitStructure.NVIC_IRQChannel=TIM8_UP_TIM13_IRQn; //定时器3中断
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=0x00; //抢占优先级0
	NVIC_InitStructure.NVIC_IRQChannelSubPriority=0x02; //子优先级2
	NVIC_InitStructure.NVIC_IRQChannelCmd=ENABLE;
	NVIC_Init(&NVIC_InitStructure);
	
	//初始化TIM8 Channel1 PWM模式	 
	TIM_SelectOnePulseMode(TIM8,TIM_OPMode_Single);
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM2; //选择定时器模式:TIM脉冲宽度调制模式2
 	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable; //比较输出使能
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_Low; //输出极性:TIM输出比较极性低
	TIM_OCInitStructure.TIM_Pulse = 400;//占空比20%
	TIM_OCInitStructure.TIM_OCIdleState = TIM_OCIdleState_Reset;//不加这句PWM不会输出！！！
	TIM_OC1Init(TIM8, &TIM_OCInitStructure);  //根据T指定的参数初始化外设TIM8OC1
	
	TIM_CtrlPWMOutputs(TIM8,ENABLE);//使能TIM1PWM输出

	TIM_OC1PreloadConfig(TIM8, TIM_OCPreload_Enable);  //使能TIM8在CCR1上的预装载寄存器
 
  TIM_ARRPreloadConfig(TIM8,ENABLE);//ARPE使能 
	
	//TIM_Cmd(TIM1, ENABLE);  //使能TIM8
 										  
} 

//定义全局变量Old_Position用于记录上一个时刻电机的位置
u8 Old_x_Position = 0;
u8 Old_y_Position = 0;

u16 x_Pluse_num = 0;
u16 y_Pluse_num = 0;

u8 x_completeFlag = 0;
u8 y_completeFlag = 0;

//屏幕点击函数，控制镜头伸缩，当x，y的completeflag都为1时启用

void touch()
{
	 if((x_completeFlag==1)&(y_completeFlag==1)&(Old_x_Position==0)&(Old_y_Position==0))//电机归位时不点击
	 {
	   x_completeFlag = 0;	 
	   y_completeFlag = 0;
		 
		 GPIO_SetBits(GPIOG,GPIO_Pin_8);
		 while(USART_GetFlagStatus(USART2,USART_FLAG_TC)==RESET);
		 USART_SendData(USART2,0xFF);
		 while(USART_GetFlagStatus(USART2,USART_FLAG_TC)==RESET); //等待发送结束
		 GPIO_ResetBits(GPIOG,GPIO_Pin_8);
	 }
	 
   if((x_completeFlag==1)&(y_completeFlag==1)&((Old_x_Position!=0)|(Old_y_Position!=0)))//当xy电机都转到指定位置时开启照相机电机，由PA4、5控制
	 {
	   GPIO_SetBits(GPIOA,GPIO_Pin_5);//正转放出
     GPIO_ResetBits(GPIOA,GPIO_Pin_4);		 
	 	 
	   delay_ms(750);
	   GPIO_SetBits(GPIOA,GPIO_Pin_4);//反转收回
     GPIO_ResetBits(GPIOA,GPIO_Pin_5);
	   delay_ms(750);
	   GPIO_ResetBits(GPIOA,GPIO_Pin_4);	

     x_completeFlag = 0;	 
	   y_completeFlag = 0;
		 
		 GPIO_SetBits(GPIOG,GPIO_Pin_8);
		 while(USART_GetFlagStatus(USART2,USART_FLAG_TC)==RESET);
		 USART_SendData(USART2,0xFF);
		 while(USART_GetFlagStatus(USART2,USART_FLAG_TC)==RESET); //等待发送结束
		 GPIO_ResetBits(GPIOG,GPIO_Pin_8);
   }
}
//手机屏幕122*68mm
//x轴电机控制函数，步进电机每200个脉冲转一圈，丝杆螺距4mm
//该函数一次最多输出256个脉冲
void motor_x(u8 pluse_num)
{	
	TIM_SetCounter(TIM1,0);  //清除计数器
	TIM1->RCR=pluse_num;   //改变重复计数器的值
	x_Pluse_num-=(pluse_num+1);
  TIM_Cmd(TIM1, ENABLE);   //使能TIM1
}


//y轴电机控制函数，电机参数同上
void motor_y(u8 pluse_num)
{
  TIM_SetCounter(TIM8,0);  //清除计数器
	TIM8->RCR=pluse_num;   //改变重复计数器的值
	y_Pluse_num-=(pluse_num+1);
  TIM_Cmd(TIM8, ENABLE);   //使能TIM8
}

#define sub  8;  //定义细分值

//x轴电机方向由PB0控制，y轴电机方向由PB1控制
//函数返回相应的电机需要的脉冲数量
void motor_x_reversecontrol(u8 New_Postion)
{
if (New_Postion<Old_x_Position) 
 {
	GPIO_SetBits(GPIOB,GPIO_Pin_0);                           //反转时加一点脉冲作为丢步补偿
	x_Pluse_num = 50+244*(Old_x_Position-New_Postion)/4*sub;  //244是iphone6sp屏幕高度的2倍，单位毫米
	Old_x_Position =  New_Postion;
 }
else
 {
	GPIO_ResetBits(GPIOB,GPIO_Pin_0);
	x_Pluse_num = 244*(New_Postion-Old_x_Position)/4*sub;
	Old_x_Position =  New_Postion;
 }
}

void motor_y_reversecontrol(u8 New_Postion)
{
if (New_Postion<Old_y_Position) 
 {
	GPIO_SetBits(GPIOB,GPIO_Pin_1);
	y_Pluse_num = 40+136*(Old_y_Position-New_Postion)/4*sub;   //136是iphone6sp屏幕宽度的2倍，单位毫米
	Old_y_Position =  New_Postion;
 }
else
 {
	GPIO_ResetBits(GPIOB,GPIO_Pin_1);
	y_Pluse_num = 136*(New_Postion-Old_y_Position)/4*sub;
	Old_y_Position =  New_Postion;
 }
}



void move_xy(u8 x_position, u8 y_position)
{
			motor_x_reversecontrol(x_position);
			motor_y_reversecontrol(y_position);
	
	    x_completeFlag = 0;	 
	    y_completeFlag = 0;
	
	    if((x_position==0)&(y_position==0))    //复位时补偿800个脉冲，保证完全回到原点
			{
				  GPIO_SetBits(GPIOB,GPIO_Pin_0);
				  GPIO_SetBits(GPIOB,GPIO_Pin_1);
			    x_Pluse_num+=850;
				  y_Pluse_num+=800;
			}
	
	    delay_ms(50);

		if(x_Pluse_num>0)
		{
			TIM_SetAutoreload(TIM1,1200-1);//启动频率800Hz，之后在中断里改为2kHZ
			
		  if(x_Pluse_num<=30)            //发30个脉冲作为启动脉冲
			{
        motor_x(x_Pluse_num-1);
			}
			else
			{
			  motor_x(29);
			}
		}
			
		if(y_Pluse_num>0)
		{
			TIM_SetAutoreload(TIM8,1200-1);
			
		  if(y_Pluse_num<=30)
			{
        motor_y(y_Pluse_num-1);
			}
			else
			{
			  motor_y(29);
			}
		}
		
		if(x_Pluse_num==0)//如果不需要电机转动则完成标志位直接置1
			x_completeFlag=1;
		
		if(y_Pluse_num==0)
			y_completeFlag=1;


}


//中断函数:当电机转到相应位置时（即PWM波完全输出后）关闭定时器
void TIM1_UP_TIM10_IRQHandler(void)
{
	if (TIM_GetITStatus(TIM1, TIM_IT_Update) != RESET)//检查指定的TIM中断发生与否:TIM 中断源 
	{
		TIM_ClearITPendingBit(TIM1, TIM_IT_Update);//清除TIMx的中断待处理位:TIM 中断源 
    TIM_Cmd(TIM1, DISABLE);
		
		
			if(x_Pluse_num>0)
		{
			TIM_SetAutoreload(TIM1,450-1);
		  if(x_Pluse_num<=256)
			{
        motor_x(x_Pluse_num-1);
			}
			else
			{
			  motor_x(255);
			}
		}
		
		if(x_Pluse_num==0)
		  x_completeFlag = 1;	
  }
}

void TIM8_UP_TIM13_IRQHandler()
{
	if (TIM_GetITStatus(TIM8, TIM_IT_Update) != RESET)//检查指定的TIM中断发生与否:TIM 中断源 
	{
		TIM_ClearITPendingBit(TIM8, TIM_IT_Update);//清除TIMx的中断待处理位:TIM 中断源 
    TIM_Cmd(TIM8, DISABLE);
		
		
			if(y_Pluse_num>0)
		{
			TIM_SetAutoreload(TIM8,500-1);
		  if(y_Pluse_num<=256)
			{
        motor_y(y_Pluse_num-1);
			}
			else
			{
			  motor_y(255);
			}
		}
		if(y_Pluse_num==0)
		  y_completeFlag = 1;	
  }
}

