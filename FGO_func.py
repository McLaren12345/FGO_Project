# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""
import time
import sys
from tqdm import tqdm
sys.path.append(r'F:\FGO_Project')
from playsound import playsound 
import Serial 
import Base_func
import Config

def enter_battle(template='F:/FGO_Project/Template/LastOrder_sign.jpg'):    
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Menu_button.jpg')
    while bool(1-Flag):
        time.sleep(1)       
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Menu_button.jpg')
        #不停检测菜单按键，确认已经返回菜单界面
    Flag,Position = Base_func.match_template(template)
    if bool(1-Flag):
        Serial.send(1060,480) #如果没有找到，点一下滚动条
        Serial.wait_for_flag()
    i=1    
    while bool(1-Flag):
        i+=1
        time.sleep(2)       
        Flag,Position = Base_func.match_template(template)
        if i>3:
            k=input('未找到上次执行关卡，需人工操作，按0退出执行:')
            if k==0:
                Serial.send(0,0)
                Serial.wait_for_flag()
                exit() 
    if Flag:
        Serial.send(Position[0]+230,Position[1]+50)    #加一点偏移量，保证点在关卡图标上
        Serial.wait_for_flag() 
        Flag,Position = Base_func.match_template(template)
        while Flag:
            time.sleep(2)       
            Flag,Position = Base_func.match_template(template)
        print(' ')
        print(' enter battle success')
        return Flag
    else:
        print(' enter battle fail')
        return Flag
    
def apple_feed():   
    #喂苹果，先银后金
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/AP_recover.jpg')
    if Flag:
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Silver_apple.jpg')
        if Flag:
            Serial.send(709,Position[1])
            Serial.wait_for_flag()
            Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Feedapple_decide.jpg')
            Serial.send(Position[0],Position[1])
            Serial.wait_for_flag()
            print(' feed silver apple success')
            return Flag
        else:
            Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Gold_apple.jpg')
            if Flag:
                Serial.send(709,Position[1])
                Serial.wait_for_flag()
                Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Feedapple_decide.jpg')
                Serial.send(Position[0],Position[1])
                Serial.wait_for_flag()
                print(' feed gold apple success')
                return Flag
            else:
                print(' no apple remain')
                Serial.send(0,0)
                Serial.wait_for_flag()
                exit()
                return Flag
    else:
        print(' no need to feed apple')
        
def find_friend():
    time.sleep(1)    
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Caster_sign.jpg')
    while bool(1-Flag):
        time.sleep(1)       
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Caster_sign.jpg') 
    #检测到滚动条说明好友已经刷出
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/friend_sign.jpg')
    while bool(1-Flag):
        time.sleep(1)       
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/friend_sign.jpg')
        
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/CBA_skill_level.jpg')
    time_limit_flag = 1
    #找310CBA直到找到为止
    while bool(1-Flag):
        print(' didn\'t find CBA, retry. attempt{}'.format(time_limit_flag))
        if time_limit_flag>1:
            time.sleep(15)    #如果不是第一次刷新，等待15秒      
        #Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Refresh_friend.jpg')
        Serial.send(720,110)
        Serial.wait_for_flag()
        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Refresh_decide.jpg')
        Serial.send(Position[0],Position[1])
        Serial.wait_for_flag()
        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/friend_signal.jpg')
        while bool(1-Flag):
            time.sleep(1)       
            Flag,Position = Base_func.match_template('F:/FGO_Project/Template/friend_signal.jpg')
        
        if time_limit_flag>4:
            k=input(' 5次刷新未找到CBA，需人工操作，按0退出执行:')
            if k==0:
                Serial.send(0,0)
                Serial.wait_for_flag()
                exit()
        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/CBA_skill_level.jpg')
        time_limit_flag+=1
        
    if Flag:
        print(' success find CBA')
        Serial.send(Position[0],Position[1]-50)
        Serial.wait_for_flag()
        #识别“开始任务”按钮
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Start_button.jpg')
        while bool(1-Flag):
            time.sleep(1)
            Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Start_button.jpg')
        Serial.send(Position[0],Position[1])
        Serial.wait_for_flag()
        print(' Start battle button pressed')
        
def quit_battle():
    time.sleep(15)
    while True:
        time.sleep(1)
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Battlefinish_sign.jpg')
        if Flag:
            break
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
        if Flag:
            break
    #检测到战斗结束标志或御主的脸时跳出循环
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    if Flag:
        for i in range(3):
            playsound('F:/FGO_Project/11750.mp3')
        print(' 翻车，需要人工处理')          #翻车检测，系统三声报警
        Serial.send(0,0)
        Serial.wait_for_flag()
        exit() 
    print(' battle finished')
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Next_step.jpg')
    Serial.send(936,571)                   #一直点，直到发现“下一步”的按钮
    Serial.wait_for_flag()
    while bool(1-Flag):
        time.sleep(2)        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Next_step.jpg')
        if Flag:
            Serial.send(Position[0],Position[1])
            Serial.wait_for_flag()
        else:
            Serial.send(936,571) 
            Serial.wait_for_flag()
    #time.sleep(7)
    print(' quit success')
        
def Master_skill(skill_no,para1=3,para2=2):
    Serial.send(1000,266)               #御主技能按键
    Serial.wait_for_flag()
    if skill_no==1:                     #加攻
        Serial.send(760,266)
        Serial.wait_for_flag()
    elif skill_no==2:                   #眩晕
        Serial.send(835,266)
        Serial.wait_for_flag()
    elif skill_no==3:                   #换人
        Serial.send(910,266)
        Serial.wait_for_flag()                   
        Serial.send(630+(para2-1)*170,300)            #默认换最后一人与替换区第二人
        Serial.wait_for_flag()
        Serial.send(120+(para1-1)*170,300)
        Serial.wait_for_flag()
        Serial.send(530,530)
        Serial.wait_for_flag()
        
#    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
#    while bool(1-Flag):
#        time.sleep(1)        
#        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    print(' master skill{} has pressed'.format(skill_no))
        
def character_skill(character_no,skill_no,para=None):   #角色编号，技能编号，选人（可选）
    Position = (50+(character_no-1)*270+(skill_no-1)*80,488)#50是第一个技能按键的x像素坐标，80为技能的像素偏移量，270为从者位置偏移量
    Serial.send(Position[0],Position[1])
    Serial.wait_for_flag()
    if para != None:
        Position = (280+(para-1)*250,350)  #技能选人
        Serial.send(Position[0],Position[1])
        Serial.wait_for_flag()
    #time.sleep(5)         #等待技能动画时间
#    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
#    while bool(1-Flag):
#        time.sleep(1)        
#        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    print(' character{}\'s skill{} has pressed'.format(character_no,skill_no))
    
def card(Baoju_no=1):
    Serial.send(950,510)   #点击attack按钮
    Serial.wait_for_flag()
    time.sleep(1)
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    i=0
    while Flag:
        i+=1
        if i>3:
            print(' 发卡失败，需人工处理')
            Serial.send(0,0)
            Serial.wait_for_flag()
            exit()
        time.sleep(2)
        Serial.send(950,510)   #如没有进入选卡界面再次点击attack按钮
        Serial.wait_for_flag()        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    
    Serial.send(340+(Baoju_no-1)*200,170)   #打手宝具,参数可选1-3号宝具位
    Serial.wait_for_flag()
    
    Serial.send(340+(Baoju_no-1)*200,430)  #随便两张牌，先选宝具下面那张
    Serial.wait_for_flag()
    
    Serial.send(540,430)                  #默认选中间的牌
    Serial.wait_for_flag()
    
    print(' Card has pressed')
    
    
def battle(): 
    #判断是否进入战斗界面
    time.sleep(10)                          #等待战斗开始
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    while bool(1-Flag):
        time.sleep(1)        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    #Turn1    
    character_skill(1,1)
    character_skill(2,1,1)
    character_skill(2,3,1)
    character_skill(3,1,1)
    card()
    
    time.sleep(10)                          #等待战斗动画播放完成
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    while bool(1-Flag):
        time.sleep(1)        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    #Turn2
    character_skill(3,2)
    character_skill(3,3,1)
    Master_skill(3)
    character_skill(3,3)
    card(3)    
    
    time.sleep(10)                          #等待战斗动画播放完成
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    while bool(1-Flag):
        time.sleep(1)        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    #Tun3
    character_skill(1,2)
    character_skill(1,3)
    character_skill(3,3)
    Master_skill(1)    
    card()


#该函数与battle功能完全一致，区别在于该函数读取的是csv脚本
def config2battle():
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    while bool(1-Flag):
        time.sleep(2)        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    #Turn1    
    Config.Config2Command(Config.df1)
    
    time.sleep(5)                          #等待战斗动画播放完成
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    while bool(1-Flag):
        time.sleep(2)        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    #Turn2
    Config.Config2Command(Config.df2)
    
    time.sleep(5)                          #等待战斗动画播放完成
    Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    while bool(1-Flag):
        time.sleep(2)        
        Flag,Position = Base_func.match_template('F:/FGO_Project/Template/Master_face.jpg')
    #Tun3
    Config.Config2Command(Config.df3)
    
    
def FGO_process(times=1,command_switch=False):
    for i in tqdm(range(times)):
        times-=1
        enter_battle()
        apple_feed()
        find_friend()
        if command_switch:
           config2battle()
        else:
           battle()        
        quit_battle()
        Serial.send(0,0)         #电机复位,防止误差累积
        Serial.wait_for_flag()
        print(' ')
        print(' {}times of battles remain'.format(times))
        time.sleep(1)
      
def main(port_no,times=1,use_commmand=False):
    Serial.port_open(port_no)   #写入通讯的串口号
    FGO_process(times,use_commmand)
    Serial.port_close()
    print(' All done!') 
    
    
if __name__=='__main__':
	main('com5')

