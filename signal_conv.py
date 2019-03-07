#-*-coding:utf-8 -*-
# read the dir and get all the name path
import os
import array
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
            print(file_path)
            list_name.append(file_path)

    return 0

'''
def read_pcm(pcm_path,sample_rate = 16000,num_channel = 1):

    voice_data = AudioSegment.from_file(
        file = pcm_path,
        sample_width = 2,
        frame_rate = sample_rate,
        channels = num_channel)

    pcm_data = np.array(voice_data.get_array_of_samples())
    return (pcm_data / (2.**15))

def read_pcm2(pcm_path):
    data = np.memmap(pcm_path,dtpye = 'float32',mode = 'r')
    print('value',data)

'''




def read_pcm3(pcm_path,channels):
    data = []
    data1 = []
    data2 = []

    print(pcm_path)
    
    with open(pcm_path,'rb') as file:
        shortArray = array.array('h')# int16
        size = int(os.path.getsize(pcm_path)/shortArray.itemsize)
        count = int(size / channels)
        shortArray.fromfile(file, size) # faster
        if channels == 1:
            data = shortArray
            return np.array(data)/(2.0**15)
        elif channels ==2:
            data1 = (shortArray[0::2])
            data2 = (shortArray[1::2])
            return np.array(data1)/(2.0**15), np.array(data2)/(2.0**15)
        else:
            return -1



def write_pcm(pcm_path,left,right):
    
    with open(pcm_path,'wb') as file:
        out = np.zeros(2*len(left),dtype='int16')
        left = left*(2**15)
        right = right*(2**15)

        for i in range(0,left.size):
            out[2*i] = left[i]
            out[2*i + 1]= right[i]
        
        file.write(out)

        
def data_conv(data,rir):
    cc = np.convolve(data.flatten(),rir,'full')
    return cc 


list_name = []
# clean_data = read_pcm('clean.pcm',16000,1)
clean_data = read_pcm3('clean.pcm',1)
pcm_path = ''
out_path = './rev_res'
if __name__ =='__main__':

    if (len(sys.argv) < 2):
	print('please input dir path')
        os._exit(-1) 
#    out_path = pcm_path.replace('room_rir','conv_res')
#    dirp = os.path.split(out_path)[0]
#    if os.path.isdir(dirp) == False:
#        os.mkdirs(dirp)
#    if os.path.isdir(out_path) == False:
#        os.mkdir(out_path)

    pcm_path = sys.argv[1]
    listdir(pcm_path,list_name)
    print('list name is :',len(list_name))
    
 #   expath = '/mnt/hgfs/tf_download/room_rir/Room_7_9_6/dist_1_degree_75_beta_0.2.pcm'
    #list_name = expath
    for filepath in list_name:
 #       print(filepath)
        leftdata,rightdata = read_pcm3(filepath,2)
        leftconv = data_conv(np.array(clean_data),leftdata)
        rightconv = data_conv(np.array(clean_data),rightdata)
        
        roomnum = os.path.split(filepath)[0].split('/')[-1]
        dir_path =os.path.join(out_path,roomnum)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        filename = os.path.split(filepath)[1]
        final_path =os.path.join(out_path,roomnum,filename)
        print(final_path)
        write_pcm(final_path,leftconv,rightconv)


