#!/usr/bin/env python
# coding: utf-8

# In[60]:


get_ipython().system('unzip -q 作业-基于OCR的点名检测.zip -d data/')


# In[61]:


get_ipython().system('unzip -q simfang_downyi.com.zip')


# In[62]:


get_ipython().system('unzip -q QQ图片20220520105515.zip -d data/作业-基于OCR的点名检测/0225/')


# In[63]:


get_ipython().system('pip install paddleocr')


# In[64]:


import os
import numpy as np
import pandas as pd


# In[65]:


word_list = []
datas = []


# In[66]:


path = '名单.csv'
data_name = pd.read_csv(path, encoding= 'GBK')


# In[67]:


data_name


# In[68]:


for text in data_name['姓名']:
    word_list.append(text)


# In[69]:


num_list = []
for num in data_name['序号']:
    num_list.append(num)
num_list


# In[70]:


word_list


# In[71]:


get_ipython().run_line_magic('cd', '~')
path = 'data/作业-基于OCR的点名检测/'
filelist_dir = os.listdir('data/作业-基于OCR的点名检测')
filelist_dir


# In[72]:


filelist_dir.remove('名单.csv')
filelist_dir.remove('作业要求.doc')


# In[73]:


filelist_dir.sort()
filelist_dir


# In[74]:


def getFileList(dir,Filelist, ext=None):
    """
    获取文件夹及其子文件夹中文件列表
    输入 dir：文件夹根目录
    输入 ext: 扩展名
    返回： 文件路径列表
    """
    newDir = dir
    if os.path.isfile(dir):
        if ext is None:
            Filelist.append(dir)
        else:
            if ext in dir[-3:]:
                Filelist.append(dir)
    
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            getFileList(newDir, Filelist, ext)
 
    return Filelist
 
#org_img_folder=path + filelist_dir[0]
 
# 检索文件
#for name in filelist_dir:
#    imglist = getFileList(org_img_folder, [], 'png')
#imglist


# In[75]:


chuqin = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
#chuqin = []


# In[ ]:


from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

i = -1
for name in filelist_dir:
    org_img_folder=path + name
    imglist = getFileList(org_img_folder, [], 'png')
    number = 1
    i = i + 1
    for name_file in imglist:
        img_path = name_file
        result = ocr.ocr(img_path, cls=True)
        for line in result:
            print(line)
        
        # 显示结果

        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        print(i)
        for word_x in txts:
            if word_x == '马':
                word_x = '马珺'
            if word_x == '潘润家长':
                word_x = '潘润'
            for word_y in word_list:
                if word_x[-3:] == word_y or word_x[-2:] == word_y[-2:]:
                    flag = 0
                    for word_z in chuqin[i]:
                        if word_y == word_z:
                            flag = 1
                    if flag == 0:
                        chuqin[i].append(word_y)
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang_ttf/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('result/result' + name + '_' + str(number) + '.jpg')
        number = number + 1


# In[ ]:


chuqin[0]


# In[ ]:


for i in range(15):
    print(len(chuqin[i]))


# In[ ]:


tongji = np.zeros((80, 15))
for i in range(15):
    for j in range(80):
        for word_exam in chuqin[i]:
            if word_list[j] == word_exam:
                tongji[j][i] = 1


# In[ ]:


columns = ['0']*17
columns[0] = 'number'
columns[1] = 'name'
k = 2
for filename_x in filelist_dir:
    columns[k] = filename_x
    k = k + 1
data = [['0']*17 for i in range(80)]
for i in range(80):
    data[i][0] = num_list[i]
    data[i][1] = word_list[i]
for i in range(2, 17):
    for j in range(80):
        data[j][i] = tongji[j][i - 2]
df = pd.DataFrame(columns=columns, data=data)

df


# In[ ]:


#将DataFrame存储为csv,index表示是否显示行名，default=True，path指写入的文件名称
df.to_csv('出勤统计.csv', index=True, sep=',', encoding = 'utf_8_sig')


# In[ ]:




