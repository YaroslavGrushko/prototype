# prototype
 
# steps to run

**1.** Record samples of voice (2 minutes length) of three different people with this file https://github.com/YaroslavGrushko/prototype-Auto/blob/master/recordBigText.py
(to record person voice only launch .py file above and the person should read any text trough 2 minutes to microphone that connected to your computer). It's automatically stops recording after 2 minutes of recording and save to demo.wav . Rename demo.wav with name of person that read text, for example for me it will be yaroslav.wav and save it to real_voices_texts folder of prototype project. Do the same with do the same with two other people. 
o now you have database of voices of 3 different people 2 minutes duration each.
**2.** Go to writeToDb.py file and uncomment (if it commented) section  

3 REAL PERSONS VOICE RECORDING PART : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
...  
uncomment this  
...  
3 REAL PERSONS VOICE RECORDING PART  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
  
And comment this part:  
REAL PERSON VOICE RECORDING PART: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
...  
comment this  
...  
REAL PERSON VOICE RECORDING PART <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
  
launch writeToDb.py. The result of running of this file it creating dataset of voiceprints (24 MFCCs coeficients) of three different people (that you record it's voices on previous step). It is demo_dataset.csv file you can check it. 

