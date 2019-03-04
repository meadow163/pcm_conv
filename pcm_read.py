import numpy as np
# import matplotlib.pyplot as plt
from pydub import AudioSegment
'''
normalized data
'''
def read_pcm(pcm_path,sample_rate = 16000,num_channel = 1):

    voice_data = AudioSegment.from_file(
        file = pcm_path,
        sample_width = 2,
        frame_rate = sample_rate,
        channels = num_channel)

    pcm_data = np.array(voice_data.get_array_of_samples())
    # print(pcm_data)
    print('data length = ',len(pcm_data))
    return (pcm_data / (2.**15))



