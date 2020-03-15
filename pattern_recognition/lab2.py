#!/usr/bin/env python
# coding: utf-8


# ***
# ## Step 1
# ***

# 
#   -   Μέση τιμή pitch για άντρα ομιλητή:
#       -  α(one): 134.7Hz
#       -  ου(two): 128.8Hz
#       -  ι(three): 131.0Hz
#       -  [ου(one): 133.2Hz] 
# 
# 
#    -  Πρώτα 3 formants για άντρα ομιλητή: 
#        -  α(one): 1ο: 755.4Hz, 2ο: 1118.4Hz, 3o: 2410.6Hz
#        -  ου(two): 1ο: 349.5Hz, 2ο: 1782.5Hz, 3o: 2377.2Hz
#        -  ι(three): 1ο: 388.5Hz, 2ο: 1867.5Hz, 3o: 2284.3Hz
#        -  [ου(one): 1ο: 554.6Hz, 2ο: 998.9Hz, 3o: 2273.7Hz] 
#     
#                                   
#    - Μέση τιμή pitch για γυναίκα ομιλητή: 
#        -  α(one): 177.5Hz
#        -  ου(two): 187.6Hz
#        -  ι(three): 178.4Hz
#        -  [ου(one): 187.4Hz] 
# 
# 
#   -  Πρώτα 3 formants για γυναίκα ομιλητή: 
#         -  α(one): 1ο: 877.0Hz, 2ο: 1657.2Hz, 3o: 3076.6Hz
#         -  ου(two): 1ο: 334.5Hz, 2ο: 1737.0Hz, 3o: 2678.6Hz 
#         -  ι(three): 1ο: 333.6Hz, 2ο: 2189.6Hz, 3o: 2907.8Hz
#         -  [ου(one): 1ο: 425.9Hz, 2ο: 936.1Hz, 3o: 2454.8Hz] 
# 
# ##### Συμπεράσματα
# Το pitch είναι ένα μέγεθος που καθορίζεται από τις διαφορετικές δονήσεις που παράγει η ανθρώπινη φωνή κατά την ομιλία. Περιμένουμε χαμηλότερες τιμές pitch όταν η ηχογράφηση γινόταν από άντρα. Πράγματι, παρατηρούμε ότι το γυναικείο pitch είναι υψηλότερο από το αντρικό.
# Από τα formants μπορούμε να εξάγουμε συμπεράσματα για το ηχητικό σήμα. Παραδείγματος χάριν παρατηρούμε ότι οι γυναικες έχουν μεγαλύτερες συχνότητες στα πρώτα formants που εξετάσαμε (στις περισσότερες περιπτώσεις). Επίσης, βλέπουμε ότι τα formants έχουν παρόμοιες τιμές ανάλογα με το φώνημα.
#                                

# *** 
# ## Step 2
# ***
# Διαβάζουμε όλα τα αρχεία ήχου και παίρνουμε σε λίστες τα αρχεία wav, τον ομιλητή (με αύξον αριθμό) και το ψηφίο που ακούγεται.
# (Ο φάκελος "digits" με τις ηχογραφήσεις πρέπει να βρίσκεται στο ίδιο directory με το script. Σε διαφορετική περίπτωση το path πρέπει να τροποποιηθεί κατάλληλα)

# In[1]:


import librosa
import re
from os import listdir

def parse_data():
    wav = []
    speaker = []
    digit = []
    for file in listdir("./digits/"):
        wav.append(librosa.load("digits/"+file,sr=None)[0])
        num = re.split('(\d+)',file)
        speaker.append(num[1])
        digit.append(num[0])
    return wav, speaker, digit


# ***
# ## Step 3
# ***
# Για κάθε αρχείο wav παίρνουμε 13 συντελεστές MFCCs σε χρονικά παράθυρα 25ms και με βήμα 10ms (length = sr * 0.025, time = sr * 0.01). 
# Επίσης, υπολογίζουμε τις παραγώγους των MFCCs (deltas) καθώς και τις δεύτερες παραγώγους (delta deltas).
# 

# In[2]:


wavs, speakers, digits = parse_data()

mfccs = []
mfccs_delta = []
mfccs_delta2 = []

for i in range(len(digits)):
    M = librosa.feature.mfcc(y = wavs[i], sr = 16000, n_mfcc = 13, hop_length = 160, n_fft = 400)
    mfccs.append(M)
    D = librosa.feature.delta(M)
    mfccs_delta.append(D)
    D2 = librosa.feature.delta(M, order=2)
    mfccs_delta2.append(D2)


# ***
# ## Step 4
# ***

# Ιστογράμματα για τους αριθμούς 2 και 9 (0311402<b>2</b> και 0311414<b>9</b>)

# In[3]:


n1 = "two"
n2 = "nine"

import matplotlib.pyplot as plt

for i in range(len(digits)):
    if (digits[i]==n1):
        plt.figure(figsize=(12, 5))
        a = (mfccs[i][0], mfccs[i][1])
        plt.subplot(121)
        plt.hist(a[0], bins='auto')
        plt.title('Histogram of 1st MFCC for digit ' + n1 + ' and speaker ' + speakers[i])
        plt.subplot(122)
        plt.hist(a[1], bins='auto')
        plt.title('Histogram of 2nd MFCC for digit ' + n1 + ' and speaker ' + speakers[i])


# In[4]:


for i in range(len(digits)):
    if (digits[i]==n2):
        plt.figure(figsize=(12, 5))
        a = (mfccs[i][0], mfccs[i][1])
        plt.subplot(121)
        plt.hist(a[0], bins='auto')
        plt.title('Histogram of 1st MFCC for digit ' + n2 + ' and speaker ' + speakers[i])
        plt.subplot(122)
        plt.hist(a[1], bins='auto')
        plt.title('Histogram of 2nd MFCC for digit ' + n2 + ' and speaker ' + speakers[i])


# Επιλέγουμε τυχαία τους ομιλητές 3 και 5 και απεικονίζουμε επιπλέον από αυτά που ζητούνται και τα ακόλουθα ιστογράμματα για αντιπαραβολή με τα προηγούμενα όπου εξετάζαμε μόνο 2 χαρακτηριστικά MFCC (1ο - 2ο).

# In[5]:


n1 = "two"
n2 = "nine"

import numpy as np
import matplotlib.cm as cm

plt.figure(figsize=(24, 10))

for i in range(len(digits)):
    if (digits[i]==n1):
        if (speakers[i]==str(3)):
            plt.subplot(121)
            plt.hist(np.transpose(mfccs[i]), bins=8)
            plt.title('MFCCs for digit ' + n1 + ' and speaker ' + speakers[i])
        elif(speakers[i]==str(5)):
            plt.subplot(122)
            plt.hist(np.transpose(mfccs[i]), bins=8)
            plt.title('MFCCs for digit ' + n1 + ' and speaker ' + speakers[i])
            
plt.figure(figsize=(24, 10))

for i in range(len(digits)):
    if (digits[i]==n2):
        if (speakers[i]==str(3)):
            plt.subplot(121)
            plt.hist(np.transpose(mfccs[i]), bins=8)
            plt.title('MFCCs for digit ' + n2 + ' and speaker ' + speakers[i])
        elif(speakers[i]==str(5)):
            plt.subplot(122)
            plt.hist(np.transpose(mfccs[i]), bins=8)
            plt.title('MFCCs for digit ' + n2 + ' and speaker ' + speakers[i])            


# ##### Απεικόνιση των MFCCs

# In[6]:


import librosa.display

plt.figure(figsize=(24, 10))
        
for i in range(len(digits)):
    if (digits[i]==n1):
        if (speakers[i]==str(3)):
            plt.subplot(121)
            librosa.display.specshow(mfccs[i], x_axis = 'time')
            plt.colorbar()
            plt.tight_layout()
            plt.title('Mfccs for digit ' + n1 + ' and speaker ' + speakers[i])
        elif(speakers[i]==str(5)):
            plt.subplot(122)
            librosa.display.specshow(mfccs[i], x_axis = 'time')
            plt.colorbar()
            plt.tight_layout()
            plt.title('Mfccs for digit ' + n1 + ' and speaker ' + speakers[i])

plt.figure(figsize=(24, 10))

for i in range(len(digits)):
    if (digits[i]==n2):
        if (speakers[i]==str(3)):
            plt.subplot(121)
            librosa.display.specshow(mfccs[i], x_axis = 'time')
            plt.colorbar()
            plt.tight_layout()
            plt.title('Mfccs for digit ' + n2 + ' and speaker ' + speakers[i])
        elif(speakers[i]==str(5)):
            plt.subplot(122)
            librosa.display.specshow(mfccs[i], x_axis = 'time')
            plt.colorbar()
            plt.tight_layout()
            plt.title('Mfccs for digit ' + n2 + ' and speaker ' + speakers[i])


# ##### Σπεκτρογράμματα (εφαρμογή fourier στο αρχικό σήμα ήχου)

# In[7]:


plt.figure(figsize=(24, 10))
        
for i in range(len(digits)):
    if (digits[i]==n1):
        if (speakers[i]==str(3)):      
            D = librosa.amplitude_to_db(np.abs(librosa.stft(wavs[i])), ref=np.max)
            plt.subplot(121)
            librosa.display.specshow(D)
            plt.colorbar(format='%+2.0f dB')
            plt.title('Spectrogram for digit ' + n1 + ' and speaker ' + speakers[i])
        elif(speakers[i]==str(5)):
            D = librosa.amplitude_to_db(np.abs(librosa.stft(wavs[i])), ref=np.max)
            plt.subplot(122)
            librosa.display.specshow(D)
            plt.colorbar(format='%+2.0f dB')
            plt.title('Spectrogram for digit ' + n1 + ' and speaker ' + speakers[i])          
            
plt.figure(figsize=(24, 10))

for i in range(len(digits)):
    if (digits[i]==n2):
        if (speakers[i]==str(3)):
            D = librosa.amplitude_to_db(np.abs(librosa.stft(wavs[i])), ref=np.max)
            plt.subplot(121)
            librosa.display.specshow(D)
            plt.colorbar(format='%+2.0f dB')
            plt.title('Spectrogram for digit ' + n2 + ' and speaker ' + speakers[i])
        elif(speakers[i]==str(5)):
            D = librosa.amplitude_to_db(np.abs(librosa.stft(wavs[i])), ref=np.max)
            plt.subplot(122)
            librosa.display.specshow(D)
            plt.colorbar(format='%+2.0f dB')
            plt.title('Spectrogram for digit ' + n2 + ' and speaker ' + speakers[i]) 


#   ##### Συμπεράσματα.
# Εφαρμόζοντας το Μ/Σ Fourier έχουμε την ενέργεια κατανεμημένη σε συχνότητες. Όμως, ο ανθρώπινος εγκέφαλος δεν είναι το ίδιο ευαίσθητος σε όλες τις συχνότητες. Επομένως, έχει δημιουργηθεί συμφωνα με ψυχοακουστικές μελέτες η κλίμακα Mel, η οποία αντιστοιχίζει ισαπέχουσες μονάδες σε ισαπέχουσες τονικότητες όπως τις αντιλαμβάνεται ο άνθρωπος. Συγκεκριμένα, κάτω από 1000Hz θέλουμε φίλτρα τοποθετημένα με γραμμική απόσταση το ένα από το άλλο, ενώ πάνω από τα 1000 θέλουμε λογαριθμική. Έτσι, με την εφαρμογή της κλίμακας Mel κατά τη δημιουργία των MFCCs προσαρμόζουμε τον ήχο στα δεδομένα της ανθρώπινης ακοής.
# Κατά τη διαδικασία παραγωγής της φωνής, η γλωττίδα πάλλεται, παράγοντας έναν ήχο, ο οποίος διέρχεται από τη φωνητική οδό. Ανάλογα με την ακριβή θέση και τα χαρακτηριστικά της φωνητικής οδού προσδίδονται ορισμένα χαρακτηριστικά στον εκφερόμενο ήχο. Η φωνητική οδός λοιπόν λειτουργεί σαν «φίλτρο» για τον ήχο, που έρχεται από την «πηγή». Επομένως, θέλουμε να απομονώσουμε το «φίλτρο» για την επεξεργασία στο σύστημα μας.
# Αυτό γίνεται εφικτό με το cepstrum, το οποίο είναι το φάσμα του λογαρίθμου του φάσματος. Οι ιδιότητες του λογαρίθμου επιτρέπουν αυτό το διαχωρισμό, αφού μετασχηματίζουν το γινόμενο σε άθροισμα.
# Οι τιμές του cepstrum που προκύπτουν μπορούν να χωριστούν σε χαμηλές, που αντιστοιχούν στο «φίλτρο» και τις υψηλές που αντιστοιχούν στην «πηγή» (δηλαδή στο pitch). Συγκεκριμένα, για την εξαγωγή των MFCC Vectors εδώ χρησιμοποιήσαμε τα πρώτα 13 cepstral values, που αντιστοιχούν αποκλειστικά και μόνο στο φίλτρο. 
# 
# Όσον αφορά τα σπεκτρογραφήματα, μπορούμε να δούμε το σήμα και να μελετήσουμε ορισμένα χαρακτηριστικά του (π.χ. τα φωνήματα) ώστε να ξεχωρίσουμε τους ήχους από τα Formants και τις μεταβάσεις τους. Γενικά, στο σπεκτρογράφημα παρατηρώντας τα formants μπορούμε να πάρουμε πολλές πληροφορίες για το σήμα, όπως το φύλο του ομιλητή (οι γυναίκες όπως είδαμε στο Βήμα 1 έχουν υψηλότερες average συχνότητες στα πρώτα formants), ο τόνος της ομιλίας του για ανίχνευση συναισθημάτων (π.χ. το γέλιο έχει υψηλότερες συχνότητες) κλπ.
# Από τα MFCCs μπορούμε να πάρουμε δεδομένα πιο κοντά στην "βιολογική" αντίληψη του ανθρώπου, όπως εξηγήσαμε. Τελικά, η εικόνα από τα MFCCs είναι πολύ πιο στοχευμένη στην πληροφορία που μας ενδιαφέρει και είναι πολύ πιο εύκολο να ερμηνευθεί οπτικά αφού η "ένταση" που βλέπουμε στο διάγραμμα αντιστοιχίζεται με την ανθρώπινη αντίληψη. Επίσης, όπως θα κάνουμε στη συνέχεια, μπορούμε να βελτιώσουμε ακόμη περισσότερο το μοντέλο αν υπολογιστούν τα deltas και τα delta deltas, δηλαδή τιμές που είναι ενδεικτικές των μεταβολών για τα χαρακτηριστικά του cepstrum. 
# 

# ### Προσθήκη για το Lab2
# 
# Σε αυτό στο σημείο θα αναπαραστήσουμε τα MFSCs για τις 4 παραπάνω εκφωνήσεις. Τα MFSCs είναι τα χαρακτηριστικά που εξάγονται μετά την εφαρμογήτου Mel Filter-Bank αλλά πριν την εφαρμογή του μετασχηματισμού διακριτού συνημιτόνου.

# In[8]:


plt.figure(figsize=(24, 10))

pre_emphasis = 0.97
NFFT = 512

high_freq_mel = (2595 * np.log10(1 + (16000 / 2) / 700))
mel_points = np.linspace(0, high_freq_mel, 42)
hz_points = (700 * (10**(mel_points / 2595) - 1))
bin = np.floor((NFFT + 1) * hz_points / 16000)

fbank = np.zeros((40, int(np.floor(NFFT / 2 + 1))))
for m in range(1, 41):
    f_m_minus = int(bin[m - 1])   # left
    f_m = int(bin[m])             # center
    f_m_plus = int(bin[m + 1])    # right

    for k in range(f_m_minus, f_m):
        fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
    for k in range(f_m, f_m_plus):
        fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])


for i in range(len(digits)):
    if (digits[i]==n1):
        if (speakers[i]==str(3)):
            emphasized_signal = np.append(wavs[i][0], wavs[i][1:] - pre_emphasis * wavs[i][:-1])
            signal_length = len(emphasized_signal)
            num_frames = int(np.ceil(float(np.abs(signal_length - 400)) / 160))
            pad_signal_length = num_frames * 160 + 400
            z = np.zeros((pad_signal_length - signal_length))
            pad_signal = np.append(emphasized_signal, z)
            indices = np.tile(np.arange(0, 400), (num_frames, 1)) + np.tile(np.arange(0, num_frames * 160, 160), (400, 1)).T
            frames = pad_signal[indices.astype(np.int32, copy=False)]
            frames *= np.hamming(400)
            mag_frames = np.absolute(np.fft.rfft(frames, NFFT))  # Magnitude of the FFT
            pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))
            filter_banks = np.dot(pow_frames, fbank.T)
            filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)
            filter_banks = 20 * np.log10(filter_banks)
            plt.subplot(221)
            librosa.display.specshow(filter_banks, x_axis = 'time')
            plt.colorbar()
            plt.tight_layout()
            plt.title('Mfscs for digit ' + n1 + ' and speaker ' + speakers[i])
        elif (speakers[i]==str(5)):
            emphasized_signal = np.append(wavs[i][0], wavs[i][1:] - pre_emphasis * wavs[i][:-1])
            signal_length = len(emphasized_signal)
            num_frames = int(np.ceil(float(np.abs(signal_length - 400)) / 160))
            pad_signal_length = num_frames * 160 + 400
            z = np.zeros((pad_signal_length - signal_length))
            pad_signal = np.append(emphasized_signal, z)
            indices = np.tile(np.arange(0, 400), (num_frames, 1)) + np.tile(np.arange(0, num_frames * 160, 160), (400, 1)).T
            frames = pad_signal[indices.astype(np.int32, copy=False)]
            frames *= np.hamming(400)
            mag_frames = np.absolute(np.fft.rfft(frames, NFFT))  # Magnitude of the FFT
            pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))
            filter_banks = np.dot(pow_frames, fbank.T)
            filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)
            filter_banks = 20 * np.log10(filter_banks)
            plt.subplot(222)
            librosa.display.specshow(filter_banks, x_axis = 'time')
            plt.colorbar()
            plt.tight_layout()
            plt.title('Mfscs for digit ' + n1 + ' and speaker ' + speakers[i])
    elif (digits[i]==n2):   
        if (speakers[i]==str(3)):
            emphasized_signal = np.append(wavs[i][0], wavs[i][1:] - pre_emphasis * wavs[i][:-1])
            signal_length = len(emphasized_signal)
            num_frames = int(np.ceil(float(np.abs(signal_length - 400)) / 160))
            pad_signal_length = num_frames * 160 + 400
            z = np.zeros((pad_signal_length - signal_length))
            pad_signal = np.append(emphasized_signal, z)
            indices = np.tile(np.arange(0, 400), (num_frames, 1)) + np.tile(np.arange(0, num_frames * 160, 160), (400, 1)).T
            frames = pad_signal[indices.astype(np.int32, copy=False)]
            frames *= np.hamming(400)
            mag_frames = np.absolute(np.fft.rfft(frames, NFFT))  # Magnitude of the FFT
            pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))
            filter_banks = np.dot(pow_frames, fbank.T)
            filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)
            filter_banks = 20 * np.log10(filter_banks)
            plt.subplot(223)
            librosa.display.specshow(filter_banks, x_axis = 'time')
            plt.colorbar()
            plt.tight_layout()
            plt.title('Mfscs for digit ' + n1 + ' and speaker ' + speakers[i])
        elif (speakers[i]==str(5)):
            emphasized_signal = np.append(wavs[i][0], wavs[i][1:] - pre_emphasis * wavs[i][:-1])
            signal_length = len(emphasized_signal)
            num_frames = int(np.ceil(float(np.abs(signal_length - 400)) / 160))
            pad_signal_length = num_frames * 160 + 400
            z = np.zeros((pad_signal_length - signal_length))
            pad_signal = np.append(emphasized_signal, z)
            indices = np.tile(np.arange(0, 400), (num_frames, 1)) + np.tile(np.arange(0, num_frames * 160, 160), (400, 1)).T
            frames = pad_signal[indices.astype(np.int32, copy=False)]
            frames *= np.hamming(400)
            mag_frames = np.absolute(np.fft.rfft(frames, NFFT))  # Magnitude of the FFT
            pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))
            filter_banks = np.dot(pow_frames, fbank.T)
            filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)
            filter_banks = 20 * np.log10(filter_banks)
            plt.subplot(224)
            librosa.display.specshow(filter_banks, x_axis = 'time')
            plt.colorbar()
            plt.tight_layout()
            plt.title('Mfscs for digit ' + n1 + ' and speaker ' + speakers[i])


# Ο παραπάνω κώδικας βασίστηκε στο https://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html
# Στην ουσία υπολογίζουμε τον STFT και εφαρμόζουμε το Mel Bank-Filter ενώ δεν εφαρμόζουμε τον DCT όπως παραπάνω. Βλέπουμε ότι δεν έχουμε αποσυσχέτιση σε αντίθεση με τα MFCS κάτι που δυσκολεύει την αναγνώριση κυρίως όταν θα χρειαστεί να περάσουμε τα χαρακτηριστικά σε κάποιον classifier. Βέβαια χρησιμοποιώντας βαθιά νευρωνικά δίκτυα ή άλλους classifiers που δεν επηρεάζονται απο χαρακτηριστικά με υψηλή συσχέτιση ίσως τα αποτελέσματα να είναι αρκετά κοντά, όμως τα mfccs είναι πολύ περισσότερο διαδεδομένα λόγω της χρήσης τους με Gaussian ή Markovian μοντέλα.

# ***
# ## Step 5
# ***
# 
# Δημιουργούμε ένα scatter plot δύο διαστάσεων όπου στον έναν άξονα έχουμε το πρώτο χαρακτηριστικό και στον άλλον το δεύτερο. 
# Τα χαρακτηριστικά που απεικονίζουμε έχουν προκύψει παίρνοντας τη μέση τιμή και την τυπική απόκλιση των MFCCs στα παράθυρα και ενώνοντας σε ένα διάνυσμα.

# In[9]:


featureM = []
featureSD = []

comb = []

for i in range(len(mfccs)):
    comb.append(np.concatenate((mfccs[i], mfccs_delta[i],mfccs_delta2[i])))
    featureM.append(np.mean(comb[i], axis=1))
    featureSD.append(np.std(comb[i], axis=1))
    
features = featureM.copy()

for i in range(len(featureM)):
    features[i] = np.concatenate((featureM[i],featureSD[i]))


# In[10]:


dgts = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
markers = [(5, 0), (5, 1), (5, 2), '+', '>', 'o', 'v', '8', '*', 'X']

colors = cm.rainbow(np.linspace(0, 1, 10))

for i in range(len(mfccs)):
    for dgt, c, m in zip(dgts, colors, markers):
        if (digits[i]==dgt):
            x = features[i][0]
            y = features[i][1]
            plt.scatter(x,y,color=c, marker=m)


#   ##### Συμπεράσματα.
# Χρησιμοποιώντας διανύσματα 78 χαρακτηριστικών (13 mffcs, 13 deltas, 13 delta-deltas μέσες τιμές και διακυμάνσεις αυτών), αντί για τα αρχικά 13 των MFCCs έχουμε καλύτερη απόδοση, καθώς υπάρχει καλύτερη πληροφορία για τα συμφραζόμενα σε κάθε παράθυρο.
# Από το scatter plot βλέπουμε ότι τα διανύσματα που παίρνουμε δεν είναι γραμμικά διαχωρίσιμα.

# ***
# ## Step 6
# ***
# Θέλουμε να απεικονίσουμε το πολυδιάστατο διάνυσμα που είχαμε στα προηγούμενα ερωτήματα σε λιγότερες διαστάσεις. Η μείωση των διαστάσεων επιτυγχάνεται εφαρμόζοντας την ανάλυση Principal Component Analysis  (PCA). Δοκιμάζουμε για 2 συνιστώσες αρχικά και στη συνέχεια για 3 και δείχνουμε τα αποτελέσματα σε scatter plots όπου κάθε άξονας αντιστοιχεί σε μια συνιστώσα (principal component) που έδωσε η PCA.

# In[11]:


from sklearn.decomposition import PCA

pca2 = PCA(n_components=2)
f2 = pca2.fit_transform(features)
colors = cm.rainbow(np.linspace(0, 1, 10))

for i in range(len(f2)):
    for dgt, c, m in zip(dgts, colors, markers):
        if (digits[i]==dgt):
            x = f2[i][0]
            y = f2[i][1]
            plt.scatter(x, y,color=c, marker=m)
            
print(pca2.explained_variance_ratio_)


# In[12]:


from mpl_toolkits.mplot3d import Axes3D 

pca3 = PCA(n_components=3)
f3 = pca3.fit_transform(features)
colors = cm.rainbow(np.linspace(0, 1, 10))

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

for i in range(len(f3)):
    for dgt, c, m in zip(dgts, colors, markers):
        if (digits[i]==dgt):
            x = f3[i][0]
            y = f3[i][1]
            z = f3[i][2]
            ax.scatter(x, y, z, color=c, marker=m)
            
            
print(pca3.explained_variance_ratio_)


# ##### Αποτελέσματα
# Για κάθε συνιστώσα που προέκυψε από τη μείωση των διαστάσεων με PCA, παίρνουμε το ποσοστό της αρχικής διασποράς που διατηρεί. Εδώ έχουμε τις τιμές 0.58 0.11 και 0.10 αντίστοιχα. Η συνολική διασπορά δε θα αλλάξει, αλλά θα μοιραστεί με διαφορετικό τρόπο στις νέες συνιστώσες που θα προκύψουν από την PCA, αφού η τακτική αυτή δεν αλλάζει την πληροφορία που διαθέτουμε αλλά μόνο τις συνιστώσες με τις οποίες την εκφράζουμε. Η πρώτη διάσταση  διατηρεί σημαντικό ποσοστό, ενώ μικρότερα ποσοστά έχουμε στις άλλες 2 συνιστώσες. Η πρώτη συνιστώσα διατηρεί πολύ μεγαλύτερη διασπορά και ενώ υπάρχει μείωση όσο αυξάνονται οι συνιστώσες, η μεγαλύτερη απόκλιση παρατηρείται μεταξύ της πρώτης και της δεύτερης. Άρα βλέπουμε ότι τα πρώτα principal components διατηρούν την περισσότερη διασπορά που μπορεί να διατηρηθεί από αυτό τον αριθμό components, ενώ τα τελευταία διατηρούν τη λιγότερη δυνατή διασπορά.

# ***
# ## Step 7
# ***

# Ταξινομούμε τα δεδομένα με τον Bayesian ταξινομητή που υλοποιήσαμε στο 1ο εργαστήριο και με τον έτοιμο Naive Bayes. Δοκιμάσαμε επιπλέον 2 ταξινομητές, τον K-Neighbors και τον SVC, με δύο kernels (γραμμικό και σιγμοειδές).
# 
# ##### Bonus.
# Χρησιμοποιούμε ως επιπλέον χαρακτηριστικά το zero-crossing rate και την ενέργεια βραχέως χρόνου. 

# In[13]:


def zeroCrossingRate(frame):
    signs = np.sign(frame)
    signs[signs == 0] = -1
    return len(np.where(np.diff(signs))[0])/len(frame)

def shortTermEnergy(frame):
    return sum( [ abs(x)**2 for x in frame ] ) / len(frame)

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

scaler = StandardScaler()

features_f = features.copy() 

# comment out for adding or removing extra features
for i,wav in enumerate(wavs):
    features_f[i] = np.append(features[i],zeroCrossingRate(wav))
    features_f[i] = np.append(features_f[i],shortTermEnergy(wav))

X_train, X_test, y_train, y_test = train_test_split(features_f, digits, test_size=0.3)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# In[14]:


from sklearn.base import BaseEstimator, ClassifierMixin

D = {0: 'one', 1: 'two', 2: 'three', 3: 'four', 
           4: 'five', 5: 'six', 6: 'seven', 7: 'eight', 8: 'nine'}
D_ = {v: k for k, v in D.items()}

class MyNB(BaseEstimator, ClassifierMixin):  
    """Classify samples using our own Naive Bayes Classifier"""

    def __init__(self):
        self.X_mean_ = None
        self.X_var_ = None
        self.a_priori_ = None


    def fit(self, X, y, variation="else", var_smooth=0.001):
        meanlist = []
        varlist = []
        lis = [[] for i in range(9)]

        for idx,num in enumerate(y):
            lis[D_[num]].append(X[idx,:])

        arr = np.array(lis)
        
        for i in range(9):
            mean = np.mean(arr[i], axis=0)
            meanlist.append(mean)
            var = np.var(arr[i], axis=0)
            varlist.append(var)
        
        a_priori = np.zeros(9)
        for i in y:
            a_priori[D_[i]]+=1
        a_priori = np.true_divide(a_priori, a_priori.sum(axis=0, keepdims=True))
        
        self.X_mean_ = np.array(meanlist)
        if (variation == 1):
            self.X_var_ = np.ones((9,256))
        else:
            self.X_var_ = np.array(varlist) + var_smooth
        self.a_priori_ = np.array(a_priori)
        return self


    def predict(self, X):
        resultlist = []
        a_priori = np.log(self.a_priori_)
        log_var = np.log(self.X_var_)

        for n in X:
            logMAPlist = []

            for i in range(9):
                logMAP = a_priori[i]
                logMAP -= 0.5*np.sum(log_var[i])
                logMAP -= 0.5*np.sum(((n-self.X_mean_[i])**2)/self.X_var_[i])
                logMAPlist.append(logMAP)
    
            res = logMAPlist.index(max(logMAPlist))
            resultlist.append(res)
        
        return resultlist;
        
        
    def score(self, X, y):
        correct = 0
        acc = zip(y,self.predict(X))
        for i in acc:
            if(D_[i[0]] == i[1]):
                correct+=1
        return correct/len(y)


# In[15]:


mnb = MyNB()
mnb.fit(X=X_train, y=y_train)
print ('Our classifier score: ' + str(mnb.score(X_test,y_test)))

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(X_train, y_train)
print ('Naive Bayes score: ' + str(clf.score(X_test,y_test)))

from sklearn.neighbors import KNeighborsClassifier
knc = KNeighborsClassifier(1)
knc.fit(X_train,y_train)
print ('K-Neighbors score: ' + str(knc.score(X_test,y_test)))


# In[16]:


from sklearn.svm import SVC
svc = {}
for i in ['linear', 'sigmoid']:
    svc[i] = SVC(kernel=i, gamma='auto',probability=True)
    svc[i].fit(X_train,y_train)
    print ('SVC with ' + str(i) + ' kernel ' + str(svc[i].score(X_test,y_test)))


# #### Αποτελέσματα.
# 
# ##### Χωρίς επιπλέον χαρακτηριστικά
# Our classifier score: 0.45
# Naive Bayes score: 0.45
# K-Neighbors score: 0.7
# SVC with linear kernel 0.6
# SVC with sigmoid kernel 0.575
# 
# ##### Με zero-crossing rate
# Our classifier score: 0.675
# Naive Bayes score: 0.675
# K-Neighbors score: 0.6
# SVC with linear kernel 0.825
# SVC with sigmoid kernel 0.7
# 
# ##### Με ενέργεια βραχέως χρόνου 
# Our classifier score: 0.6
# Naive Bayes score: 0.6
# K-Neighbors score: 0.55
# SVC with linear kernel 0.725
# SVC with sigmoid kernel 0.55
# 
# ##### Με zero-crossing rate και ενέργεια βραχέως χρόνου
# Our classifier score: 0.725
# Naive Bayes score: 0.725
# K-Neighbors score: 0.6
# SVC with linear kernel 0.675
# SVC with sigmoid kernel 0.75
# 
# Βλέπουμε ότι μεταξύ των δύο πρώτων ταξινομητών έχουμε καλύτερα αποτελέσματα με τη δική μας υλοποιήση αλλά, όπως είχαμε δει και από την πρώτη εργαστηριακή άσκηση, ο SVC δίνει καλύτερα αποτελέσματα στις περισσότερες περιπτώσεις.
# Έπειτα, προσθέτουμε στα χαρακτηριστικά και κάποιες επιπλέον ποσότητες. Αρχικά, δοκιμάζουμε το zero-crossing rate και στη συνέχεια την ενέργεια βραχέως χρόνου. Προφανώς, προσθέτοντας περισσότερα χαρακτηριστικά έχουμε καλύτερα αποτελέσματα, βέβαια χάνουμε από την υπολογιστική ταχύτητα (π.χ. παρατηρούμε εύκολα ότι για τον υπολογισμό της ενέργειας βραχέως χρόνου απαιτείται σημαντικός χρόνος υπολογισμού). 

# ***
# ## Step 8
# ***

# Στο βήμα αυτό χρησιμοποιήσαμε τον κώδικα που δόθηκε για την κλάση BasicLSTM στο εσωτερικό της οποίας όμως χρησιμοποιούμε την έτοιμη υλοποίηση για GRU (Gated recurrent unit), μια παραλλαγή RNN (Recurrent Neural Network) που μείωνει την πολυπλοκότητα, λύνει το πρόβλημα της έλλειψης μακροχρόνιας μνήμης, καθώς με χρήση memory cell "θυμάται" καλύτερα σε μεγαλύτερο εύρος παλιές τιμές. Για αυτούς τους λόγους χρησιμοποιείται και ευρέως μαζί με το LSTM αντί για συμβατικά RNN. Δημιουργούμε τυχαίες ακολουθίες ημιτόνων και συνιμιτόνων σε batches και προβλέπουμε τις εξόδους με δεδομένα τα ημίτονα test. Τυπώνουμε το ολικό loss.

# In[51]:


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.set_default_tensor_type('torch.FloatTensor')

class BasicLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(BasicLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.gru = nn.GRU(input_dim, hidden_dim)
        self.init_hidden()

    def init_hidden(self):
        self.hidden = torch.zeros(1,1,10)
    
    def forward(self, features, lengths=None):
        """ Features: N x L x D
            N: batch index
            L: sequence index
            D: feature index
            lengths: N x 1 -> lengths of sequences (needed for pack_padded_sequence nad pad_packed_sequence)
         """
        features = features.unsqueeze(1)
        output, _ = self.gru(features, self.hidden)
        output.squeeze_(1)

        return output

batches = 50

t = []
x_t = []
y_t = []

r = np.random.uniform(0,1/40,batches)
for i in range(batches):
    t.append(np.linspace(r[i],1/40,10))
    
for i in range(batches):
    x_t.append(np.sin(80*np.pi*t[i]))
    y_t.append(np.cos(80*np.pi*t[i]))

X_train = torch.from_numpy(np.asarray(x_t)).type(torch.FloatTensor)
Y_train = torch.from_numpy(np.asarray(y_t)).type(torch.FloatTensor)

r = np.random.uniform(0,1/40,batches)
for i in range(batches):
    t.append(np.linspace(r[i],1/40,10))

for i in range(batches):
    x_t.append(np.sin(80*np.pi*t[i]))
    y_t.append(np.cos(80*np.pi*t[i]))
    
X_test = torch.from_numpy(np.asarray(x_t)).type(torch.FloatTensor)
Y_test = torch.from_numpy(np.asarray(y_t)).type(torch.FloatTensor)

rnn = BasicLSTM(10, 10)

loss_function = nn.MSELoss()
optimizer = optim.SGD(rnn.parameters(), lr=0.1)

for epoch in range(400):
    rnn.zero_grad()
    rnn.init_hidden()
    pred = rnn(X_train)
    loss = loss_function(pred, Y_train)
    loss.backward()
    optimizer.step()

   
with torch.no_grad():
    output = rnn(X_test)
    loss = loss_function(output, Y_test)
    print(loss)


# # Main Part

# ## Step 9

# In[242]:


from glob import glob
import os

from sklearn.preprocessing import StandardScaler

def parser(directory):
    # Parse relevant dataset info
    files = glob(os.path.join(directory, '*.wav'))
    fnames = [f.split('/')[2].split('.')[0].split('_') for f in files]
    ids = [f[2] for f in fnames]
    y = [int(f[0]) for f in fnames]
    speakers = [f[1] for f in fnames]
    _, Fs = librosa.core.load(files[0], sr=None)

    def read_wav(f):
        global Fs
        wav, fs = librosa.core.load(f, sr=None)
        return wav

    # Read all wavs
    wavs = [read_wav(f) for f in files]

    # Extract MFCCs for all wavs
    window = 30 * Fs // 1000
    step = window // 2
    frames = [librosa.feature.mfcc(wav, Fs, n_fft=window, hop_length=window - step, n_mfcc=6).T for wav in wavs]
    # Print dataset info
    print('Total wavs: {}'.format(len(frames)))

    # Standardize data
    scaler = StandardScaler()
    scaler.fit(np.concatenate(frames))
    for i in range(len(frames)):
        frames[i] = scaler.transform(frames[i])

    # Split to train-test
    X_train, y_train, spk_train = [], [], []
    X_test, y_test, spk_test = [], [], []
    test_indices = ['0', '1', '2', '3', '4']
    for idx, frame, label, spk in zip(ids, frames, y, speakers):
        if str(idx) in test_indices:
            X_test.append(frame)
            y_test.append(label)
            spk_test.append(spk)
        else:
            X_train.append(frame)
            y_train.append(label)
            spk_train.append(spk)

    return X_train, X_test, y_train, y_test, spk_train, spk_test


# In[243]:


from sklearn.model_selection import train_test_split

X, X_test, y, y_test, _, _ = parser("fsddm/recordings/")
X_train, X_val, y_train, y_val = train_test_split(X,y,test_size=0.2,stratify=y)


# ## Step 10 - 11

# Θέλουμε ένα μοντέλο για κάθε ψηφίο επομένως πρέπει τα δεδομένα να διαχωριστούν ανάλογα για κάθε ψηφίο.
# Δημιουργούμε ένα μαρκοβιανό μοντέλο για κάθε ψηφίο, και συνδυάζουμε όλες τις εκφωνήσεις σε μια λίστα ώστε για την εκπαίδευση του μοντέλου του εκάστοτε ψηφίου να έχουν χρησιμοποιηθεί όλες οι εκφωνήσεις. 
# Για την εκπαίδευση του μοντέλου αρχικοποιούμε τους πίνακες: για την αρχική πιθανότητα όπως δίνεται από την εκφώνηση σε 0,1 και για το transition matrix θεωρούμε αρχικά ισοπίθανες τις μεταβάσεις άρα στις διαδοχικές θέσεις δίνουμε 0.5 και 0.5, εκτός από την τελευταία που είναι προφανώς 1.
# Εκπαιδεύουμε το μοντέλο με κριτήριο ή τον αριθμό των επαναλήψεων ή ένα threshold για το λογάριθμο της πιθανοφάνειας, όπως ορίζονται από τα parameters στην model.fit.
# Τελικά έχουμε 10 μοντέλα, ένα για κάθε ψηφίο.

# In[244]:


import itertools
import matplotlib.pyplot as plt

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()


# In[245]:


def number_dictionary(X, Y):
    dictionary = {}
    for d in range(10):
        x = [X[i] for i in range(len(X)) if Y[i] == d]
        y = [d for i in range(len(x))]  
        dictionary[d] = (x, y)
    return dictionary

D_train = number_dictionary(X_train, y_train)
D_val = number_dictionary(X_val, y_val)
D_test = number_dictionary(X_test, y_test)


# In[248]:


from pomegranate import *

n_states = 3 # the number of HMM states
n_mixtures = 2 # the number of Gaussians
gmm = True # whether to use GMM or plain Gaussian

GHMM = {}

for d in range(10):  
    X, y = D_train[d]
        
    dists = [] # list of probability distributions for the HMM states
    for i in range(n_states):
        X_dic = np.concatenate(X)
        if gmm:
            a = GeneralMixtureModel.from_samples(MultivariateGaussianDistribution, n_mixtures, X_dic)
        else:
            a = MultivariateGaussianDistribution.from_samples(X_dic)
        dists.append(a)
    
    starts = np.zeros(n_states)
    starts[0] = 1 
    ends = np.zeros(n_states)
    ends[-1] = 1
    
    # transitions only possible for consecutive states
    # for final element possibility is 1
    trans_mat = np.zeros((n_states, n_states))
    for i in range(n_states):
        for j in range(n_states):
            if(j==i):
                trans_mat[i,j] = 0.5
            elif(j==i+1):
                trans_mat[i,j] = 0.5           
    trans_mat[-1, -1] = 1
    
    # combine all data in one list
    data = [] 
    for x in X:
        data.append(x.tolist())
    
    # Define the GMM-HMM
    model = HiddenMarkovModel.from_matrix(trans_mat, dists, starts, ends, state_names=['s{}'.format(i) for i in range(n_states)])
    
    # Fit the model
    model.fit(data, max_iterations=5, stop_threshold=1e-6)
    
    GHMM[d] = model
      


# ## Step 12

# Για να υπολογίσουμε το λογάριθμο της πιθανοφάνειας, τρέχουμε τον αλγόριθμο viterbi στα δεδομένα του validation set, δηλαδή για κάθε εκφώνηση κάθε ψηφίου. Από τους λογαρίθμους που προκύπτουν κρατάμε το μέγιστο. Η τιμή της μέγιστης πιθανοφάνειας υποδεικνύει το ψηφίο που ήταν πιθανότερο να ακούστηκε στην εκάστοτε εκφώνηση. 
# Υπολογίζουμε την ακρίβεια της εκτίμησης και δοκιμάζουμε διαφορετικές τιμές για τις παραμέτρους του μοντέλου. Δοκιμάζουμε όπως δίνεται από την εκφώνηση στο βήμα 11 αριθμό καταστάσεων 1-4 για το HMM και 2-5 για το GMM. Ενδεικτικά οι τιμές για τις διάφορες τιμές των καταστάσεων του μαρκοβιανού μοντέλου:
#  - Για n_states = 1 και n_mixtures = 2 Accuracy for validation set is 0.8629629629629629
#  - Για n_states = 2 και n_mixtures = 2 Accuracy for validation set is 0.9333333333333333
#  - Για n_states = 3 και n_mixtures = 2 Accuracy for validation set is 0.9592592592592593
#  - Για n_states = 4 και n_mixtures = 2 Accuracy for validation set is 0.9629629629629629
# 
# Η διαδικασία αυτή βοηθάει στην αξιολόγηση του συστήματος πρόβλεψης ώστε να βελτιώσουμε - εκτιμήσουμε το μοντέλο πριν αυτό δοκιμαστεί στα "πραγματικά" δεδομένα, δηλαδή στο test set. Έτσι μπορούμε να τροποποιήσουμε τις παραμέτρους και να πάρουμε καλύτερα αποτελέσματα, δηλαδή έχουμε ενα feedback για τον predictor.
# Αν χρησιμοποιούσαμε το test set ως validation δεν θα είχαμε καμία ιδέα για την επίδοση του μοντέλου μας αφού δεν μπορούμε να χρησιμοποιήσουμε το set αυτό ως test καθώς επηρέασε τις αποφάσεις μας σχετικά με τις υπερπαραμέτρους.

# In[250]:


from sklearn.metrics import accuracy_score, confusion_matrix

pred = []
real = []
for d in range(10):
    X, y = D_val[d]
    for sample in X:
        prob = []
        real.append(d)
        for i in range(10):
            logp, _ = GHMM[i].viterbi(sample) # Run viterbi algorithm and return log-probability
            prob.append(logp)
        maxprob =  np.argmax(prob)
        pred.append(maxprob)

    
acc = accuracy_score(pred, real)
print('Accuracy for validation set is ' + str(acc))


# ## Step 13

# Για το validation set σχεδιάζουμε το confusion matrix. Βλέπουμε ότι οι μεγαλύτερες τιμές είναι στη διαγώνιο, δηλαδή τις περισσότερες φορές η τιμή της πρόβλεψης συμπίπτει με την πραγματική τιμή του ψηφίου. Υπάρχουν κάποιες λάθος εκτιμήσεις, που μπορούμε να δούμε από τον πίνακα, π.χ. το 6 με το 3, το 2 με το 3 κλπ.
# 
# Έπειτα, επαναλαμβάνουμε τη διαδικασία πρόβλεψης και αξιολόγησης και για το test set και σχεδιάζουμε πάλι το confusion matrix.

# In[251]:


print('For Validation Set \n')
conf_matrix = confusion_matrix(pred, real, labels=[i for i in range(10)])
plot_confusion_matrix(conf_matrix, classes=[i for i in range(10)])
plt.show()


# In[252]:


pred = []
real = []

for d in range(10):
    X, y = D_test[d]
    for sample in X:
        prob = []
        real.append(d)
        for i in range(10):
            logp, _ = GHMM[i].viterbi(sample) # Run viterbi algorithm and return log-probability
            prob.append(logp)
        maxprob =  prob.index(max(prob))
        pred.append(maxprob)

print('For Test Set \n')

acc = accuracy_score(pred, real)
print('Accuracy for test set is ' + str(acc) + '\n')

conf_matrix = confusion_matrix(pred, real, labels=[i for i in range(10)])
plot_confusion_matrix(conf_matrix, classes=[i for i in range(10)])
plt.show()


# ## Step 14

# Στο μέρος αυτό χρησιμοποιούμε ένα LSTM (Long short-term memory) μια παραλλαγή RNN για να ταξινομήσουμε τα ψηφία που εκφωνούνται. Αρχικά χρησιμοποιήσαμε όπως βλέπουμε στο κάτω μέρος τις κλάσεις για το Dataset αλλά και για το BasicLSTM που μας δόθηκαν και συμπληρώσαμε ότι ήταν απαραίτητο. Αξίζει να τονιστεί η προσθήκη Dropout αλλά και L2 Regularization που μας έδωσαν βελτίωση στα αποτελέσματα καθώς αποφεύγουμε το overfitting. Στο dropout χρησιμοποιήθηκε η έτοιμη υλοποίηση του pytorch στην οποία δώσαμε ποσοστό 30% ως όρισμα αφού έχουμε τα καλύτερα αποτελέσματα. Το dropout στην ουσία επιλέγει να μη χρησιμοποιεί σε κάθε στάδιο της εκπαίδευσης ένα τυχαίο μέρος (σταθερό ποσοστό) των νευρώνων του δικτύου ενώ κατα την πρόβλεψη μειώνει εξόδους κατά έναν παράγοντα ανάλογο του ποσοστού. Το dropout όπως είπαμε βοηθάει στην αποφυγή του overfitting αφού επικεντρωνόμαστε στην ευρωστότητα των χαρακτηριστικών. Επίσης, δίνοντας ως όρισμα στον optimizer weight_decay=0.01 (διάφορο του 0) χρησιμοποιούμε και L2 regularization. Η παράμετρος της L2 regularization επηρεάζει τη συνάρτηση κόστους και έχει ως αποτέλεσμα τη μείωση των βαρών και της πολυπλοκότητας του μοντέλου.
# Μια άλλη βελτίωση που κάναμε στο μοντέλο μας ήταν η μετατροπή σε Bidirectional LSTM. Η μετατροπή αυτή έχει ως αποτέλεσμα τον διπλασιασμό του μεγέθους του δικτύου και την επέκταση του forward propagation σε δύο στάδια αφού γίνεται προς τα εμπρός χρονικά αλλά και από το τέλος στην αρχή και συνδυάζονται οι προβλέψεις. Έτσι η πρόβλεψη μας δεν εξαρτάται μόνο από τα προηγούμενα στιγμιότυπα αλλά και από τα επόμενα με αποτέλεσμα να έχουμε καλύτερη αντίληψη του context και έτσι καλύτερες προβλέψεις. 

# In[198]:


from torch.utils.data import Dataset

class FrameLevelDataset(Dataset):
    def __init__(self, feats, labels):
        """
            feats: Python list of numpy arrays that contain the sequence features.
                   Each element of this list is a numpy array of shape seq_length x feature_dimension
            labels: Python list that contains the label for each sequence (each label must be an integer)
        """
        self.lengths =  [len(feats[i]) for i in range(len(feats))] 
        self.feature_dim = len(feats[0][0])
        self.feats = self.zero_pad_and_stack(feats)
        if isinstance(labels, (list, tuple)):
            self.labels = np.array(labels).astype('int64')

    def zero_pad_and_stack(self, x):
        """
            This function performs zero padding on a list of features and forms them into a numpy 3D array
            returns
                padded: a 3D numpy array of shape num_sequences x max_sequence_length x feature_dimension
        """
        padded = []
        longest = max(self.lengths)
        for i in range(len(self.lengths)):
            zeros = np.zeros((longest, self.feature_dim)).astype('float32')
            zeros[:self.lengths[i], :] = x[i].astype('float32')
            padded.append(zeros)

        padded = np.stack(padded)

        return padded

    def __getitem__(self, item):
        return self.feats[item], self.labels[item], self.lengths[item]

    def __len__(self):
        return len(self.feats)


class BasicLSTM(nn.Module):
    def __init__(self, input_dim, rnn_size, output_dim, num_layers, dropout=0, bidirectional=False):
        super(BasicLSTM, self).__init__()
        self.bidirectional = bidirectional
        self.feature_size = rnn_size * 2 if self.bidirectional else rnn_size
        self.lstm = nn.LSTM(input_dim,
                            rnn_size,
                            batch_first=True,
                            num_layers=num_layers,
                            bidirectional=bidirectional)
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(self.feature_size, output_dim)

    def forward(self, x, lengths):
        """ 
            x : 3D numpy array of dimension N x L x D
                N: batch index
                L: sequence index
                D: feature index

            lengths: N x 1
         """
        outputs, _ = self.lstm(x)
        last_outputs = self.last_timestep(outputs, lengths, bidirectional=self.bidirectional)
        last_outputs = self.dropout(last_outputs)
        last_outputs = self.out(last_outputs)

        return last_outputs

    def last_timestep(self, outputs, lengths, bidirectional=False):
        """
            Returns the last output of the LSTM taking into account the zero padding
        """
        if bidirectional:
            forward, backward = self.split_directions(outputs)
            last_forward = self.last_by_index(forward, lengths)
            last_backward = backward[:, 0, :]
            # Concatenate and return - maybe add more functionalities like average
            return torch.cat((last_forward, last_backward), dim=-1)

        else:
            return self.last_by_index(outputs, lengths)

    @staticmethod
    def split_directions(outputs):
        direction_size = int(outputs.size(-1) / 2)
        forward = outputs[:, :, :direction_size]
        backward = outputs[:, :, direction_size:]
        return forward, backward

    @staticmethod
    def last_by_index(outputs, lengths):
        # Index of the last output for each sequence.
        idx = (lengths - 1).view(-1, 1).expand(outputs.size(0),
                                               outputs.size(2)).unsqueeze(1)
        return outputs.gather(1, idx).squeeze()


# In[199]:


train = FrameLevelDataset(X_train, y_train)
validation = FrameLevelDataset(X_val, y_val)
test = FrameLevelDataset(X_test, y_test)

trainl = torch.utils.data.DataLoader(train, batch_size=32, shuffle=True)
validationl = torch.utils.data.DataLoader(validation, batch_size=32, shuffle=True)
testl = torch.utils.data.DataLoader(test, batch_size=32, shuffle=True)


# In[200]:


input_dim = train.feature_dim
rnn_size = 64
output_dim = 10
num_layers = 2
bidirectional = True
dropout = 0.3

lstm = BasicLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)


# Με τη συνάρτηση stop_early υλοποιούμε το early stopping. Κάθε φορά που βρίσκουμε ελάχιστο validation loss αποθηκεύουμε το μοντέλο με την συνάρτηση save και δίνουμε my_patience ευκαιρίες στο μοντέλο μας να συνεχίσει να μειώνει με το πέρασμα των εποχών το loss. Στο τέλος φορτώνουμε το καλύτερο μοντέλο. Το early stopping αντιμετωπίζει το πρόβλημα του overfitting, αφού από ένα σημείο και μετά το μοντέλο θα μαθαίνει υπερβολικά καλά τα train δεδομένα και δεν θα γενικεύει καλά. Έτσι θα πρέπει να σταματήσουμε την εκπαίδευση για να μην σπαταλάμε χρόνο χωρίς λόγο αλλά και να επαναφέρουμε το καλύτερο μοντέλο μας.

# In[201]:


my_patience = 2

def stop_early(patience, curr_loss, min_loss, model):
    if (curr_loss[0] < min_loss[0]):
        min_loss[0] = curr_loss[0]
        patience[0] = my_patience
        torch.save(model,'best_lstm.pt')
        return False
    else:
        patience[0] -= 1
        return patience[0] < 0


# In[202]:


from sklearn.metrics import accuracy_score, confusion_matrix

epochs = 25

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(lstm.parameters(), weight_decay=0.01)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    lstm.train()
    loss_sum = 0.0
    batches = 0
    for features, labels, lengths in trainl:
        optimizer.zero_grad()
        outputs = lstm(features, lengths)
        loss = criterion(outputs.squeeze(), labels)
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    lstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, labels, lengths in validationl:
            outputs = lstm(features, lengths)
            loss = criterion(outputs.squeeze(), labels)
            loss_sum += loss.item()
            prediction = torch.argmax(outputs, 1)
            accuracy_sum += accuracy_score(prediction, labels)
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    accuracy = accuracy_sum / batches
    print('Epoch {}: Train Loss = {}, Validation Loss = {}, Accuracy(validation) = {}'.format(epoch, train_loss, validation_loss,
                                                                              accuracy))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, lstm):
        print('Early Stopping!')
        break
    
lstm = torch.load('best_lstm.pt')


# In[203]:


plt.plot(range(epoch+1),train_losses)
plt.plot(range(epoch+1),validation_losses)
plt.legend(['Train Loss', 'Validation Loss'], loc='upper left')
plt.show


# In[204]:


accuracy_sum = 0.0
batches = 0
predictions = torch.empty(1).type(torch.LongTensor)
truth = torch.empty(1).type(torch.LongTensor)
with torch.no_grad():
    for features, labels, lengths in testl:
        outputs = lstm(features, lengths)
        prediction = torch.argmax(outputs, 1)
        accuracy_sum += accuracy_score(prediction, labels)
        batches += 1
        predictions = torch.cat((predictions,prediction))
        truth = torch.cat((truth,labels))
    accuracy = accuracy_sum / batches
    print('Accuracy(test) = {}'.format(accuracy))
    accuracy_sum = 0.0
    batches = 0
    for features, labels, lengths in validationl:
        outputs = lstm(features, lengths)
        prediction = torch.argmax(outputs, 1)
        accuracy_sum += accuracy_score(prediction, labels)
        batches += 1
    accuracy = accuracy_sum / batches
    print('Accuracy(best in validation) = {}'.format(accuracy))


# In[205]:


labels = list(set(y_train))
plot_confusion_matrix(confusion_matrix(predictions, truth, labels=labels), classes=labels)
plt.show()


# In[ ]:




