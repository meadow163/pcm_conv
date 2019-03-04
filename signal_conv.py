#-*- coding:utf-8 -*-
# read the dir and get all the name path
import os
import numpy as np
import sys
# from pydub import AudioSegment

def get_path_name_list(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root) #当前目录路径i
        print(dirs) #当前路径下所有子目录
        print(files) #当前路径下所有非目录子文件

def file_name(file_dir):   
    L=[]   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            # file name split
            if os.path.splitext(file)[1] == '.pcm':  
                L.append(os.path.join(root, file))  
    return L  


def listdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        elif os.path.splitext(file_path)[1]=='.pcm':
            list_name.append(file_path)

def read_pcm(pcm_path,sample_rate = 16000,num_channel = 1):

    voice_data = AudioSegment.from_file(
        file = pcm_path,
        sample_width = 2,
        frame_rate = sample_rate,
        channels = num_channel)

    pcm_data = np.array(voice_data.get_array_of_samples())
    return (pcm_data / (2.**15))


'''
def read_pcm2(pcm_path):
	data = np.memmap(pcm_path,dtpye = 'float32',mode = 'r')
	print('value',data)
'''
def data_conv(data,rir):
      return  np.convolve(data,rir,'full') 


list_name = []
clean_data = read_pcm('clean.pcm',16000,2)
if __name__ =='__main__':

    if len(sys.argv < 2):
	print('para error')


    listdir(pcm_path,list_name)
    print('list name is :',len(list_name))
    for file in list_name[0]:
        rir_data = read_pcm2(pcm_path,fs,2)
        data_conv(clean,rir_data)



