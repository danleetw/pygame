# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 09:13:28 2020

@author: Dan Lee
"""
#-----檢查左下右上斜線
for s in range(2,8+1):
    for i in range(1,s+1):
        print(i,s-i+1)
    print("-"*8)    
'''
#Output --------------
1 2
2 1
--------
1 3
2 2
3 1
--------
1 4
2 3
3 2
4 1
--------
1 5
2 4
3 3
4 2
5 1
--------
1 6
2 5
3 4
4 3
5 2
6 1
--------
1 7
2 6
3 5
4 4
5 3
6 2
7 1
--------
1 8
2 7
3 6
4 5
5 4
6 3
7 2
8 1
--------
'''
    
    
    
#-----檢查左上右下斜線    
for s in range(2,8+1):
    for i in range(1,s+1):
        print(8-s+i,i)
    print("-"*8)        

'''
#Output --------------
7 1
8 2
--------
6 1
7 2
8 3
--------
5 1
6 2
7 3
8 4
--------
4 1
5 2
6 3
7 4
8 5
--------
3 1
4 2
5 3
6 4
7 5
8 6
--------
2 1
3 2
4 3
5 4
6 5
7 6
8 7
--------
1 1
2 2
3 3
4 4
5 5
6 6
7 7
8 8
--------
'''