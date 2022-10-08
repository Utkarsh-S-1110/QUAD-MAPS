#! /usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import pickle



class animate_map:
    def __init__(self):
        try:
            infile = open("final_map.txt","rb")
        except:
            return None    
        try:
            self.focused_map = pickle.load(infile)
        except:
            print("Couldn't update map")    
        finally:
            infile.close()
            
        self.fig= plt.figure()
        try:
            H = np.array(self.focused_map)
            self.im = plt.imshow(H, interpolation='none',cmap='gray', vmin=0, vmax=1)
        except AttributeError:
            pass            
        

    def animate(self,i):
        try:
            infile = open("final_map.txt","rb")
        except:
            return None             
        try:
            backup= self.focused_map
            self.focused_map = pickle.load(infile)
            for t in range(62,64):                      #61,63  511,531
                for u in range(59,65):                  #61,63  511,531
                    self.focused_map[t][u]=1
            self.focused_map[60][58]=1
            self.focused_map[59][57]=1   
            self.focused_map[64][59]=1
            self.focused_map[65][59]=1 
            self.focused_map[64][64]=1
            self.focused_map[65][64]=1 
            self.focused_map[61][65]=1
            self.focused_map[62][65]=1 
            self.focused_map[61][66]=1
            self.focused_map[62][66]=1
            self.im.set_data(np.array(self.focused_map))                                                     
        except:
            try:
                self.im.set_data(np.array(backup))
            except:
                pass                
        finally:
            infile.close()                
        return self.im     

if __name__ == '__main__':
    starter_obj= animate_map()
    anim = animation.FuncAnimation(starter_obj.fig, starter_obj.animate,interval=10)
    plt.show()        



"""class animate_map:
    def __init__(self):
        self.focused_map = [[0]*1023 for _ in range(1023)]
        try:
            file = open("current_map.txt", "r")
            content = file.read()
            for i in range(1023):
                for j in range(1023):
                    k=0
                    str2=""
                    while content[k]!=",":
                        str2+=content[k]
                        k+=1
                    self.focused_map[i][j]=float(str2)
                    if not ((j==1022) and (i==1022)):
                        content=content[k+1:]
                    print("reading:",i, ',',j)    
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

            for i in range(1023):
                for j in range(1023):
                    k=0
                    str2=""
                    while content[k]!=",":
                        str2+=content[k]
                        k+=1
                    self.focused_map[i][j]=float(str2)
                    if not ((j==1022) and (i==1022)):
                        content=content[k+1:]
            file.close()   
            for t in range(511,531):                      #61,63
                for u in range(511,531):                  #61,63
                    self.focused_map[t][u]=0.9

        except:
            print("Couldn't update map")             
        self.im.set_data(np.array(self.focused_map))
        return self.im     

if __name__ == '__main__':
    starter_obj= animate_map()
    anim = animation.FuncAnimation(starter_obj.fig, starter_obj.animate,interval=500)
    plt.show()        
"""