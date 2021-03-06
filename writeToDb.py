# IMPORT HEADER FROM HEADER.PY
from header import *

# for work with directories
import os
# for .flac to .wav converting
from pydub import AudioSegment

# import text_into_phrases
from text_into_phrases import *

# for random text:
from read_text import *

# about audio file >>>>>>>>:
DURATION_of_all_phrase = 20
TIME_TO_SPLIT = 4.5
# about audio file <<<<<<<<


# ABOUT DATASET>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# dataset directory
dataset_directory = 'real_voices'

# # number of persons to learn (at all = 40):
# number_of_persons_to_learn = 5

# minimal number of records per each person = 55

# sequence number of record from start FROM
# //////////////////////
number_to_learn_FROM = 0
# //////////////////////

# number of records to learn:
number_to_learn = 3
# sequence number of record to learn TO
number_to_learn_TO = number_to_learn_FROM+number_to_learn

# avout dataset <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# temporary directory for phrases
temp_directory_for_phrases = 'temp_directory_for_phrases/demo/'

# VOICE-FILE RECORDING:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# timer>>>>>:
# isSilent flag. whn thiflag is silent, than recording is stop
letsStop = False

def timeout():
    global letsStop
    letsStop=True

    # duration is in seconds
t = Timer(DURATION_of_all_phrase, timeout)
# timer<<<<<<
def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    # let's make it not truncate when it is silent
    return max(snd_data) < THRESHOLD
    # return isSilent

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')
  
    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True
            # start timer: >>>
            t.start()
            # start timer <<<<

        # if snd_started and num_silent > 30:
        #     break
        if letsStop:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    # r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
# VOICE-FILE RECORDING:<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


if __name__ == '__main__':

# # 3 REAL PERSONS VOICE RECORDING PART : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # first sample in Db: 
#    # create dataset.csv with mfccs header
#     with open('demo_dataset.csv','w') as file:
#         # strLine = 'person, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13'
#         strLine = 'person, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24'
#         file.write(strLine)
#         file.write('\n')
#     # let's split voices:
#     split_all_files(PERSONS_DIRECTORY_FROM, dataset_directory, TIME_TO_SPLIT)
#     # extract all person's (folders)
#     persons_to_learn = os.listdir(dataset_directory)
#     # let's write each person to Db
#     for person_dir in persons_to_learn:
#         # extract full person directory path
#         full_person_dir = os.path.join(dataset_directory, person_dir)
#         # all audio-files in current person's folder
#         files = [os.path.join(full_person_dir,f) for f in os.listdir(full_person_dir) if os.path.isfile(os.path.join(full_person_dir, f))]
#         # selected audio files from person's folder
#         files_new = files[:number_to_learn]

#         # let's foreach every file from person's folder
#         for demo in files_new:
#             # PUT THEIR NAME OF CURRENT INDIVIDUAL SAMPLE
#             LABEL = person_dir
#             # # for DICTORS: >>>>>>>>>>>>>>>>>>>>>>>>>
#             #     # let's convert .flac to .wav
#             # demo = AudioSegment.from_file(demo, "flac")

#             # # convert to .wav
#             # demo.export("demo.wav", format="wav")
#             # (rate,sig) = wav.read("demo.wav")
#             # # for DICTORS <<<<<<<<<<<<<<<<<<<<<<<<<

#             # for REAL VOICES: >>>>>>>>>>>>>>>>>>>>
#             # read .wav file
#             (rate,sig) = wav.read(demo)
#             # extract mfccs from demo.wav
#             # for REAL VOICES <<<<<<<<<<<<<<<<<<<<
            
#             # EXTRACT MFCCs FROM SIG, RATE:
#             mfcc_feat = mfcc(sig,rate,winlen=0.094,nfft=FFT_LENGTH, numcep=numcep, lowfreq=lowfreq, highfreq=highfreq) #bachlor parameter

#             #let's dump mfccs string to .csv:
#             with open('demo_dataset.csv','a') as file:
#                 for line in mfcc_feat:
#                     strLine = str(LABEL) + ',' + ','.join(map(str, line))
#                     file.write(strLine)
#                     file.write('\n')
#         # message to terminal after every person is recorded to DB-file
#         print("mfccs of "+str(person_dir)+" was recorded to .csv")
                        
# # 3 REAL PERSONS VOICE RECORDING PART  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# =========================================================================================

# REAL PERSON VOICE RECORDING PART: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  recording part
    # print("please, enter your name:")
    # label = input("")
    # PUT THEIR NAME OF CURRENT INDIVIDUAL SAMPLE
    # LABEL = "y"
    # print("ваше ім'я:" + str(LABEL))
    LABEL = input("введіть своє ім'я (на англійській): ")

    print('==================================================================================')
    print("прочитайте фразу в мікрофон поки не вісвітиться повідомлення (20 сек):")
    print('==================================================================================')

    print(read_random_text(10))
    # print(str(random_sentence))
    record_to_file('demo.wav')

    print('==================================================================================')
    print('==================================================================================')
    print('==================================================================================')
    print('==================================================================================')
    print('=================================ФРАЗА ЗАПИСАНА!=================================')
    print('==================================================================================')
    print('==================================================================================')
    print('==================================================================================')
    print('==================================================================================')
    
    # # COMMENT CODE BELOW IF THIS IS NOT FIRST RECORD FOR THIS DB: >>>>>>>>>
    # # create dataset.csv with mfccs header
    # with open('demo_dataset.csv','w') as file:
    #     # strLine = 'person, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13'
    #     strLine = 'person, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24'
    #     file.write(strLine)
    #     file.write('\n')
    # # COMMENT CODE ABOVE IF THIS IS NOT FIRST RECORD FOR THIS DB: <<<<<<<<<


    # let's delete directory:
    delete_folder_content(temp_directory_for_persons)
    # let's split voice to smaller audio files:
    split_file('',temp_directory_for_persons, 'demo.wav', TIME_TO_SPLIT)
    
     # all audio-files in current person's folder
    files = [os.path.join(temp_directory_for_phrases,f) for f in os.listdir(temp_directory_for_phrases) if os.path.isfile(os.path.join(temp_directory_for_phrases, f))]

    files_to_learn = files[:number_to_learn]              

    for file_phrase in files_to_learn:
        (rate,sig) = wav.read(file_phrase)
        mfcc_feat = mfcc(sig,rate,winlen=0.094,nfft=FFT_LENGTH, numcep=numcep, lowfreq=lowfreq, highfreq=highfreq) #bachlor parameter

        # st sample in Db:
        #text=List of strings to be written to file
        with open('demo_dataset.csv','a') as file:
            for line in mfcc_feat:
                strLine = str(LABEL) + ',' + ','.join(map(str, line))
                file.write(strLine)
                file.write('\n')

    print("mfccs було записано в .csv")
# REAL PERSON VOICE RECORDING PART <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<