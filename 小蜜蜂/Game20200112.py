# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 15:53:21 2019

@author: danle
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#https://www.youtube.com/watch?v=FfWpgLFMI7w

import pygame
import random
import os
import math
import datetime

#Init
pygame.init()


#----子彈模組
class Bullet():
    def __init__(self,screen):
        self.shot_delay=500
        
        #子彈圖片
        playerImg=pygame.image.load("Bullet.png")
        self.width=10
        self.playerImg = pygame.transform.scale(playerImg, (self.width, 20))
        
        self.x=500
        self.y=700 #子彈由下方射出
        self.shoot_flag=False
        self.ready=True
        
        #self.lastshoot=datetime.datetime.now()+datetime.timedelta(microseconds=self.shot_delay)
        #microseconds
        
        #----子彈擊中，稍候自己也需要消失
        self.gothit=0
        
        #畫在哪
        self.screen=screen
        
        #---Get Rect 抓出子彈的外框，稍後用於比對子彈是否擊中敵人
        self.rect=self.playerImg.get_rect()
    def draw(self):
        #-----可以設定需要擊穿多少目標，目前設定為只要擊穿一項
        if self.gothit>0:
            #將子彈恢復原來樣子(init)
            self.shoot_flag=False
            self.gothit=0
            self.y=700
            
        #----如果為射出狀況，則畫出子彈       
        if self.shoot_flag==True:
            self.screen.blit(self.playerImg,(self.x,self.y))
        
        #---更新子彈的碰撞外框，因為目前設定子彈不會變大變小，所以只要更新子彈的左上角
        self.rect[0]=self.x
        self.rect[1]=self.y
        
        self.move()
       
    def drawgun(self,x,y):    
        #給太空船用，單純只是畫在太空船上，表示可以發射了
        self.screen.blit(self.playerImg,(x,y))
 
    #---發射
    def shoot(self,x):
        #一艘太空船可以多顆子彈，所以檢查本子彈目前是否可以射出(未射出模式)
        if self.shoot_flag==False:
            #if self.lastshoot < datetime.datetime.now():
            #    self.lastshoot=datetime.datetime.now()+datetime.timedelta(microseconds=self.shot_delay)
                
            self.shoot_flag=True
            self.x=x-int(self.width/2)
            return True #---傳回成功表示射出
            #else:
            #    return False
        else:
            return False
        pass
    
    #---檢查本彈艙是否可設出
    def shootable(self):
        if self.shoot_flag==False:
            return True
        else:
            return False
    #子彈向上飛    
    def move(self):
        if self.shoot_flag==True:
            self.y=self.y-2
            if self.y<1:
                 self.shoot_flag=False
                 self.y=700


#-----蜜蜂模組                 
class Bee():
    def __init__(self,screen=None,x=0,y=0):
            self.screen=screen
            
            self.playerImg=list()
            #----載入三張蜜蜂動態
            for i in ("Bee1.png","Bee2.png","Bee3.png"):
                pyimage=pygame.image.load(i)
                pyimage=pygame.transform.scale(pyimage, (40, 50))
                self.playerImg.append(pyimage)
            self.x=x
            self.y=y
            self.y_dist=random.randint(0,10)
            
            #---目前顯示動作(0,1,2)
            self.showmode=0
            
            self.gothit=0 #---被擊中次數
            
            self.live=True #密蜂還活著，等等需要畫出來
            
            #---Get Rect
            self.rect=self.playerImg[0].get_rect()
    
    #畫出蜜蜂        
    def draw(self):
        
        if self.gothit>0:
            self.live=False
            self.gothit=0
            print("Bee Dead")
        
        if self.live==True:
            self.showmode=self.showmode+0.01
            self.screen.blit(self.playerImg[int(self.showmode % 3)],(self.x,self.y))
        
            self.rect[0]=self.x
            self.rect[1]=self.y
        
#----首腦---敵人運動模式控制
class BeesBrain():
    def __init__(self,bees):
        self.bees_direct=1 #---1 Right, 2 Left
        self.bees_move=300   #已移動次數
        self.bees_max_move=600
        self.bees=bees
        self.downfloorcnt=0
        self.naxdownfloorcnt=600
        self.downfloorflag=False
        
    #----簡易左右模式    
    def move(self):
        self.bees_move=self.bees_move+1
        if self.bees_move>self.bees_max_move:
            self.bees_move=0
            if self.bees_direct==1:
                self.bees_direct=2
            else:
                self.bees_direct=1
                
        for id,bee in enumerate(self.bees):
            bee.x=bee.x+pow(-1,self.bees_direct)*0.42
            if self.downfloorflag==True:
                bee.y=bee.y+5
                print(bee.y)
                if bee.y>800:
                   self.bees.pop(id)
        self.downfloorflag=False
                
    #--- 密蜂策略選擇
    def think(self):
        self.downfloorcnt=self.downfloorcnt+1
        if self.downfloorcnt>self.naxdownfloorcnt:
           self.downfloorcnt=0 
           self.downfloorflag=True    
        self.move()
        pass


#------Space Ship 太空船模組
class SpaceShip():
    def __init__(self,screen,sound):
        self.screen=screen
        self.sound=sound

        #載入太空船照片
        playerImg=pygame.image.load("ROCKET.png")
        self.playerImg = pygame.transform.scale(playerImg, (50, 100))
        self.shot_delay=450
        self.lastshoot=None
        #datetime.datetime.now()+datetime.timedelta(microseconds=self.shot_delay)
        
        self.x=random.randint(1,1200-100)
        self.y=800-100
        self.y_dist=random.randint(0,10)


        self.rock_gun=Bullet(screen) #---這顆不會射出，只是表示子彈目前是否可發射
        #====建立飛彈倉        
        self.bullets=list()
        #-----多顆飛彈
        for b in range(5):
            self.bullets.append(Bullet(screen))
        
    #-----
    #def up(self):
    #    if self.y>300:
    #       self.y=self.y-self.y_dist
    #    else:
    #       self.y=self.y-self.y_dist*2
    #       
    #    if self.y<0:
    #       self.x= random.randint(0,1200)
    #       self.y= 900+random.randint(0,500)  
           
    #向左移動
    def left(self):
        if self.x>1:
            self.x=self.x-1
    #向右移動
    def right(self):
        if self.x<1200-50:
            self.x=self.x+1
    #發射飛彈
    def shoot(self):
        #---發射後等待秒數
        if self.lastshoot!=None:
            if self.lastshoot>datetime.datetime.now():
               return False
           
        
        
        #----逐一檢查彈倉是否可發射
        for i in self.bullets:
            if i.shoot(self.x+25)==True:
               self.sound.play_sound("shoot")
               #發射，並設定要稍後才能再次發射
               self.lastshoot=datetime.datetime.now()+datetime.timedelta(microseconds=self.shot_delay)
               return True 
        return False

    def shootable(self):
        for i in self.bullets:
            if i.shootable()==True:
               return True 
        return False
    
    #---畫太空船       
    def draw(self):
        self.screen.blit(self.playerImg,(self.x,self.y))
        
        #---畫出飛彈在太空船上
        if self.shootable():
            self.rock_gun.drawgun(self.x+19,self.y-5)
        
        #Draw Bullet
        for bullet in self.bullets:
            bullet.draw()
            
        #self.shoot()
        #==True:
            
            #for bullet in self.bullets:
            #    if bullet.shot()==True:
            #       return


#----顯示得分狀況及過關說明
class Score():
    def __init__(self,screen):
        self.screen=screen
        self.font = pygame.font.SysFont('宋體', 32, True)
        
        self.hiscore=0
        
        self.score=list()
        self.score.append(0)
        self.score.append(0)
        
        self.stageclear=False
        self.stagecleartime=None
        
    def show(self):
        #----Show 1UP的分數
        surface1 = self.font.render(u'1UP', True, [255, 255, 255])
        self.screen.blit(surface1, [45, 20])
        score=self.score[0]

        surface2 = self.font.render("{:10d}".format(self.score[0]), True, [255, 255, 255])
        self.screen.blit(surface2, [40, 52])
        
        #----Show 最高分分數
        surface1 = self.font.render(u'HI-SCORE', True, [255, 255, 255])
        self.screen.blit(surface1, [520, 20])
        surface2 = self.font.render("{:10d}".format(self.hiscore), True, [255, 255, 255])
        self.screen.blit(surface2, [560, 52])
        
        #-----Show Stage Clear
        if self.stageclear==True:
           #顯示三秒鐘
           if self.stagecleartime==None:
              self.stagecleartime=datetime.datetime.now()+datetime.timedelta(seconds=5)
           else:
               if datetime.datetime.now()>self.stagecleartime:
                   self.stageclear=False
                   self.stagecleartime=None
           if self.stageclear ==True:          
               font = pygame.font.SysFont('宋體', 52, True)
               
               #surface1 = font.render('STAGE CLEAR', True, [255,255, 255])
               surface1 = font.render('STAGE CLEAR', True, [random.randint(0,255),random.randint(0,255), random.randint(0,255)])
               self.screen.blit(surface1, [500, 400])
        
    #----增加分數    
    def add_score(self,player=0,score=0):
        self.score[player]=self.score[player]+score

        if self.score[player]>self.hiscore:
            self.hiscore=self.score[player]
        

#------音效模組
class Sound():
    def __init__(self):
        self.sound=dict()
        self.bgm=list()
        self.changesong=False
    #----載入稍後要播放背景音樂    
    def load_bgm(self,path,volume=0.1,times=-1):
        self.bgm.append((path,volume,times))
 
    #----載入稍後要播放音效 
    # 載入音效並指定音效名稱，播放音效(与背景音乐可同时播放，但默认只支持wav格式)
    def load_sound(self,name,path,volume=0.1):
        #載入後放字典中，所以檢查如果是全新音效
        #if self.sound.get(name,None)==None:
                #temp=path
        temp = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(temp)
        sound.set_volume(volume)
        #載入後放字典中     
        self.sound[name]=sound
    # 播放音效，給定音效名稱
    def play_sound(self,name):
        self.sound[name].play()
    
    
    #----檢查是否要換背景音樂
    def check(self):
        if pygame.mixer.music.get_busy()==0:
           self.changesong=True
           
           if len(self.bgm)>0:
              path,volume,times=self.bgm.pop(0)
              pygame.mixer.music.load(path) 
              pygame.mixer.music.set_volume(volume)
              pygame.mixer.music.play(times, 0)
               
        pass  
    
    #----停止背景音樂
    def stop(self):
        pygame.mixer.music.stop()
        self.bgm=list()

#----檢查是否碰撞    
def CheckCollect(sound,rocket,bees,score):
    #檢查太空船射出的飛彈跟蜜蜂
    for id,obj in enumerate(rocket.bullets):
        if obj.shoot_flag==True:
            #print(id,"Shot",obj.rect)
            #print("bee:",bee.rect)
            for id,bee in enumerate(bees):
                if bee.live:
                    if pygame.Rect.colliderect(obj.rect,bee.rect):
                       obj.gothit=obj.gothit+1
                       bee.gothit=bee.gothit+1
                       #boom_sound.play()
                       sound.play_sound("boom")
                       score.add_score(0,100)
                       bees.pop(id)
                       print("BOOM!!")
    #需再檢查太空船跟蜜蜂及蜜蜂的飛彈                  
               

#---生成蜜蜂群
def MakeBees(screen,x=8,y=5):
    width=1200
    beewidth=Bee().rect[3]
    beeheight=Bee().rect[3]
    
    beewidthDist=int(beewidth*0.55)
    startx=int((width-(beewidth+beewidthDist)*x)/2)
    starty=100
    
    bees=list()
    for ix in range(x):
        for iy in range(y):
            bees.append(Bee(screen,int(startx+(beewidth+beewidthDist)*ix),starty+int(beeheight*iy*1.03)))
    return bees

#def StageClear(screen,sound):
#    font = pygame.font.SysFont('宋體', 48, True)
#    surface1 = font.render('STAGE CLEAR', True, [255, 255, 255])
#    screen.blit(surface1, [500, 400])
#        
#    #surface2 = self.font.render("{:10d}".format(self.score[0]), True, [255, 255, 255])
#    #    self.screen.blit(surface2, [40, 52])
    
#主程式
def MainProgram():
    bee_x_no=3
    bee_y_no=3
    
    #create the screen 設定遊戲畫面
    screen=pygame.display.set_mode((1200,800))
    
    #載入音效
    sound=Sound()
    sound.load_sound("shoot","D:/PauLee/bullet.wav",0.2)
    sound.load_sound("boom","D:/PauLee/boom.wav",0.2)  
    #sound.load_bgm("BeesStart.mp3",0.3,1)
    #sound.load_bgm("music.mp3",0.1,-1)

    #設定太空船       
    player=SpaceShip(screen,sound)

    #設定記分板
    score=Score(screen)
    
    #按鍵狀況
    left_key_down=False
    right_key_down=False
    space_key_down=False
    
    #Game Loop
    running=True
    
    #pass_countdown=10
    passtime=None
    #datetime.datetime.now()
    
    #第一關
    NewStage=True
    
    while running:
        if NewStage==True:
           sound.load_bgm("BeesStart.mp3",0.3,1)
           sound.load_bgm("music.mp3",0.1,-1)
            
            
           #---重建蜜蜂群
           bees=MakeBees(screen,bee_x_no,bee_y_no)
           #給蜂群戰略
           beesbrain=BeesBrain(bees)
           
           
           
           NewStage=False
        
        # 畫畫面
        screen.fill((0,0,0)) 
        
        #檢查按鍵
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:    
               if event.key==pygame.K_ESCAPE:
                   running=False
               elif event.key==pygame.K_LEFT:
                   left_key_down=True
                   #player.left()
               elif event.key==pygame.K_RIGHT:
                   right_key_down=True
                   #player.right()
               elif event.key==pygame.K_SPACE:
                   space_key_down=True
                   #player.shoot()
            elif event.type==pygame.KEYUP:
               if event.key==pygame.K_LEFT:
                   left_key_down=False
               elif event.key==pygame.K_RIGHT:
                   right_key_down=False
               elif event.key==pygame.K_SPACE:
                   #space_key_down=False    
                   if len(bees)>0:
                      player.shoot() 
                
        if left_key_down==True:
            player.left()
        if right_key_down==True:
            player.right()
            
        #----沒蜜蜂時不給射    
        #if space_key_down==True and len(bees)>0:
        #    player.shoot()    
            
        
        #檢查音效狀況
        sound.check()
        #檢查碰撞狀況
        CheckCollect(sound,player,bees,score)
        
        
        
        
        #畫太空船   
        player.draw()
        
        #蜜蜂動態決定
        beesbrain.think()
        #畫蜜蜂
        for bee in bees:
            bee.draw()
        #畫記分板
        score.show()
        
        #檢查過關沒
        #一隻蜜蜂都沒有
        if len(bees)==0:
            if passtime==None:
                passtime=datetime.datetime.now()+datetime.timedelta(seconds=3)
            else:
                #--敵人全亡後等三秒
                if datetime.datetime.now()>passtime:
                   sound.stop()
                   #---下一關卡
                   NewStage=True
                   #StageClear(screen,sound)
                   #sound.changesong=False
                   score.stageclear=True
                   #print("Stage Clear")
                   
                   #---增家蜜蜂數量
                   bee_x_no=bee_x_no+1
                   if bee_x_no>=10:
                      bee_y_no=bee_y_no+1
                      bee_x_no=3
                   if bee_y_no>=6:
                       bee_y_no=6
                   
        if passtime!=None:
            print(datetime.datetime.now()-passtime)
        pygame.display.flip() 
        #pygame.display.update()   
             
    pygame.quit()


MainProgram()

