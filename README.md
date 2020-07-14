# Voice authentication application prototype based on MFCCs, K-Nearest Neighbours (K-NN), Local Outlier Factor (LOF). 
### With using of [Scikit learn](https://scikit-learn.org/stable/) and [python_speech_features](https://python-speech-features.readthedocs.io/en/latest/) libs.
## Theoretical background of using such Machine Learning methods and parameters 
This application was created as part of a [master's thesis](https://ela.kpi.ua/handle/123456789/32176) [(presentation)](http://mmsa.kpi.ua/sites/default/files/abstracts/2019_m_sai_grushko_y_uk_presentation.pdf) (in Ukrainian language). As you can see in the presentation the unique scheme of voice authentication system was proposed, the main blocks of which were the voiceprint extraction method **MFCCs**, **K-NN** classifier and **LOF** method of detecting anomalies. System parameters and ML methods were chosen to minimize computer resources, minimize incorrectly recognized persons, minimize processing speed and maximize correctly recognized persons. This parameters were optimized using a voice samples of 40 different individuals. Precision of this app at dataset of 80 voice samples of **40** different peoples was **96%.** 
In terms of speed, the average duration of voice processing when learning the system was **22** seconds (processed 20 seconds of speech). And during authentication, when 6 seconds of speech were processed, signal processing lasted **2 seconds**.
Thus, the primary goal of the thesis was achieved - to build a fast and unpretentious to computing resources system of voice biometrics, which, moreover, would have a sufficiently high accuracy.
## Steps to run project
### 1. Initial voice recording and Voiceprint (MFCCs) extraction   
#### Open writeToDb.py file and
comment this: 
```
# 3 REAL PERSONS VOICE RECORDING PART : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
...  
# comment this  
...  
# 3 REAL PERSONS VOICE RECORDING PART  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   
```
And uncomment this part:  
```
#REAL PERSON VOICE RECORDING PART: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
...  
#uncomment this  
...  
#REAL PERSON VOICE RECORDING PART <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   
```
#### then launch this writeToDb.py and follow the instructions in terminal. 
such way record the voices of 3 people  
  
### 3. Learning K-NN Classifier   
To learn Classifier run learning.py . Python will use demo_dataset.csv file with MFCCs coefficients created on previous step. The result of learning will be model of K-NN classifier (Classifier_model.joblib) and LabelEncoder.joblib file, that will be  needed for authentication.  
  
### 4. Let's pass authentication 
Launch authentication.py file and follow instructions in terminal. The result will be something like that (for me):  
```
{-1: 240, 1: 202}  
NOVELTY_RELATION: 0.457  
RELATION: 5.516  
individual: yaroslav  
action: ALLOW
```
#### Description of authentication.py output:
```individual: yaroslav``` is person that was identificated with voice that was recorded on step 4. action:   
```ALLOW``` mean that application recognized this person and varified as yaroslav and allow access to, exampl, secret files.    
```RELATION``` is the ratio of the probability of the forecast of the person with the highest probability of recognition to the probability of the second person with the highest probability.  
```NOVELTY_RELATION``` is the probability ratio, which corresponds to the fact that the two vectors are the same. (0<=```NOVELTY_RELATION```<=1)  For my example above ```NOVELTY_RELATION```=202/(240+202)=0.457. 202 responsible for two voice samples (input with authentication and identified person) is same and 240 - that this two vectors is different.

## Other options
You can previoiusly record voices to real_voices_texts folder one time (than you needen't to record voice every time you run writeToDb.py), to do it  instead of **1st step** follow instructions below.  
### 1. Voice recording  
Record samples of voice (2 minutes length) of three different people with this file https://github.com/YaroslavGrushko/prototype-Auto/blob/master/recordBigText.py
(to record person voice only launch .py file above and the person should read any text trough 2 minutes to microphone that connected to your computer). It's automatically stops recording after 2 minutes of recording and save to demo.wav . Rename demo.wav with name of person that read text, for example for me it will be yaroslav.wav and save it to real_voices_texts folder of prototype project. Do the same with do the same with two other people. 
o now you have database of voices of 3 different people 2 minutes duration each.  
### 2. MFCCs coeficients extracting from voice  
Go to writeToDb.py file and uncomment (if it commented) section    
```  
# 3 REAL PERSONS VOICE RECORDING PART : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
...  
# uncomment this  
...  
# 3 REAL PERSONS VOICE RECORDING PART  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
``` 
And comment this part: 
```
# REAL PERSON VOICE RECORDING PART: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
...  
# comment this  
...  
# REAL PERSON VOICE RECORDING PART <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
```  
launch writeToDb.py. The result of running of this file it creating dataset of voiceprints (24 MFCCs coeficients) of three different people (that you record it's voices on previous step). It is demo_dataset.csv file you can check it. 
