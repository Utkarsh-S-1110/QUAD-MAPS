#! /usr/bin/env python3

import rospy
import pickle
import numpy as np
#import threading
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point,Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

from NewScan import Quadmaps
from final_map_manipulator import final_map

class start_script:                          
    def __init__(self):
        self.current_x=0.0
        self.current_y=0.0
        self.last_recorded_x=0.0
        self.last_recorded_y=0.0
        #threading.Thread.__init__(self)
        self.obj=Quadmaps()
        self.obj.load_mini_map(0,2,0,2)
        print("Ready to scan")
        rospy.init_node('listener', anonymous=True)
        self.r = rospy.Rate(10)
        self.delay_scan=False
                
    def callback(self,msg):
        if not self.delay_scan:
           
            if self.obj.New_Scan:
                self.obj.scan(msg.ranges,self.obj.current_orientation,self.obj.current_grid_position[0],self.obj.current_grid_position[1])
            self.write_map_to_file()     
        
    def write_map_to_file(self):
        outfile= open("current_map.txt","wb")
        pickle.dump(self.obj.focus_on_position(),outfile)
        outfile.close()


    def newOdom(self,msg):
        #print(self.obj.current_box)
        if not self.delay_scan:
           
            grid_changed= False
            self.current_x = msg.pose.pose.position.x
            self.current_y = msg.pose.pose.position.y
            difference_x=self.current_x-self.last_recorded_x
            difference_y=self.current_y-self.last_recorded_y
            if (abs(difference_x)>self.obj.accuracy):
                if difference_x >0:
                    self.obj.current_grid_position[1]+=1
                else:
                    self.obj.current_grid_position[1]-=1
                self.last_recorded_x=self.current_x    
                grid_changed= True
          
            if (abs(difference_y)>self.obj.accuracy):
                if difference_y>0:
                    self.obj.current_grid_position[0]-=1
                else:
                    self.obj.current_grid_position[0]+=1   
                self.last_recorded_y=self.current_y  
                grid_changed= True      

            if grid_changed:
                diff_grid_x= self.obj.current_grid_position[1]-self.obj.centre_map[1]
                diff_grid_y= self.obj.current_grid_position[0]-self.obj.centre_map[0]
                if (abs(diff_grid_x)> int(self.obj.array_length/2)):
                    print("MAP CHANGING")
                    self.delay_scan=True
                                        
                    if diff_grid_x >0:
                        self.obj.split_map_to_boxes(self.obj.current_box[1]-1,self.obj.current_box[1]-1,self.obj.current_box[0]-1,self.obj.current_box[0]+1)
                        self.obj.current_box[1]+=1
                        self.change_map(self.obj.current_box[1]+1,self.obj.current_box[1]+1,self.obj.current_box[0]-1,self.obj.current_box[0]+1)
                        self.obj.current_grid_position[1]=(abs(diff_grid_x)-int(self.obj.array_length/2))+(self.obj.array_length-1)
                        self.delay_scan=False
                    else:
                        self.obj.split_map_to_boxes(self.obj.current_box[1]+1,self.obj.current_box[1]+1,self.obj.current_box[0]-1,self.obj.current_box[0]+1)
                        self.obj.current_box[1]-=1
                        self.change_map(self.obj.current_box[1]-1,self.obj.current_box[1]-1,self.obj.current_box[0]-1,self.obj.current_box[0]+1)
                        self.obj.current_grid_position[1]=((2*self.obj.array_length)-1)-(abs(diff_grid_x)-int(self.obj.array_length/2))
                        self.delay_scan=False
                
                if (abs(diff_grid_y)> int(self.obj.array_length/2)):
                    print("MAP CHANGING")
                    self.delay_scan=True
                                        
                    if diff_grid_y >0:
                        self.obj.split_map_to_boxes(self.obj.current_box[1]-1,self.obj.current_box[1]+1,self.obj.current_box[0]-1,self.obj.current_box[0]-1)
                        self.obj.current_box[0]+=1
                        self.change_map(self.obj.current_box[1]-1,self.obj.current_box[1]+1,self.obj.current_box[0]+1,self.obj.current_box[0]+1)
                        self.obj.current_grid_position[0]=(abs(diff_grid_y)-int(self.obj.array_length/2))+(self.obj.array_length-1)
                        self.delay_scan=False
                    else:
                        self.obj.split_map_to_boxes(self.obj.current_box[1]-1,self.obj.current_box[1]+1,self.obj.current_box[0]+1,self.obj.current_box[0]+1)
                        self.obj.current_box[0]-=1
                        self.change_map(self.obj.current_box[1]-1,self.obj.current_box[1]+1,self.obj.current_box[0]-1,self.obj.current_box[0]-1)
                        self.obj.current_grid_position[0]=((2*self.obj.array_length)-1)-(abs(diff_grid_y)-int(self.obj.array_length/2))
                        self.delay_scan=False
                    print(self.obj.current_box[0])    
                        
                                      

            rot_q = msg.pose.pose.orientation
            (roll, pitch, self.obj.current_orientation) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    
    def change_map(self,range_xi,range_xf,range_yi,range_yf):
        while self.obj.scanning:
            continue
        self.obj.load_mini_map(range_xi,range_xf,range_yi,range_yf)  
        #self.obj.focus_on_position()  
        #self.delay_scan=False
        print("MAP CHANGED")

    def listener(self):
        
        try:
            rospy.Subscriber('/scan', LaserScan, self.callback)
            rospy.Subscriber("/odom", Odometry, self.newOdom)
            self.r.sleep()
            rospy.spin()
        except:
            print("ROBOT TURNED OFF")   

    def save(self):
        file = open("final_map_details.txt", "w+")
        file.write(str(self.obj.pow_of_2)+"\n")
        file.write(str(self.obj.array_length)+"\n")
        file.write(str(self.obj.maxx[0])+"\n")
        file.write(str(self.obj.maxx[1])+"\n")
        file.write(str(self.obj.minn[0])+"\n")
        file.write(str(self.obj.minn[1])+"\n")       
        file.close() 
        self.final_map = np.full(((self.obj.maxx[0]-self.obj.minn[0]+1)*self.obj.array_length,(self.obj.maxx[1]-self.obj.minn[1]+1)*self.obj.array_length), 0.5)
        for l1 in self.obj.root.children:
            for l2 in l1.children:
                pos = self.obj.return_pos(l1.box_pos,l2.box_pos)
                if not ((pos[0] == None) or (pos[1]==None)):
                    box = self.obj.root.children[pos[0]].children[pos[1]]
                    uncompressed_box=self.obj.get_box(box)
                    y_base = pos[0]*self.obj.array_length
                    x_base = pos[1]*self.obj.array_length
                    for l3 in range(y_base,y_base+self.obj.array_length):
                        for l4 in range(x_base,x_base+self.obj.array_length):
                            self.final_map[l3,l4] = uncompressed_box[l3-y_base][l4-x_base]
        outfile= open("final_map.txt","wb")
        pickle.dump(self.final_map,outfile)
        outfile.close()                    

    
    
if __name__ == '__main__':
    starter_obj= start_script()
    starter_obj.listener()
    if starter_obj.obj.New_Scan:
        starter_obj.obj.split_map_to_boxes(starter_obj.obj.current_box[1]-1,starter_obj.obj.current_box[1]+1,starter_obj.obj.current_box[0]-1,starter_obj.obj.current_box[0]+1)
        print("Saving ...")
        starter_obj.save()
        print("Saved")
    

