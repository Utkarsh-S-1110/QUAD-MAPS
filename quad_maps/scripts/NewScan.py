#! /usr/bin/env python3

import math
import concurrent.futures


from TreeNode import TreeNode
from final_map_manipulator import final_map

class Quadmaps:
    def __init__(self):
        self.New_Scan= True
        self.pow_of_2=7
        self.accuracy=0.03
        self.scanning = False
        self.no_of_threads = 4
        self.maxx=[1,1]
        self.minn=[1,1]
        self.result_by_index=[]
        self.array_length=int(math.pow(2,self.pow_of_2))
        if self.New_Scan:
            self.root=TreeNode("Quad-Map")
            for l1 in range(3):
                self.root.children.append(TreeNode("Y-axis",l1))
                for l2 in range(3):
                    self.root.children[l1].children.append(TreeNode("X-axis",l2))
                    self.create_empty_box(self.root.children[l1].children[l2])
        else:
            loader_obj=final_map()
            loader_obj.load()
            self.root=loader_obj.root    
            self.maxx=loader_obj.maxx
            self.minn=loader_obj.minn                
        self.current_box=[1,1]
        self.current_orientation=math.radians(0)                                             # Enter angle made by horizontal axis
        self.centre_map=[int(1.5*(self.array_length))-1,int(1.5*(self.array_length))-1]
        self.current_grid_position=[int(1.5*(self.array_length))-1,int(1.5*(self.array_length))-1]
        self.mini_map=[[0.5]*(self.array_length*3) for _ in range((self.array_length*3))]     
        print("Initialization done")


    def create_empty_box(self,obj):
        obj.children.append(TreeNode(0.5))    

    

    def load_mini_map(self,range_xi,range_xf,range_yi,range_yf):
        for l1 in range(range_yi,range_yf+1):
            for l2 in range(range_xi,range_xf+1):
                self.make_sure_box_exists(l1,l2)
                self.result_by_index=self.return_pos(l1,l2)
                self.add_box_to_mini_map(self.root.children[self.result_by_index[0]].children[self.result_by_index[1]],(l1-self.current_box[0]+1),(l2-self.current_box[1]+1))
                   
    

    def return_pos(self,l1,l2):
        l=0
        r=len(self.root.children)-1
        result=[None,None]
        while l <= r:
            mid = l + (r - l) // 2
            if self.root.children[mid].box_pos == l1:
                result[0]=mid
                break                
            elif self.root.children[mid].box_pos < l1:
                l = mid + 1
            else:
                r = mid - 1
        
        l=0
        r=len(self.root.children[result[0]].children)-1
        while l <= r:
            mid = l + (r - l) // 2
            if self.root.children[result[0]].children[mid].box_pos == l2:
                result[1]=mid   
                break             
            elif self.root.children[result[0]].children[mid].box_pos < l2:
                l = mid + 1
            else:
                r = mid - 1    
        return result

    


    def search_map(self,l1,l2):
        l=0
        r=len(self.root.children)-1
        result="Y"
        while l <= r:
            mid = l + (r - l) // 2;
            if self.root.children[mid].box_pos == l1:
                result="X"
                break                
            elif self.root.children[mid].box_pos < l1:
                l = mid + 1
            else:
                r = mid - 1
        if result=="Y":
            return [result,0]
        result_y=mid    
        l=0
        r=len(self.root.children[result_y].children)-1
        while l <= r:
            mid = l + (r - l) // 2;
            if self.root.children[result_y].children[mid].box_pos == l2:
                result="NOTHING"   
                break             
            elif self.root.children[result_y].children[mid].box_pos < l2:
                l = mid + 1
            else:
                r = mid - 1    
        result2=[result,result_y]        
        return result2        

    


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

    


    def sort(self,list1):
        n = len(list1)
        for i in range(n-1):
            exit=True
            for j in range(0, n-i-1):
                if list1[j].box_pos > list1[j + 1].box_pos :
                    list1[j], list1[j + 1] = list1[j + 1], list1[j]
                    exit=False
            if exit:
                return                   


    
    def make_sure_box_exists(self,l1,l2):
        if l1<self.minn[0]:
            self.minn[0]=l1
        elif l1>self.maxx[0]:
            self.maxx[0]=l1
        if l2<self.minn[1]:
            self.minn[1]=l2
        elif l2>self.maxx[1]:
            self.maxx[1]=l2            
        result2=self.search_map(l1,l2)
        result=result2[0]
        if result=="Y":
            self.root.children.append(TreeNode("Y-axis",l1))
            self.root.children[-1].children.append(TreeNode("X-axis",l2))
            self.create_empty_box(self.root.children[-1].children[-1])
            self.sort(self.root.children)
        elif result=="X":
            self.root.children[result2[1]].children.append(TreeNode("X-axis",l2))
            self.create_empty_box(self.root.children[result2[1]].children[-1])
            self.sort(self.root.children[result2[1]].children)

    

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

    def scan(self,ranges,current_orientation,y_pos,x_pos):
        if not self.scanning:
            self.scanning=True
            theta_strips=1
            laser_range=1.90#3.5
            #round_off_to_decimal_spaces = 1 if (self.accuracy==0.1) else 2
            for cnt,i in enumerate(ranges):
                angle=math.radians(theta_strips*cnt) + current_orientation
                if (angle <= (-180)):
                    angle+=360
                elif (angle>180):
                    angle-=360
                if abs(math.cos(angle)) > abs(math.sin(angle)):
                    larger = abs(math.cos(angle))
                else:
                    larger=abs(math.sin(angle))              
                distance_to_travel_to_mark_black= self.accuracy / larger
                if i <=laser_range:
                    j=0.000
                    while(j<float(i)-(self.accuracy*distance_to_travel_to_mark_black)):
                        x=int(round(float(j)*math.cos(angle)/self.accuracy,0))
                        x=min(x,int(laser_range/self.accuracy))
                        x=max(-int(laser_range/self.accuracy),x)
                        y=int(round(float(j)*math.sin(angle)/self.accuracy,0))
                        y=min(y,int(laser_range/self.accuracy))
                        y=max(-int(laser_range/self.accuracy),y)
                        x+=x_pos
                        y=y_pos-y  
                        
                        self.mini_map[y][x]=max(0.1,(1/(1+(((1-0.3)/0.3)*((1-self.mini_map[y][x])/self.mini_map[y][x])))))
                        j+=distance_to_travel_to_mark_black
                    
                    x=int(round(float(i)*math.cos(angle)/self.accuracy,0))
                    y=int(round(float(i)*math.sin(angle)/self.accuracy,0))
                    x+=x_pos
                    y=y_pos-y   
                                    
                    self.mini_map[y][x]=min(0.95,(1/(1+(((1-0.7)/0.7)*((1-self.mini_map[y][x])/self.mini_map[y][x])))))    
                else:
                    j=0.000
                    while(j<laser_range):
                        x=int(round(float(j)*math.cos(angle)/self.accuracy,0))
                        x=min(x,int(laser_range/self.accuracy))
                        x=max(-int(laser_range/self.accuracy),x)
                        y=int(round(float(j)*math.sin(angle)/self.accuracy,0))
                        y=min(y,int(laser_range/self.accuracy))
                        y=max(-int(laser_range/self.accuracy),y)
                        x+=x_pos
                        y=y_pos-y  

                        self.mini_map[y][x]=max(0.1,(1/(1+(((1-0.3)/0.3)*((1-self.mini_map[y][x])/self.mini_map[y][x])))))
                        j+=distance_to_travel_to_mark_black
            self.scanning=False       
        else:
            print("Missed it")             
    
    def split_map_to_boxes(self,range_xi,range_xf,range_yi,range_yf):
        control_loop_x = self.current_box[1]-1#range_xi #self.current_box[1]-1
        control_loop_y = self.current_box[0]-1#range_yi #self.current_box[0]-1
        box = [[0.5]*self.array_length for _ in range(self.array_length)]
        for l1 in range(range_yi,range_yf+1):
            for l2 in range(range_xi,range_xf+1):
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
        elif range_yi==range_yf:
            for l1 in range(range_yi,range_yf+1):
                for l3 in range((l1-control_loop_y)*self.array_length,(l1+1-control_loop_y)*self.array_length):
                    if(range_yi<self.current_box[0]):
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
        
        


        
      