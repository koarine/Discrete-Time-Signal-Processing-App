import customtkinter as ctk
import tkinter as tk
import math
import matplotlib.pyplot as plot
import numpy as np

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1)  
ctk.set_window_scaling(1)  
#Discrete Signals Class
class Discrete_Signal:
    def __init__(self,name):
        self.name = name
        self.value_sequence = []
        self.left_val = None

    def time_shift(self,time_shift_val):
        self.left_val=int(self.left_val)+int(time_shift_val)

    def time_scale(self,time_scale_val):
        k=float(time_scale_val)
        self.left_val=int(self.left_val)
        DS1_Left_Val=self.left_val
        Discrete_Signal_1=self.value_sequence
        
        temp_axis = []
        temp_signal = []
        DS1_Right_Val = len(self.value_sequence)+DS1_Left_Val-1
        DS1_X_Axis =[i for i in range(DS1_Left_Val,DS1_Right_Val+1)]
        if k<0:
            DS1_X_Axis.reverse()
            for i in range(len(DS1_X_Axis)):
                DS1_X_Axis[i] *=-1
            Discrete_Signal_1.reverse()
        k=abs(k)
        for i in range(len(DS1_X_Axis)):
            DS1_X_Axis[i] *=k
        for i in range(len(DS1_X_Axis)):
            if math.floor(DS1_X_Axis[i]) == DS1_X_Axis[i]:
                temp_axis.append(int(DS1_X_Axis[i]))
                temp_signal.append(Discrete_Signal_1[i])
        for i in range(temp_axis[-1]-temp_axis[0]):
            if temp_axis[i+1]-temp_axis[i]!=1:
                temp_axis.insert(i+1,temp_axis[i]+1)
                temp_signal.insert(i+1,0)
        DS1_X_Axis = temp_axis
        Discrete_Signal_1 = temp_signal
        DS1_Left_Val = DS1_X_Axis[0]
        self.left_val=DS1_Left_Val
        self.value_sequence=Discrete_Signal_1
    
    def amplitude_shift(self,amp_shift_val):
        amp_shift_val=float(amp_shift_val)
        for i in range(len(self.value_sequence)):
            self.value_sequence[i]+=amp_shift_val 
    
    def amplitude_scale(self,amp_scale_val):
        amp_scale_val=float(amp_scale_val)
        for i in range(len(self.value_sequence)):
            self.value_sequence[i]*=amp_scale_val

    def convolution(self,Discrete_Obj_1,Discrete_Obj_2):
        Discrete_Obj_1.left_val=int(Discrete_Obj_1.left_val)
        Discrete_Obj_2.left_val=int(Discrete_Obj_2.left_val)
        temp_obj_2 = Discrete_Signal("temp_1")
        temp_obj_2.value_sequence, temp_obj_2.left_val = list(Discrete_Obj_2.value_sequence),Discrete_Obj_2.left_val
        temp_obj_2.time_scale(-1)
        temp_obj_2_right= temp_obj_2.left_val+len(temp_obj_2.value_sequence)-1
        Difference = Discrete_Obj_1.left_val-temp_obj_2_right
        temp_obj_2.time_shift(Difference)
        temp_obj_2_right= temp_obj_2.left_val+len(temp_obj_2.value_sequence)-1
        Discrete_Obj_1_right= Discrete_Obj_1.left_val+len(Discrete_Obj_1.value_sequence)-1
        DS1_temp_axis = [i for i in range(Discrete_Obj_1.left_val,Discrete_Obj_1_right+1)]
        DS2_temp_axis = [i for i in range(temp_obj_2.left_val,temp_obj_2_right+1)]
        Conv_Signal = []
        while(temp_obj_2.left_val<(Discrete_Obj_1.left_val+len(Discrete_Obj_1.value_sequence))):
            common = []
            for i in DS2_temp_axis:
                if i in DS1_temp_axis:
                    common +=[i]
            Sum=0
            for common_x_val in common:
                DS1_index = DS1_temp_axis.index(common_x_val)
                DS2_index =  DS2_temp_axis.index(common_x_val)
                Sum += Discrete_Obj_1.value_sequence[DS1_index]*temp_obj_2.value_sequence[DS2_index]
            for i in range(len(DS2_temp_axis)):
                DS2_temp_axis[i]+=1
            Conv_Signal.append(Sum)
            temp_obj_2.time_shift(1)
        return Difference,Conv_Signal

    def correlation(self,Discrete_Obj_1,Discrete_Obj_2):
        Discrete_Obj_1.left_val=int(Discrete_Obj_1.left_val)
        Discrete_Obj_2.left_val=int(Discrete_Obj_2.left_val)
        temp_obj_2 = Discrete_Signal("temp_1")
        temp_obj_2.value_sequence, temp_obj_2.left_val =  Discrete_Obj_2.value_sequence,Discrete_Obj_2.left_val
        temp_obj_2_right= temp_obj_2.left_val+len(temp_obj_2.value_sequence)-1
        Difference = Discrete_Obj_1.left_val-temp_obj_2_right
        temp_obj_2.time_shift(Difference)
        temp_obj_2_right= temp_obj_2.left_val+len(temp_obj_2.value_sequence)-1
        Discrete_Obj_1_right= Discrete_Obj_1.left_val+len(Discrete_Obj_1.value_sequence)-1
        DS1_temp_axis = [i for i in range(Discrete_Obj_1.left_val,Discrete_Obj_1_right+1)]
        DS2_temp_axis = [i for i in range(temp_obj_2.left_val,temp_obj_2_right+1)]
        corr_signal = []
        while(temp_obj_2.left_val<(Discrete_Obj_1.left_val+len(Discrete_Obj_1.value_sequence))):
            common = []
            for i in DS2_temp_axis:
                if i in DS1_temp_axis:
                    common +=[i]
            Sum=0
            for common_x_val in common:
                DS1_index = DS1_temp_axis.index(common_x_val)
                DS2_index =  DS2_temp_axis.index(common_x_val)
                Sum += Discrete_Obj_1.value_sequence[DS1_index]*temp_obj_2.value_sequence[DS2_index]
            for i in range(len(DS2_temp_axis)):
                DS2_temp_axis[i]+=1
            corr_signal.append(Sum)
            temp_obj_2.time_shift(1)
        return Difference,corr_signal

    def elementary_operations(self,Discrete_Obj_1,Discrete_Obj_2,operation):
        temp_obj_1 = Discrete_Signal("temp_1")
        temp_obj_2 = Discrete_Signal("temp_2")
        temp_obj_3 = Discrete_Signal("temp_3")
        temp_obj_1.left_val,temp_obj_1.value_sequence = Discrete_Obj_1.left_val,list(Discrete_Obj_1.value_sequence)
        temp_obj_2.left_val,temp_obj_2.value_sequence = Discrete_Obj_2.left_val,list(Discrete_Obj_2.value_sequence)
        x_array_1 = [i for i in range(int(temp_obj_1.left_val),int(temp_obj_1.left_val)+len(temp_obj_1.value_sequence))]
        x_array_2 = [i for i in range(int(temp_obj_2.left_val),int(temp_obj_2.left_val)+len(temp_obj_2.value_sequence))]
        min_val = min(x_array_1[0],x_array_2[0])
        max_val = max(x_array_1[-1],x_array_2[-1])
        x_array_3 = [i for i in range(min_val,max_val+1)]
        left_1= x_array_1[0]-x_array_3[0]
        right_1= x_array_3[-1]-x_array_1[-1]
        left_2= x_array_2[0]-x_array_3[0]
        right_2= x_array_3[-1]-x_array_2[-1]
        temp_obj_1.value_sequence = [0]*left_1+temp_obj_1.value_sequence+[0]*right_1
        temp_obj_2.value_sequence = [0]*left_2+temp_obj_2.value_sequence+[0]*right_2
        
        if operation == "+":
            for i in range(len(temp_obj_2.value_sequence)):
                temp_obj_3.value_sequence+=[temp_obj_1.value_sequence[i]+temp_obj_2.value_sequence[i]]
            return x_array_3[0],temp_obj_3.value_sequence
        if operation =="-":
            for i in range(len(temp_obj_2.value_sequence)):
                temp_obj_3.value_sequence+=[temp_obj_1.value_sequence[i]-temp_obj_2.value_sequence[i]]
            return x_array_3[0],temp_obj_3.value_sequence
        if operation =="*":
            for i in range(len(temp_obj_2.value_sequence)):
                temp_obj_3.value_sequence+=[temp_obj_1.value_sequence[i]*temp_obj_2.value_sequence[i]]
            return x_array_3[0],temp_obj_3.value_sequence
    
    def energy(self):
        energy=0
        for element in self.value_sequence:
            energy+=element*element
        return energy
    
    def power(self):
        return self.energy()/len(self.value_sequence)


#Main App 
class App(ctk.CTk):
    #---Initialization Of Class Attributes---#
    X1 = Discrete_Signal("X1")
    X2 = Discrete_Signal("X2")
    X3 = Discrete_Signal("X3")
    X4 = Discrete_Signal("X4")
    X5 = Discrete_Signal("X5")
    Convolution_GLOBAL = Discrete_Signal("Convolution")
    Auto_Correlation_GLOBAL = Discrete_Signal("Auto_Correlation")
    Correlation_GLOBAL = Discrete_Signal("Correlation")
    elementary_operations_GLOBAL = Discrete_Signal("Elementary_Operations")
    Selected = None
    Global_Coord_X1 = []
    Global_Coord_Y1 = []

    #---Startup---#
    def __init__(self):
        super().__init__()
        #---Window Size Information---#
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        #---Background grid weight Information---#
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        #---Needed for background startup---#
        self.main_contained()
        #---Create Main Page---#
        self.page_main_menu()

    #---Frame Initialization---#
    def main_contained(self):
        self.main_container = ctk.CTkFrame(self)
        self.main_container.grid(row=0,column=0,sticky="nsew",padx=0,pady=0)
        
    #---Main Menu Page---#
    def page_main_menu(self):
        self.main_container.destroy()
        self.main_contained()   
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_menu_window_container=ctk.CTkFrame(self.main_container)
        self.main_menu_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_menu_window_container.rowconfigure((1,2,3,4,5,6,7,8),weight=0)
        self.main_menu_window_container.rowconfigure(0,weight=2)
        self.main_menu_window_container.rowconfigure(15,weight=3)
        self.main_menu_window_container.columnconfigure((0,3),weight=1)
        self.logo_label = ctk.CTkLabel(self.main_menu_window_container, text="Main Menu", font=ctk.CTkFont(size=50, weight="bold"))
        self.logo_label.grid(row=1, column=1, padx=20, pady=(20, 10), columnspan=2, sticky="ew")
        #---View Discrete Time Signal Button---#
        self.button = ctk.CTkButton(self.main_menu_window_container, text="View Discrete Time Signals", command=lambda:self.page_view(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=2,column=1,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Elementary Operations", command=lambda:self.page_elementary_operations(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=2,column=2,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Time Shifting", command=lambda:self.page_time_shifting(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=3,column=1,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Time Scaling", command=lambda:self.page_time_scaling(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=3,column=2,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="DC Shift", command=lambda:self.page_amplitude_shifting(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=4,column=1,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Amplitude Scaling", command=lambda:self.page_amplitude_scaling(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=4,column=2,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Energy", command=lambda:self.page_energy(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=5,column=1,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Power", command=lambda:self.page_power(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=5,column=2,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Auto Correlation", command=lambda:self.page_auto_correlation(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=6,column=1,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Cross Correlation", command=lambda:self.page_correlation(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=6,column=2,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Convolution", command=lambda:self.page_convolution(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=7,column=1,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Discrete Time Fourier Transform", command=lambda:self.page_discrete_fourier_transform(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=7,column=2,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_menu_window_container, text="Plot Signal", command=lambda:self.page_plot_signal(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=8,column=1,padx=10,pady=10,columnspan=2,sticky="ew")

        

    #---Temp Placeholder to do nothing when button is pressed that has not been assigned command---#
    def button_event(self):
        pass

    #---View Discrete Time Signals Page---#
    def page_view(self):
        self.selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="View Signals", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:self.page_view_button_XSignal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:self.page_view_button_XSignal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:self.page_view_button_XSignal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:self.page_view_button_XSignal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:self.page_view_button_XSignal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)


        self.main_right_window_container.columnconfigure(0,weight=1)
        self.main_right_window_container.rowconfigure((0,8),weight=1)
        self.signal_displayt =ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"),anchor="e")
        self.signal_displayt.grid(row=1,column=0,pady=(20,10))
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=2,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.signal_display =ctk.CTkLabel(scrollable_frame, text = "None selected",font=("Arial",20,"bold"),wraplength=1300)
        self.signal_display.grid(row=1,column=1,pady=10)
        self.signal_display_sample =ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.signal_display_sample.grid(row=3,column=0,pady=10)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Clear selected signal", command=lambda:self.page_view_button_ClearSelectedSignal() if self.selected != None else None,width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=4,column=0,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Manual input signal",command=lambda:self.page_manual_input(self.selected) if self.selected != None else self.label_error.configure(text="Error : No selected signal to modify!"), width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=5,column=0,padx=10,pady=10)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Function input signal",command=lambda:self.page_view_function_input(self.selected) if self.selected != None else self.label_error.configure(text="Error : No selected signal to modify!"),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=6,column=0,padx=10,pady=10)
        self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
        self.label_error.grid(row=7,column=0,padx=10,pady=10)

    def page_view_function_input(self,discrete_signal_obj):
        self.selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=0)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(7,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="Function Input", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="Sine Wave", command=lambda:sine(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=20,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="Cosine Wave", command=lambda:cosine(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=20,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="Rectangular Pulse", command=lambda:rect(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=20,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="Triangular Pulse", command=lambda:trig(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=20,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="Unit Ramp", command=lambda:ramp(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=20,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="Unit Step", command=lambda:step(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=6,column=0,padx=20,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=8,column=0,padx=20,pady=10)

        def sine():

            self.main_right_window_container.destroy()
            self.main_right_window_container=ctk.CTkFrame(self.main_container)
            self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)

            self.main_right_window_container.rowconfigure((0,99),weight=1)
            self.main_right_window_container.columnconfigure((0,99),weight=1)
            text_val = "You are editing signal : "+ discrete_signal_obj.name
            self.label = ctk.CTkLabel(self.main_right_window_container, text=text_val, font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=1, column=1, padx=20, pady=(20, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="Sine Wave : A Sin(2πnf/fs + Φ) , for T0 < 0 < T1", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=2, column=1, padx=20, pady=(10, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="A (amplitude of sine wave) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=3, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_a = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_a.grid(row=3,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="f (frequency of sine wave in hz) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=4, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_f = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_f.grid(row=4,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S0 (Starting sample S0) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=5, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S0 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S0.grid(row=5,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S1 (Ending sample S1) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=6, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S1 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S1.grid(row=6,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="fs (sampling frequency in hz) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=7, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_fs = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_fs.grid(row=7,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="Φ (Phase shift in Radians) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=8, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_phase = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_phase.grid(row=8,column=2,pady=10)
            self.button = ctk.CTkButton(self.main_right_window_container, text="Generate Signal", command=lambda:calculate(),height=65,font=("Arial",20,"bold"),width=300)
            self.button.grid(row=9,column=1,padx=20,pady=10,columnspan=2)
            self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
            self.label_error.grid(row=10,column=1,columnspan=2,padx=0,pady=(20,10))
            
            
            def calculate():
                def error_check(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            float(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non floats!")
                            return True
                    else:   
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                def error_check_int(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            int(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non integers!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                if error_check(self.text_input_a.get('1.0','end').strip()):
                    return
                if error_check(self.text_input_f.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S0.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S1.get('1.0','end').strip()):
                    return
                if error_check(self.text_input_fs.get('1.0','end').strip()):
                    return
                if error_check(self.text_input_phase.get('1.0','end').strip()):
                    return
                
                var_a = float(self.text_input_a.get('1.0','end').strip())
                var_f = float(self.text_input_f.get('1.0','end').strip())
                var_S0 = int(self.text_input_S0.get('1.0','end').strip())
                var_S1 = int(self.text_input_S1.get('1.0','end').strip())
                var_fs = float(self.text_input_fs.get('1.0','end').strip())
                var_phase = float(self.text_input_phase.get('1.0','end').strip())
                if var_S0>var_S1:
                    self.label_error.configure(text="Error : Starting time cannot be late   r than end time!")
                    return
                if var_fs <=0:
                    self.label_error.configure(text="Error : Sampling frequency must be positive!")
                    return
                x=[]
                for n in range(int(var_S0),int(var_S1)+1):
                    x.append(var_a * math.sin((2 * math.pi * var_f * n /var_fs)+var_phase))
                discrete_signal_obj.left_val = var_S0
                discrete_signal_obj.value_sequence = list(x)
                self.label_error.configure(text="")
                return self.page_view()
        
        sine()

        def cosine():
            self.main_right_window_container.destroy()
            self.main_right_window_container=ctk.CTkFrame(self.main_container)
            self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)

            self.main_right_window_container.rowconfigure((0,99),weight=1)
            self.main_right_window_container.columnconfigure((0,99),weight=1)
            text_val = "You are editing signal : "+ discrete_signal_obj.name
            self.label = ctk.CTkLabel(self.main_right_window_container, text=text_val, font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=1, column=1, padx=20, pady=(20, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="Cosine Wave : A Cos(2πnf/fs + Φ) , for T0 < 0 < T1", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=2, column=1, padx=20, pady=(10, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="A (amplitude of coine wave) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=3, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_a = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_a.grid(row=3,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="f (frequency of cosine wave in hz) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=4, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_f = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_f.grid(row=4,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S0 (Starting time T0) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=5, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S0 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S0.grid(row=5,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S1 (Ending time T1) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=6, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S1 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S1.grid(row=6,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="fs (sampling frequency in hz) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=7, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_fs = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_fs.grid(row=7,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="Φ (Phase shift in Radians) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=8, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_phase = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_phase.grid(row=8,column=2,pady=10)
            self.button = ctk.CTkButton(self.main_right_window_container, text="Generate Signal", command=lambda:calculate(),height=65,font=("Arial",20,"bold"),width=300)
            self.button.grid(row=9,column=1,padx=20,pady=10,columnspan=2)
            self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
            self.label_error.grid(row=10,column=1,columnspan=2,padx=0,pady=(20,10))
            
            
            def calculate():
                def error_check(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            float(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non floats!")
                            return True
                    else:   
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                def error_check_int(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            int(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non integers!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                if error_check(self.text_input_a.get('1.0','end').strip()):
                    return
                if error_check(self.text_input_f.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S0.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S1.get('1.0','end').strip()):
                    return
                if error_check(self.text_input_fs.get('1.0','end').strip()):
                    return
                if error_check(self.text_input_phase.get('1.0','end').strip()):
                    return
                
                var_a = float(self.text_input_a.get('1.0','end').strip())
                var_f = float(self.text_input_f.get('1.0','end').strip())
                var_S0 = int(self.text_input_S0.get('1.0','end').strip())
                var_S1 = int(self.text_input_S1.get('1.0','end').strip())
                var_fs = float(self.text_input_fs.get('1.0','end').strip())
                var_phase = float(self.text_input_phase.get('1.0','end').strip())
                if var_S0>var_S1:
                    self.label_error.configure(text="Error : Starting time cannot be late   r than end time!")
                    return
                if var_fs <=0:
                    self.label_error.configure(text="Error : Sampling frequency must be positive!")
                    return
                x=[]
                for n in range(int(var_S0),int(var_S1)+1):
                    x.append(var_a * math.cos((2 * math.pi * var_f * n /var_fs)+var_phase))
                discrete_signal_obj.left_val = var_S0
                discrete_signal_obj.value_sequence = list(x)
                self.label_error.configure(text="")
                return self.page_view()

        def rect():
            self.main_right_window_container.destroy()
            self.main_right_window_container=ctk.CTkFrame(self.main_container)
            self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
            
            self.main_right_window_container.rowconfigure((0,99),weight=1)
            self.main_right_window_container.columnconfigure((0,99),weight=1)
            text_val = "You are editing signal : "+ discrete_signal_obj.name
            self.label = ctk.CTkLabel(self.main_right_window_container, text=text_val, font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=1, column=1, padx=20, pady=(20, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="Rectangular Pulse : A Rect(n/N) = A for n <= |N/2| , 0 otherwise" , font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=2, column=1, padx=20, pady=(10, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="A (Amplitude) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=3, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_a = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_a.grid(row=3,column=2,pady=10,sticky="w")
            self.label = ctk.CTkLabel(self.main_right_window_container, text="N (Rectangle Width) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=4, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_N = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_N.grid(row=4,column=2,pady=10,sticky="w")
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S0 (Starting sample S0) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=5, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S0 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S0.grid(row=5,column=2,pady=10,sticky="w")
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S1 (Ending Sample S1) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=6, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S1 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S1.grid(row=6,column=2,pady=10,sticky="w")
            self.button = ctk.CTkButton(self.main_right_window_container, text="Generate Signal", command=lambda:calculate(),height=65,font=("Arial",20,"bold"),width=300)
            self.button.grid(row=7,column=1,padx=20,pady=10,columnspan=2)
            self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
            self.label_error.grid(row=9,column=1,columnspan=2,padx=0,pady=(20,10))

            def calculate():
                def error_check(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            float(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non floats!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                def error_check_int(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            int(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non integers!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                if error_check(self.text_input_a.get('1.0','end').strip()):
                    return
                if error_check(self.text_input_N.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S0.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S1.get('1.0','end').strip()):
                    return
                
                var_a = float(self.text_input_a.get('1.0','end').strip())   
                var_N = (float(self.text_input_N.get('1.0','end').strip()))
                var_S0 = int(self.text_input_S0.get('1.0','end').strip())
                var_S1 = int(self.text_input_S1.get('1.0','end').strip())
                if var_N<=0 :
                    self.label_error.configure(text="Error : N must be a postiive float!")
                    return
                if var_S0>var_S1:
                    self.label_error.configure(text="Error : Starting index cannot be greater than end index!")
                    return
                
                x=[]
                for n in range(var_S0,var_S1+1):
                    if n <= var_N/2 and n>=-var_N/2:
                        x.append(var_a)
                    else:
                        x.append(0)

                discrete_signal_obj.left_val = var_S0
                discrete_signal_obj.value_sequence = list(x)
                self.label_error.configure(text="")
                return self.page_view()

        def trig():
            self.main_right_window_container.destroy()
            self.main_right_window_container=ctk.CTkFrame(self.main_container)
            self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)

            self.main_right_window_container.rowconfigure((0,99),weight=1)
            self.main_right_window_container.columnconfigure((0,99),weight=1)
            text_val = "You are editing signal : "+ discrete_signal_obj.name
            self.label = ctk.CTkLabel(self.main_right_window_container, text=text_val, font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=1, column=1, padx=20, pady=(20, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="Triangular Pulse △[n] = A*(1-n/|N|) for |n| <= N , 0 otherwise", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=2, column=1, padx=20, pady=(10, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="A (Amplitude of triangular pulse) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=3, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_A = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_A.grid(row=3,column=2,pady=10,sticky="w")
            self.label = ctk.CTkLabel(self.main_right_window_container, text="N (Half Width of triangular pulse) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=4, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_N = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_N.grid(row=4,column=2,pady=10,sticky="w")
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S0 (Starting sample S0) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=5, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S0 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S0.grid(row=5,column=2,pady=10,sticky="w")
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S1 (Ending sample S1) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=6, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S1 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S1.grid(row=6,column=2,pady=10,sticky="w")
            self.button = ctk.CTkButton(self.main_right_window_container, text="Generate Signal", command=lambda:calculate(),height=65,font=("Arial",20,"bold"),width=300)
            self.button.grid(row=8,column=1,padx=20,pady=10,columnspan=2)
            self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
            self.label_error.grid(row=9,column=1,columnspan=2,padx=0,pady=(20,10))

            def calculate():
                def error_check(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            float(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non floats!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                def error_check_int(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            int(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non integers!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                if error_check(self.text_input_N.get('1.0','end').strip()):
                    return
                if error_check(self.text_input_A.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S0.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S1.get('1.0','end').strip()):
                    return
                var_N = (float(self.text_input_N.get('1.0','end').strip()))
                var_A = (float(self.text_input_A.get('1.0','end').strip()))
                var_S0 = int(self.text_input_S0.get('1.0','end').strip())
                var_S1 = int(self.text_input_S1.get('1.0','end').strip())
                if var_S0>var_S1:
                    self.label_error.configure(text="Error : Starting index cannot be greater than end index!")
                    return
                if var_N <=0:  
                    self.label_error.configure(text="Error : N must be a postiive float!")
                    return
                x=[]
                for n in range(var_S0,var_S1+1):
                    if -(var_N)<=n<=(var_N):
                        x.append(var_A*(1-(abs(n)/var_N)))
                    else:
                        x.append(0)

                discrete_signal_obj.left_val = var_S0
                discrete_signal_obj.value_sequence = list(x)
                self.label_error.configure(text="")
                return self.page_view()

        def ramp():
            self.main_right_window_container.destroy()
            self.main_right_window_container=ctk.CTkFrame(self.main_container)
            self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)

            self.main_right_window_container.rowconfigure((0,99),weight=1)
            self.main_right_window_container.columnconfigure((0,99),weight=1)
            text_val = "You are editing signal : "+ discrete_signal_obj.name
            self.label = ctk.CTkLabel(self.main_right_window_container, text=text_val, font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=1, column=1, padx=20, pady=(20, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="Unit Ramp : A r[n] = A*n for n >= 0 , 0 otherwise", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=2, column=1, padx=20, pady=(10, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="A (amplitude of unit ramp) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=3, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_a = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_a.grid(row=3,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S0 (Starting sample S0) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=4, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S0 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S0.grid(row=4,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S1 (Ending sample S1) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=5, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S1 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S1.grid(row=5,column=2,pady=10)
            self.button = ctk.CTkButton(self.main_right_window_container, text="Generate Signal", command=lambda:calculate(),height=65,font=("Arial",20,"bold"),width=300)
            self.button.grid(row=8,column=1,padx=20,pady=10,columnspan=2)
            self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
            self.label_error.grid(row=9,column=1,columnspan=2,padx=0,pady=(20,10))
            
            
            def calculate():
                def error_check(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            float(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non floats!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                def error_check_int(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            int(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non integers!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                if error_check(self.text_input_a.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S0.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S1.get('1.0','end').strip()):
                    return  
                
                var_a = float(self.text_input_a.get('1.0','end').strip())
                var_S0 = int(self.text_input_S0.get('1.0','end').strip())
                var_S1 = int(self.text_input_S1.get('1.0','end').strip())
                if var_S0>var_S1:
                    self.label_error.configure(text="Error : Starting index cannot be greater than end index!")
                    return
                x=[]
                for n in range(var_S0,var_S1+1):
                    if n >= 0:
                        x.append(var_a*n)
                    else:
                        x.append(0)

                discrete_signal_obj.left_val = var_S0
                discrete_signal_obj.value_sequence = list(x)
                self.label_error.configure(text="")
                return self.page_view()
        
        def step():
            self.main_right_window_container.destroy()
            self.main_right_window_container=ctk.CTkFrame(self.main_container)
            self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)

            self.main_right_window_container.rowconfigure((0,99),weight=1)
            self.main_right_window_container.columnconfigure((0,99),weight=1)
            text_val = "You are editing signal : "+ discrete_signal_obj.name
            self.label = ctk.CTkLabel(self.main_right_window_container, text=text_val, font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=1, column=1, padx=20, pady=(20, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="Unit Step : A u[n] = A for n >= 0 , 0 otherwise", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=2, column=1, padx=20, pady=(10, 10),columnspan=2)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="A (amplitude of unit ramp) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=3, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_a = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_a.grid(row=3,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S0 (Starting sample S0) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=4, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S0 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S0.grid(row=4,column=2,pady=10)
            self.label = ctk.CTkLabel(self.main_right_window_container, text="S1 (Ending sample S1) : ", font=ctk.CTkFont(size=30, weight="bold"))
            self.label.grid(row=5, column=1, padx=20, pady=(10, 10),sticky="e")
            self.text_input_S1 = ctk.CTkTextbox(self.main_right_window_container,height=50,font=("test",40),width=200,wrap='none')
            self.text_input_S1.grid(row=5,column=2,pady=10)
            self.button = ctk.CTkButton(self.main_right_window_container, text="Generate Signal", command=lambda:calculate(),height=65,font=("Arial",20,"bold"),width=300)
            self.button.grid(row=8,column=1,padx=20,pady=10,columnspan=2)
            self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
            self.label_error.grid(row=9,column=1,columnspan=2,padx=0,pady=(20,10))
            
            
            def calculate():
                def error_check(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            float(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non floats!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                def error_check_int(y):
                    y=y.strip()
                    if (y!=""):
                        try:
                            int(str(y))
                        except:
                            self.label_error.configure(text="Error : Field contains non integers!")
                            return True
                    else:
                        self.label_error.configure(text="Error : Field is empty!")
                        return True
                if error_check(self.text_input_a.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S0.get('1.0','end').strip()):
                    return
                if error_check_int(self.text_input_S1.get('1.0','end').strip()):
                    return  
                
                var_a = float(self.text_input_a.get('1.0','end').strip())
                var_S0 = int(self.text_input_S0.get('1.0','end').strip())
                var_S1 = int(self.text_input_S1.get('1.0','end').strip())
                if var_S0>var_S1:
                    self.label_error.configure(text="Error : Starting index cannot be greater than end index!")
                    return
                x=[]
                for n in range(var_S0,var_S1+1):
                    if n >= 0:
                        x.append(var_a)
                    else:
                        x.append(0)

                discrete_signal_obj.left_val = var_S0
                discrete_signal_obj.value_sequence = list(x)
                self.label_error.configure(text="")
                return self.page_view()
        
    def page_view_button_ClearSelectedSignal(self):
        self.selected.value_sequence=[]
        self.selected.left_val=None
        self.signal_display_sample.configure(text="Left most sample index: "+str(self.selected.left_val))
        self.signal_display.configure(text="Selected discrete time signal is empty")

    def page_view_button_XSignal(self,discrete_signal):
        self.label_error.configure(text="")
        self.selected = discrete_signal
        self.signal_display_sample.configure(text="")
        if discrete_signal.value_sequence!=[]:
            string="Signal = [ "
            for i in discrete_signal.value_sequence:
                string+=str(i)+" "
            string+="]"
        else:
            string = "Selected discrete time signal is empty"
        self.signal_display_sample.configure(text="Left most sample index: "+str(discrete_signal.left_val))
        self.signal_display.configure(text=string)
        self.signal_displayt.configure(text="Discrete time signal selected : "+str(discrete_signal.name))
        
    def page_manual_input(self,discrete_signal_obj):
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1) 
        self.main_left_window_container.rowconfigure(0,weight=1)
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_view(),height=65,font=("Arial",20,"bold"),width=290)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.signal_label = ctk.CTkLabel(self.main_right_window_container, text = "Enter the left most sample index N of the signal : " , font=ctk.CTkFont(size=40, weight="bold"))
        self.signal_label.grid(row=1,column=1,padx=0,pady=(20,10))
        self.main_right_window_container.columnconfigure((0,3),weight=1)
        self.main_right_window_container.rowconfigure((0,4),weight=1)
        self.text_input = ctk.CTkTextbox(self.main_right_window_container,height=100,font=("test",85),width=200,wrap='none')
        self.text_input.grid(row=1, column=2,padx=0,pady=(20,10),sticky="w")
        self.button = ctk.CTkButton(self.main_right_window_container, text = "Enter", command=lambda:self.page_manual_input_button_enter_index(discrete_signal_obj,self.text_input.get('1.0','end')),height=65,font=("Arial",20,"bold"),width=290)
        self.button.grid(row=2,column=1,columnspan=2,padx=0,pady=(20,10))
        self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
        self.label_error.grid(row=3,column=1,columnspan=2,padx=0,pady=(20,10))
        
    def page_manual_input_button_enter_index(self,z,y):
        y=y.strip()
        if (y!=""):
            try:
                int(str(y))
                return self.page_manual_input_array(z,y)
            except:
                self.label_error.configure(text="Error : Field contains non integers!")
        else:
            self.label_error.configure(text="Error : Field is empty!")

    def page_manual_input_array(self,discrete_signal_obj,n_index_input):
        temp_signal_array=[]
        curr_N = int(n_index_input)
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1) 
        self.main_left_window_container.rowconfigure(0,weight=1)
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_manual_input(discrete_signal_obj),height=65,font=("Arial",20,"bold"),width=290)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.main_right_window_container.columnconfigure((0,3),weight=1)
        self.main_right_window_container.rowconfigure((0,7),weight=1)
        self.signal_display_label = ctk.CTkLabel(self.main_right_window_container, text = "Current Signal (Unsaved): Empty", font=ctk.CTkFont(size=40, weight="bold"))
        self.signal_display_label.grid(row=1,column=1,padx=0,pady=(20,10),columnspan=2)
        self.signal_label = ctk.CTkLabel(self.main_right_window_container, text = "You are editing " +discrete_signal_obj.name+" with left most index value of "+str(curr_N), font=ctk.CTkFont(size=40, weight="bold"))
        self.signal_label.grid(row=2,column=1,padx=0,pady=(20,10),columnspan=2)
        self.index_label = ctk.CTkLabel(self.main_right_window_container, text = "Enter the value of X["+str(curr_N)+"]: " , font=ctk.CTkFont(size=40, weight="bold"))
        self.index_label.grid(row=3,column=1,padx=0,pady=(20,10),sticky="e")
        self.text_input_no = ctk.CTkTextbox(self.main_right_window_container,height=100,font=("test",85),wrap='none')
        self.text_input_no.grid(row=3, column=2,padx=0,pady=(20,10),sticky="w")
        self.button = ctk.CTkButton(self.main_right_window_container, text = "Enter", command=lambda:page_manual_input_array_button_text_validation(self.text_input_no.get('1.0','end')),height=65,font=("Arial",20,"bold"),width=290)
        self.button.grid(row=4,column=1, padx=0,pady=(20,10),columnspan=2)
        self.button = ctk.CTkButton(self.main_right_window_container, text = "Save to "+discrete_signal_obj.name, command= lambda:page_manual_input_array_button_save(discrete_signal_obj,n_index_input) ,height=65,font=("Arial",20,"bold"),width=290)
        self.button.grid(row=5,column=1, padx=0,pady=(20,10),columnspan=2)
        self.label_error = ctk.CTkLabel(self.main_right_window_container, text = "", font=ctk.CTkFont(size=20),text_color="red")
        self.label_error.grid(row=6,column=1,padx=0,pady=(20,10),columnspan=2)

        def page_manual_input_array_button_text_validation(text_input):
            nonlocal temp_signal_array 
            nonlocal curr_N
            text_input=text_input.strip()
            self.label_error.configure(text="")
            if (text_input!=""):
                try:
                    float(str(text_input))
                except:
                    self.label_error.configure(text="Error : Field contains non integers!")
                    return
                curr_N+=1
                self.text_input_no.delete('1.0','end')
                temp_signal_array+=[float(text_input)]
                self.index_label.configure(text="Enter the value of X["+str(curr_N)+"]: ")
                string="Current Signal (Unsaved) = [ "
                for i in temp_signal_array:
                    string+=str(i)+" "
                string+="]"
                self.signal_display_label.configure(text=string)
            else:
                self.label_error.configure(text="Error : Field is empty!")
        
        def page_manual_input_array_button_save(discrete_signal_obj,n_index_input):
            nonlocal temp_signal_array
            discrete_signal_obj.value_sequence=temp_signal_array
            discrete_signal_obj.left_val=n_index_input
            self.page_view()

    def page_energy(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="Energy", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_energy_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_energy_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_energy_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_energy_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_energy_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)
        
        self.main_right_window_container.columnconfigure((0,1),weight=1)
        self.main_right_window_container.rowconfigure((0,16),weight=1)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal Selected",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=10,columnspan=2)
        self.label_s1_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s1_name.grid(row=2,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=3,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.label_s1_valseq=ctk.CTkLabel(scrollable_frame, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s1_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s1_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s1_valleft.grid(row=4,column=0,padx=0,pady=10,columnspan=2)

        self.button = ctk.CTkButton(self.main_right_window_container, text="Calculate Energy", command=lambda:page_energy_button_calculate(),height=65,font=("Arial",20,"bold"),width=350)
        self.button.grid(row=5,column=0,padx=0,pady=10,columnspan=2)
        self.label_result=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"))
        self.label_result.grid(row=6, column=0,padx=0,pady=10, columnspan=2)
        self.label_error=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"),text_color="red")
        self.label_error.grid(row=7, column=0,padx=0,pady=10, columnspan=2)


        def page_energy_button_signal(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.label_s1_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s1_valseq.configure(text=string)
            else:
                self.label_s1_valseq.configure(text="Selected discrete signal is empty")
            self.label_s1_valleft.configure(text="Left most sample index: "+str(signal_selected.left_val))
        
        def page_energy_button_calculate():
            self.label_error.configure(text="")
            nonlocal signal_selected
            if signal_selected!=None:
                if signal_selected.value_sequence !=[]:
                    text_val = "Energy : "+str(signal_selected.energy())
                    self.label_result.configure(text=text_val)
                else:
                    self.label_error.configure(text="Error: Selected signal is empty")
            else:
                self.label_error.configure(text="Error: No signal selected")
    
    def page_power(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="Power", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_power_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_power_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_power_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_power_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_power_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)
        
        self.main_right_window_container.columnconfigure((0,1),weight=1)
        self.main_right_window_container.rowconfigure((0,16),weight=1)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal Selected",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=10,columnspan=2)
        self.label_s1_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s1_name.grid(row=2,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=3,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.label_s1_valseq=ctk.CTkLabel(scrollable_frame, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s1_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s1_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s1_valleft.grid(row=4,column=0,padx=0,pady=10,columnspan=2)

        self.button = ctk.CTkButton(self.main_right_window_container, text="Calculate Power", command=lambda:page_power_button_calculate(),height=65,font=("Arial",20,"bold"),width=350)
        self.button.grid(row=5,column=0,padx=0,pady=10,columnspan=2)
        self.label_result=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"))
        self.label_result.grid(row=6, column=0,padx=0,pady=10, columnspan=2)
        self.label_error=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"),text_color="red")
        self.label_error.grid(row=7, column=0,padx=0,pady=10, columnspan=2)


        def page_power_button_signal(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.label_s1_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s1_valseq.configure(text=string)
            else:
                self.label_s1_valseq.configure(text="Selected discrete signal is empty")
            self.label_s1_valleft.configure(text="Left most sample index: "+str(signal_selected.left_val))
        
        def page_power_button_calculate():
            self.label_error.configure(text="")
            nonlocal signal_selected
            if signal_selected!=None:
                if signal_selected.value_sequence !=[]:
                    text_val = "Power : "+str(signal_selected.power())
                    self.label_result.configure(text=text_val)
                else:
                    self.label_error.configure(text="Error: Selected signal is empty")
            else:
                self.label_error.configure(text="Error: No signal selected")
    

    def page_time_shifting(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="Time Shifting", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_time_shifting_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_time_shifting_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_time_shifting_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_time_shifting_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_time_shifting_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)

        self.main_right_window_container.columnconfigure((0,3),weight=1)
        self.main_right_window_container.rowconfigure((1,2,3,4,5,6), weight=0)
        self.main_right_window_container.rowconfigure(0,weight=2)
        self.main_right_window_container.rowconfigure(8,weight=3)
        self.signal_displayt =ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"),anchor="e")
        self.signal_displayt.grid(row=1,column=1,pady=(20,10),columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=2,column=0,columnspan=4,sticky="ew", padx=10)
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.signal_display =ctk.CTkLabel(scrollable_frame, text = "None selected",font=("Arial",20,"bold"),wraplength=1300)
        self.signal_display.grid(row=1,column=1,pady=10)
        self.signal_display_sample =ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.signal_display_sample.grid(row=3,column=1,pady=10,columnspan=2)
        self.signal_display_text =ctk.CTkLabel(self.main_right_window_container, text = "Apply shift of X[N-K], K: ",font=("Arial",50,"bold"))
        self.signal_display_text.grid(row=4,column=1,pady=10)
        self.text_input = ctk.CTkTextbox(self.main_right_window_container,height=100,font=("test",85),width=200,wrap='none')
        self.text_input.grid(row=4,column=2,pady=10)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Enter",command=lambda:page_time_shifting_enter_signal(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=5,column=1,padx=10,pady=10,columnspan=2)
        self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
        self.label_error.grid(row=6,column=1,padx=10,pady=10,columnspan=2)

        def page_time_shifting_button_signal(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.signal_displayt.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.signal_display.configure(text=string)
            else:
                self.signal_display.configure(text="Selected discrete signal is empty")
            self.signal_display_sample.configure(text="Left most sample index: "+str(signal_selected.left_val))
        
        def page_time_shifting_enter_signal():
            self.label_error.configure(text="")
            text_input=self.text_input.get('1.0','end').strip()
            if (text_input!=""):
                try:
                    int(str(text_input))
                except:
                    self.label_error.configure(text="Error : Field contains non integers!")
                    return
            else:
                self.label_error.configure(text="Error : Field is empty!")
                return
            if (signal_selected==None):
                self.label_error.configure(text="Error: No signal selected")
                return
            else: 
                if(signal_selected.value_sequence==[]):
                    self.label_error.configure(text="Error: Signal selected is empty")
                    return
                else: 
                    signal_selected.time_shift(text_input)
                    self.text_input.delete('1.0','end')
                    self.signal_display_sample.configure(text="Left most sample index: "+str(signal_selected.left_val))

    def page_time_scaling(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="Time Scaling", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_time_scaling_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_time_scaling_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_time_scaling_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_time_scaling_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_time_scaling_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)

        self.main_right_window_container.columnconfigure((0,7),weight=1)
        self.main_right_window_container.rowconfigure((1,2,3,4,5,6), weight=0)
        self.main_right_window_container.rowconfigure(0,weight=2)
        self.main_right_window_container.rowconfigure(8,weight=3)
        self.signal_displayt =ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"),anchor="e")
        self.signal_displayt.grid(row=1,column=1,pady=(20,10),columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=2,column=0,columnspan=78,sticky="ew", padx=10)
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.signal_display =ctk.CTkLabel(scrollable_frame, text = "None selected",font=("Arial",20,"bold"),wraplength=1300)
        self.signal_display.grid(row=1,column=1,pady=10)
        self.signal_display_sample =ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.signal_display_sample.grid(row=3,column=1,pady=10,columnspan=2)
        self.signal_display_text =ctk.CTkLabel(self.main_right_window_container, text = "Apply shift of X[N/K], K: ",font=("Arial",50,"bold"))
        self.signal_display_text.grid(row=4,column=1,pady=10)
        self.text_input = ctk.CTkTextbox(self.main_right_window_container,height=100,font=("test",85),width=200,wrap='none')
        self.text_input.grid(row=4,column=2,pady=10)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Enter",command=lambda:page_time_scaling_enter_signal(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=5,column=1,padx=10,pady=10,columnspan=2)
        self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
        self.label_error.grid(row=6,column=1,padx=10,pady=10,columnspan=2)

        def page_time_scaling_button_signal(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.signal_displayt.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.signal_display.configure(text=string)
            else:
                self.signal_display.configure(text="Selected discrete signal is empty")
            self.signal_display_sample.configure(text="Left most sample index: "+str(signal_selected.left_val))

        def page_time_scaling_enter_signal():
            self.label_error.configure(text="")
            text_input=self.text_input.get('1.0','end').strip()
            if (text_input!=""):
                try:
                    float(str(text_input))
                except:
                    self.label_error.configure(text="Error : Field contains non numbers!")
                    return
            else:
                self.label_error.configure(text="Error : Field is empty!")
                return
            if (signal_selected==None):
                self.label_error.configure(text="Error: No signal selected")
                return
            else: 
                if(signal_selected.value_sequence==[]):
                    self.label_error.configure(text="Error: Signal selected is empty")
                    return
                else: 
                    string=signal_selected.name+" = [ "
                    signal_selected.time_scale(text_input)
                    self.text_input.delete('1.0','end')
                    self.signal_display_sample.configure(text="Left most sample index: "+str(signal_selected.left_val))
                    for i in signal_selected.value_sequence:
                        string+=str(i)+" "
                    string+="]"
                    self.signal_display.configure(text=string)

    def page_amplitude_shifting(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="DC Shift", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_time_shifting_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_time_shifting_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_time_shifting_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_time_shifting_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_time_shifting_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)

        self.main_right_window_container.columnconfigure((0,7),weight=1)
        self.main_right_window_container.rowconfigure((1,2,3,4,5,6), weight=0)
        self.main_right_window_container.rowconfigure(0,weight=2)
        self.main_right_window_container.rowconfigure(8,weight=3)
        self.signal_displayt =ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"),anchor="e")
        self.signal_displayt.grid(row=1,column=1,pady=(20,10),columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=2,column=0,columnspan=8, padx=10,sticky="ew")
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.signal_display =ctk.CTkLabel(scrollable_frame, text = "None selected",font=("Arial",20,"bold"),wraplength=1300)
        self.signal_display.grid(row=1,column=1,pady=10)
        self.signal_display_sample =ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.signal_display_sample.grid(row=3,column=1,pady=10,columnspan=2)    
        self.signal_display_text =ctk.CTkLabel(self.main_right_window_container, text = "Apply shift of X[N]+K, K: ",font=("Arial",50,"bold"))
        self.signal_display_text.grid(row=4,column=1,pady=10)
        self.text_input = ctk.CTkTextbox(self.main_right_window_container,height=100,font=("test",85),width=200,wrap='none')
        self.text_input.grid(row=4,column=2,pady=10)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Enter",command=lambda:page_time_shifting_enter_signal(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=5,column=1,padx=10,pady=10,columnspan=2)
        self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
        self.label_error.grid(row=6,column=1,padx=10,pady=10,columnspan=2)

        def page_time_shifting_button_signal(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.signal_displayt.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.signal_display.configure(text=string)
            else:
                self.signal_display.configure(text="Selected discrete signal is empty")
            self.signal_display_sample.configure(text="Left most sample index: "+str(signal_selected.left_val))

        def page_time_shifting_enter_signal():
            self.label_error.configure(text="")
            text_input=self.text_input.get('1.0','end').strip()
            if (text_input!=""):
                try:
                    float(str(text_input))
                except:
                    self.label_error.configure(text="Error : Field contains non numbers!")
                    return
            else:
                self.label_error.configure(text="Error : Field is empty!")
                return
            if (signal_selected==None):
                self.label_error.configure(text="Error: No signal selected")
                return
            else:
                if(signal_selected.value_sequence==[]):
                    self.label_error.configure(text="Error: Signal selected is empty")
                    return
                else: 
                    string=signal_selected.name+" = [ "
                    signal_selected.amplitude_shift(text_input)
                    self.text_input.delete('1.0','end')
                    for i in signal_selected.value_sequence:
                        string+=str(i)+" "
                    string+="]"
                    self.signal_display.configure(text=string)

    def page_amplitude_scaling(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="Amplitude Scaling", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_time_scaling_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_time_scaling_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_time_scaling_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_time_scaling_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_time_scaling_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)

        self.main_right_window_container.columnconfigure((0,7),weight=1)
        self.main_right_window_container.rowconfigure((1,2,3,4,5,6), weight=0)
        self.main_right_window_container.rowconfigure(0,weight=2)
        self.main_right_window_container.rowconfigure(8,weight=3)
        self.signal_displayt =ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"),anchor="e")
        self.signal_displayt.grid(row=1,column=1,pady=(20,10),columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=2,column=0,columnspan=8, padx=10,sticky="ew")
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.signal_display =ctk.CTkLabel(scrollable_frame, text = "None selected",font=("Arial",20,"bold"))
        self.signal_display.grid(row=1,column=1,pady=10)
        self.signal_display_sample =ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.signal_display_sample.grid(row=3,column=1,pady=10,columnspan=2)
        self.signal_display_text =ctk.CTkLabel(self.main_right_window_container, text = "Apply shift of KX[N], K: ",font=("Arial",50,"bold"))
        self.signal_display_text.grid(row=4,column=1,pady=10)
        self.text_input = ctk.CTkTextbox(self.main_right_window_container,height=100,font=("test",85),width=200,wrap='none')
        self.text_input.grid(row=4,column=2,pady=10)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Enter",command=lambda:page_time_scaling_enter_signal(),width=400,height=65,font=("Arial",20,"bold"))
        self.button.grid(row=5,column=1,padx=10,pady=10,columnspan=2)
        self.label_error = ctk.CTkLabel(self.main_right_window_container,text="", font=ctk.CTkFont(size=20),text_color="red")
        self.label_error.grid(row=6,column=1,padx=10,pady=10,columnspan=2)

        def page_time_scaling_button_signal(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.signal_displayt.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.signal_display.configure(text=string)
            else:
                self.signal_display.configure(text="Selected discrete signal is empty")
            self.signal_display_sample.configure(text="Left most sample index: "+str(signal_selected.left_val))

        def page_time_scaling_enter_signal():
            self.label_error.configure(text="")
            text_input=self.text_input.get('1.0','end').strip()
            if (text_input!=""):
                try:
                    float(str(text_input))
                except:
                    self.label_error.configure(text="Error : Field contains non numbers!")
                    return
            else:
                self.label_error.configure(text="Error : Field is empty!")
                return
            if (signal_selected==None):
                self.label_error.configure(text="Error: No signal selected")
                return
            else:
                if(signal_selected.value_sequence==[]):
                    self.label_error.configure(text="Error: Signal selected is empty")
                    return
                else: 
                    string=signal_selected.name+" = [ "
                    signal_selected.amplitude_scale(text_input)
                    self.text_input.delete('1.0','end')
                    for i in signal_selected.value_sequence:
                        string+=str(i)+" "
                    string+="]"
                    self.signal_display.configure(text=string)

    def page_convolution(self):
        signal1_selected = None
        signal2_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1) 
        self.main_container.columnconfigure(1,weight=1)
        self.main_container.columnconfigure(2,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_middle_window_container=ctk.CTkFrame(self.main_container)
        self.main_middle_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=2,sticky="nsew",padx=10,pady=10)

        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(7,weight=1)
        self.label=ctk.CTkLabel(self.main_left_window_container, text = "Signal 1",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_convolution_button_signal1(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_convolution_button_signal1(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_convolution_button_signal1(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_convolution_button_signal1(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_convolution_button_signal1(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=6,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=8,column=0,padx=0,pady=10)

        self.main_middle_window_container.columnconfigure(0,weight=1)
        self.main_middle_window_container.rowconfigure(7,weight=1)
        self.label=ctk.CTkLabel(self.main_middle_window_container, text = "Signal 2",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X1[N]", command=lambda:page_convolution_button_signal2(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X2[N]", command=lambda:page_convolution_button_signal2(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X3[N]", command=lambda:page_convolution_button_signal2(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X4[N]", command=lambda:page_convolution_button_signal2(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X5[N]", command=lambda:page_convolution_button_signal2(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=6,column=0,padx=0,pady=10) 

        self.main_right_window_container.columnconfigure((0,1),weight=1)
        self.main_right_window_container.rowconfigure((0,16),weight=1)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal 1",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=10,columnspan=2)
        self.label_s1_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s1_name.grid(row=2,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=3,column=0,columnspan=2, padx=10,sticky="ew")
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.label_s1_valseq=ctk.CTkLabel(scrollable_frame, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s1_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s1_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s1_valleft.grid(row=4,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal 2",font=("Arial",20,"bold"))
        self.label.grid(row=5,column=0,padx=0,pady=10,columnspan=2)
        self.label_s2_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s2_name.grid(row=6,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame_1 = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame_1.grid(row=7,column=0,columnspan=2, padx=10 ,sticky="ew")
        scrollable_frame_1.rowconfigure((0,2),weight=1)
        scrollable_frame_1.columnconfigure((0,2),weight=1)
        scrollable_frame_1._scrollbar.configure(height=0)
        self.label_s2_valseq=ctk.CTkLabel(scrollable_frame_1, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s2_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s2_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s2_valleft.grid(row=8,column=0,padx=0,pady=10,columnspan=2)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Perform Convolution", command=lambda:page_convolution_button_convolution(),height=65,font=("Arial",20,"bold"),width=250)
        self.button.grid(row=9,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Resultant Signal : Convolution of Signal 1 and Signal 2, S1 * S2",font=("Arial",20,"bold"))
        self.label.grid(row=10,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame_2 = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame_2.grid(row=11,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame_2.rowconfigure((0,2),weight=1)
        scrollable_frame_2.columnconfigure((0,2),weight=1)
        scrollable_frame_2._scrollbar.configure(height=0)
        self.label_c_valseq=ctk.CTkLabel(scrollable_frame_2, text = "No Signal Generated",font=("Arial",20,"bold"),wraplength=1300)
        self.label_c_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_c_val_left=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_c_val_left.grid(row=12,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Save to: ",font=("Arial",20,"bold"))
        self.label.grid(row=13,column=0,padx=0,pady=10,sticky="e")
        self.combobox=ctk.CTkComboBox(self.main_right_window_container, state="readonly" ,values=["X1[N]", "X2[N]", "X3[N]", "X4[N]", "X5[N]"])
        self.combobox.set("X1[N]")
        self.combobox.grid(row=13,column=1,padx=0,pady=10,sticky="w")
        self.button = ctk.CTkButton(self.main_right_window_container, text="Save", height=65,font=("Arial",20,"bold"),width=250,command=lambda:page_convolution_button_save())
        self.button.grid(row=14,column=0,padx=0,pady=10,columnspan=2)
        self.label_error=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"),text_color="red")
        self.label_error.grid(row=15, column=0,padx=0,pady=10, columnspan=2)
        
        def page_convolution_button_signal1(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal1_selected
            signal1_selected=discrete_signal_obj
            self.label_s1_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal1_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal1_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s1_valseq.configure(text=string)
            else:
                self.label_s1_valseq.configure(text="Selected discrete signal is empty")
            self.label_s1_valleft.configure(text="Left most sample index: "+str(signal1_selected.left_val))

        def page_convolution_button_signal2(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal2_selected
            signal2_selected=discrete_signal_obj
            self.label_s2_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal2_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal2_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s2_valseq.configure(text=string)
                self.label_error.configure(text="")
            else:
                self.label_s2_valseq.configure(text="Selected discrete signal is empty")
            self.label_s2_valleft.configure(text="Left most sample index: "+str(signal2_selected.left_val))
        
        def page_convolution_button_convolution():
            nonlocal signal1_selected
            nonlocal signal2_selected
            if (signal1_selected!=None and signal2_selected!=None):
                if(signal1_selected.value_sequence != [] and signal2_selected.value_sequence !=[]):
                    self.Convolution_GLOBAL.left_val,self.Convolution_GLOBAL.value_sequence=signal1_selected.convolution(signal1_selected,signal2_selected)
                    string="Convolution Result"+" = [ "
                    for i in self.Convolution_GLOBAL.value_sequence:
                        string+=str(i)+" "
                    string+="]" 
                    self.label_c_valseq.configure(text=string)
                    self.label_c_val_left.configure(text="Left most sample index: "+ str(self.Convolution_GLOBAL.left_val))
                else:
                    self.label_error.configure(text="Error: Signal(s) selected are empty")
            else:
                self.label_error.configure(text="Error: Signal(s) are unselected")
                
        def page_convolution_button_save():
            x= self.combobox.get()
            if(x=="X1[N]"):
                self.X1.left_val,self.X1.value_sequence=self.Convolution_GLOBAL.left_val,self.Convolution_GLOBAL.value_sequence
            elif(x=="X2[N]"):
                self.X2.left_val,self.X2.value_sequence=self.Convolution_GLOBAL.left_val,self.Convolution_GLOBAL.value_sequence
            elif(x=="X3[N]"): 
                self.X3.left_val,self.X3.value_sequence=self.Convolution_GLOBAL.left_val,self.Convolution_GLOBAL.value_sequence
            elif(x=="X4[N]"):
                self.X4.left_val,self.X4.value_sequence=self.Convolution_GLOBAL.left_val,self.Convolution_GLOBAL.value_sequence
            elif(x=="X5[N]"):
                self.X5.left_val,self.X5.value_sequence=self.Convolution_GLOBAL.left_val,self.Convolution_GLOBAL.value_sequence

    
    def page_auto_correlation(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="Auto Correlation", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_auto_correlation_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_auto_correlation_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_auto_correlation_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_auto_correlation_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_auto_correlation_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)
        
        self.main_right_window_container.columnconfigure((0,1),weight=1)
        self.main_right_window_container.rowconfigure((0,16),weight=1)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal Selected",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=10,columnspan=2)
        self.label_s1_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s1_name.grid(row=2,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=3,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.label_s1_valseq=ctk.CTkLabel(scrollable_frame, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s1_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s1_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s1_valleft.grid(row=4,column=0,padx=0,pady=10,columnspan=2)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Perform Auto Correlation", command=lambda:page_auto_correlation_button_auto_correlation(),height=65,font=("Arial",20,"bold"),width=350)
        self.button.grid(row=9,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Resultant Signal : Auto Correlation of Signal 1",font=("Arial",20,"bold"))
        self.label.grid(row=10,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame_2 = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame_2.grid(row=11,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame_2.rowconfigure((0,2),weight=1)
        scrollable_frame_2.columnconfigure((0,2),weight=1)
        scrollable_frame_2._scrollbar.configure(height=0)
        self.label_c_valseq=ctk.CTkLabel(scrollable_frame_2, text = "No Signal Generated",font=("Arial",20,"bold"),wraplength=1300)
        self.label_c_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_c_val_left=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_c_val_left.grid(row=12,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Save to: ",font=("Arial",20,"bold"))
        self.label.grid(row=13,column=0,padx=0,pady=10,sticky="e")
        self.combobox=ctk.CTkComboBox(self.main_right_window_container, state="readonly", values=["X1[N]", "X2[N]", "X3[N]", "X4[N]", "X5[N]"])
        self.combobox.set("X1[N]")
        self.combobox.grid(row=13,column=1,padx=0,pady=10,sticky="w")
        self.button = ctk.CTkButton(self.main_right_window_container, text="Save", height=65,font=("Arial",20,"bold"),width=350,command=lambda:page_auto_correlation_button_save())
        self.button.grid(row=14,column=0,padx=0,pady=10,columnspan=2)
        self.label_error=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"),text_color="red")
        self.label_error.grid(row=15, column=0,padx=0,pady=10, columnspan=2)
        

        def page_auto_correlation_button_signal(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.label_s1_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s1_valseq.configure(text=string)
            else:
                self.label_s1_valseq.configure(text="Selected discrete signal is empty")
            self.label_s1_valleft.configure(text="Left most sample index: "+str(signal_selected.left_val))

        def page_auto_correlation_button_auto_correlation():
            nonlocal signal_selected
            if (signal_selected!=None):
                if(signal_selected.value_sequence!=[]):
                    self.Auto_Correlation_GLOBAL.left_val,self.Auto_Correlation_GLOBAL.value_sequence=signal_selected.correlation(signal_selected,signal_selected)
                    string="Auto Correlation Result"+" = [ "
                    for i in self.Auto_Correlation_GLOBAL.value_sequence:
                        string+=str(i)+" "
                    string+="]" 
                    self.label_c_valseq.configure(text=string)
                    self.label_c_val_left.configure(text="Left most sample index: "+ str(self.Auto_Correlation_GLOBAL.left_val))
                    self.label_error.configure(text="")
                else:
                    self.label_error.configure(text="Error: Signal selected is empty")
            else:
                self.label_error.configure(text="Error: No Signal selected")

        def page_auto_correlation_button_save():
            x= self.combobox.get()
            if(x=="X1[N]"):
                self.X1.left_val,self.X1.value_sequence=self.Auto_Correlation_GLOBAL.left_val,self.Auto_Correlation_GLOBAL.value_sequence
            elif(x=="X2[N]"):
                self.X2.left_val,self.X2.value_sequence=self.Auto_Correlation_GLOBAL.left_val,self.Auto_Correlation_GLOBAL.value_sequence
            elif(x=="X3[N]"): 
                self.X3.left_val,self.X3.value_sequence=self.Auto_Correlation_GLOBAL.left_val,self.Auto_Correlation_GLOBAL.value_sequence
            elif(x=="X4[N]"):
                self.X4.left_val,self.X4.value_sequence=self.Auto_Correlation_GLOBAL.left_val,self.Auto_Correlation_GLOBAL.value_sequence
            elif(x=="X5[N]"):
                self.X5.left_val,self.X5.value_sequence=self.Auto_Correlation_GLOBAL.left_val,self.Auto_Correlation_GLOBAL.value_sequence

    def page_correlation(self):
        signal1_selected = None
        signal2_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1) 
        self.main_container.columnconfigure(1,weight=1)
        self.main_container.columnconfigure(2,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_middle_window_container=ctk.CTkFrame(self.main_container)
        self.main_middle_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=2,sticky="nsew",padx=10,pady=10)

        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(7,weight=1)
        self.label=ctk.CTkLabel(self.main_left_window_container, text = "Signal 1",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_correlation_button_signal1(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_correlation_button_signal1(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_correlation_button_signal1(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_correlation_button_signal1(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_correlation_button_signal1(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=6,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=8,column=0,padx=0,pady=10)

        self.main_middle_window_container.columnconfigure(0,weight=1)
        self.main_middle_window_container.rowconfigure(7,weight=1)
        self.label=ctk.CTkLabel(self.main_middle_window_container, text = "Signal 2",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X1[N]", command=lambda:page_correlation_button_signal2(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X2[N]", command=lambda:page_correlation_button_signal2(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X3[N]", command=lambda:page_correlation_button_signal2(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X4[N]", command=lambda:page_correlation_button_signal2(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X5[N]", command=lambda:page_correlation_button_signal2(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=6,column=0,padx=0,pady=10) 

        self.main_right_window_container.columnconfigure((0,1),weight=1)
        self.main_right_window_container.rowconfigure((0,16),weight=1)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal 1",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=10,columnspan=2)
        self.label_s1_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s1_name.grid(row=2,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=3,column=0,columnspan=2, padx=10,sticky="ew")
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.label_s1_valseq=ctk.CTkLabel(scrollable_frame, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s1_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s1_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s1_valleft.grid(row=4,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal 2",font=("Arial",20,"bold"))
        self.label.grid(row=5,column=0,padx=0,pady=10,columnspan=2)
        self.label_s2_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s2_name.grid(row=6,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame_1 = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame_1.grid(row=7,column=0,columnspan=2, padx=10,sticky="ew")
        scrollable_frame_1.rowconfigure((0,2),weight=1)
        scrollable_frame_1.columnconfigure((0,2),weight=1)
        scrollable_frame_1._scrollbar.configure(height=0)
        self.label_s2_valseq=ctk.CTkLabel(scrollable_frame_1, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s2_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s2_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s2_valleft.grid(row=8,column=0,padx=0,pady=10,columnspan=2)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Perform Cross Correlation", command=lambda:page_correlation_button_correlation(),height=65,font=("Arial",20,"bold"),width=250)
        self.button.grid(row=9,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Resultant Signal : Correlation of Signal 1 and Signal 2, S1 ● S2",font=("Arial",20,"bold"))
        self.label.grid(row=10,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame_2 = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame_2.grid(row=11,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame_2.rowconfigure((0,2),weight=1)
        scrollable_frame_2.columnconfigure((0,2),weight=1)
        scrollable_frame_2._scrollbar.configure(height=0)
        self.label_c_valseq=ctk.CTkLabel(scrollable_frame_2, text = "No Signal Generated",font=("Arial",20,"bold"),wraplength=1300)
        self.label_c_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_c_val_left=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_c_val_left.grid(row=12,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Save to: ",font=("Arial",20,"bold"))
        self.label.grid(row=13,column=0,padx=0,pady=10,sticky="e")
        self.combobox=ctk.CTkComboBox(self.main_right_window_container, state="readonly", values=["X1[N]", "X2[N]", "X3[N]", "X4[N]", "X5[N]"])
        self.combobox.set("X1[N]")
        self.combobox.grid(row=13,column=1,padx=0,pady=10,sticky="w")
        self.button = ctk.CTkButton(self.main_right_window_container, text="Save", height=65,font=("Arial",20,"bold"),width=250,command=lambda:page_correlation_button_save())
        self.button.grid(row=14,column=0,padx=0,pady=10,columnspan=2)
        self.label_error=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"),text_color="red")
        self.label_error.grid(row=15, column=0,padx=0,pady=10, columnspan=2)
        
        def page_correlation_button_signal1(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal1_selected
            signal1_selected=discrete_signal_obj
            self.label_s1_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal1_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal1_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s1_valseq.configure(text=string)
            else:
                self.label_s1_valseq.configure(text="Selected discrete signal is empty")
            self.label_s1_valleft.configure(text="Left most sample index: "+str(signal1_selected.left_val))

        def page_correlation_button_signal2(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal2_selected
            signal2_selected=discrete_signal_obj
            self.label_s2_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal2_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal2_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s2_valseq.configure(text=string)
            else:
                self.label_s2_valseq.configure(text="Selected discrete signal is empty")
            self.label_s2_valleft.configure(text="Left most sample index: "+str(signal2_selected.left_val))
        
        def page_correlation_button_correlation():
            nonlocal signal1_selected
            nonlocal signal2_selected
            if (signal1_selected!=None and signal2_selected!=None):
                if(signal1_selected.value_sequence != [] and signal2_selected.value_sequence !=[]):
                    self.Correlation_GLOBAL.left_val,self.Correlation_GLOBAL.value_sequence=signal1_selected.correlation(signal1_selected,signal2_selected)
                    string="Correlation Result"+" = [ "
                    for i in self.Correlation_GLOBAL.value_sequence:
                        string+=str(i)+" "
                    string+="]" 
                    self.label_c_valseq.configure(text=string)
                    self.label_c_val_left.configure(text="Left most sample index: "+ str(self.Correlation_GLOBAL.left_val))
                    self.label_error.configure(text="")
                else:
                    self.label_error.configure(text="Error: Signal(s) selected are empty")
            else:
                self.label_error.configure(text="Error: Signal(s) are unselected")
                
        def page_correlation_button_save():
            x= self.combobox.get()
            if(x=="X1[N]"):
                self.X1.left_val,self.X1.value_sequence=self.Correlation_GLOBAL.left_val,self.Correlation_GLOBAL.value_sequence
            elif(x=="X2[N]"):
                self.X2.left_val,self.X2.value_sequence=self.Correlation_GLOBAL.left_val,self.Correlation_GLOBAL.value_sequence
            elif(x=="X3[N]"): 
                self.X3.left_val,self.X3.value_sequence=self.Correlation_GLOBAL.left_val,self.Correlation_GLOBAL.value_sequence
            elif(x=="X4[N]"):
                self.X4.left_val,self.X4.value_sequence=self.Correlation_GLOBAL.left_val,self.Correlation_GLOBAL.value_sequence
            elif(x=="X5[N]"):
                self.X5.left_val,self.X5.value_sequence=self.Correlation_GLOBAL.left_val,self.Correlation_GLOBAL.value_sequence
    
    def page_plot_signal(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="Plot Signal", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_plot_signal_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_plot_signal_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_plot_signal_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_plot_signal_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_plot_signal_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)
    
        self.main_right_window_container.columnconfigure((0,1),weight=1)
        self.main_right_window_container.rowconfigure((0,16),weight=1)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal Selected",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=10,columnspan=2)
        self.label_s1_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s1_name.grid(row=2,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=3,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.label_s1_valseq=ctk.CTkLabel(scrollable_frame, text = "None Selected",font=("Arial",20,"bold") ,wraplength=1300)
        self.label_s1_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s1_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s1_valleft.grid(row=4,column=0,padx=0,pady=10,columnspan=2)

        self.button = ctk.CTkButton(self.main_right_window_container, text="Plot Graph", command=lambda:page_plot_signal_button_plot_signal(),height=65,font=("Arial",20,"bold"),width=350)
        self.button.grid(row=9,column=0,padx=0,pady=10,columnspan=2)
        self.label_error=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"),text_color="red")
        self.label_error.grid(row=10, column=0,padx=0,pady=10, columnspan=2)

        def page_plot_signal_button_signal(discrete_signal_obj):
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.label_s1_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s1_valseq.configure(text=string)
            else:
                self.label_s1_valseq.configure(text="Selected discrete signal is empty")
            self.label_s1_valleft.configure(text="Left most sample index: "+str(signal_selected.left_val))
        
        def page_plot_signal_button_plot_signal():
            nonlocal signal_selected
            if (signal_selected != None):
                if (signal_selected.value_sequence!=[]):
                    temp_coord_array = [i for i in range(int(signal_selected.left_val),int(signal_selected.left_val)+len(signal_selected.value_sequence))]
                    plot.clf()
                    plot.xlabel("Sample index n")
                    plot.ylabel("X[N]")
                    plot.title("Plot of Signal X[N]")
                    plot.stem(temp_coord_array,signal_selected.value_sequence) 
                    plot.show()
                else:
                    self.label_error.configure(text="Error: Signal selected is empty")
            else:
                self.label_error.configure(text="Error: No Signal selected")
            
    def page_elementary_operations(self):
        signal1_selected = None
        signal2_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1) 
        self.main_container.columnconfigure(1,weight=1)
        self.main_container.columnconfigure(2,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_middle_window_container=ctk.CTkFrame(self.main_container)
        self.main_middle_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=2,sticky="nsew",padx=10,pady=10)

        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(7,weight=1)
        self.label=ctk.CTkLabel(self.main_left_window_container, text = "Signal 1",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_elementary_operations_button_signal1(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_elementary_operations_button_signal1(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_elementary_operations_button_signal1(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_elementary_operations_button_signal1(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_elementary_operations_button_signal1(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=6,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=8,column=0,padx=0,pady=10)

        self.main_middle_window_container.columnconfigure(0,weight=1)
        self.main_middle_window_container.rowconfigure(7,weight=1)
        self.label=ctk.CTkLabel(self.main_middle_window_container, text = "Signal 2",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X1[N]", command=lambda:page_elementary_operations_button_signal2(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X2[N]", command=lambda:page_elementary_operations_button_signal2(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X3[N]", command=lambda:page_elementary_operations_button_signal2(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X4[N]", command=lambda:page_elementary_operations_button_signal2(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_middle_window_container, text="X5[N]", command=lambda:page_elementary_operations_button_signal2(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=6,column=0,padx=0,pady=10) 

        self.main_right_window_container.columnconfigure((0,1),weight=1)
        self.main_right_window_container.rowconfigure((0,18),weight=1)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal 1",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=10,columnspan=2)
        self.label_s1_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s1_name.grid(row=2,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=3,column=0,columnspan=2, padx=10,sticky="ew")
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.label_s1_valseq=ctk.CTkLabel(scrollable_frame, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s1_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s1_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s1_valleft.grid(row=4,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal 2",font=("Arial",20,"bold"))
        self.label.grid(row=5,column=0,padx=0,pady=10,columnspan=2)
        self.label_s2_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s2_name.grid(row=6,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame_1 = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame_1.grid(row=7,column=0,columnspan=2, padx=10,sticky="ew")
        scrollable_frame_1.rowconfigure((0,2),weight=1)
        scrollable_frame_1.columnconfigure((0,2),weight=1)
        scrollable_frame_1._scrollbar.configure(height=0)
        self.label_s2_valseq=ctk.CTkLabel(scrollable_frame_1, text = "None Selected",font=("Arial",20,"bold"),wraplength=1300)
        self.label_s2_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s2_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s2_valleft.grid(row=8,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Operation: ",font=("Arial",20,"bold"))
        self.label.grid(row=9,column=0,padx=0,pady=10,sticky="e")
        self.combobox_op=ctk.CTkComboBox(self.main_right_window_container, state="readonly", values=["+", "-", "*"])
        self.combobox_op.set("+")
        self.combobox_op.grid(row=9,column=1,padx=0,pady=10,sticky="w")
        self.button = ctk.CTkButton(self.main_right_window_container, text="Perform operation selected", command=lambda:page_elementary_operations_button_elementary_operations(),height=65,font=("Arial",20,"bold"),width=350)
        self.button.grid(row=10,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Resultant Signal : S1 (Operation Selected) S2",font=("Arial",20,"bold"))
        self.label.grid(row=11,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame_2 = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame_2.grid(row=12,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame_2.rowconfigure((0,2),weight=1)
        scrollable_frame_2.columnconfigure((0,2),weight=1)
        scrollable_frame_2._scrollbar.configure(height=0)
        self.label_c_valseq=ctk.CTkLabel(scrollable_frame_2, text = "No Signal Generated",font=("Arial",20,"bold"),wraplength=1300)
        self.label_c_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_c_val_left=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_c_val_left.grid(row=13,column=0,padx=0,pady=10,columnspan=2)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Save to: ",font=("Arial",20,"bold"))
        self.label.grid(row=14,column=0,padx=0,pady=10,sticky="e")
        self.combobox=ctk.CTkComboBox(self.main_right_window_container, state="readonly", values=["X1[N]", "X2[N]", "X3[N]", "X4[N]", "X5[N]"])
        self.combobox.set("X1[N]")
        self.combobox.grid(row=14,column=1,padx=0,pady=10,sticky="w")
        self.button = ctk.CTkButton(self.main_right_window_container, text="Save", height=65,font=("Arial",20,"bold"),width=350,command=lambda:page_elementary_operations_button_save())
        self.button.grid(row=15,column=0,padx=0,pady=10,columnspan=2)
        self.label_error=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"),text_color="red")
        self.label_error.grid(row=16, column=0,padx=0,pady=10, columnspan=2)
        
        def page_elementary_operations_button_signal1(discrete_signal_obj):
            nonlocal signal1_selected
            signal1_selected=discrete_signal_obj
            self.label_s1_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal1_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal1_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s1_valseq.configure(text=string)
            else:
                self.label_s1_valseq.configure(text="Selected discrete signal is empty")
            self.label_s1_valleft.configure(text="Left most sample index: "+str(signal1_selected.left_val))

        def page_elementary_operations_button_signal2(discrete_signal_obj):
            nonlocal signal2_selected
            signal2_selected=discrete_signal_obj
            self.label_s2_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal2_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal2_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s2_valseq.configure(text=string)
            else:
                self.label_s2_valseq.configure(text="Selected discrete signal is empty")
            self.label_s2_valleft.configure(text="Left most sample index: "+str(signal2_selected.left_val))
        
        def page_elementary_operations_button_elementary_operations():
            nonlocal signal1_selected
            nonlocal signal2_selected
            if (signal1_selected!=None and signal2_selected!=None):
                if(signal1_selected.value_sequence != [] and signal2_selected.value_sequence !=[]):
                    self.elementary_operations_GLOBAL.left_val,self.elementary_operations_GLOBAL.value_sequence=signal1_selected.elementary_operations(signal1_selected,signal2_selected,self.combobox_op.get())
                    string="New Signal"+" = [ "
                    for i in self.elementary_operations_GLOBAL.value_sequence:
                        string+=str(i)+" "
                    string+="]" 
                    self.label_c_valseq.configure(text=string)
                    self.label_c_val_left.configure(text="Left most sample index: "+ str(self.elementary_operations_GLOBAL.left_val))
                else:
                    self.label_error.configure(text="Error: Signal(s) selected are empty")
            else:
                self.label_error.configure(text="Error: Signal(s) are unselected")
                
        def page_elementary_operations_button_save():
            x= self.combobox.get()
            if(x=="X1[N]"):
                self.X1.left_val,self.X1.value_sequence=self.elementary_operations_GLOBAL.left_val,self.elementary_operations_GLOBAL.value_sequence
            elif(x=="X2[N]"):
                self.X2.left_val,self.X2.value_sequence=self.elementary_operations_GLOBAL.left_val,self.elementary_operations_GLOBAL.value_sequence
            elif(x=="X3[N]"): 
                self.X3.left_val,self.X3.value_sequence=self.elementary_operations_GLOBAL.left_val,self.elementary_operations_GLOBAL.value_sequence
            elif(x=="X4[N]"):
                self.X4.left_val,self.X4.value_sequence=self.elementary_operations_GLOBAL.left_val,self.elementary_operations_GLOBAL.value_sequence
            elif(x=="X5[N]"):
                self.X5.left_val,self.X5.value_sequence=self.elementary_operations_GLOBAL.left_val,self.elementary_operations_GLOBAL.value_sequence

    def page_discrete_fourier_transform(self):
        signal_selected = None
        self.main_container.destroy()
        self.main_contained()
        self.main_container.rowconfigure(0,weight=1)
        self.main_container.columnconfigure(0,weight=1)
        self.main_container.columnconfigure(1,weight=20)
        self.main_left_window_container=ctk.CTkFrame(self.main_container)
        self.main_left_window_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.main_right_window_container=ctk.CTkFrame(self.main_container)
        self.main_right_window_container.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)
        self.main_left_window_container.columnconfigure(0,weight=1)
        self.main_left_window_container.rowconfigure(6,weight=1)
        self.label = ctk.CTkLabel(self.main_left_window_container, text="DTFT", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X1[N]", command=lambda:page_discrete_fourier_transform_button_signal(self.X1),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=1,column=0,padx=0,pady=(20,10))
        self.button = ctk.CTkButton(self.main_left_window_container, text="X2[N]", command=lambda:page_discrete_fourier_transform_button_signal(self.X2),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=2,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X3[N]", command=lambda:page_discrete_fourier_transform_button_signal(self.X3),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=3,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X4[N]", command=lambda:page_discrete_fourier_transform_button_signal(self.X4),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=4,column=0,padx=0,pady=10)
        self.button = ctk.CTkButton(self.main_left_window_container, text="X5[N]", command=lambda:page_discrete_fourier_transform_button_signal(self.X5),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=5,column=0,padx=0,pady=10) 
        self.button = ctk.CTkButton(self.main_left_window_container, text="Back", command=lambda:self.page_main_menu(),height=65,font=("Arial",20,"bold"),width=300)
        self.button.grid(row=7,column=0,padx=0,pady=10)
    
        self.main_right_window_container.columnconfigure((0,1),weight=1)
        self.main_right_window_container.rowconfigure((0,16),weight=1)
        self.label=ctk.CTkLabel(self.main_right_window_container, text = "Signal Selected",font=("Arial",20,"bold"))
        self.label.grid(row=1,column=0,padx=0,pady=10,columnspan=2)
        self.label_s1_name=ctk.CTkLabel(self.main_right_window_container, text = "Discrete time signal selected : None",font=("Arial",20,"bold"))
        self.label_s1_name.grid(row=2,column=0,padx=0,pady=10,columnspan=2)
        scrollable_frame = ctk.CTkScrollableFrame(self.main_right_window_container,height=50,fg_color="gray16")
        scrollable_frame.grid(row=3,column=0,columnspan=2,sticky="ew", padx=10)
        scrollable_frame.rowconfigure((0,2),weight=1)
        scrollable_frame.columnconfigure((0,2),weight=1)
        scrollable_frame._scrollbar.configure(height=0)
        self.label_s1_valseq=ctk.CTkLabel(scrollable_frame, text = "None Selected",font=("Arial",20,"bold") ,wraplength=1300)
        self.label_s1_valseq.grid(row=1,column=1,padx=0,pady=10)
        self.label_s1_valleft=ctk.CTkLabel(self.main_right_window_container, text = "Left most sample index: No Signal Selected",font=("Arial",20,"bold"))
        self.label_s1_valleft.grid(row=4,column=0,padx=0,pady=10,columnspan=2)

        self.button = ctk.CTkButton(self.main_right_window_container, text="Plot Graph", command=lambda:page_discrete_fourier_transform_button_plot_signal(),height=65,font=("Arial",20,"bold"),width=350)
        self.button.grid(row=9,column=0,padx=0,pady=10,columnspan=2)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Plot Magnitude Spectrum", command=lambda:page_discrete_fourier_transform_button_plot_magnitude_spectrum_signal(),height=65,font=("Arial",20,"bold"),width=350)
        self.button.grid(row=11,column=0,padx=0,pady=10,columnspan=2)
        self.button = ctk.CTkButton(self.main_right_window_container, text="Plot Phase spectrum", command=lambda:page_discrete_fourier_transform_button_plot_phase_spectrum_signal(),height=65,font=("Arial",20,"bold"),width=350)
        self.button.grid(row=12,column=0,padx=0,pady=10,columnspan=2)
        self.label_error=ctk.CTkLabel(self.main_right_window_container, text ="",font=("Arial",20,"bold"),text_color="red")
        self.label_error.grid(row=13, column=0,padx=0,pady=10, columnspan=2)

        def page_discrete_fourier_transform_button_signal(discrete_signal_obj):
            self.label_error.configure(text="")
            nonlocal signal_selected
            signal_selected=discrete_signal_obj
            self.label_s1_name.configure(text= "Discrete time signal selected: "+discrete_signal_obj.name)
            if(signal_selected.value_sequence !=[]):
                string=discrete_signal_obj.name+" = [ "
                for i in signal_selected.value_sequence:
                    string+=str(i)+" "
                string+="]"
                self.label_s1_valseq.configure(text=string)
            else:
                self.label_s1_valseq.configure(text="Selected discrete signal is empty")
            self.label_s1_valleft.configure(text="Left most sample index: "+str(signal_selected.left_val))
        
        def page_discrete_fourier_transform_button_plot_signal():
            nonlocal signal_selected
            if (signal_selected != None):
                if (signal_selected.value_sequence!=[]):
                    temp_coord_array = [i for i in range(int(signal_selected.left_val),int(signal_selected.left_val)+len(signal_selected.value_sequence))]
                    plot.clf()
                    plot.xlabel("Sample index n")
                    plot.ylabel("X[N]")
                    plot.title("Plot of Signal X[N]")
                    plot.stem(temp_coord_array,signal_selected.value_sequence) 
                    plot.show()
                else:
                    self.label_error.configure(text="Error: Signal selected is empty")
            else:
                self.label_error.configure(text="Error: No Signal selected")

        def page_discrete_fourier_transform_button_plot_magnitude_spectrum_signal():
            nonlocal signal_selected
            if signal_selected is not None:
                if signal_selected.value_sequence:
                    temp_coord_array = [i for i in range(int(signal_selected.left_val), int(signal_selected.left_val) + len(signal_selected.value_sequence))]
                    n = np.array(temp_coord_array)
                    x_n = np.array(signal_selected.value_sequence)
                    omega = np.linspace(-np.pi, np.pi, 10000, endpoint=False)
                    X_magnitude = np.zeros(len(omega))
                    for i, w in enumerate(omega):
                        dtft = np.sum(x_n * np.exp(-1j * w * n))  
                        X_magnitude[i] = np.abs(dtft)  
                    plot.clf()
                    plot.xlabel("Frequency (ω)")
                    plot.ylabel("Magnitude")
                    plot.title("magnitude spectrum (DTFT)")
                    plot.plot(omega, X_magnitude)
                    plot.grid(True)
                    plot.show()
                else:
                    self.label_error.configure(text="Error: Signal selected is empty")
            else:
                self.label_error.configure(text="Error: No Signal selected")

        def page_discrete_fourier_transform_button_plot_phase_spectrum_signal():
            nonlocal signal_selected
            if signal_selected is not None:
                if signal_selected.value_sequence:
                    temp_coord_array = [i for i in range(int(signal_selected.left_val), int(signal_selected.left_val) + len(signal_selected.value_sequence))]
                    n = np.array(temp_coord_array)
                    x_n = np.array(signal_selected.value_sequence)
                    omega = np.linspace(-np.pi, np.pi, 10000, endpoint=False)
                    X_omega = np.zeros(len(omega), dtype=complex)
                    for i, w in enumerate(omega):
                        X_omega[i] = np.sum(x_n * np.exp(-1j * w * n))
                    X_phase = np.unwrap(np.angle(X_omega))

                    plot.clf()
                    plot.xlabel("Frequency (ω)")
                    plot.ylabel("Phase (radians)")
                    plot.title("phase spectrum (DTFT)")
                    plot.plot(omega, X_phase)
                    plot.grid(True)
                    plot.show()
                else:
                    self.label_error.configure(text="Error: Signal selected is empty")
            else:
                self.label_error.configure(text="Error: No Signal selected")

app = App()
app.mainloop()