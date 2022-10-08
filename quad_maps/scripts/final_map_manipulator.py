from TreeNode import TreeNode
import pickle
import numpy as np

class final_map:
    def __init__(self):
        self.root=TreeNode("Quad-Map")
    
    def load(self):
        file = open("final_map_details.txt", "r")
        Lines = file.readlines()
        self.pow_of_2=int(Lines[0])
        self.array_length=int(Lines[1])
        self.maxx=[int(Lines[2]),int(Lines[3])]
        self.minn=[int(Lines[4]),int(Lines[5])]
        try:
            infile = open("final_map.txt","rb")
        except:
            return     
        try:
            self.final_map = pickle.load(infile)
            print(len(self.final_map))
            print(len(self.final_map[0]))
        except:
            print("Couldn't update map")    
        finally:
            infile.close()        
        y_diff = self.maxx[0] - self.minn[0]  
        x_diff = self.maxx[1] - self.minn[1]      
        for l1 in range(y_diff+1):
            self.root.children.append(TreeNode("Y-axis",l1+self.minn[0]))
            for l2 in range(x_diff+1):
                self.root.children[l1].children.append(TreeNode("X-axis",l2+self.minn[1]))
                box = np.zeros([self.array_length,self.array_length])
                for l3 in range(l1*self.array_length,(l1+1)*self.array_length):
                    for l4 in range(l2*self.array_length,(l2+1)*self.array_length):
                        box[l3 - (l1*self.array_length),l4 - (l2*self.array_length)] = self.final_map[l3,l4]
                self.update_box(box,l1,l2) 
        print("MAP LOADED")        
                       


    
    def update_box(self,box2,y,x):
        root = self.root.children[y].children[x]
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

    
