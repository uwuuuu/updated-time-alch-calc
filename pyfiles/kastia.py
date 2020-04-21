from tkinter import *
from tkinter import messagebox
import dicts
import os
import base64
import image_enc
import webbrowser

total_success_rate=0
totalz=""

#Materials
tier1=dicts.tier1
tier2=dicts.tier2
tier3=dicts.tier3
tier4=dicts.tier4
master=dicts.master

all_tiers=dicts.all_tiers
enc_dict = image_enc.image_enc
sub_base = dicts.sub_base
sub_base2 = dicts.sub_base2

##for item in all_tiers:
##    j = item+".gif"
##    with open(j, "rb") as image_file:
##        encoded_string = base64.b64encode(image_file.read())
##        enc_dict[item]=encoded_string#print string to copy it (see step 2)
##
##for item in master:
##    j = item+".gif"
##    with open(j, "rb") as image_file:
##        encoded_string = base64.b64encode(image_file.read())
##        enc_dict[item]=encoded_string#print string to copy it (see step 2)
##print(enc_dict, file=open("dict.txt","a"))
        

craftables = dicts.craftables
desc = dicts.desc
tier1cost=dicts.tier1cost
tier2cost=dicts.tier2cost
tier3cost=dicts.tier3cost
tier4cost=dicts.tier4cost
materials_dict=dicts.materials_dict

from collections import defaultdict

dicts = [tier1cost,tier2cost,tier3cost,tier4cost,sub_base2,craftables]
super_dict = defaultdict(set)  # uses set to avoid duplicates
for d in dicts:
    for k, v in d.items():  # use d.iteritems() in python 2
        super_dict[k].add(v)

total_list = {}
total_mats = {}
total_raw_mats = {}
total_raw2={}


def find_succ(item):
    if item in materials_dict:
        return False
    x = desc[item].split("\n")
    cats = [cat.split(": ")[1] for cat in x if "Success Rate: " in cat]
    return cats[0]        


def lookup_master(item):
    parts = super_dict[item].split("|")
    parts2=parts.split(",")
    return 

##for item in total_raw_mats:
##    breakdown(item)
##    if item in super_dict:
##        parts = super_dict[item].split("|")
##        parts2=parts.split(",")
##        if parts2[0] in total_raw_mats:
##            total_raw_mats[parts2[0]]+=int(parts2[1])
##        else:
##            total_raw_mats[parts2[0]]=int(parts2[1])
##    else:
##        
##        if item in total_raw_mats:
##            total_raw_mats[item]+=total_mats[item]
##        else:
##            total_raw_mats[item]=total_mats[item]
##
##
##def breakdown(item):
##    if item in super_dict:
##        


def add_item(event, item, times):
    global totalz
    global total_success_rate
    #print(item)
    if item in tier1:
        itemdict=tier1cost
    if item in tier2:
        itemdict=tier2cost
    if item in tier3:
        itemdict=tier3cost
    if item in tier4:
        itemdict=tier4cost
    if item in materials_dict:
        itemdict=materials_dict

    photo=PhotoImage(data=enc_dict[item])
    item_lab.configure(image=photo,height = 44, width = 44)
    item_lab.photo=photo
    CreateToolTip(item_lab, text =item)
    item_name.configure(text=item)

    for i in range(times):
    
        for mats in (itemdict[item]).split("|"):
            parts = mats.split(",")
            
            if parts[0] in total_mats:
                total_mats[parts[0]]+=int(parts[1])
                total_raw_mats[parts[0]]+=int(parts[1])
            else:
                total_mats[parts[0]]=int(parts[1])
                total_raw_mats[parts[0]]=int(parts[1])
            #print("You will need "+parts[1]+"x "+parts[0])
        if item in total_list:
            total_list[item]+=1
        else:
            total_list[item]=1
                    
        total_success_rate += int(find_succ(item))
        if total_success_rate >= 0:
            totalz = "+"+str(total_success_rate)
            success_counter.config(fg="#2d8a57")
        else:
            totalz = total_success_rate
            success_counter.config(fg="#9c2525")
        success_counter.config(text=totalz)

        #print(total_list)
        #print(total_mats)
        update_buttons()
        populate_list(item)
        populate_raw()
    #breakdown()
    
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 37
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def populate_list(item):
    lb.delete(0,'end')
    total_items={k: v for k, v in sorted(total_list.items(), key=lambda x: x[1],reverse=TRUE)}
    for item in total_items:
        lb.insert(END, f'{total_list[item]:,}'+"x "+item)

def populate_raw():
    lb2.delete(0,'end')
    total_items={k: v for k, v in sorted(total_mats.items(), key=lambda x: x[1],reverse=TRUE)}
    for item in total_items:
        lb2.insert(END, f'{total_mats[item]:,}'+"x "+item)
        #str(total_mats[item])



def select_item(event):
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)

        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], part_text.get(), customer_text.get(),
              retailer_text.get(), price_text.get())
    populate_list()


def clear_text():
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)

def right(event, mat):
    global total_success_rate
    global totalz
    update_buttons()
    #print(mat)
    #print(total_list)

    photo=PhotoImage(data=enc_dict[mat])
    item_lab.configure(image=photo,height = 44, width = 44)
    item_lab.photo=photo
    CreateToolTip(item_lab, text =mat)
    item_name.configure(text=mat)

    if mat in tier1:
        itemdict=tier1cost
    if mat in tier2:
        itemdict=tier2cost
    if mat in tier3:
        itemdict=tier3cost
    if mat in tier4:
        itemdict=tier4cost
    if mat in materials_dict:
        itemdict=materials_dict
            
    if mat in total_list:
        total_list[mat]-=1
        for mats in (itemdict[mat]).split("|"):
            parts = mats.split(",")
            total_mats[parts[0]]-=int(parts[1])
            if total_mats[parts[0]]==0:
                del total_mats[parts[0]]
        
                    
        total_success_rate -= int(find_succ(mat))
        if total_success_rate >= 0:
            totalz = "+"+str(total_success_rate)
            success_counter.config(fg="#2d8a57")
        else:
            totalz = total_success_rate
            success_counter.config(fg="#9c2525")
        success_counter.config(text=totalz)
        
        if total_list[mat]==0:
            del total_list[mat]
        update_buttons()
    populate_list(mat)
    populate_raw()

def update_buttons():
    for btn in btn_dict:
        if btn in total_list:
            btn_dict[btn].config(relief="sunken",bg="#fad7f6")
        else:
            btn_dict[btn].config(relief="raised",bg="SystemButtonFace")

def clear():
    global total_list
    global total_mats
    global total_success_rate
    global item_lab
    global item_name
    total_success_rate=0
    total_list={}
    total_mats={}
    populate_raw()
    populate_list("")
    update_buttons()
    success_counter.config(text="+0",fg="#2d8a57")
    item_lab.pack_forget()
    item_name.pack_forget()
    item_lab = Label(item_frame, borderwidth=3, image="",font=("Helvetica", 10))
    item_lab.pack(side=LEFT, padx=10, pady=10,anchor=W)
    item_name = Label(item_frame, borderwidth=3,text="Left click button = Add one\nMiddle click button = Add five\nRight click button = Remove one",font=("Helvetica", 12, "bold"))
    item_name.pack(side=LEFT, padx=10, pady=10, anchor=W)


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def copy_mats():
    global total_list
    global total_mats
    copy_list = {k: v for k, v in sorted(total_mats.items(), key=lambda x: x[1],reverse=TRUE)}
    copy_list2 = {k: v for k, v in sorted(total_list.items(), key=lambda x: x[1],reverse=TRUE)}
    copy_str = ""
    

    for item in copy_list2:
        copy_str+=str(f'{copy_list2[item]:,}')+"x "+str(item)+"\n"

    copy_str +="------------------------------\n"
    for item in copy_list:
        copy_str+=str(f'{copy_list[item]:,}')+"x "+str(item)+"\n"
        #new_list.append(str(item))
#        copy_str(str(total_mats[item]).strip()+"x "+str(item).strip()+"\n")

    a=Tk()
    a.withdraw()
    a.clipboard_clear()
    a.clipboard_append(copy_str)
    a.update()
    #print(copy_list)

def copy_raw():
    global total_list
    global total_mats
    copy_list = {k: v for k, v in sorted(total_mats.items(), key=lambda x: x[1],reverse=TRUE)}
    copy_list2 = {k: v for k, v in sorted(total_list.items(), key=lambda x: x[1],reverse=TRUE)}
    copy_str = ""
    

    for item in copy_list2:
        copy_str+=str(f'{copy_list2[item]:,}')+"x "+str(item)+"\n"

    copy_str +="------------------------------\n"
    for item in copy_list:
        copy_str+=str(f'{copy_list[item]:,}')+"x "+str(item)+"\n"
        #new_list.append(str(item))
#        copy_str(str(total_mats[item]).strip()+"x "+str(item).strip()+"\n")

    a=Tk()
    a.withdraw()
    a.clipboard_clear()
    a.clipboard_append(copy_str)
    a.update()
    print(copy_list)

def onselect(evt):
    global enc_dict
    w = evt.widget
    if w.curselection():
        index = w.curselection()[0]
        value = w.get(index)
        value = " ".join(value.split(" ")[1:]).strip()
        photo=PhotoImage(data=enc_dict[value])
        item_lab.configure(image=photo,height = 44, width = 44)
        item_lab.photo=photo
        item_lab.pack(side=LEFT, padx=10, pady=10,anchor=W)
        CreateToolTip(item_lab, text =value)
        item_name.configure(text=value)

def open_forums():
    webbrowser.open('https://kastia.ms/forum/') 

# Create window object
app = Tk()
app.title('Kastia Time Alchemy Calculator')
#app['bg']= '#a2a4a6'

master_frame=LabelFrame(app,font=("Helvetica", 10))
master_frame.grid(column=0,row=0,sticky="nesw")

master_frame2=LabelFrame(app,font=("Helvetica", 10))
master_frame2.grid(column=0,row=1,sticky="nw")
master_frame3=LabelFrame(app,width=0,font=("Helvetica", 10))
master_frame3.grid(column=1,row=0, sticky="wens")
master_frame4=LabelFrame(app,width=0,font=("Helvetica", 10))
master_frame4.grid(column=1,row=1, sticky="wens")
master_frame5=LabelFrame(app,width=0,font=("Helvetica", 10))
master_frame5.grid(column=0,row=2, sticky="wens")
master_frame6=LabelFrame(app,width=0,font=("Helvetica", 10))
master_frame6.grid(column=1,row=2, sticky="wens")

frame1 = LabelFrame(master_frame, text="Tier 1",font=("Helvetica", 10))
frame1.grid(column = 0,row=0, sticky="W", padx=5, pady=5)
frame2 = LabelFrame(master_frame, text="Tier 2",font=("Helvetica", 10))
frame2.grid(column = 0,row=1, sticky="W", padx=5, pady=5)


frame3 = LabelFrame(master_frame2, text="Tier 3",font=("Helvetica", 10))
frame3.grid(column = 0,row=2, sticky="W", padx=5, pady=5)
frame4 = LabelFrame(master_frame2, text="Unique",font=("Helvetica", 10))
frame4.grid(column = 0,row=3, sticky="W", padx=5, pady=5)

frame5 = LabelFrame(master_frame3, text="Selections",font=("Helvetica", 10))
frame5.grid(column = 0,row=0, sticky="wnes", padx=5, pady=5)


mat_frame = LabelFrame(master_frame5, text="Materials",font=("Helvetica", 10))
mat_frame.grid(column = 0,row=0, sticky="W", padx=5, pady=5)

success_frame=LabelFrame(master_frame4)
success_frame.pack(expand=False, fill=X)

success_frame2=LabelFrame(success_frame, text="Success Rate",font=("Helvetica", 10))
success_frame2.pack(padx=5, pady=5, side="left")
frame7=LabelFrame(success_frame, text="Functions",font=("Helvetica", 10))
frame7.pack(padx=5,pady=5,fill="both",side="right",expand=True)

success_counter = Label(success_frame2, text="+0",fg="#2d8a57", borderwidth=3,font=("Helvetica", 14))
success_counter.pack(padx=10, pady=10)

clear_all = Button(frame7,text="Clear all",command=clear)
clear_all.grid(column = 0, row=1, padx=3, pady=3, sticky="w")

copy_mats = Button(frame7,text="Copy base materials",command=copy_mats)
copy_mats.grid(column = 1, row=0, padx=3, pady=3, sticky="w")

forum_post = Button(frame7,text="Forum Post",command=open_forums)
forum_post.grid(column = 0, row=0, padx=3, pady=3, sticky="w")

itemi_frame=LabelFrame(master_frame4)
itemi_frame.pack(expand=False,fill=X)
itemi_frame.columnconfigure(1, weight=1)

item_frame=LabelFrame(itemi_frame, text="Item Info",font=("Helvetica", 10))
item_frame.pack(padx=5, pady=5, anchor=W, fill="both")
item_lab = Label(item_frame, borderwidth=3, image="",font=("Helvetica", 10))
item_lab.pack(side=LEFT, padx=10, pady=10,anchor=W, fill="both")
item_name = Label(item_frame, borderwidth=3,text="Left click button = Add one\nMiddle click button = Add five\nRight click button = Remove one",font=("Helvetica", 12, "bold"))
item_name.pack(side=LEFT, padx=10, pady=10, anchor=W, fill="both")

btn_dict = {}

#frame = Frame(app)
#frame.place(x = 5, y = 260) # Position of where you would place your listbox
lb = Listbox(frame5,height=8,width=35,font=("Helvetica", 12), activestyle=NONE)
lb.pack(side = 'right',fill = 'both',expand=TRUE )
scrollbar = Scrollbar(frame5, orient="vertical",command=lb.yview)
scrollbar.pack(side="right", fill="y")
lb.config(yscrollcommand=scrollbar.set)
lb.bind('<<ListboxSelect>>', onselect)

#base materials
frame6=LabelFrame(master_frame6, text="Base Materials",font=("Helvetica", 10))
frame6.grid(padx=5, pady=5, sticky='wesn')
lb2 = Listbox(frame6, width=35, height=15,font=("Helvetica", 12),activestyle=NONE)
lb2.pack(side = 'right',fill = 'y' )
scrollbar2 = Scrollbar(frame6, orient="vertical",command=lb2.yview)
scrollbar2.pack(side="right", fill="y")
lb2.config(yscrollcommand=scrollbar2.set)
lb2.bind('<<ListboxSelect>>', onselect)

#frame8=LabelFrame(master_frame6, text="Raw Materials",font=("Helvetica", 10))
#frame8.grid(padx=5, pady=5, sticky='wesn')
##lb3 = Listbox(frame8, width=35, height=15,font=("Helvetica", 12),activestyle=NONE)
##lb3.pack(side = 'right',fill = 'y' )
##scrollbar3 = Scrollbar(frame8, orient="vertical",command=lb3.yview)
##scrollbar3.pack(side="right", fill="y")
##lb3.config(yscrollcommand=scrollbar3.set)
##lb3.bind('<<ListboxSelect>>', onselect)


def createtier1():
    global enc_dict
    col = 0
    rowv = 0
    rowc=0
    for mat in tier1:
        if rowc > 4:
            rowv+=1
            col=0
            rowc=0
##        imagefile = mat+'.png'
##        photo=PhotoImage(file=resource_path(imagefile))
        photo=PhotoImage(data=enc_dict[mat])
        btn_dict[mat] = Label(frame1, text=mat, image=photo, height = 44, width = 44, borderwidth=3, relief="raised")
        btn_dict[mat].grid(row=rowv, column=col, pady=5, padx=5)
        btn_dict[mat].image=photo
        btn_dict[mat].bind('<Button-1>', lambda event, name=mat:add_item(event, name,1))
        btn_dict[mat].bind('<Button-2>', lambda event, mat=mat: add_item(event, mat,5))
        btn_dict[mat].bind('<Button-3>', lambda event, mat=mat: right(event, mat))
        CreateToolTip(btn_dict[mat], text =mat+"\n"+desc[mat])
        col += 1
        rowc+=1


def createtier2():
    global enc_dict
    col = 0
    rowv = 0
    rowc=0
    for mat in tier2:
        if rowc > 4:
            rowv+=1
            col=0
            rowc=0
##        imagefile = mat+'.png'
##        photo=PhotoImage(file=resource_path(imagefile))
        photo=PhotoImage(data=enc_dict[mat])
        btn_dict[mat] = Label(frame2, text=mat, image=photo, height = 44, width = 44, borderwidth=3, relief="raised") 
        btn_dict[mat].grid(row=rowv, column=col, pady=5, padx=5)
        btn_dict[mat].image=photo
        btn_dict[mat].bind('<Button-1>', lambda event, name=mat:add_item(event, name,1))
        btn_dict[mat].bind('<Button-2>', lambda event, mat=mat: add_item(event, mat,5))
        btn_dict[mat].bind('<Button-3>', lambda event, mat=mat: right(event, mat))
        CreateToolTip(btn_dict[mat], text =mat+"\n"+desc[mat])
        col += 1
        rowc+=1

def createtier3():
    global enc_dict
    col = 0
    rowv = 0
    rowc=0
    for mat in tier3:
        if rowc > 4:
            rowv+=1
            col=0
            rowc=0
##        imagefile = mat+'.png'
##        photo=PhotoImage(file=resource_path(imagefile))
        photo=PhotoImage(data=enc_dict[mat])
        btn_dict[mat] = Label(frame3, text=mat, image=photo, height = 44, width = 44, borderwidth=3, relief="raised") 
        btn_dict[mat].grid(row=rowv, column=col, pady=5, padx=5)
        btn_dict[mat].image=photo
        btn_dict[mat].bind('<Button-1>', lambda event, name=mat:add_item(event, name,1))
        btn_dict[mat].bind('<Button-2>', lambda event, mat=mat: add_item(event, mat,5))
        btn_dict[mat].bind('<Button-3>', lambda event, mat=mat: right(event, mat))
        CreateToolTip(btn_dict[mat], text =mat+"\n"+desc[mat])
        col += 1
        rowc+=1

def createtier4():
    global enc_dict
    col = 0
    rowv = 0
    rowc=0
    for mat in tier4:
        #action = lambda x = mat: text_update(x)
        if rowc > 4:
            rowv+=1
            col=0
            rowc=0
##        imagefile = mat+'.png'
##        photo=PhotoImage(file=resource_path(imagefile))
        photo=PhotoImage(data=enc_dict[mat])
        btn_dict[mat] = Label(frame4, text=mat, image=photo, height = 44, width = 44, borderwidth=3, relief="raised") 
        btn_dict[mat].grid(row=rowv, column=col, pady=5, padx=5)
        btn_dict[mat].image=photo
        btn_dict[mat].bind('<Button-1>', lambda event, name=mat:add_item(event, name,1))
        btn_dict[mat].bind('<Button-2>', lambda event, mat=mat: add_item(event, mat,5))
        btn_dict[mat].bind('<Button-3>', lambda event, mat=mat: right(event, mat))
        CreateToolTip(btn_dict[mat], text =mat+"\n"+desc[mat])
        col += 1    
        rowc+=1

def createmats():
    global enc_dict
    col = 0
    rowv = 0
    rowc=0
    for mat in materials_dict:
        #action = lambda x = mat: text_update(x)
        if rowc > 4:
            rowv+=1
            col=0
            rowc=0
##        imagefile = mat+'.png'
##        photo=PhotoImage(file=resource_path(imagefile))
        photo=PhotoImage(data=enc_dict[mat])
        btn_dict[mat] = Label(mat_frame, text=mat, image=photo, height = 44, width = 44, borderwidth=3, relief="raised") 
        btn_dict[mat].grid(row=rowv, column=col, pady=5, padx=5)
        btn_dict[mat].image=photo
        btn_dict[mat].bind('<Button-1>', lambda event, name=mat:add_item(event, name,1))
        btn_dict[mat].bind('<Button-2>', lambda event, mat=mat: add_item(event, mat,5))
        btn_dict[mat].bind('<Button-3>', lambda event, mat=mat: right(event, mat))
        CreateToolTip(btn_dict[mat], text =mat+"\n"+desc[mat])
        col += 1    
        rowc+=1

def popup_showinfo():
    messagebox.showinfo("Info", "To add an item, left click on the button.\nTo add five on an item, middle click on the button.\nTo remove an item, right click on the button.\n\
Base materials = materials needed to craft selections.\n----------------------------------------------------------------------\nAdditional features are still under development.\nCheck Kastia forums for latest updates!")


menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Info", command=popup_showinfo)
filemenu.add_command(label="Exit", command=app.quit)
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Help", menu=helpmenu)
app.config(menu=menubar)

createtier1()
createtier2()
createtier3()
createtier4()
createmats()

# Start program
app.resizable(False,False)
center(app)
app.mainloop()
