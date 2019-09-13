# let's import all other imports
from header import *

# about audio file: >>>>>>>>
DURATION_of_all_phrase = 6
TIME_TO_SPLIT = 4.5
# about audio file: <<<<<<<<

# temporary directory for phrases
temp_directory_for_phrases = 'temp_directory_for_phrases/on_inspection/'

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



# ========================+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Varification
    # check if X_inspect and  X_pred belongs to one cluster
def check_by_Verificator(X_inspect, Y_inspect, X_pred, Y_pred, result_individual, IDENT_flag):

    novelty_relation = 0
    #  Local Outlier Factor (LOF)
    # novelty = True / it is to make novelty prediction.
    # when you train clean data and check it with anomaly on new data
    clf = LocalOutlierFactor(n_neighbors=20, algorithm='auto', leaf_size=30, metric='minkowski', p=2, metric_params=None,contamination='legacy', novelty=True, n_jobs=None)
   
    # let's fit with predict X-value
    clf.fit(X_pred)
    # let's predict with inspect X-value
    Y_clf_pred = clf.predict(X_inspect)
    unique, counts = np.unique(Y_clf_pred, return_counts=True)
    print(dict(zip(unique, counts)))
    # (-1)/1   novelty_relation = not_equels_count/equels_count
    if(len(counts)>1):
        novelty_relation = counts[1]/counts[0]
    else:
        novelty_relation = 9999

    print('NOVELTY_RELATION: '+str('%.3f'%(novelty_relation)))
    if novelty_relation > 0.68:
        VARIFY_flag = 2
    else:
        if novelty_relation < 0.4:
            VARIFY_flag = 0
        else:
            VARIFY_flag = 1

       
# when main method is one of both:
    if(IDENT_flag==2):
        action = "ALLOW"
    else:
        if(IDENT_flag==0):
            action = "DENY"
        # if IDENT_flag == TRY MORE
        else:
            if VARIFY_flag==2:
                action = "ALLOW"
            else:
                if VARIFY_flag==0:
                    action = "DENY"
                # if IDENT_flag == TRY MORE and VARIFY_flag==TRY MORE
                else:
                    action = "TRY MORE"

    # print("action: "+str(action))

# ///////////////////////////////////////////////////////////////////////////////////////////////////
    return result_individual, action 
# ==============================+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Varification
if __name__ == '__main__':
    # recording part
    label = "on_inspection"

    print('==================================================================================')
    print("прочитайте фразу в мікрофон поки не вісвітиться повідомлення (6 сек):")
    print('==================================================================================')

    print(read_random_text(10))
   
    record_to_file('on_inspection.wav')

    print('==================================================================================')
    print('==================================================================================')
    print('==================================================================================')
    print('==================================================================================')
    print('=================================ФРАЗА ЗАПИСАНА!=================================')
    print('==================================================================================')
    print('==================================================================================')
    print('==================================================================================')
    print('==================================================================================')

    # let's delete directory:
    delete_folder_content(temp_directory_for_persons)
    # let's split voice to smaller audio files:
    split_file('',temp_directory_for_persons, 'on_inspection.wav', TIME_TO_SPLIT)

    # all audio-files in current person's folder
    files = [os.path.join(temp_directory_for_phrases,f) for f in os.listdir(temp_directory_for_phrases) if os.path.isfile(os.path.join(temp_directory_for_phrases, f))]

    on_inspection = files[0]
    (rate,sig) = wav.read(on_inspection)
    mfcc_feat = mfcc(sig,rate,winlen=0.094,nfft=FFT_LENGTH, numcep=numcep, lowfreq=lowfreq, highfreq=highfreq)
    # le's print results
    print('\n\n')
    print('============================================================================')
    print('================================results:====================================')
    print('============================================================================')
    print('\n\n')

    print('DURATION: '+str(len(sig)/rate))
    ##text=List of strings to be written to file
    with open('on_inspection_dataset.csv','w+') as file:
        file.write('person, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24 \n')
        for line in mfcc_feat:
            strLine = str(label) + ',' + ','.join(map(str, line))
            file.write(strLine)
            file.write('\n')

    # LET'S TEST ON_INSPECTION SAMPLE
    # header = None if dataset has no header
    dataset =  pd.read_csv('on_inspection_dataset.csv',sep=',')

    # let's encode catigorial data to numbers
    dataset_encoded = dataset.copy() 
    # creating labelEncoder
    le = preprocessing.LabelEncoder()
    # Converting string labels into numbers.
    dataset_encoded['person']=le.fit_transform(dataset['person'])

    # make 2 datasets X - for input data and Y- for output
    #  input data
   # X_inspect = dataset_encoded.iloc[:, 1:14].values # for default mfccs parameters
    X_inspect = dataset_encoded.iloc[:, 1:25].values #for bachlors work mfccs parametrs
    
    #  output data
    Y_inspect = dataset_encoded.iloc[:, 0].values

# ==============================+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Identification>>>>>>>>>>>>>>>>
    # kneigbours:>>>
    # load the learned model
    clf = load('Classifier_model.joblib') 
    # let's predict 
    # simple sci-learn clissifier
    y_pred = clf.predict(X_inspect)


    counts = np.bincount(y_pred)
    counts_sorted = np.argsort(counts, axis = 0)
    index_of_max_elem = counts_sorted[len(counts) - 1]
    index_of_second_max_elem = counts_sorted[len(counts) - 2]


    max_elem = counts[index_of_max_elem]
    second_max_elem = counts[index_of_second_max_elem]

    
    # let's count percentege between 1st max and 2nd max 
    # must be from [1,9999]
    first_max_second_max_relation = max_elem/second_max_elem
    # ->>>the more so the better!

    # let's reverse from int to marks

    # load labelEncoder
    le = load('LabelEncoder.joblib') 
    # result_mark = le.inverse_transform([max_freq_item])
    result_mark = le.classes_[index_of_max_elem]

    # global current_count
    IDENT_flag =0

    # three state: ALLOW(2)/TRY MORE(1)/DENY(0):
    if(first_max_second_max_relation < 2):
        IDENT_flag=0 #DENY
    if(2 <= first_max_second_max_relation and first_max_second_max_relation < 5):
        IDENT_flag=1 #TRY MORE
    if(first_max_second_max_relation>=5):
        IDENT_flag=2 #ALLOW

    # print('RELATION:'+ str(first_max_second_max_relation))
    # ==============================+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Identification<<<<<<<<<<<<<<<<

    # let's find all X_pred according to result_mark[0]
    demo_dataset = pd.read_csv('demo_dataset.csv') 
    result_individual = result_mark
    pred = demo_dataset.loc[demo_dataset['person'].astype(str)==result_individual]
    # input data of predicted  individual
    # X_pred = pred.iloc[:, 1:14].values #for default mfccs parametrs
    X_pred = pred.iloc[:, 1:25].values #for mfccs parametrs from bachlor's work
    # output data of predicted  individual
    Y_pred = pred.iloc[:, 0].values
    # ==============================+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Varification
    individual, action = check_by_Verificator(X_inspect, Y_inspect, X_pred, Y_pred, result_individual, IDENT_flag)
    print('RELATION: '+ str('%.3f'%(first_max_second_max_relation)))
    print('individual: ' + str(individual)+'\naction: '+str(action))