#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pathlib as path
import os
import re
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm


# In[59]:


class multicolor_plotter():
    '''df = dataframe with your information, x_df_pos = column position of your x variables, x_label = x axis label, 
    y_df_pos = column position of your y variables, y_label = y axis label, label_df_pos = the label you want associated with each data point, 
    title = title of chart, chunk = corresponds to how many of the same variable you have & want plotted
    name_png = png naming'''
    
    #imports
    import numpy as np
    import pandas as pd
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    
    def __init__(self, df, x_df_pos, x_label, y_df_pos, y_label, label_df_pos, title, chunk):
        self.df = df
        self.x_df_pos = x_df_pos
        self.x_label = x_label
        self.y_df_pos = y_df_pos
        self.y_label = y_label
        self.label_df_pos = label_df_pos
        self.title = title
        self.chunk = chunk
        #self.name_png = name_png 
        
    def plotter(self):
        
        def delist(args):
            'Taking mutliple lists within a list and returning a single list of values'
            delist = [var for small_list in args for var in small_list]
            return(delist)
        
        assay_num = [var for var in range(len(self.df.iloc[:,self.x_df_pos]))]
        
        offset_x = 0
        offset_y = 0
        offset_label = 0
        
        xf = []
        yf = []
        labelf = []
        
        while offset_x < len(assay_num):
            i_x = assay_num[offset_x:offset_x+self.chunk]
            x = self.df.iloc[i_x, self.x_df_pos]
            xf.append(x)
            
            offset_x += self.chunk
        
        while offset_y < len(assay_num):
            i_y = assay_num[offset_y:offset_y+self.chunk]
            y = self.df.iloc[i_y, self.y_df_pos]
            yf.append(y)
            
            offset_y += self.chunk
            
        while offset_label < len(assay_num):
            i_label = assay_num[offset_label:offset_label+self.chunk]
            label = self.df.iloc[i_label, self.label_df_pos]
            labelf.append(label)
            
            offset_label += self.chunk
        
        label_unique = []
        for var in labelf:
            labelu = var.unique()
            label_list = labelu.tolist()
            label_unique.append(label_list)
        
        labeld = delist(label_unique)
        
        colors = cm.rainbow(np.linspace(0,1, (len(labeld))))
        
        xylc_zip = zip(xf,yf, labeld, colors)
        
        fig, ax = plt.subplots(figsize=(6,4))
        for x, y, l, c in xylc_zip:
            plt.plot(x,y, color = c, label = l)
            ax.grid()
            ax.legend()
            ax.set(xlabel = self.x_label, ylabel = self.y_label, title = self.title)
            plt.legend(bbox_to_anchor =(1.1, 1))
            #plt.savefig(self.name_png)
            


# In[60]:


_path = path.Path.cwd()

experiment_pos_dict = {}
experiment_dict = {}

for _filepath in _path.iterdir():
    if _filepath.suffix != '.tsv':
        pass
    elif _filepath.suffix == '.tsv':
        
        head, tail = os.path.split(_filepath)
        #print(tail)
        
        with open(_filepath) as file:
            
            data = file.read()
            
            #regex matches values preceeded by QOS Optical Signal
            qos_finder = re.compile(r'(?<=QOS Optical Signal: )[0-9]+\.[0-9]+')
            qos_values = qos_finder.findall(data)
            
            y_val = [float(var) for var in qos_values]
            
            #function for seperating QOS values
            def pos_data(data, start_position, step=3):
                '''This function will iterate thru data and create smaller 
                datasets based on a start location and a step value.
                data=the list of interest, start position=index in list 
                to begin at, step=skipping step'''
                
                pos_index = [var for var in range(start_position, len(data),step)]

                pos_list = []

                for var in pos_index:
                    pos = y_val[var]
                    pos_list.append(pos)
                return pos_list

            #seperate out the QOS values
            pos_1 = pos_data(y_val, 0)
            pos_2 = pos_data(y_val, 1)
            pos_3 = pos_data(y_val, 2)
            pos_total = pos_1 + pos_2 + pos_3
            
            #generate exploratory data to aid in graphing
            position_dict = {}
            position_dict['assay'] = tail
            position_dict['length of QOS reads'] = len(pos_total)
            
            df_position = pd.DataFrame(position_dict, index=[0])
            experiment_pos_dict[f'{tail}'] = df_position
            display(df_position)
            
            
            #align x values
            x_val = [var for var in range(len(pos_1))]
            x_val_total = x_val*3


            #align positions to x and y values
            position = ['spatial_position_1','spatial_position_2','spatial_position_3']
            pos_values = np.repeat(position, len(pos_1))

            
            #mold data into dictionary for pandas df
            assay_dict = {}
            assay_dict['position'] = pos_values
            assay_dict['x'] = x_val_total
            assay_dict['y'] = pos_total
            
            #create df and add a key/value pair for each tsv file
            df = pd.DataFrame(assay_dict)
            experiment_dict[f'{tail}']=df
            
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            #display(df)
            


# In[62]:


for key, value in experiment_dict.items():
    if len(value.iloc[:,0]) > 3:
        graph = multicolor_plotter(value,1, 'Reading',2,'QOS Optical Signal',0,f'Peroxide Data for {key}',(int(len(value.iloc[:,0])/3)))
        graph.plotter()
        #display(key,value)
        
    else:
        print(f'Assay {key} has less than 4 QOS reads')


# In[ ]:




