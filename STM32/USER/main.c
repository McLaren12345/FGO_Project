#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "led.h"
#include "pwm.h"
#include "rs485.h"
#include "key.h"
#include "exti.h"

//ALIENTEK ̽����STM32F407������ ʵ��9
//PWM���ʵ��-�⺯���汾
//����֧�֣�www.openedv.com
//�Ա����̣�http://eboard.taobao.com  
//�������������ӿƼ����޹�˾  
//���ߣ�����ԭ�� @ALIENTEK

int main(void)
{ 

	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//����ϵͳ�ж����ȼ�����2
	delay_init(168);  //��ʼ����ʱ����
	RS485_Init(9600);
	KEY_Init();
	EXTIX_Init();
//	uart_init(115200);//��ʼ�����ڲ�����Ϊ115200
	TIM1_PWM_Init(600-1,168-1);
	TIM8_PWM_Init(600-1,168-1);
// 	TIM14_PWM_Init(500-1,84-1);	//84M/84=1Mhz�ļ���Ƶ��,��װ��ֵ500������PWMƵ��Ϊ 1M/500=2Khz.     
   while(1) //ʵ�ֱȽ�ֵ��0-300��������300���300-0�ݼ���ѭ��
	{
     touch();
	}
}