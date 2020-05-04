from tkinter import *
from tkinter import messagebox
import dicts
import os
import base64
import image_enc
import webbrowser

total_success_rate=0
totalz=""
personal_rate = 0

#Materials
tier1=dicts.tier1
tier2=dicts.tier2
tier3=dicts.tier3
tier4=dicts.tier4
master=dicts.master

flat_cata=dicts.flat_cata
per_cata=dicts.per_cata

all_tiers=dicts.all_tiers
enc_dict = image_enc.image_enc
sub_base = dicts.sub_base
sub_base2 = dicts.sub_base2    

craftables = dicts.craftables
desc = dicts.desc
tier1cost=dicts.tier1cost
tier2cost=dicts.tier2cost
tier3cost=dicts.tier3cost
tier4cost=dicts.tier4cost
materials_dict=dicts.materials_dict
rawest = dicts.rawest

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

def refresh_raw():
    global total_mats
    global total_raw_mats
    total_raw_mats=total_mats.copy()
    populate_raw()
    
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
            else:
                total_mats[parts[0]]=int(parts[1])

            if parts[0] in total_raw_mats:
                total_raw_mats[parts[0]]+=int(parts[1])
            else:
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

def pop_rawest(item, itemdict):
    global total_raw_mats
    times = total_raw_mats[item]
    del total_raw_mats[item]

    #['Black Scroll (Level 2),3', 'Elixir of Purity,5', 'Meso,30000000', 'NX Cash,3000000']
    for mats in (itemdict[item]).split("|"):
        parts = mats.split(",")
        #['Black Scroll (Level 2)', '3']

        for i in range(times):
            if parts[0] in total_raw_mats:
                total_raw_mats[parts[0]]+=int(parts[1])
            else:
                total_raw_mats[parts[0]]=int(parts[1])
            #print("You will need "+parts[1]+"x "+parts[0])

            populate_raw()


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
    lb3.delete(0,'end')
    populate_rawest()
    total_items={k: v for k, v in sorted(total_mats.items(), key=lambda x: x[1],reverse=TRUE)}
    for item in total_items:
        lb2.insert(END, f'{total_mats[item]:,}'+"x "+item)
        #str(total_mats[item])

def populate_rawest():
    lb3.delete(0,'end')
    total_items2={k: v for k, v in sorted(total_raw_mats.items(), key=lambda x: x[1],reverse=TRUE)}
    for item in total_items2:
        lb3.insert(END, f'{total_raw_mats[item]:,}'+"x "+item)
        if item in rawest:
            lb3.itemconfigure(END, background='#d0f7e6')
        #str(total_mats[item])


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
    refresh_raw()

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
    global total_raw_mats
    global item_lab
    global item_name
    global stat1_in
    total_success_rate=0
    total_list={}
    total_raw_mats={}
    total_mats={}
    populate_raw()
    populate_rawest()
    populate_list("")
    update_buttons()
    custom_rate2.configure(text="")
    success_counter.config(text="+0",fg="#2d8a57")
    stat1_in.delete('1.0',END)
    stat2_in.delete('1.0',END)
    stat3_in.delete('1.0',END)
    stat4_in.delete('1.0',END)
    stat5_in.delete('1.0',END)
    stat6_in.delete('1.0',END)
    post_stat1_val.config(text="0")
    post_stat2_val.config(text="0")
    post_stat3_val.config(text="0")
    post_stat4_val.config(text="0")
    post_stat5_val.config(text="0")
    post_stat6_val.config(text="0")
    item_lab.pack_forget()
    item_name.pack_forget()
    item_lab = Label(item_frame, borderwidth=3, image="",font=("Helvetica", 10))
    item_lab.pack(side=LEFT, padx=10, pady=10,anchor=W)
    item_name = Label(item_frame, borderwidth=3,text="Left click button = Add one\nMiddle click button = Add five\nRight click button = Remove one",font=("Helvetica", 12, "bold"))
    item_name.pack(side=LEFT, padx=10, pady=10, anchor=W)

def clear_raw_only():
    global total_raw_mats
    total_raw_mats = {}
    populate_raw()

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

def copy_raw_only():
    global total_list
    global total_mats
    copy_list = {k: v for k, v in sorted(total_raw_mats.items(), key=lambda x: x[1],reverse=TRUE)}
    copy_str = ""
    
    for item in copy_list:
        copy_str+=str(f'{copy_list[item]:,}')+"x "+str(item)+"\n"
        #new_list.append(str(item))
#        copy_str(str(total_mats[item]).strip()+"x "+str(item).strip()+"\n")

    a=Tk()
    a.withdraw()
    a.clipboard_clear()
    a.clipboard_append(copy_str)
    a.update()

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
    webbrowser.open('https://kastia.ms/forum/viewtopic.php?f=10&t=2898') 

def check(item):
    global total_raw_mats
    global materials_list
    
    if item in tier4cost:
        pop_rawest(item, tier4cost)
    if item in tier3cost:
        pop_rawest(item, tier3cost)
    if item in tier2cost:
        pop_rawest(item, tier2cost)
    if item in tier1cost:
        pop_rawest(item, tier1cost)
    if item in sub_base2:
        pop_rawest(item, sub_base2)
    if item in craftables:
        pop_rawest(item, craftables)

def condense(dct):
    global rawest
    global total_raw2
    global total_raw_mats
    total_raw2 = total_raw_mats
    try:
        for item in total_raw2:
            if item not in rawest:
                check(item)
    except RuntimeError:
        condense(dct)

def condense1():
    global total_raw_mats
    global total_raw2
    condense(total_raw_mats)
    

def breakdown(evt):
    global enc_dict
    global total_raw_mats
    w=evt.widget
    value = w.get(w.curselection()[0])
    value = " ".join(value.split(" ")[1:]).strip()
    check(value)

def calc_rate():
    global total_success_rate
    base_succ = e1.get("1.0",END)
    tot = int(base_succ)+int(total_success_rate)
    if int(tot) < 1:
        tot="0"
    custom_rate2.configure(text=str(tot)+"%")


def test(event):
    a1 = e1.get(1.0, END)
    calc_rate()
    return 'break'

def test2(event):
    a1 = e1.get(1.0, END)
    return 'break'

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")

def calc_stats():
    global flat_cata
    global per_cata

    stat_calc_dict = {}
    mult_calc_dict = {}

    for item in total_list:
        if item in flat_cata:
            parts = flat_cata[item].split("|")
            for piece in parts:
                for i in range(int(total_list[item])):
                    if piece.split(",")[0] not in stat_calc_dict:
                        stat_calc_dict[piece.split(",")[0]] = int(piece.split(",")[1])
                    else:
                        stat_calc_dict[piece.split(",")[0]] += int(piece.split(",")[1])

        elif item in per_cata:
            parts = per_cata[item].split("|")
            for piece in parts:
                for i in range(int(total_list[item])):
                    if piece.split(",")[0] not in mult_calc_dict:
                        mult_calc_dict[piece.split(",")[0]] = 1.0 + eval(piece.split(",")[1])
                    else:
                        mult_calc_dict[piece.split(",")[0]] += eval(piece.split(",")[1])

    stat_str = stat1_in.get("1.0",END).strip()
    stat_dex = stat2_in.get("1.0",END).strip()
    stat_int = stat3_in.get("1.0",END).strip()
    stat_luk = stat4_in.get("1.0",END).strip()
    stat_watt = stat5_in.get("1.0",END).strip()
    stat_matt = stat6_in.get("1.0",END).strip()

    if stat_str == "":
        stat_str=0
    else:
        stat_str=int(stat_str)
    if stat_dex == "":
        stat_dex=0
    else:
        stat_dex=int(stat_dex)
    if stat_int == "":
        stat_int=0
    else:
        stat_int=int(stat_int)
    if stat_luk == "":
        stat_luk=0
    else:
        stat_luk=int(stat_luk)
    if stat_watt == "":
        stat_watt=0
    else:
        stat_watt=int(stat_watt)
    if stat_matt == "":
        stat_matt=0
    else:
        stat_matt=int(stat_matt)

    #print(stat_str,stat_dex,stat_int, stat_luk, stat_watt,stat_matt)

    for stat in stat_calc_dict:
        if stat == "STATS":
            stat_str += stat_calc_dict[stat]
            stat_dex += stat_calc_dict[stat]
            stat_int += stat_calc_dict[stat]
            stat_luk += stat_calc_dict[stat]
        if stat == "WATT":
            stat_watt += stat_calc_dict[stat]
        if stat == "MATT":
            stat_matt += stat_calc_dict[stat]

    for stat in mult_calc_dict:
        if stat == "STATS":
            stat_str = stat_str * round(mult_calc_dict[stat],2)
            stat_dex = stat_dex * round(mult_calc_dict[stat],2)
            stat_int = stat_int * round(mult_calc_dict[stat],2)
            stat_luk = stat_luk * round(mult_calc_dict[stat],2)
        if stat == "WATT":
            stat_watt = stat_watt * round(mult_calc_dict[stat],2)
        if stat == "MATT":
            stat_matt = stat_matt * round(mult_calc_dict[stat],2)

    post_stat1_val.config(text=str(int(stat_str)))
    post_stat2_val.config(text=str(int(stat_dex)))
    post_stat3_val.config(text=str(int(stat_int)))
    post_stat4_val.config(text=str(int(stat_luk)))
    post_stat5_val.config(text=str(int(stat_watt)))
    post_stat6_val.config(text=str(int(stat_matt)))
        
    pass


# Create window object
app = Tk()
app.title('Kastia Time Alchemy Calculator')
#app['bg']= '#a2a4a6'

master_frame=LabelFrame(app,font=("Helvetica", 10))
master_frame.grid(column=0,row=0,sticky="nesw")

master_frame3=LabelFrame(app,width=0,font=("Helvetica", 10))
master_frame3.grid(column=1,row=0, sticky="wens")

master3_sub1=LabelFrame(master_frame3,width=0,font=("Helvetica", 10))
master3_sub1.grid(column=0,row=0, sticky="wens")
master3_sub2=LabelFrame(master_frame3,width=0,font=("Helvetica", 10))
master3_sub2.grid(column=0,row=1, sticky="wens")
master3_sub3=LabelFrame(master_frame3,width=0,font=("Helvetica", 10))
master3_sub3.grid(column=0,row=2, sticky="wens")
master3_sub4=LabelFrame(master_frame3,width=0,font=("Helvetica", 10))
master3_sub4.grid(column=1,row=0, sticky="wens")
master3_sub5=LabelFrame(master_frame3,width=0,font=("Helvetica", 10))
master3_sub5.grid(column=1,row=1, sticky="wens")
master3_sub6=LabelFrame(master_frame3,width=0,font=("Helvetica", 10))
master3_sub6.grid(column=1,row=2, sticky="wens")
master3_sub7=LabelFrame(master_frame3,width=0,font=("Helvetica", 10))
master3_sub7.grid(column=1,row=3, sticky="wens")
master3_sub8=LabelFrame(master_frame3,width=0,font=("Helvetica", 10))
master3_sub8.grid(column=1,row=4, sticky="wens")


frame1 = LabelFrame(master_frame, text="Tier 1",font=("Helvetica", 10))
frame1.grid(column = 0,row=0, sticky="W", padx=5, pady=5)
frame2 = LabelFrame(master_frame, text="Tier 2",font=("Helvetica", 10))
frame2.grid(column = 0,row=1, sticky="W", padx=5, pady=5)


frame3 = LabelFrame(master_frame, text="Tier 3",font=("Helvetica", 10))
frame3.grid(column = 0,row=2, sticky="W", padx=5, pady=5)
frame4 = LabelFrame(master_frame, text="Unique",font=("Helvetica", 10))
frame4.grid(column = 0,row=3, sticky="W", padx=5, pady=5)

frame5 = LabelFrame(master3_sub1, text="Selections",font=("Helvetica", 10))
frame5.grid(column = 0,row=0, sticky="wnes", padx=5, pady=5)


mat_frame = LabelFrame(master_frame, text="Materials",font=("Helvetica", 10))
mat_frame.grid(column = 0,row=4, sticky="W", padx=5, pady=5)

success_frame=LabelFrame(master3_sub2)
success_frame.pack(fill=X, expand=FALSE)
success_frame3=LabelFrame(master3_sub2)
success_frame3.pack(fill=X, expand=FALSE)

e1_label = Label(success_frame3, borderwidth=3, image="",font=("Helvetica", 10), text="Enter your base success rate here: ")
e1_label.grid(column=0, row=0,pady=5, padx=5)
e1 = Text(success_frame3,height=0, width=8)
e1.grid(column=1, row=0,pady=5, padx=5)
e1.bind('<Return>', test)
custom_rate = Label(success_frame3, borderwidth=3, image="",font=("Helvetica", 10), text="Your total success rate is: ")
custom_rate.grid(column=0, row=1,pady=5, padx=5)
custom_rate2 = Label(success_frame3, borderwidth=3, image="",font=("Helvetica", 10), text="")
custom_rate2.grid(column=1, row=1,pady=5, padx=5)
rate_btn = Button(success_frame3, text="Calculate", command=calc_rate)
rate_btn.grid(column=1, row=2,pady=5, padx=5)

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
copyraw = Button(frame7,text="Copy raw materials",command=copy_raw_only)
copyraw.grid(column = 1, row=1, padx=3, pady=3, sticky="w")


item_frame=LabelFrame(master3_sub4, text="Item Info",font=("Helvetica", 10))
item_frame.grid(padx=5,pady=5)
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
frame6=LabelFrame(master3_sub3, text="Base Materials",font=("Helvetica", 10))
frame6.grid(padx=5, pady=5, sticky='wesn')
lb2 = Listbox(frame6, width=35, height=15,font=("Helvetica", 12),activestyle=NONE)
lb2.pack(side = 'right',fill = 'y' )
scrollbar2 = Scrollbar(frame6, orient="vertical",command=lb2.yview)
scrollbar2.pack(side="right", fill="y")
lb2.config(yscrollcommand=scrollbar2.set)
lb2.bind('<<ListboxSelect>>', onselect)


#raw materials
frame8=LabelFrame(master3_sub6, text="Raw Materials",font=("Helvetica", 10))
frame8.grid(padx=5, pady=5, column=1, row=2,sticky='wesn')
lb3 = Listbox(frame8, width=32, height=15,font=("Helvetica", 12),activestyle=NONE)
lb3.pack(side = 'right',fill = 'both',expand=TRUE  )
scrollbar3 = Scrollbar(frame8, orient="vertical",command=lb3.yview)
scrollbar3.pack(side="right", fill="y")
lb3.config(yscrollcommand=scrollbar3.set)
lb3.bind('<<ListboxSelect>>', onselect)
lb3.bind('<Double-Button>', breakdown)

rawframe=LabelFrame(master3_sub4, text="Raw Functions",font=("Helvetica", 10))
rawframe.grid(padx=5, pady=5,sticky='wesn')

condenseraw = Button(rawframe,text="Condense",command=condense1)
condenseraw.grid(column = 1, row=0, padx=3, pady=3, sticky="w")
clearraw = Button(rawframe,text="Clear raw materials",command=clear_raw_only)
clearraw.grid(column = 2, row=0, padx=3, pady=3, sticky="w")
refreshraw = Button(rawframe,text="Refresh",command=refresh_raw)
refreshraw.grid(column = 3, row=0, padx=3, pady=3, sticky="w")
clear_all2 = Button(rawframe,text="Clear all",command=clear)
clear_all2.grid(column = 4, row=0, padx=3, pady=3, sticky="w")

howtoframe=LabelFrame(master3_sub5, text="How to Use",font=("Helvetica", 10))
howtoframe.grid(padx=5, pady=5, column=1, row=1,sticky='wesn')

howto = Label(howtoframe, text="Materials highlighted in green are already in it's rawest\nform. Double click on an item in the Raw Materials list\n that isn't highlighted to break it down further.\n\nClicking 'Condense' will break the selections down into\nthe rawest form possible. It's a little slow, so be patient\nif you have a lot of catalysts/materials selected.\n\n'Refresh' will refresh the Raw Materials list to match the\nBase Materials list. Read section above to learn why\nthe Raw Materials list doesn't always update.")
howto.grid(padx=5, pady=5)


stats_frame = LabelFrame(app,width=0,font=("Helvetica", 10),background="#f7dfdc")
stats_frame.grid(column=2,row=0, sticky="wens")

how_stats = LabelFrame(stats_frame,width=0,font=("Helvetica", 10), text="How to Use",background="#f7dfdc")
how_stats.grid(column=0,row=0, sticky="wens", padx=5, pady=5)
pre_stats = LabelFrame(stats_frame,width=0,font=("Helvetica", 10), text="Pre Time Alchemy Stats",background="#f7dfdc")
pre_stats.grid(column=0,row=1, sticky="wens", padx=5, pady=5)
post_stats = LabelFrame(stats_frame,width=0,font=("Helvetica", 10), text="Post Time Alchemy Stats",background="#f7dfdc")
post_stats.grid(column=0,row=2, sticky="wens", padx=5, pady=5)

howto_stats = Label(how_stats,background="#f7dfdc", text="Enter your item's stats\nand hit Calculate to see how\nmuch Time Alchemy will\nchange your item's stats.\nCalculations assume that you\nput flat catalysts first\nand then multiplier catalysts.")
howto_stats.grid(padx=5, pady=5)


stat1 = Label(pre_stats,text="STR:",background="#f7dfdc")
stat1.grid(column=0,row=0,padx=5, pady=5)
stat1_in = Text(pre_stats,height=0, width=8)
stat1_in.grid(column=1, row=0,pady=5, padx=5)
stat1_in.bind("<Tab>", focus_next_widget)
stat1_in.bind('<Return>', test2)

stat2 = Label(pre_stats,text="DEX:",background="#f7dfdc")
stat2.grid(column=0,row=1,padx=5, pady=5)
stat2_in = Text(pre_stats,height=0, width=8)
stat2_in.grid(column=1, row=1,pady=5, padx=5)
stat2_in.bind("<Tab>", focus_next_widget)
stat2_in.bind('<Return>', test2)

stat3 = Label(pre_stats,text="INT:",background="#f7dfdc")
stat3.grid(column=0,row=2,padx=5, pady=5)
stat3_in = Text(pre_stats,height=0, width=8)
stat3_in.grid(column=1, row=2,pady=5, padx=5)
stat3_in.bind("<Tab>", focus_next_widget)
stat3_in.bind('<Return>', test2)

stat4 = Label(pre_stats,text="LUK:",background="#f7dfdc")
stat4.grid(column=0,row=3,padx=5, pady=5)
stat4_in = Text(pre_stats,height=0, width=8)
stat4_in.grid(column=1, row=3,pady=5, padx=5)
stat4_in.bind("<Tab>", focus_next_widget)
stat4_in.bind('<Return>', test2)

stat5 = Label(pre_stats,text="Wep ATT:",background="#f7dfdc")
stat5.grid(column=0,row=4,padx=5, pady=5)
stat5_in = Text(pre_stats,height=0, width=8)
stat5_in.grid(column=1, row=4,pady=5, padx=5)
stat5_in.bind("<Tab>", focus_next_widget)
stat5_in.bind('<Return>', test2)

stat6 = Label(pre_stats,text="Mag ATT:",background="#f7dfdc")
stat6.grid(column=0,row=5,padx=5, pady=5)
stat6_in = Text(pre_stats,height=0, width=8)
stat6_in.grid(column=1, row=5,pady=5, padx=5)
stat6_in.bind("<Tab>", focus_next_widget)
stat6_in.bind('<Return>', test2)

calc_stats = Button(pre_stats, text="Calculate", command=calc_stats)
calc_stats.grid(column=1, row=6,pady=5, padx=5)

post_stat1 = Label(post_stats,text="STR:",background="#f7dfdc")
post_stat1.grid(column=0,row=0,padx=5, pady=5)
post_stat1_val = Label(post_stats,text="0",background="#f7dfdc")
post_stat1_val.grid(column=1,row=0,padx=5, pady=5)

post_stat2 = Label(post_stats,text="DEX:",background="#f7dfdc")
post_stat2.grid(column=0,row=1,padx=5, pady=5)
post_stat2_val = Label(post_stats,text="0",background="#f7dfdc")
post_stat2_val.grid(column=1,row=1,padx=5, pady=5)

post_stat3 = Label(post_stats,text="INT:",background="#f7dfdc")
post_stat3.grid(column=0,row=2,padx=5, pady=5)
post_stat3_val = Label(post_stats,text="0",background="#f7dfdc")
post_stat3_val.grid(column=1,row=2,padx=5, pady=5)

post_stat4 = Label(post_stats,text="LUK:",background="#f7dfdc")
post_stat4.grid(column=0,row=3,padx=5, pady=5)
post_stat4_val = Label(post_stats,text="0",background="#f7dfdc")
post_stat4_val.grid(column=1,row=3,padx=5, pady=5)

post_stat5 = Label(post_stats,text="Wep ATT:",background="#f7dfdc")
post_stat5.grid(column=0,row=4,padx=5, pady=5)
post_stat5_val = Label(post_stats,text="0",background="#f7dfdc")
post_stat5_val.grid(column=1,row=4,padx=5, pady=5)

post_stat6 = Label(post_stats,text="Mag ATT:",background="#f7dfdc")
post_stat6.grid(column=0,row=5,padx=5, pady=5)
post_stat6_val = Label(post_stats,text="0",background="#f7dfdc")
post_stat6_val.grid(column=1,row=5,padx=5, pady=5)


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
