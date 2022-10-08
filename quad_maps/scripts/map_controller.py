import pickle
import numpy as np
import time

import math
import concurrent.futures


from final_map_manipulator import final_map
from TreeNode import TreeNode


class start_script:                          
    def __init__(self):
        self.current_box = [1,1]
        self.accuracy=0.03
        self.no_of_threads = 4
        self.delay_scan = False
        self.centre_map=[int(1.5*(self.array_length))-1,int(1.5*(self.array_length))-1]

        self.final_map = final_map()
        self.final_map.load()

        self.pow_of_2 = self.final_map.pow_of_2
        self.array_length = self.final_map.array_length
        self.maxx = self.final_map.maxx
        self.minn = self.final_map.minn
        self.load_mini_map(0-self.minn[1],2-self.minn[1],0-self.minn[0],2-self.minn[0])

        self.current_grid_position=[int(1.5*(self.array_length))-1,int(1.5*(self.array_length))-1]
        self.mini_map=[[0.5]*(self.array_length*3) for _ in range((self.array_length*3))]

                
    def callback(self,msg):
        if not self.delay_scan:
            self.write_map_to_file()     
        
    def write_map_to_file(self):
        outfile= open("current_map.txt","wb")
        pickle.dump(self.focus_on_position(),outfile)
        outfile.close()

    def focus_on_position(self):
        focused_map = [[0.5]*(self.array_length-int(5*(0.1/self.accuracy))) for _ in range(self.array_length-int(5*(0.1/self.accuracy)))]
        cnt_y=0
        cnt_x=0
        for l1 in range(self.current_grid_position[0]-(int(self.array_length/2)-int(3*(0.1/self.accuracy))),self.current_grid_position[0]+int(self.array_length/2)-int(2*(0.1/self.accuracy))):
            for l2 in range(self.current_grid_position[1]-(int(self.array_length/2)-int(3*(0.1/self.accuracy))),self.current_grid_position[1]+int(self.array_length/2)-int(2*(0.1/self.accuracy))):
                focused_map[cnt_y][cnt_x]=self.mini_map[l1][l2]
                cnt_x+=1
            cnt_y+=1
            cnt_x=0
        return focused_map

    def load_mini_map(self,range_xi,range_xf,range_yi,range_yf):
        for l1 in range(range_yi,range_yf+1):
            for l2 in range(range_xi,range_xf+1):
                self.add_box_to_mini_map(self.root.children[l1].children[l2],(l1-self.current_box[0]+self.minn[0]+1),(l2-self.current_box[1]+self.minn[1]+1))
    
    def add_box_to_mini_map(self,box,l3,l4):
        #print(l3,",",l4)
        uncompressed_box=self.get_box(box)
        uncompressed_box_grid=[0,0] 
        for l1 in range(l3*self.array_length,(l3+1)*self.array_length):
            for l2 in range(l4*self.array_length,(l4+1)*self.array_length):
                #print(len(self.mini_map))
                #print(len(self.mini_map[0]))
                self.mini_map[l1][l2]= uncompressed_box[uncompressed_box_grid[0]][uncompressed_box_grid[1]]
                uncompressed_box_grid[1]+=1
            uncompressed_box_grid[0]+=1
            uncompressed_box_grid[1]=0  
        
            

    def get_box(self,obj):
        self.list1=obj.children
        self.list2=[]
        for l1 in range(self.pow_of_2):                                                   #self.pow_of_2-1
            for l2 in self.list1:
                if not l2.children:
                    for l3 in range(0,4):
                        if l1==(self.pow_of_2-1):
                            self.list2.append(l2.data)
                        else:
                            self.list2.append(TreeNode(l2.data))
                else:
                    for l3 in l2.children:
                        if l1==(self.pow_of_2-1):
                            self.list2.append(l3.data)  
                        else:
                            self.list2.append(l3)
            self.list1= self.list2
            self.list2=[]
        num = math.pow(self.array_length,2)#16384#9437184
        r1_list,r2_list=[],[]
        for thread_num in range(self.no_of_threads):
            r1_list.append(int(thread_num*(num/self.no_of_threads)))
            r2_list.append(int((thread_num+1)*(num/self.no_of_threads)))
        self.list3=[[0.5]*self.array_length for _ in range(self.array_length)]
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for i in range(self.no_of_threads):
                result=executor.submit(self.parallel_calaculation,r1_list[i],r2_list[i])
                for j in result.result():
                    self.list3[j[1]][j[2]]=self.list1[j[0]]
        return self.list3

    def parallel_calaculation(self,r1,r2):
        cnt=r1
        temp_multiprocess_list=[]
        for l1 in range(r1,r2):
            cnt1=0
            cnt2=0
            self.list2=[]
            temp_cnt=cnt
            for l2 in reversed(range(1,self.pow_of_2+1)):
                l3=math.pow(2,l2-1)
                l4=int((temp_cnt/(l3*l3)))
                self.list2.append(l4)
                temp_cnt-= (l3*l3)*(l4)
            for l3,l2 in enumerate(self.list2):
                l4=self.pow_of_2-l3
                if l2==0:
                    cnt1+=0
                    cnt2+=0
                elif l2==1:
                    cnt1+=int(math.pow(2,l4-1))
                    cnt2+=0
                elif l2==2:
                    cnt1+=0
                    cnt2+=int(math.pow(2,l4-1))
                else :
                    cnt1+=int(math.pow(2,l4-1))
                    cnt2+=int(math.pow(2,l4-1)) 
            temp_multiprocess_list.append([l1,cnt2,cnt1])      
            cnt+=1               
        return(temp_multiprocess_list)
    
    def newOdom(self,msg):
        if not self.delay_scan:
            grid_changed= False
            if moved up:
                self.current_grid_position[0] -= 1      
                grid_changed = True
            elif moved down:
                self.current_grid_position[0] += 1
                grid_changed = True
            elif moved left:
                self.current_grid_position[1] -= 1
                grid_changed = True
            elif moved right:
                self.current_grid_position[1] += 1
                grid_changed = True

            if grid_changed:
                diff_grid_x= self.current_grid_position[1]-self.centre_map[1]
                diff_grid_y= self.current_grid_position[0]-self.centre_map[0]
                if (abs(diff_grid_x)> int(self.array_length/2)):
                    print("MAP CHANGING")
                    self.delay_scan=True
                                        
                    if diff_grid_x >0:
                        self.split_map_to_boxes(self.current_box[1]-1,self.current_box[1]-1,self.current_box[0]-1,self.current_box[0]+1)
                        self.current_box[1]+=1
                        self.change_map(self.current_box[1]+1,self.current_box[1]+1,self.current_box[0]-1,self.current_box[0]+1)
                        self.current_grid_position[1]=(abs(diff_grid_x)-int(self.array_length/2))+(self.array_length-1)
                        self.delay_scan=False
                    else:
                        self.split_map_to_boxes(self.current_box[1]+1,self.current_box[1]+1,self.current_box[0]-1,self.current_box[0]+1)
                        self.current_box[1]-=1
                        self.change_map(self.current_box[1]-1,self.current_box[1]-1,self.current_box[0]-1,self.current_box[0]+1)
                        self.current_grid_position[1]=((2*self.array_length)-1)-(abs(diff_grid_x)-int(self.array_length/2))
                        self.delay_scan=False
                
                if (abs(diff_grid_y)> int(self.array_length/2)):
                    print("MAP CHANGING")
                    self.delay_scan=True
                                        
                    if diff_grid_y >0:
                        self.split_map_to_boxes(self.current_box[1]-1,self.current_box[1]+1,self.current_box[0]-1,self.current_box[0]-1)
                        self.current_box[0]+=1
                        self.change_map(self.current_box[1]-1,self.current_box[1]+1,self.current_box[0]+1,self.current_box[0]+1)
                        self.current_grid_position[0]=(abs(diff_grid_y)-int(self.array_length/2))+(self.array_length-1)
                        self.delay_scan=False
                    else:
                        self.split_map_to_boxes(self.current_box[1]-1,self.current_box[1]+1,self.current_box[0]+1,self.current_box[0]+1)
                        self.current_box[0]-=1
                        self.change_map(self.current_box[1]-1,self.current_box[1]+1,self.current_box[0]-1,self.current_box[0]-1)
                        self.current_grid_position[0]=((2*self.array_length)-1)-(abs(diff_grid_y)-int(self.array_length/2))
                        self.delay_scan=False
                        
    def change_map(self,range_xi,range_xf,range_yi,range_yf):
        self.load_mini_map(range_xi,range_xf,range_yi,range_yf)  
        #self.obj.focus_on_position()  
        #self.delay_scan=False
        print("MAP CHANGED")

    def split_map_to_boxes(self,range_xi,range_xf,range_yi,range_yf):
        control_loop_x = self.current_box[1]-1#range_xi #self.current_box[1]-1
        control_loop_y = self.current_box[0]-1#range_yi #self.current_box[0]-1
        box = [[0.5]*self.array_length for _ in range(self.array_length)]
        for l1 in range(range_yi,range_yf+1):
            for l2 in range(range_xi,range_xf+1):
                #print(l1,",",l2)
                for l3 in range((l1-control_loop_y)*self.array_length,(l1+1-control_loop_y)*self.array_length):
                    for l4 in range((l2-control_loop_x)*self.array_length,(l2+1-control_loop_x)*self.array_length):
                        box[l3%self.array_length][l4%self.array_length]=self.mini_map[l3][l4]
                self.update_box(box,l1,l2)
        if range_xi==range_xf:
            for l1 in range(range_yi,range_yf+1):
                for l2 in range(range_xi,range_xf+1):
                    for l3 in range((l1-control_loop_y)*self.array_length,(l1+1-control_loop_y)*self.array_length):
                        for l4 in range((l2-control_loop_x)*self.array_length,(l2+1-control_loop_x)*self.array_length):
                            if(range_xi<self.current_box[1]):
                                self.mini_map[l3].pop(0)
                                self.mini_map[l3].append(0.5)                               
                            else:
                                self.mini_map[l3].pop()
                                self.mini_map[l3].insert(0, 0.5)
        else:
            for l1 in range(range_yi,range_yf+1):
                for l3 in range((l1-control_loop_y)*self.array_length,(l1+1-control_loop_y)*self.array_length):
                    if(range_yi<self.current_box[1]):
                        self.mini_map.pop(0)
                        self.mini_map.append(([0.5]*self.array_length*3))                               
                    else:
                        self.mini_map.pop()
                        self.mini_map.insert(0,([0.5]*self.array_length*3)) 
#        else:
#            for l1 in range(range_yi,range_yf+1):
#                for l2 in range(range_xi,range_xf+1):
#                    for l3 in range((l1-control_loop_y)*self.array_length,(l1+1-control_loop_y)*self.array_length):
#                        list=[]
#                        for l4 in range((l2-control_loop_x)*self.array_length,(l2+1-control_loop_x)*self.array_length):
#                            if(range_yi<self.current_box[1]):
#                                self.mini_map[l3].pop(0)
#                                self.mini_map[l3].append(0.5)
#                            else:
#                                self.mini_map[l3].pop()
#                                self.mini_map[l3].insert(0,0.5)

    def update_box(self,box2,y,x):
        found_pos=self.return_pos(y,x)
        self.root.children[found_pos[0]].children[found_pos[1]].children=[]
        root = self.root.children[found_pos[0]].children[found_pos[1]]
        self.dep=0
        broken=False
        count_club=0
        list_obj=[root]
        current_grid_size=int(self.array_length/2)
        octo_list_layer=[]
        octo_list_layer.append(box2)
        for i in range(0,self.pow_of_2-1):
            half_counter=0
            adder_List=[root]
            adder_list_count=0
            temp_list1=[]
            list_obj3=[]
            temp_list4=[]
            list_obj2=[]
            track=0
                        
            for t in octo_list_layer:
                look_out_for=t[0][0]
                for j in range(0,4):
                    temp_list2=[]
                    if j==0:
                        start_x=0
                        stop_x=current_grid_size
                        start_y=0
                        stop_y=current_grid_size

                    elif j==1:
                        start_x=current_grid_size
                        stop_x=2*current_grid_size
                        start_y=0
                        stop_y=current_grid_size
                    elif j==2:
                        start_x=0
                        stop_x=current_grid_size
                        start_y=current_grid_size
                        stop_y=2*current_grid_size
                    else:
                        start_x=current_grid_size
                        stop_x=2*current_grid_size
                        start_y=current_grid_size
                        stop_y=2*current_grid_size
                    for k in range(start_y,stop_y):
                        temp_list3=[]
                        for l in range(start_x,stop_x):
                            temp_list3.append(t[k][l])
                            if t[k][l]==look_out_for:
                                count_club+=1
                        temp_list2.append(temp_list3)    
                    temp_list4.append(temp_list2)
                if(count_club==(2*current_grid_size)*(2*current_grid_size)):
                    temp_list1.append(look_out_for)
                    for z in range(0,4):
                        temp_list4.pop(track*4)
                    list_obj3.append(TreeNode(look_out_for))    
                else:
                    temp_list1.append(2)  
                    obj_child=TreeNode(2)
                    list_obj2.append(obj_child)
                    list_obj3.append(obj_child)
                    half_counter+=1
                    track+=1   
                count_club=0    
                adder_list_count+=1

            current_grid_size=int(current_grid_size/2)
            octo_list_layer=temp_list4        
            for obj_to_add in list_obj:
                if self.dep==0:
                    obj_to_add.children.append(list_obj3.pop(0))
                else:
                    for v1 in range(0,4):
                        obj_to_add.children.append(list_obj3.pop(0))
            self.dep+=1    
            list_obj=list_obj2
            if not (half_counter):
                broken =True
                break
        if not broken:
            for obj_to_add in list_obj:
                    for v1 in range(0,4):
                        obj_to_add.children.append(TreeNode(octo_list_layer.pop(0)[0][0]))  
    
    def listener(self):
        while True:
            try:
                self.callback()
                self.newOdom()
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("FINISHED")   
                exit()

      
if __name__ == '__main__':
    starter_obj= start_script()
    starter_obj.listener()
    
    
