# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 21:28:59 2020

@author: danle
"""

  
#----印棋盤
def showmap(score):
    for i in range(8):
        for j in range(8):
            print("["+score[i][j]+"]",end="")
        print()    

#----檢查狀態，將衝突設為X
def check_map(map_str):
    map_arr=[[' ']*8 for i in range(8)]
    #print(map_str)
    
    for i in range(1,9):
        map_arr[int(map_str[i-1:i])-1][i-1]='O'
        
    w_flag=False            
    #檢查橫線
    pass_flag=True
    #y_pass=True
    for i in range(8):
        cnt=0
        for j in range(8):
            if map_arr[i][j]!=" ":
                cnt=cnt+1
        if cnt>1:
           pass_flag=False
           for j in range(8):
               if map_arr[i][j]!=" ":
                  map_arr[i][j]="-"
    if pass_flag==True or True:           
        #檢查直線          
        for j in range(8): #0-7              
            cnt=0    
            for i in range(8):
                if map_arr[i][j]!=" ":
                    cnt=cnt+1
            if cnt>1:
                pass_flag=False
                for i in range(8):
                    if map_arr[i][j]!=" ":
                        map_arr[i][j]="|"
    if pass_flag==True or True:      
        #w_flag=True        
        #檢查左下斜右上 
        
        for s in range(2,8):
            cnt=0 
            for i in range(0,s):
               #print("Check:",s-i,i+1)
               if map_arr[i+1-1][s-i-1]!=" ":
                    cnt=cnt+1
            #print("----",cnt)        
            if cnt>1:
               #
               pass_flag=False
               
               for i in range(0,s):
                  if map_arr[i+1-1][s-i-1]!=" ":
                      map_arr[i+1-1][s-i-1]="\\"
        #if pass_flag==False: 
        #   print("----------")
        #   showmap(map_arr)       
        #   input("Croxx A")
    if pass_flag==True or True:      
        #w_flag=True        
        #檢查左上斜右下
        for s in range(2,8):
            cnt=0 
            for i in range(0,s):
               #print("Check:",s-i,i+1)
               if map_arr[s-i-1][i+1-1]!=" ":
                    cnt=cnt+1
            #print("----",cnt)        
            if cnt>1:
               #showmap(map_arr)  
               pass_flag=False
               
               for i in range(0,s):
                  if map_arr[s-i-1][i+1-1]!=" ":
                      map_arr[s-i-1][i+1-1]="/"                      
                      
                      
        #if pass_flag==False: 
        #   showmap(map_arr)       
        #   input("Croxx B")    
        #input("A")
              
        #if pass_flag==False:
        #    showmap(map_arr) 
        #    input("wrong")
                     
                   
                    
                    
                   
                        
    #showmap(map_arr)      
    #if w_flag:
    #    input("Wrong") 
     
    #if pass_flag:
    print(map_str)
    showmap(map_arr)
    input("Check")
       #print(showmap(score))
       #print("Bingo!!!")
       #input("Bingo!")
       #end   
       #input("B")          



#------進位函數
def AddOne(ValStr,enter_val=9,base_val=1):
    move_flag=True #進位
    #enter_val=9
    #base_val=1
    ret=ValStr[:len(ValStr)-1]+str(int(ValStr[-1:])+1)
    x=len(ValStr)
    while move_flag :
        #------從最後一位開始檢查，是否進位
        if int(ret[x-1:x])>=enter_val:
           # 如果需要進位,12345679
           # 本身回復成Base_Val
           # 左邊一格加1
           # 左邊兩格以前照搬 
           # x=8 123456 7+1 base
           ret=ret[:x-2]+str(int(ret[x-2:x-1])+1)+str(base_val)+ret[x:]
           # 從右邊第一位開始檢查完以後，接下來往左邊檢查
           x=x-1
           #-----如果來到第一位，再進位就溢位，全部歸零，回復成基本Base_Val
           if x==1:
               ret=str(base_val)*len(ret)
               move_flag=False
               #break
        else:
            move_flag=False
    #print(a)        
    return ret


proc_cnt=0
map_str='12345678'
while True:
    proc_cnt=proc_cnt+1
    #if proc_cnt% 137==0:
    #    print(map_str)
    check_map(map_str)
    map_str=AddOne(map_str)
