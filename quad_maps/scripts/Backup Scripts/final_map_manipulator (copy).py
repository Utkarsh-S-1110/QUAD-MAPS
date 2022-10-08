#! /usr/bin/env python3
from TreeNode import TreeNode


class final_map:
    def __init__(self,root=[[0]],maxx=[0,0],minn=[0,0],pow_of_2=0,array_length=0):
        self.pow_of_2=pow_of_2
        self.array_length=array_length
        self.root=root
        self.maxx=maxx
        self.minn=minn
        self.last_x=self.minn[1]
        self.dep=0
        self.diff_x=maxx[1]-minn[1] +1
        self.diff_y=maxx[0]-minn[0] +1
        """
        self.last_y=minn[0]
        diff_y=maxx[0]-minn[0]
        diff_x=maxx[1]-minn[1]
        self.decider=0
        if (diff_x> diff_y):
            self.max_diff=diff_x
            self.decider=1
        else:
            self.max_diff=diff_y
            self.decider=0
        """    
        self.final_saver=""    


    def store(self):
        file = open("final_map.txt", "w+")
        file.write(str(self.pow_of_2)+"\n")
        file.write(str(self.array_length)+"\n")
        file.write(str(self.maxx[0])+"\n")
        file.write(str(self.maxx[1])+"\n")
        file.write(str(self.minn[0])+"\n")
        file.write(str(self.minn[1])+"\n")
        for l1 in self.root.children:
            self.last_x=self.minn[1]
            cnt_enu=0
            help_counter=0
            last_number=self.minn[1]-1
            for l2 in l1.children:
                if not (last_number==(l2.box_pos-1)):
                    self.last_x=last_number
                else:
                    self.last_x=l2.box_pos                    
                for l3 in range(l2.box_pos-self.last_x):
                    for l4 in range(self.array_length*self.array_length):
                        self.final_saver+=str(0.5) + " "
                    help_counter+=1
                    print(l1.box_pos,",",help_counter)    
                box=self.get_box(l2)
                for l5 in box:
                    for l6 in l5:
                        self.final_saver+=str(l6) + " "
                last_number=l2.box_pos

                help_counter+=1
                print(l1.box_pos,",",help_counter-1)
                cnt_enu=l2.box_pos+1
            if not ((cnt_enu)==self.diff_x):
                for l7 in range(self.diff_x-cnt_enu):
                    for l8 in range(self.array_length*self.array_length):
                        self.final_saver+=str(0.5) + " "
                    help_counter+=1
                    print(l1.box_pos,",",help_counter)
                
                        
        file.write(self.final_saver)
        print("Final Map Saved")
        file.close()
    
    def save(self):
        file = open("final_map.txt", "r")
        Lines = file.readlines()
        self.pow_of_2=int(Lines[0])
        self.array_length=int(Lines[1])
        self.maxx=[int(Lines[2]),int(Lines[3])]
        self.minn=[int(Lines[4]),int(Lines[5])]
        content=Lines[6]
        self.root=TreeNode("Quad-Map")
        for l1 in range(self.minn[0],self.maxx[0]+1):
            self.root.children.append(TreeNode("Y-axis",l1))
            for l2 in range(self.minn[1],self.maxx[1]+1):
                self.root.children[-1].children.append(TreeNode("X-axis",l2))
                print(l1,",",l2)
                a1=[[0.5]*self.array_length for _ in range(self.array_length)]
                for i in range(128):
                    for j in range(128):
                        k=0
                        str2=""
                        while content[k]!=" ":
                            str2+=content[k]
                            k+=1
                        a1[i][j]=float(str2)
                        if (not ((j==127) and (i==127))) or (not ((l1==((self.maxx[0]-self.minn[0]))) and (l2==((self.maxx[1]-self.minn[1]))))):
                            content=content[k+1:]
                        print(l1,l2)    
                self.update_box(a1,l1,self.minn[0],l2,self.minn[1])            
                #self.root.children[l1].add_child()
        file.close()
        return self.root        


    
    def update_box(self,box2,y,ymin,x,xmin):
        #found_pos=self.return_pos(y,x)
        print("Updating started")
        self.root.children[y-ymin].children[x-xmin].children=[]
        root = self.root.children[y-ymin].children[x-xmin]
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
            octo_list=[]
            
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
            octo_list.append(temp_list1)
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
        octo_list.append(octo_list_layer)
        print("Updation done")

    def get_box(self,obj):
        list1=obj.children
        list2=[]
        for l1 in range(self.pow_of_2):                                                   #self.pow_of_2-1
            for l2 in list1:
                if not l2.children:
                    for l3 in range(0,4):
                        list2.append(TreeNode(l2.data))
                else:
                    for l3 in l2.children:
                        list2.append(l3)
            list1= list2
            list2=[]
        for l1 in list1:
            list2.append(l1.data)             
        list1=list2
        list2=[]
        side=2
        for l1 in range(0,(self.pow_of_2)-1):
                while len(list1):
                    for l2 in range(1,side+1):
                        k=side-l2
                        for l in range(0,side):
                            list2.append(list1.pop(0))
                        for l in range(0,side):
                            list2.append(list1.pop(side*k))   
                list1=list2
                list2=[]
                side*=2 
        cnt1=0
        cnt2=0
        list3=[[0.5]*self.array_length for _ in range(self.array_length)]
        for l1 in list1:
            list3[cnt2][cnt1]=l1
            cnt1+=1
            if cnt1==self.array_length:
                cnt2+=1
                cnt1=0
        return list3    
