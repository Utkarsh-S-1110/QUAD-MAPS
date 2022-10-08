#! /usr/bin/env python3

import rospy
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
        self.obj=Quadmaps()
        self.obj.load_mini_map()
        print("Ready to scan")
        rospy.init_node('listener', anonymous=True)
        self.r = rospy.Rate(20)
        self.delay_scan=False
                
    def callback(self,msg):
        if not self.delay_scan:
            if self.obj.New_Scan:
                self.obj.scan(msg.ranges)
            str1=""
            List = self.obj.focus_on_position()
            for ci,i in enumerate(List):
                for cj,j in enumerate(i):
                    str1+=str(j)
                    str1+=","
            file = open("current_map.txt", "w+")
            file.write(str1)
            file.close()
        
    def newOdom(self,msg):
        if not self.delay_scan:
            grid_changed= False
            self.current_x = msg.pose.pose.position.x
            self.current_y = msg.pose.pose.position.y
            difference_x=self.current_x-self.last_recorded_x
            difference_y=self.current_y-self.last_recorded_y
            if (abs(difference_x)>0.10):
                if difference_x >0:
                    self.obj.current_grid_position[1]+=1
                else:
                    self.obj.current_grid_position[1]-=1
                self.last_recorded_x=self.current_x    
                grid_changed= True
          
            if (abs(difference_y)>0.10):
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
                    self.delay_scan=True
                    self.obj.split_map_to_boxes()
                    
                    if diff_grid_x >0:
                        self.obj.current_box[1]+=1
                        self.change_map()
                        self.obj.current_grid_position[1]=(abs(diff_grid_x)-int(self.obj.array_length/2))+(self.obj.array_length-1)
                    else:
                        self.obj.current_box[1]-=1
                        self.change_map()
                        self.obj.current_grid_position[1]=((2*self.obj.array_length)-1)-(abs(diff_grid_x)-int(self.obj.array_length/2))
                if (abs(diff_grid_y)> int(self.obj.array_length/2)):
                    self.delay_scan=True
                    self.obj.split_map_to_boxes()
                    
                    if diff_grid_y >0:
                        self.obj.current_box[0]+=1
                        self.change_map()
                        self.obj.current_grid_position[0]=(abs(diff_grid_y)-int(self.obj.array_length/2))+(self.obj.array_length-1)
                    else:
                        self.obj.current_box[0]-=1
                        self.change_map()
                        self.obj.current_grid_position[0]=((2*self.obj.array_length)-1)-(abs(diff_grid_y)-int(self.obj.array_length/2))
                        
                                      

            rot_q = msg.pose.pose.orientation
            (roll, pitch, self.obj.current_orientation) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    
    def change_map(self):
        self.obj.load_mini_map()  
        self.obj.focus_on_position()  
        self.delay_scan=False
        print("MAP CHANGED")

    def listener(self):
        
        try:
            rospy.Subscriber('/scan', LaserScan, self.callback)
            rospy.Subscriber("/odom", Odometry, self.newOdom)
            self.r.sleep()
            rospy.spin()
        except:
            print("ROBOT TURNED OFF")   

    
    
if __name__ == '__main__':
    starter_obj= start_script()
    starter_obj.listener()
    print("Saving map, please wait ...")
    if starter_obj.obj.New_Scan:
        starter_obj.obj.split_map_to_boxes()
        last_obj=final_map(starter_obj.obj.root,starter_obj.obj.maxx,starter_obj.obj.minn,starter_obj.obj.pow_of_2,starter_obj.obj.array_length)
        last_obj.store()
    