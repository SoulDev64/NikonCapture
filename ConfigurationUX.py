from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import gphoto2 as gp
from pprint import pprint

class ConfigurationUX:

    '''
    Init function
    '''
    def __init__(self,ancestor,root,camera) -> None:

        self.ancestor = ancestor
        self.camera = camera
        self.root = root
        self.initConf()
        
        self.setUx()
        self.fixGrid()

        self.populate()
              

    '''
    Base configuration
    '''
    def initConf(self) -> None:
        self.columnsTitle = ('Slug', 'Title', 'Values')


    '''
    Set a new Window and add some elements
    '''
    def setUx(self):

        # Root content
        self.content = ttk.Frame(self.root, padding=(3,3,3,3))
        #self.content.grid() # Set as grid content

        # Contextual view (for edit option selected in Tree View)
        self.editOptionFrame = ttk.Frame(self.content, borderwidth=5, relief="ridge")


        # Add Tree View
        self.tree = ttk.Treeview(self.content,columns=self.columnsTitle, show='headings', selectmode='browse')
        for col in self.columnsTitle:
            # Binding header column to sort content by column
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))
        
        # Add a scrollbar to the Tree View
        self.scrollbar = ttk.Scrollbar(self.content, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        # TODO remove
        self.popup = Menu(self.root, tearoff=0)
        self.popup.add_command(label="Shutdown")
        self.popup.add_command(label="Edit Name")
        self.popup.add_separator()
        self.popup.add_command(label="Exit", command=lambda: self.closeWindow())




    '''
    Set position of each widget in the content grid
    '''
    def fixGrid(self):

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.content.grid(column=0, row=0, sticky=(N, S, E, W))

        self.content.columnconfigure(0, weight=2)
        self.content.columnconfigure(1, weight=0)
        self.content.columnconfigure(2, weight=1)
        self.content.rowconfigure(0, weight=1)

        self.tree.grid(column=0, row=0, rowspan=1, sticky=(N, S, E, W))
        self.scrollbar.grid(column=1, row=0, rowspan=1, sticky='ns')
        
        self.editOptionFrame.grid(column=2, row=0, sticky=(N, S, E, W))

        self.editOptionFrame.columnconfigure(0, weight=1)
        self.editOptionFrame.rowconfigure(0, weight=1)
    

    '''
    Insert data to the Tree View and add binding
    '''
    def populate(self):
        
        categories = {}
        self.rowsTree = {}
        context = gp.Context()
        camera = self.camera
        config_tree = camera.get_config(context)

        total_child = config_tree.count_children()
        
        for i in range(total_child):
            child = config_tree.get_child(i)
            
            categorie = child.get_name()
            categorieLabel = child.get_label()
            categories[categorie] =  self.tree.insert("", tk.END, text=categorie, open=False, values=('> '+categorieLabel,'',''))

            for a in range(child.count_children()):
                grandchild = child.get_child(a)
                
                # Set group
                tags = []
                if grandchild.get_readonly() == 1:
                    tags.append('r')
                else:
                    tags.append('rw')

                row = self.tree.insert(categories[categorie], tk.END, text=grandchild.get_name(), values=(grandchild.get_name(),'   '+grandchild.get_label(),grandchild.get_value()),tags=tags)
                self.rowsTree[grandchild.get_name()] = row

        #camera.exit(context)
        
        self.tree.tag_configure('r', background='#FFEEEE')
        self.tree.tag_configure('rw', background='#EEFFEE')
        
        self.tree.bind("<Double-Button-1>", self.do_selectOption)
        # tree.pack(side=tk.TOP,fill=tk.X)


    '''
    Callback when row is selected in the Tree View
    '''
    def do_selectOption(self, event):
        optionSelected = self.tree.focus()
        item = self.tree.item(optionSelected)
        pprint(item)
        record = item['values']
        if record[1] != '' and 'rw' in item['tags']:
            #cOption = gp.gp_camera_get_single_config(self.camera, str(record[0]))
            cOption = self.camera.get_single_config(str(record[0]))
            pprint(cOption)
            if cOption is not None:
                # TODO This code is very dirty for store the context of the option edited... not? Dict global?
                self.optionEdited = str(record[0])
                currentChoiceIndex = 0
                config_widget = cOption
                #currentChoice = gp.gp_widget_get_value(config_widget)[1]
                currentChoice = config_widget.get_value()
                print('-->')
                pprint(config_widget.count_choices())
                choices = []
                for indexChoice in range(config_widget.count_choices()):
                    choice = config_widget.get_choice(indexChoice)
                    pprint(choice)
                    choices.append(choice)
                    if currentChoice == choice:
                        currentChoiceIndex = indexChoice
                self.editOption(choices,currentChoiceIndex)
                '''
                '''


    def editOption(self,choices,currentChoice):

        namelbl = ttk.Label(self.editOptionFrame, text="Options")
        
        choicesvar = StringVar(value=choices)
        print(choices)
        self.listOptions = Listbox(self.editOptionFrame, listvariable=choicesvar)
        
        #if option.currentIndex != False:
        self.listOptions.selection_set(currentChoice)
        self.listOptions.see(currentChoice)

        ok = ttk.Button(self.editOptionFrame, text="Save")
        #cancel = ttk.Button(self.editOptionFrame, text="Reset")

        namelbl.grid(column=0, row=0, sticky=tk.NSEW, padx=5)
        self.listOptions.grid(column=0, row=1, sticky=tk.NSEW, pady=5, padx=5)
        ok.grid(column=0, row=2, sticky=tk.NSEW, padx=5)
        #cancel.grid(column=0, row=3, sticky=(N, S, E, W), pady=5, padx=5)

        ok.bind("<Button-1>", self.saveOption)

    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()
    
    def saveOption(self,event):
        print('clicked')
        selectedChoice = self.listOptions.selection_get()
        # print(gp.gp_camera_set_single_config(self.camera, self.optionEdited, selectedChoice))

        config_name =  self.optionEdited
        value = selectedChoice

        while True:
                # wait for config widget
                config_widget = self.camera.get_single_config(config_name)
                if config_widget is not None:
                    pprint(config_widget)
                    break
        
        config_set_response = config_widget.set_value(value)
        
        print('set response:', config_widget.get_value())
        res = (self.camera.set_single_config(config_name, config_widget))

        print(self.rowsTree[config_name])
        
        oldValue = self.tree.item(self.rowsTree[config_name])['values']
        oldValue[2] = selectedChoice

        self.tree.item(self.rowsTree[config_name], value=oldValue)
        
        # Refres Dashboard summary
        # TODO Make more clean (ex.: event)
        self.ancestor.getSummary()
        # show a message
        showinfo(title='Information', message='Option <' + self.optionEdited + '> saved\nNew value: ' + selectedChoice)
        
        '''
        # Update TreeView
        for rootChild in self.tree.get_children():
            print(self.tree.item(rootChild))
            for child in self.tree.item(rootChild):
                print(self.tree.item(child))
                if self.optionEdited == self.tree.item(child)['text']:
                    print('found')
                    self.tree.item(child)['values'][2] = selectedChoice
        '''


    '''
    Sort function by column in Tree View
    '''
    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)

        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))