
import os
from pathlib import Path
from PIL import ImageColor as ColorSelectorPIL
from PIL import Image
import matplotlib.colors as ColorSelectorMPL
import customtkinter as ctk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser



# 
from barcode import Code128
from barcode.writer import ImageWriter

# QR Code
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.compat.pil import Image as pil_Image
# Style
from qrcode.image.styles.moduledrawers.pil import SquareModuleDrawer
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer
from qrcode.image.styles.moduledrawers.pil import HorizontalBarsDrawer
from qrcode.image.styles.moduledrawers.pil import VerticalBarsDrawer

# Color
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.colormasks import SquareGradiantColorMask
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from qrcode.image.styles.colormasks import ImageColorMask




class App(ctk.CTk):

    def __init__(self) -> None:
        ctk.set_appearance_mode("Dark") 
        ctk.set_default_color_theme("dark-blue")


        # Initialize Variables
        Width = 440 ;
        Height = 690 ;

        # Initialize Objects
        super().__init__()
        self.resizable(0,0)
        self.folder_path = os.path.join(os.path.dirname(__file__))
        self.title("QR & Bar Code Generator")   
        self.geometry(str(Width)+"x"+str(Height)+"+0+0")
        self.iconbitmap(os.path.join(self.folder_path,'MainIcon.ico')) # python
        # print(self.cget("fg_color"))
        self.Main_BG_color = self.cget("fg_color") # ['gray95', 'gray10']
        self.Button_BG_color = ['#3a7ebf', '#1f538d']
        self.Button_Font_color = ['#DCE4EE', '#DCE4EE']
        


        # 1
        # self.image_path = "D:\\Full_Codes\\Python\\QRCode\\Dynamic\\Me"
        self.MiddleImage = None
        self.ImageColorMaskPath = None


        # Localize Variables
        self.style_dict = {"Square Model":SquareModuleDrawer(),"Circle Model":CircleModuleDrawer(),"Rounded Model":RoundedModuleDrawer(),"Gapped Square":GappedSquareModuleDrawer(),"Horizontal Bars":HorizontalBarsDrawer(),"Vertical Bars":VerticalBarsDrawer()}
        self.style_list = list(self.style_dict.keys())
        self.combo31_var = ctk.StringVar(value=self.style_list[0])
        self.Stylish = self.style_dict[self.combo31_var.get()]

        self.color_dict = {"Solid Fill Color":0,"Radial Gradiant Color":1,"Square Gradiant Color":2,"Horizontal Gradiant Color":3,"Vertical Gradiant Color":4,"Image Color":5}
        self.color_list = list(self.color_dict.keys())
        self.combo32_var = ctk.StringVar(value=self.color_list[0])

        self.text11_var = ctk.StringVar(value="")
        self.text11_var.trace_add("write", self.update_label_box)

        self.check72_var = ctk.IntVar(value=0)
       
        
        ## Boxes
        self.label01 = ctk.CTkLabel(master=self,text=" Write Link/String:",font=('Consolas bold',10),width=30,height=30)
        self.label01.grid(row=0, column=0,columnspan=4,padx=(10,10), pady=(5, 5), sticky="nw")
        
        self.text11 = ctk.CTkEntry(master=self,font=('Consolas bold',12),textvariable=self.text11_var)
        self.text11.grid(row=1, column=0,columnspan=4, padx=(10,10), pady=(5, 5), sticky="w")
        self.text11.configure(width=Width-20,height=35)

        self.label21 = ctk.CTkLabel(master=self,text="Style Options:  ",font=('Consolas bold',10),width=30,height=30)
        self.label21.grid(row=2, column=0,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nw")
        self.blank22 = ctk.CTkButton(master=self,text="      Blank     ",font=('Consolas bold',10),width=30,height=30)
        self.blank22.grid(row=2, column=1,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nw")
        self.Blank(self.blank22)
        self.label23 = ctk.CTkLabel(master=self,text="Color Options:  ",font=('Consolas bold',10),width=30,height=30)
        self.label23.grid(row=2, column=2,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nw")
        self.blank24 = ctk.CTkButton(master=self,text="      Blank     ",font=('Consolas bold',10),width=30,height=30)
        self.blank24.grid(row=2, column=3,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nw")
        self.Blank(self.blank24)

        self.combo31 = ctk.CTkOptionMenu(master=self,font=('Times New Roman bold',12),width=40,height=30,dropdown_font=('Times New Roman',12),dynamic_resizing=True,)
        self.combo31.grid(row=3, column=0,columnspan=2,padx=(10,10), pady=(5, 5), sticky="nsew")

        self.combo32 = ctk.CTkOptionMenu(master=self,font=('Times New Roman bold',12),width=40,height=30,dropdown_font=('Times New Roman',12),dynamic_resizing=True)
        self.combo32.grid(row=3,column=2,columnspan=2,padx=(10,10), pady=(5, 5), sticky="nsew")

        self.button41 = ctk.CTkButton(master=self,text="Background Color",font=('Consolas bold',10),width=30,height=30)
        self.button41.grid(row=4, column=0,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.label42 = ctk.CTkLabel(master=self,text="                ",font=('Consolas bold',10),width=30,height=30)
        self.label42.grid(row=4, column=1,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")
        self.button43 = ctk.CTkButton(master=self,text="Background Color",font=('Consolas bold',10),width=30,height=30)
        self.button43.grid(row=4, column=2,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.label44 = ctk.CTkLabel(master=self,text="                ",font=('Consolas bold',10),width=30,height=30)
        self.label44.grid(row=4, column=3,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")
        
        self.button51 = ctk.CTkButton(master=self,text="Foreground Color",font=('Consolas bold',10),width=30,height=30)
        self.button51.grid(row=5, column=0,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.label52 = ctk.CTkLabel(master=self,text="                ",font=('Consolas bold',10),width=30,height=30)
        self.label52.grid(row=5, column=1,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")
        self.button53 = ctk.CTkButton(master=self,text="Foreground Color",font=('Consolas bold',10),width=30,height=30)
        self.button53.grid(row=5, column=2,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.label54 = ctk.CTkLabel(master=self,text="                ",font=('Consolas bold',10),width=30,height=30)
        self.label54.grid(row=5, column=3,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")

        self.button61 = ctk.CTkButton(master=self,text="Import Embed Image",font=('Consolas bold',8),width=30,height=30)
        self.button61.grid(row=6, column=0,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.button62 = ctk.CTkButton(master=self,text="Remove Embed Image",font=('Consolas bold',8),width=30,height=30)
        self.button62.grid(row=6, column=1,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")
        self.button63 = ctk.CTkButton(master=self,text="  Option Color  ",font=('Consolas bold',10),width=30,height=30)
        self.button63.grid(row=6, column=2,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.label64 = ctk.CTkLabel(master=self,text="                ",font=('Consolas bold',10),width=30,height=30)
        self.label64.grid(row=6, column=3,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")

        self.blank71 = ctk.CTkButton(master=self,text="      Blank     ",font=('Consolas bold',10),width=30,height=30)
        self.blank71.grid(row=7, column=0,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.Blank(self.blank71)
        self.check72 = ctk.CTkCheckBox(master=self,text="Preview Bar-Code To Generate",font=('Consolas bold',11),width=60,height=30)
        self.check72.grid(row=7, column=1,columnspan=2,padx=(5,10), pady=(5, 5), sticky="nsew")
        self.check72.configure(variable=self.check72_var)
        self.blank74 = ctk.CTkButton(master=self,text="      Blank     ",font=('Consolas bold',10),width=30,height=30)
        self.blank74.grid(row=7, column=3,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")
        self.Blank(self.blank74)

        self.label81 = ctk.CTkLabel(master=self, text="",font=('Times New Roman bold',40))
        self.label81.grid(row=8, column=0,columnspan=4, padx=(10,10), pady=(5, 5), sticky="nsew")

        self.blank91 = ctk.CTkButton(master=self,text="      Blank     ",font=('Consolas bold',10),width=30,height=30)
        self.blank91.grid(row=9, column=0,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.Blank(self.blank91)
        self.button92 = ctk.CTkButton(master=self,text=" Save Bar Code  ",font=('Consolas bold',10),width=30,height=30)
        self.button92.grid(row=9, column=1,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")
        self.button93 = ctk.CTkButton(master=self,text="  Save QR Code  ",font=('Consolas bold',10),width=30,height=30)
        self.button93.grid(row=9, column=2,columnspan=1,padx=(10,5), pady=(5, 5), sticky="nsew")
        self.blank94 = ctk.CTkButton(master=self,text="      Blank     ",font=('Consolas bold',10),width=30,height=30)
        self.blank94.grid(row=9, column=3,columnspan=1,padx=(5,10), pady=(5, 5), sticky="nsew")
        self.Blank(self.blank94)


        # Config and Bind
        self.combo31.configure(values=self.style_list,variable=self.combo31_var,command=self.Combo31_Changed)
        self.combo32.configure(values=self.color_list,variable=self.combo32_var,command=self.Combo32_Changed)
        self.button41.configure(command=self.Action41)
        self.label42.configure(bg_color=self.rgb_to_hex((255,255,255)))
        self.button43.configure(command=self.Action43)
        self.label44.configure(bg_color=self.rgb_to_hex((255,255,255)))
        self.button51.configure(command=self.Action51)
        self.label52.configure(bg_color=self.rgb_to_hex((0,0,0)))
        self.button53.configure(command=self.Action53)
        self.label54.configure(bg_color=self.rgb_to_hex((0,0,0)))
        self.button61.configure(command=self.Action61)
        self.button62.configure(command=self.Action62)
        self.button63.configure(command=self.Action63)
        self.label64.configure(bg_color=self.rgb_to_hex((0,0,255)))
        self.check72.configure(command=self.Action72)
        self.button92.configure(command=self.Action92)
        self.button93.configure(command=self.Action93)

        # Initialize
        self.Blank(self.button41)
        self.Blank(self.label42)
        self.Blank(self.button51)
        self.Blank(self.label52)
        self.Blank(self.button63)
        self.Blank(self.label64)
        self.Blank(self.button92)
        # Binding and Update
        self.update_bar_qr_code()

        

        

        

    # Events
    def Action41(self):
        color_code = colorchooser.askcolor(color=self.label42.cget("bg_color"),title = self.button41.cget("text"))
        if color_code[1] != None :
            self.label42.configure(bg_color=color_code[1],fg_color=color_code[1])
            self.update_bar_qr_code()

    def Action43(self):
        color_code = colorchooser.askcolor(color=self.label44.cget("bg_color"),title = self.button43.cget("text"))
        if color_code[1] != None :
            self.label44.configure(bg_color=color_code[1],fg_color=color_code[1])
            self.update_bar_qr_code()
    
    def Action51(self):
        color_code = colorchooser.askcolor(color=self.label52.cget("bg_color"),title = self.button51.cget("text"))
        if color_code[1] != None :
            self.label52.configure(bg_color=color_code[1],fg_color=color_code[1])
            self.update_bar_qr_code()

    def Action53(self):
        if self.combo32_var.get() == "Image Color":
            FileName = askopenfilename(title="Import Image to Foreground",defaultextension=".png",filetypes=[("Image Files", "*.png;*.jpg"),("Portable Network Graphic","*.png"),("Joint Photographic Group","*.jpg")])
            file_name, file_extension = os.path.splitext(FileName)
            if (FileName != None) and (file_extension == ".jpg" or file_extension == ".png"):
                self.ImageColorMaskPath = FileName
                self.update_bar_qr_code()
        else:
            color_code = colorchooser.askcolor(color=self.label54.cget("bg_color"),title = self.button53.cget("text"))
            if color_code[1] != None :
                self.label54.configure(bg_color=color_code[1],fg_color=color_code[1])
                self.update_bar_qr_code()
    
    def Action61(self):
        FileName = askopenfilename(title="Import Image to Embed in QR",defaultextension=".png",filetypes=[("Image Files", "*.png;*.jpg"),("Portable Network Graphic","*.png"),("Joint Photographic Group","*.jpg")])
        file_name, file_extension = os.path.splitext(FileName)
        if (FileName != None) and (file_extension == ".jpg" or file_extension == ".png"):
            self.button61.configure(text_color=self.rgb_to_hex((128,255,0)))
            self.MiddleImage = FileName
            self.update_bar_qr_code()

    def Action62(self):
        self.MiddleImage = None
        self.button61.configure(text_color=self.Button_Font_color) 
        self.update_bar_qr_code()
    
    def Action63(self):
        if self.combo32_var.get() == "Image Color":
            self.update_bar_qr_code()
        else:
            color_code = colorchooser.askcolor(color=self.label64.cget("bg_color"),title = self.button63.cget("text"))
            if color_code[1] != None :
                self.label64.configure(bg_color=color_code[1],fg_color=color_code[1])
                self.update_bar_qr_code()
    
    def Combo31_Changed(self,choice):
        self.Stylish = self.style_dict[self.combo31_var.get()]
        self.update_label_box()
    
    def Combo32_Changed(self,choice):
        # print("Changed:", self.combo32_var.get())
        if self.combo32_var.get() == "Radial Gradiant Color":
            self.Release(self.button43)
            self.button43.configure(text="Background Color")
            self.label44.configure(bg_color=self.rgb_to_hex((255, 255, 255)), fg_color=self.rgb_to_hex((255, 255, 255)))
            self.Release(self.button53)
            self.button53.configure(text="  Center Color  ")
            self.label54.configure(bg_color=self.rgb_to_hex((0, 0, 0)), fg_color=self.rgb_to_hex((0, 0, 0)))
            self.Release(self.button63)
            self.button63.configure(text="  Around Color  ")
            self.label64.configure(bg_color=self.rgb_to_hex((0, 0, 255)), fg_color=self.rgb_to_hex((0, 0, 255)))
        
        elif self.combo32_var.get() == "Square Gradiant Color":
            self.Release(self.button43)
            self.button43.configure(text="Background Color")
            self.label44.configure(bg_color=self.rgb_to_hex((255, 255, 255)), fg_color=self.rgb_to_hex((255, 255, 255)))
            self.Release(self.button53)
            self.button53.configure(text="  Center Color  ")
            self.label54.configure(bg_color=self.rgb_to_hex((0, 0, 0)), fg_color=self.rgb_to_hex((0, 0, 0)))
            self.Release(self.button63)
            self.button63.configure(text="  Around Color  ")
            self.label64.configure(bg_color=self.rgb_to_hex((0, 0, 255)), fg_color=self.rgb_to_hex((0, 0, 255)))
        
        elif self.combo32_var.get() == "Horizontal Gradiant Color":
            self.Release(self.button43)
            self.button43.configure(text="Background Color")
            self.label44.configure(bg_color=self.rgb_to_hex((255, 255, 255)), fg_color=self.rgb_to_hex((255, 255, 255)))
            self.Release(self.button53)
            self.button53.configure(text="   Left Color   ")
            self.label54.configure(bg_color=self.rgb_to_hex((0, 0, 0)), fg_color=self.rgb_to_hex((0, 0, 0)))
            self.Release(self.button63)
            self.button63.configure(text="  Right Color   ")
            self.label64.configure(bg_color=self.rgb_to_hex((0, 0, 255)), fg_color=self.rgb_to_hex((0, 0, 255)))

        elif self.combo32_var.get() == "Vertical Gradiant Color":
            self.Release(self.button43)
            self.button43.configure(text="Background Color")
            self.label44.configure(bg_color=self.rgb_to_hex((255, 255, 255)), fg_color=self.rgb_to_hex((255, 255, 255)))
            self.Release(self.button53)
            self.button53.configure(text="   Top Color    ")
            self.label54.configure(bg_color=self.rgb_to_hex((0, 0, 0)), fg_color=self.rgb_to_hex((0, 0, 0)))
            self.Release(self.button63)
            self.button63.configure(text="  Bottom Color  ")
            self.label64.configure(bg_color=self.rgb_to_hex((0, 0, 255)), fg_color=self.rgb_to_hex((0, 0, 255)))
        
        elif self.combo32_var.get() == "Image Color":
            self.Release(self.button43)
            self.button43.configure(text="Background Color")
            self.label44.configure(bg_color=self.rgb_to_hex((255, 255, 255)), fg_color=self.rgb_to_hex((255, 255, 255)))
            self.Release(self.button53)
            self.button53.configure(text="Foreground Image")
            self.Blank(self.label54)
            self.Blank(self.button63)
            self.Blank(self.label64)
            self.ImageColorMaskPath = None

        else:
            self.Release(self.button43)
            self.button43.configure(text="Background Color")
            self.label44.configure(bg_color=self.rgb_to_hex((255, 255, 255)), fg_color=self.rgb_to_hex((255, 255, 255)))
            self.Release(self.button53)
            self.button53.configure(text="Foreground Color")
            self.label54.configure(bg_color=self.rgb_to_hex((0, 0, 0)), fg_color=self.rgb_to_hex((0, 0, 0)))
            self.Blank(self.button63)
            self.Blank(self.label64)

        self.update_label_box()

    def Action72(self) :
        if self.check72_var.get() == 0 :
            # Generate Button
            self.Blank(self.button92)
            self.Release(self.button93)

            # Labels
            self.Release(self.label21)
            self.Release(self.label23)

            # CTkOptionMenu
            self.combo31.configure(state="normal")
            self.combo32.configure(state="normal") # disabled

            # Initilize Solid Fill Color
            self.combo32_var.set("Solid Fill Color")
            self.Release(self.button43)
            self.button43.configure(text="Background Color")
            self.label44.configure(bg_color=self.rgb_to_hex((255, 255, 255)), fg_color=self.rgb_to_hex((255, 255, 255)))
            self.Release(self.button53)
            self.button53.configure(text="Foreground Color")
            self.label54.configure(bg_color=self.rgb_to_hex((0, 0, 0)), fg_color=self.rgb_to_hex((0, 0, 0)))
            
            self.Release(self.button61)
            self.Release(self.button62)
            self.Blank(self.button63)
            self.Blank(self.label64)

            

            # On Bar
            self.Blank(self.button41)
            self.Blank(self.label42)
            self.Blank(self.button51)
            self.Blank(self.label52)
            
        else :
            # Generate Button
            self.Release(self.button92)
            self.Blank(self.button93)

            # Labels
            self.Blank(self.label21)
            self.label21.configure(text_color=self.Main_BG_color)
            self.Blank(self.label23)
            self.label23.configure(text_color=self.Main_BG_color)

            # CTkOptionMenu
            self.combo31.configure(state="disabled")
            self.combo32.configure(state="disabled")

            self.Blank(self.button43)
            self.Blank(self.label44)
            self.Blank(self.button53)
            self.Blank(self.label54)
            self.Blank(self.button63)
            self.Blank(self.label64)
            
            self.Blank(self.button61)
            self.Blank(self.button62)

            self.Release(self.button41)
            self.Release(self.label42)
            self.label42.configure(bg_color=self.rgb_to_hex((255, 255, 255)), fg_color=self.rgb_to_hex((255, 255, 255)))
            self.Release(self.button51)
            self.Release(self.label52)
            self.label52.configure(bg_color=self.rgb_to_hex((0, 0, 0)), fg_color=self.rgb_to_hex((0, 0, 0)))
        
        self.update_label_box()

    def Action92(self):
        if self.check72_var.get() == 1 :
            FileName = asksaveasfilename(title="Save Bar Code",defaultextension=".png",filetypes=[("Portable Network Graphic","*.png"),("Image Files", "*.png"),])
            file_name, file_extension = os.path.splitext(FileName)
            if (FileName != None) and (file_extension == ".png"):
                self.create_dynamic_bar_code(self.text11_var.get(),FileName)
                
    def Action93(self):
        if self.check72_var.get() == 0 :
            FileName = asksaveasfilename(title="Save QR Code",defaultextension=".png",filetypes=[("Portable Network Graphic","*.png"),("Joint Photographic Group","*.jpg"),("Image Files", "*.png;*.jpg"),])
            file_name, file_extension = os.path.splitext(FileName)
            if (FileName != None) and (file_extension.lower() == ".jpg" or file_extension == ".png"):
                self.crude_qr_image.save(FileName)
            
    # Properties
    def Blank(self,obj):
        if type(obj).__name__ == "CTkButton":
            obj.configure(state = "hidden",text_color=self.Main_BG_color,fg_color=self.Main_BG_color)
        if type(obj).__name__ == "CTkLabel":
            obj.configure(fg_color=self.Main_BG_color,bg_color=self.Main_BG_color)
    
    def Release(self,obj):
        if type(obj).__name__ == "CTkButton":
            obj.configure(state = "normal",text_color=self.Button_Font_color,fg_color=self.Button_BG_color)
        if type(obj).__name__ == "CTkLabel":
            obj.configure(state = "normal",text_color=self.Button_Font_color)

    # Methods
    def create_dynamic_qr_code(self,string):
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=1)
        qr.add_data(string)
        qr.make(fit=True)

        Stylish = self.Stylish

        Colorish = self.colorish_generator(self.combo32_var.get())

        Middlish = self.MiddleImage
        
        # A Picture For QR Code
        img_ = qr.make_image(image_factory=StyledPilImage,module_drawer=Stylish,color_mask=Colorish,embeded_image_path=Middlish)
        return img_

    def create_dynamic_bar_code(self,string,savefilepath):
        
        if (len(string) == 0) or (self.Check128ASCII(string) == False) :
            string = " "

        self.crude_bar_image = Code128(string, writer=ImageWriter())
        self.save_(savefilepath,self.label42.cget("bg_color"),self.label52.cget("bg_color")) 

        return savefilepath
    
    def save_(self,FileNamePath,BackgroundColor,ForegroundColor):
        file_name, file_extension = os.path.splitext(FileNamePath)
        self.crude_bar_image.save(file_name,{'background':BackgroundColor , 'foreground': ForegroundColor} )

    def Check128ASCII(self,Text):
        Flag = True
        for Char in Text:
            if ord(Char) > 128:
                Flag = False
        return Flag

    def colorish_generator(self,selected_color_option):
        
        if selected_color_option == "Radial Gradiant Color" :
            Colorish = RadialGradiantColorMask(back_color=self.hex_to_rgb(self.label44.cget("bg_color")),center_color=self.hex_to_rgb(self.label54.cget("bg_color")),edge_color=self.hex_to_rgb(self.label64.cget("bg_color")))
        
        elif selected_color_option == "Square Gradiant Color" :
            Colorish = SquareGradiantColorMask(back_color=self.hex_to_rgb(self.label44.cget("bg_color")),center_color=self.hex_to_rgb(self.label54.cget("bg_color")),edge_color=self.hex_to_rgb(self.label64.cget("bg_color")))
        
        elif selected_color_option == "Horizontal Gradiant Color" :
            Colorish = HorizontalGradiantColorMask(back_color=self.hex_to_rgb(self.label44.cget("bg_color")),left_color=self.hex_to_rgb(self.label54.cget("bg_color")),right_color=self.hex_to_rgb(self.label64.cget("bg_color")))

        elif selected_color_option == "Vertical Gradiant Color" :
            Colorish = VerticalGradiantColorMask(back_color=self.hex_to_rgb(self.label44.cget("bg_color")),top_color=self.hex_to_rgb(self.label54.cget("bg_color")),bottom_color=self.hex_to_rgb(self.label64.cget("bg_color")))

        elif selected_color_option == "Image Color":
            Image_Color_Mask = self.image_color_mask_generator(self.ImageColorMaskPath)
            Colorish = ImageColorMask(back_color=self.hex_to_rgb(self.label44.cget("bg_color")) ,color_mask_image=Image_Color_Mask)

        else: 
            Colorish =SolidFillColorMask(back_color=self.hex_to_rgb(self.label44.cget("bg_color")),front_color=self.hex_to_rgb(self.label54.cget("bg_color")))
            
        return Colorish

    def image_color_mask_generator(self,FilePath):
        if FilePath != None :
            if os.path.exists(FilePath) :
                image_taked_ = pil_Image.open(FilePath)
            else :
                image_taked_ = pil_Image.new(mode="RGB", size=(200, 200))
        else :
            image_taked_ = pil_Image.new(mode="RGB", size=(200, 200))

        return image_taked_

    def hex_to_rgb(self,Color_String):
        return ColorSelectorPIL.getcolor(Color_String, "RGB")
    
    def rgb_to_hex(self,Color_List):
        return '#{:02x}{:02x}{:02x}'.format(Color_List[0], Color_List[1], Color_List[2])
    
    # Binding
    def update_label_box(self, *args):
        # Cancel the previous scheduled update if any
        if self.update_id:
            self.after_cancel(self.update_id)

        # Schedule the update after 1000 milliseconds (1 second)
        self.update_id = self.after(1000, self.update_bar_qr_code)            
    
    def update_bar_qr_code(self):

        if self.check72_var.get() == 0 :
            self.crude_qr_image = self.create_dynamic_qr_code(self.text11_var.get())
            self.qr_image = ctk.CTkImage(self.crude_qr_image.get_image(),size=[300,300])
            self.label81.configure(image=self.qr_image)
            self.update_id = None  # Reset the update_id
        else :
            BarCode_Path = os.path.join(self.folder_path,'BarCode')+".png"
            self.crude_bar_image_path = self.create_dynamic_bar_code(self.text11_var.get(),BarCode_Path)
            self.bar_image = ctk.CTkImage(Image.open(self.crude_bar_image_path),size=[300,300])
            self.label81.configure(image=self.bar_image)
            self.update_id = None  # Reset the update_id


###########################################

if __name__ == "__main__":
    app = App()
    app.mainloop()




