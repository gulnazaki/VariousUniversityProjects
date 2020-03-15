#!/usr/bin/env python
# coding: utf-8

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input/data/data"))

# Any results you write to the current directory are saved as output.


# ## Step 2 - Mel Spectrograms
# *** 
# Από το φάκελο με τα train δεδομένα παίρνουμε τα labels και διαλέγουμε 2 γραμμές (2 labels) τυχαία. 

# In[2]:


import random

lines = open("../input/data/data/fma_genre_spectrograms/train_labels.txt").readlines()
first = random.choice(lines)
print (first)
second = random.choice(lines)
while(first.split()[1] == second.split()[1]):
    second = random.choice(lines)
print (second)


# Η πληροφορία που παίρνουμε από το spectrogram είναι η κατανομή του φάσματος των συχνοτήτων (στον κατακόρυφο άξονα) σε σχέση με το χρόνο (στον οριζόντιο άξονα). Για παράδειγμα, όταν στο spectrogram έχουμε κίτρινο χρώμα, η πυκνότητα της κατανομής είναι μεγαλύτερη, οπότε το spectrogram με έντονο κίτρινο χαμηλά υποδεικνύει ότι έχουμε περισσότερες χαμηλές συχνότητες, αντίστοιχα το μαύρο δείχνει απουσία των αντίστοιχων συχνοτήτων. Από το spectrogram παίρνουμε πληροφορίες για τον ήχο καθώς γνωρίζουμε ορισμένα χαρακτηριστικά, π.χ. η ανδρική φωνή κατανένεμεται συνήθως σε χαμηλότερες συχνότητες από τη γυναικεία, οπότε μπορούμε να εξάγουμε συμπεράσματα για τον ήχο.

# In[3]:


import gzip
import librosa.display
import matplotlib.pyplot as plt

path = "../input/data/data/fma_genre_spectrograms/train/"

with gzip.GzipFile(path + first.split()[0], 'r') as f:
    spectrograms = np.load(f)

mel_1 = spectrograms[:128]

with gzip.GzipFile(path + second.split()[0], 'r') as f:
    spectrograms = np.load(f)

mel_2 = spectrograms[:128]

plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
librosa.display.specshow(mel_1, y_axis='mel')
plt.subplot(2, 1, 2)
librosa.display.specshow(mel_2, y_axis='mel')


# ## Step 3 - Beat-synced spectrograms
# ***
# α) Βλέπουμε ότι κάθε mel spectogram αποτελείται απο 128 συχνότητες, όπως γνωρίζαμε, και για τα time stamps βλέπουμε ότι το πρώτο label έχει 1291 και το δεύτερο 1293, δηλαδή έχουμε πληροφορία για το φασματικό περιεχόμενο σε περίπου 1300 διακριτούς χρόνους. 

# In[4]:


print('Mel Spectrogram shape')
print('(n_features, timesteps)')

print(mel_1.shape)
print(mel_2.shape)


# β) Επαναλαμβάνουμε τα ίδια βήματα με πριν αλλά αυτή τη φορά για ήχους που έχουν προκύψει παίρνοντας median ανάμεσα στα beat της μουσικής. Με αυτό τον τρόπο έχουν μειωθεί τα timestamps, αφού πλέον έχουν "ομαδοποιηθεί" τα ενδιάμεσα διαστήματα. Συγκρίνοντας τα αρχικά σπεκτρογράμματα με τα beat-synced βλέπουμε εύκολα ότι η γενική πληροφορία έχει διατηρηθεί πολύ ικανοποιητικά (οι μαύρες περιοχές παραμένουν μαύρες κλπ). Βέβαια, η ακρίβεια έχει μειωθεί, και η λεπτομέρεια στις διακυμάνσεις έχει χαθεί. Μπορούμε όμως να πούμε ότι η κατανομή έχει διατηρηθεί σε μεγάλο βαθμό και η μείωση των timestamps, δηλαδή των διακριτών σημείων στον άξονα χ, είναι σημαντική ώστε να εκπαιδεύσουμε γρηγορότερα ένα μοντέλο.

# In[5]:


path = "../input/data/data/fma_genre_spectrograms_beat/train/"

with gzip.GzipFile(path + first.split()[0], 'r') as f:
    spectrograms = np.load(f)

mel_1_beat = spectrograms[:128]

with gzip.GzipFile(path + second.split()[0], 'r') as f:
    spectrograms = np.load(f)

mel_2_beat = spectrograms[:128]

plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
librosa.display.specshow(mel_1_beat, y_axis='mel')
plt.subplot(2, 1, 2)
librosa.display.specshow(mel_2_beat, y_axis='mel')


# In[6]:


print('Mel Spectrogram shape')
print('(n_features, timesteps)')
print(mel_1_beat.shape)
print(mel_2_beat.shape)


# ## Step 3 - Chromagrams
# ***
# Τα χρωμογράμματα είναι σήματα με 12 διανύσματα που αντιστοιχούν στις 12 νότες και συγκεκριμένα περιέχουν το ενεργειακό άθροισμα κάθε νότας για κάθε οκτάβα (pitch class). Είναι επομένως ένα μέτρο της φασματικής ενέργειας για διαφορετικές συχνοτικές περιοχές. Σε αντίθεση με το spectrogram, από το chromagram παίρνουμε μια αναπαράσταση για την σχετική συχνότητα εμφάνισης των pitch classes σε κάθε δείγμα. Η πληροφορία που εξάγουμε εδώ αφορά κυρίως τη μελωδία και το ηχόχρωμα του ήχου, εφόσον παίρνουμε ουσιαστικά πληροφορία για το "ύψος" και το "χρώμα" της νότας. 
# Βλέπουμε από τα chromagrams για τα δύο τυχαία labels πως κατανέμονται τα pitch classes (πιο έντονο κίτρινο υποδηλώνει υψηλή φασματική ενέργεια του αντίστοιχου pitch class). 
# Όπως και πριν, βλέπουμε ότι τα beat-synced chromagrams δίνουν μια ικανοποιητική εκτίμηση ολόκληρου του ήχου, δηλαδή τα σημεία υψηλής-χαμηλής ενέργειας είναι στα ίδια σημεία, απλώς η πληροφορία έχει "στρογγυλοποιηθεί", δηλαδή κάποιες επιμέρους διακυμάνσεις (κυρίως οι ενδιάμεσες αποχρώσεις του πορτοκαλί) έχουν συμπτυχθεί σε ένα μέσο όρο (όπως ήταν αναμενόμενο αφού έχει παρθεί το median τους). 

# In[7]:


path = "../input/data/data/fma_genre_spectrograms/train/"

with gzip.GzipFile(path + first.split()[0], 'r') as f:
    spectrograms = np.load(f)

chroma_1 = spectrograms[128:]

with gzip.GzipFile(path + second.split()[0], 'r') as f:
    spectrograms = np.load(f)

chroma_2 = spectrograms[128:]

plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
librosa.display.specshow(chroma_1, y_axis='chroma')
plt.subplot(2, 1, 2)
librosa.display.specshow(chroma_2, y_axis='chroma')


# In[8]:


path = "../input/data/data/fma_genre_spectrograms_beat/train/"

with gzip.GzipFile(path + first.split()[0], 'r') as f:
    spectrograms = np.load(f)

chroma_1_beat = spectrograms[128:]

with gzip.GzipFile(path + second.split()[0], 'r') as f:
    spectrograms = np.load(f)

chroma_2_beat = spectrograms[128:]

plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
librosa.display.specshow(chroma_1_beat, y_axis='chroma')
plt.subplot(2, 1, 2)
librosa.display.specshow(chroma_2_beat, y_axis='chroma')


# In[ ]:


print('Chromagram shape')
print('(n_features, timesteps)')
print(chroma_1.shape)
print(chroma_2.shape)
print(chroma_1_beat.shape)
print(chroma_2_beat.shape)


# ## Step 4 - Data Loading - Spectrogram Dataset
# ***
# Αρχικά διαβάζουμε το spectrogram dataset με το βοηθητικό κώδικα που δίνεται. Συνοπτικά, διαβάζει τα δεδομένα και χωρίζει σε train, validation και test, με class mapping σε 10 κλάσεις (Rock, Folk, Metal, Trip-Hop, Pop, Electronic κλπ). 

# In[9]:


import numpy as np
import gzip
import copy
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset
from torch.utils.data import SubsetRandomSampler, DataLoader


class_mapping = {
    'Rock': 'Rock',
    'Psych-Rock': 'Rock',
    'Indie-Rock': None,
    'Post-Rock': 'Rock',
    'Psych-Folk': 'Folk',
    'Folk': 'Folk',
    'Metal': 'Metal',
    'Punk': 'Metal',
    'Post-Punk': None,
    'Trip-Hop': 'Trip-Hop',
    'Pop': 'Pop',
    'Electronic': 'Electronic',
    'Hip-Hop': 'Hip-Hop',
    'Classical': 'Classical',
    'Blues': 'Blues',
    'Chiptune': 'Electronic',
    'Jazz': 'Jazz',
    'Soundtrack': None,
    'International': None,
    'Old-Time': None
}


def torch_train_val_split(
        dataset, batch_train, batch_eval,
        val_size=.2, shuffle=True, seed=42):
    # Creating data indices for training and validation splits:
    dataset_size = len(dataset)
    indices = list(range(dataset_size))
    val_split = int(np.floor(val_size * dataset_size))
    if shuffle:
        np.random.seed(seed)
        np.random.shuffle(indices)
    train_indices = indices[val_split:]
    val_indices = indices[:val_split]

    # Creating PT data samplers and loaders:
    train_sampler = SubsetRandomSampler(train_indices)
    val_sampler = SubsetRandomSampler(val_indices)

    train_loader = DataLoader(dataset,
                              batch_size=batch_train,
                              sampler=train_sampler)
    val_loader = DataLoader(dataset,
                            batch_size=batch_eval,
                            sampler=val_sampler)
    return train_loader, val_loader


def read_spectrogram(spectrogram_file, chroma=True):
    with gzip.GzipFile(spectrogram_file, 'r') as f:
        spectrograms = np.load(f)
    # spectrograms contains a fused mel spectrogram and chromagram
    # Decompose as follows
    return spectrograms.T


class LabelTransformer(LabelEncoder):
    def inverse(self, y):
        try:
            return super(LabelTransformer, self).inverse_transform(y)
        except:
            return super(LabelTransformer, self).inverse_transform([y])

    def transform(self, y):
        try:
            return super(LabelTransformer, self).transform(y)
        except:
            return super(LabelTransformer, self).transform([y])

        
class PaddingTransform(object):
    def __init__(self, max_length, padding_value=0):
        self.max_length = max_length
        self.padding_value = padding_value

    def __call__(self, s):
        if len(s) == self.max_length:
            return s

        if len(s) > self.max_length:
            return s[:self.max_length]

        if len(s) < self.max_length:
            s1 = copy.deepcopy(s)
            pad = np.zeros((self.max_length - s.shape[0], s.shape[1]), dtype=np.float32)
            s1 = np.vstack((s1, pad))
            return s1

        
class SpectrogramDataset(Dataset):
    def __init__(self, path, class_mapping=None, train=True, max_length=-1):
        t = 'train' if train else 'test'
        p = os.path.join(path, t)
        self.index = os.path.join(path, "{}_labels.txt".format(t))
        self.files, labels = self.get_files_labels(self.index, class_mapping)
        self.feats = [read_spectrogram(os.path.join(p, f)) for f in self.files]
        self.feat_dim = self.feats[0].shape[1]
        self.lengths = [len(i) for i in self.feats]
        self.max_length = max(self.lengths) if max_length <= 0 else max_length
        self.zero_pad_and_stack = PaddingTransform(self.max_length)
        self.label_transformer = LabelTransformer()
        if isinstance(labels, (list, tuple)):
            self.labels = np.array(self.label_transformer.fit_transform(labels)).astype('int64')

    def get_files_labels(self, txt, class_mapping):
        with open(txt, 'r') as fd:
            lines = [l.rstrip().split('\t') for l in fd.readlines()[1:]]
        files, labels = [], []
        for l in lines:
            label = l[1]
            if class_mapping:
                label = class_mapping[l[1]]
            if not label:
                continue
            files.append(l[0])
            labels.append(label)
        return files, labels

    def __getitem__(self, item):
        l = min(self.lengths[item], self.max_length)
        return self.zero_pad_and_stack(self.feats[item]), self.labels[item], l

    def __len__(self):
        return len(self.labels)


# In[10]:


specs = SpectrogramDataset('../input/data/data/fma_genre_spectrograms_beat/', train=True, class_mapping=class_mapping)
train_loader, val_loader = torch_train_val_split(specs, 32 ,32, val_size=.33)
test_loader = DataLoader(SpectrogramDataset('../input/data/data/fma_genre_spectrograms_beat/', train=False, class_mapping=class_mapping), batch_size=32, shuffle=True)


# ## Steps 5-6- LSTM
# ***
# Αρχικά ενεργοποιούμε τη gpu, εφόσον είναι διαθέσιμη από το kaggle. Σε διαφορετική περίπτωση δουλεύουμε με τη cpu. 
# Βασιστήκαμε στον κώδικα του προηγούμενου εργαστηρίου αλλά εδώ δεν χρησιμοποιούμε την έτοιμη υλοποίηση για GRU (Gated recurrent unit). Δίνουμε στο lstm την επιλογή να είναι bidirectional, δηλαδή να συνδέει δύο layers αντίθετης κατεύθυνσης με το ίδιο output. Έτσι το output layer έχει πληροφορίες και από τις προηγούμενες καταστάσεις και από τις επόμενες (forward - backward) ταυτόχρονα. Σε αυτή την περίπτωση πρέπει να αλλάξουμε αφενός το μέγεθος των features (αφού πλέον είναι διπλάσια σε πλήθος) και αφετέρου το output να είναι το concatenation των δύο επιμέρους εξόδων, ώστε να διατηρούνται και οι δύο πληροφορίες.
# Αυτό είναι χρήσιμο καθώς μπορούμε να έχουμε πληροφορία για το context, εφόσον για την κατάσταση που βρισκόμαστε ξέρουμε ταυτόχρονα και την προηγούμενη-επόμενη της, άρα μπορεί να τοποθετηθεί ως πληροφορία ενός ευρύτερου πλαισίου. 
# 
# Στη συνέχεια εκπαιδεύουμε το μοντέλο μας για rnn_size = 64 στις 10 κλάσεις του spectrogram dataset, και χρησιμοποιούμε 2 layers. Επιπλέον ενεργοποιούμε την επιλογή bidirectional. Για την εκπαίδευση ορίζουμε 25 εποχές και ως συνάρτηση κόστους επιλέξαμε την Cross Entropy. Ορίζουμε επίσης την stop_early με την οποία εξασφαλίζουμε ότι αν για 3 συνεχόμενες φορές (παράμετρος my_patience) το loss δεν έχει βελτιωθεί, σταματάει η εκπαίδευση καθώς θεωρούμε ότι περαιτέρω βήματα είναι περιττά. Όταν βρεθεί το τελικό μοντέλο (είτε με το πέρας τον εποχών είτε αν σταματήσει νωρίτερα με την stop early) αποθηκεύουμε το βέλτιστο μοντέλο στο output.
# Το τελικό accuracy του μοντέλου το παίρνουμε δοκιμάζοντας το μοντέλο στα train δεδομένα, συγκρίνοντας το prediction του μοντέλου με το label (την αναμενόμενη τιμή που δίνεται) με τις γνωστές διαδικασίες.

# In[11]:


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.set_default_tensor_type('torch.DoubleTensor')

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

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


# In[12]:


input_dim = specs.feat_dim
rnn_size = 64
output_dim = 10
num_layers = 2
bidirectional = True
dropout = 0.2

lstm = BasicLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
lstm.to(device)

my_patience = 3

def stop_early(patience, curr_loss, min_loss, model, name):
    if (curr_loss[0] < min_loss[0]):
        min_loss[0] = curr_loss[0]
        patience[0] = my_patience
        torch.save(model,'best_' + name + '.pt')
        return False
    else:
        patience[0] -= 1
        return patience[0] < 0
    
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
    for features, labels, lengths in train_loader:
        optimizer.zero_grad()
        outputs = lstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), labels.to(device))
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
        for features, labels, lengths in val_loader:
            outputs = lstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), labels.to(device))
            loss_sum += loss.item()
            prediction = torch.argmax(outputs, 1)
            accuracy_sum += accuracy_score(prediction.cpu(), labels.cpu())
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    accuracy = accuracy_sum / batches
    print('Epoch {}: Train Loss = {}, Validation Loss = {}, Accuracy(validation) = {}'.format(epoch, train_loss, validation_loss,
                                                                              accuracy))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, lstm, "lstm"):
        print('Early Stopping!')
        break
    
lstm = torch.load('best_lstm.pt')


# In[13]:


accuracy_sum = 0.0
batches = 0
predictions = torch.empty(1).type(torch.LongTensor)
truth = torch.empty(1).type(torch.LongTensor)
with torch.no_grad():
    for features, labels, lengths in test_loader:
        outputs = lstm(features.to(device), lengths.to(device))
        prediction = torch.argmax(outputs, 1)
        accuracy_sum += accuracy_score(prediction.cpu(), labels.cpu())
        batches += 1
        predictions = torch.cat((predictions,prediction.cpu()))
        truth = torch.cat((truth,labels))
    accuracy = accuracy_sum / batches
    print('Accuracy(test) = {}'.format(accuracy))


# ## Step 7
# ***
# Με τα beat δεδομένα, θα εκπαιδεύσουμε ένα νέο μοντέλο. Στο LSTM που φτιάξαμε πριν, προσθέτουμε στην αρχή 3 Convolutional layers (που πραγματοποιούν με τη σειρά convolution, Batch normalization, ReLU activation, Max pooling, όλα σε 1 διάσταση). Το μοντέλο κατά τα άλλα διατηρεί τη δομή του LSTM με τη δυνατότητα bidirectional. 
# Μετά την εκπαίδευση και τη δοκιμή με τα test δεδομένα βλέπουμε ότι αποδίδει εξίσου καλά με το απλό LSTM, μάλιστα το τελικό accuracy είναι σχεδόν το ίδιο.
# Επομένως, έχουμε καταφέρει σε μικρότερο χρόνο να πάρουμε τα ίδια αποτελέσματα με την πιο χρονοβόρα διαδικασία του προηγούμενου βήματος.

# In[14]:


class MyCNNLSTM(nn.Module):
    def __init__(self, input_dim, rnn_size, output_dim, num_layers, kernel_size=5, bidirectional=False, dropout=0.3):
        super(MyCNNLSTM, self).__init__()
        self.cnnlayer1, self.cnnlayer2, self.cnnlayer3 = [nn.Sequential(
                nn.Conv1d(input_dim, input_dim, kernel_size), nn.BatchNorm1d(input_dim),
                nn.ReLU(), nn.MaxPool1d(2)) for i in range(3)] 
        self.bidirectional = bidirectional
        self.feature_size = rnn_size * 2 if self.bidirectional else rnn_size
        self.hidden_dim = self.feature_size
        self.lstm = nn.LSTM(input_dim,
                            rnn_size,
                            batch_first=True,
                            num_layers=num_layers,
                            bidirectional=bidirectional)
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(self.feature_size, output_dim)
        
                
    def forward(self, x, lengths): 
        x = x.transpose(1,2)
        x=self.cnnlayer1(x)
        x=self.cnnlayer2(x)
        x=self.cnnlayer3(x)                  
        x = x.transpose(1,2)
        
        outputs, _ = self.lstm(x)
        last_outputs = self.last_timestep(outputs, lengths/8 - 4, bidirectional=self.bidirectional)
        last_outputs = self.dropout(last_outputs)
        return self.out(last_outputs)
        
    @staticmethod
    def split_directions(outputs):
        direction_size = int(outputs.size(-1) / 2)
        forward = outputs[:, :, :direction_size]
        backward = outputs[:, :, direction_size:]
        return forward, backward   
    
    
    @staticmethod
    def last_by_index(outputs, lengths):
        # Index of the last output for each sequence.
        idx = (lengths - 1).view(-1, 1).expand(outputs.size(0), outputs.size(2)).unsqueeze(1)
        return outputs.gather(1, idx).squeeze()   
        
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


# In[15]:


c_specs = SpectrogramDataset('../input/data/data/fma_genre_spectrograms/', train=True, class_mapping=class_mapping)
c_train_loader, c_val_loader = torch_train_val_split(c_specs, 32 , 32, val_size=.33)
c_test_loader = DataLoader(SpectrogramDataset('../input/data/data/fma_genre_spectrograms/', train=False, class_mapping=class_mapping), batch_size=32, shuffle=True)


# In[16]:


input_dim = c_specs.feat_dim
rnn_size = 64
output_dim = 10
num_layers = 2
bidirectional = True
dropout = 0.2

cnnlstm = MyCNNLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
cnnlstm.to(device)

optimizer = torch.optim.Adam(cnnlstm.parameters(), weight_decay=0.01)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    cnnlstm.train()
    loss_sum = 0.0
    batches = 0
    for features, labels, lengths in c_train_loader:
        optimizer.zero_grad()
        outputs = cnnlstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), labels.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    cnnlstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, labels, lengths in c_val_loader:
            outputs = cnnlstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), labels.to(device))
            loss_sum += loss.item()
            prediction = torch.argmax(outputs, 1)
            accuracy_sum += accuracy_score(prediction.cpu(), labels.cpu())
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    accuracy = accuracy_sum / batches
    print('Epoch {}: Train Loss = {}, Validation Loss = {}, Accuracy(validation) = {}'.format(epoch, train_loss, validation_loss,
                                                                              accuracy))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, cnnlstm, "cnnlstm"):
        print('Early Stopping!')
        break
    
cnnlstm = torch.load('best_cnnlstm.pt')


# ## Step 8

# In[17]:


accuracy_sum = 0.0
batches = 0
predictions = torch.empty(1).type(torch.LongTensor)
truth = torch.empty(1).type(torch.LongTensor)
with torch.no_grad():
    for features, labels, lengths in c_test_loader:
        outputs = cnnlstm(features.to(device), lengths.to(device))
        prediction = torch.argmax(outputs, 1)
        accuracy_sum += accuracy_score(prediction.cpu(), labels.cpu())
        batches += 1
        predictions = torch.cat((predictions,prediction.cpu()))
        truth = torch.cat((truth,labels))
    accuracy = accuracy_sum / batches
    print('Accuracy(test) = {}'.format(accuracy))

