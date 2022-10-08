#! /usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time



class animate_map:
    def __init__(self):
        self.focused_map = [[0]*123 for _ in range(123)]
        try:
            file = open("current_map.txt", "r")
            content = file.read()
            for i in range(123):
                for j in range(123):
                    k=0
                    str2=""
                    while content[k]!=",":
                        str2+=content[k]
                        k+=1
                    self.focused_map[i][j]=float(str2)
                    if not ((j==122) and (i==122)):
                        content=content[k+1:]
            file.close()            
        except:
            print("Couldn't update map")    
        self.fig= plt.figure()
        H = np.array(self.focused_map)
        self.im = plt.imshow(H, interpolation='none',cmap='gray', vmin=0, vmax=1)

    def animate(self,i):
        try:
            file = open("current_map.txt", "r")
            content = file.read()

            for i in range(123):
                for j in range(123):
                    k=0
                    str2=""
                    while content[k]!=",":
                        str2+=content[k]
                        k+=1
                    self.focused_map[i][j]=float(str2)
                    if not ((j==122) and (i==122)):
                        content=content[k+1:]
            file.close()   
            for t in range(61,63):
                for u in range(61,63):
                    self.focused_map[t][u]=0.9

        except:
            print("Couldn't update map")             
        self.im.set_data(np.array(self.focused_map))
        return self.im     

if __name__ == '__main__':
    starter_obj= animate_map()
    anim = animation.FuncAnimation(starter_obj.fig, starter_obj.animate,interval=500)
    plt.show()        
