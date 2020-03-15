#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input/data/data"))

# Any results you write to the current directory are saved as output.


#  ### Load the dataset
#  ***
# Επιλέγουμε batch_size=32, δηλαδή χωρίζουμε ανά 32 features και εκπαιδεύουμε το μοντέλο. Διαλέξαμε ένα σχετικά μικρό αριθμό ώστε να μην έχουμε κάποιο πρόβλημα με τη μνήμη, αν και μεγαλύτερο μέγεθος θα ήταν προτιμότερο. Το batch size γενικά επηρεάζει τις παραμέτρους του μοντέλου καθώς και την ακρίβεια του οπότε το 32, για τα δεδομένα της RAM που έχουμε ήταν μια καλή επιλογή.

# In[2]:


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
    def __init__(self, path, class_mapping=None, train=True, max_length=1296):
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


# In[3]:


specs = SpectrogramDataset('../input/data/data/fma_genre_spectrograms/', train=True, class_mapping=class_mapping)
train_loader, val_loader = torch_train_val_split(specs, 32 , 32, val_size=.33)
test_loader = DataLoader(SpectrogramDataset('../input/data/data/fma_genre_spectrograms/', train=False, class_mapping=class_mapping), batch_size=32, shuffle=True)


# ## Step 9 - CNN
# ***
# Ορίζουμε την κλάση MyCNN που υλοποιεί το Convolutional Neural Network. Συγκεκριμένα, έχουμε δύο διαστάσεις για το input, και 4 layers καθένα εκ των οποίων εκτελεί τα ακόλουθα, με τη σειρά, - 2D convolution, Batch normalization, ReLU activation, Max pooling. Στο τέλος έχουμε δύο fully connected layers (κάνουν γραμμικό μετασχηματισμό πάνω στα δεδομένα).
#   
#  Η αρχικοποίηση του νευρωνικού δηλαδή των τεσσάρων συνελικτικών και των δύο γραμμικών layers γίνεται στην init και στην forward ενημερώνονται κάθε φορά τα layers.
# Για την εκπαίδευση επιλέγουμε 1296 για το πρώτο input καθώς το μέγιστο μήκος ήταν κοντά αριθμητικά και θέλαμε έναν αριθμό που να διαιρείται ακριβώς με το 16. Γενικά σε κάθε στάδιο κάνουμε padding ώστε να έχουμε επιθυμητές διαστάσεις για τις διαιρέσεις. Για το εύτερο input επιλέξαμε 140 που είναι η διάσταση feature. 
# 
#  Η εκπαίδευση και η αξιολόγηση γίνονται ακριβώς όπως στο LSTM από το βήμα 5.
# ***
# 

# In[4]:


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.set_default_tensor_type('torch.DoubleTensor')

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class MyCNN(nn.Module):
    def __init__(self, input_dim1, inputdim2, output_dim, channels=8, kernel_size=5):
        super(MyCNN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, channels, kernel_size=kernel_size, stride=1, padding=2),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        channels_ = 2*channels
        self.layer2 = nn.Sequential(
            nn.Conv2d(channels, channels_, kernel_size=kernel_size, stride=1, padding=2),
            nn.BatchNorm2d(channels_),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=(0,1)))
        self.layer3 = nn.Sequential(
            nn.Conv2d(channels_, channels_, kernel_size=kernel_size, stride=1, padding=2),
            nn.BatchNorm2d(channels_),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer4 = nn.Sequential(
            nn.Conv2d(channels_, channels_, kernel_size=kernel_size, stride=1, padding=2),
            nn.BatchNorm2d(channels_),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))    
        self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(81 * 9 * channels_, 1000)
        self.fc2 = nn.Linear(1000, output_dim)
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = out.reshape(out.size(0), -1)
        out = self.drop_out(out)
        out = self.fc1(out)
        out = self.fc2(out)
        return out


# In[5]:


input_dim1 = 1296
input_dim2 = 140
output_dim = 10

cnn = MyCNN(input_dim1, input_dim2, output_dim)
cnn.to(device)

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
optimizer = torch.optim.Adam(cnn.parameters(), weight_decay=0.01)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    cnn.train()
    loss_sum = 0.0
    batches = 0
    for features, labels, lengths in train_loader:
        optimizer.zero_grad()
        outputs = cnn(features[:, None].to(device))
        loss = criterion(outputs.squeeze(), labels.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    cnn.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, labels, lengths in val_loader:
            outputs = cnn(features[:, None].to(device))
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
    if stop_early(patience, loss, min_loss, cnn, "cnn"):
        print('Early Stopping!')
        break
    
cnn = torch.load('best_cnn.pt')


# In[6]:


accuracy_sum = 0.0
batches = 0
predictions = torch.empty(1).type(torch.LongTensor)
truth = torch.empty(1).type(torch.LongTensor)
with torch.no_grad():
    for features, labels, lengths in test_loader:
        outputs = cnn(features[:,None].to(device))
        prediction = torch.argmax(outputs, 1)
        accuracy_sum += accuracy_score(prediction.cpu(), labels.cpu())
        batches += 1
        predictions = torch.cat((predictions,prediction.cpu()))
        truth = torch.cat((truth,labels))
    accuracy = accuracy_sum / batches
    print('Accuracy(test) = {}'.format(accuracy))


# ## Step 10 - Multitask Dataset
# ***
# Για να διαβάσουμε το multitask dataset πρέπει να γίνουν κάποιες αλλαγές στις μεθόδους που πήραμε από το dataloader των προηγούμενων βημάτων. 
# Τυπώνοντας ενδεικτικά κάποια δείγματα βλέπουμε τις διαφορές που υπάρχουν στο formatting για να φορτώσουμε τα labels. Στο Spectrograms ο  Seperator ήταν '\t' και το  id ήταν το full filename, ενώ για το multitask έχουμε comma seperated και το id πλέον είναι μόνο ο αριθμός, επομένως πρέπει να προστεθεί απαραίτητα η κατάληξη του αρχείου. Προσαρμόζουμε ώστε να διαβάζουμε και να επιστρέφουμε τις 3 τιμές valence, danceability και energy, αφού πρώτα τις μετατρέψουμε σε double (όπως προκείπτει από τη μορφή τους που περιγράφει η εκφώνηση). Εφόσον το test set δεν έχει αρχείο για τα labels δεν μπορούμε να το χρησιμοποιήσουμε για την αξιολόγηση, οπότε θα δουλέψουμε μόνο με το train και το validation.

# In[7]:


class MultitaskDataset(Dataset):
    def __init__(self, path, train=True, max_length=1296):
        t = 'train' if train else 'test'
        p = os.path.join(path, t)
        self.index = os.path.join(path, "{}_labels.txt".format(t))
        self.files, valence, energy, danceability = self.get_files_labels(self.index, class_mapping, train)
        self.feats = [read_spectrogram(os.path.join(p, f)) for f in self.files]
        self.feat_dim = self.feats[0].shape[1]
        self.lengths = [len(i) for i in self.feats]
        self.max_length = max(self.lengths) if max_length <= 0 else max_length
        self.zero_pad_and_stack = PaddingTransform(self.max_length)
        self.valence = np.asarray(valence).astype(np.double)
        self.danceability = np.asarray(danceability).astype(np.double)
        self.energy = np.asarray(energy).astype(np.double)

    def get_files_labels(self, txt, class_mapping, train):
        files, valence, energy, danceability = [], [], [], []
        if (train):
            with open(txt, 'r') as fd:
                lines = [l.rstrip().split(',') for l in fd.readlines()[1:]]
            for l in lines:
                files.append(l[0] + ".fused.full.npy.gz")
                valence.append(l[1])
                energy.append(l[2])
                danceability.append(l[3])
        return files, valence, energy, danceability

    def __getitem__(self, item):
        l = min(self.lengths[item], self.max_length)
        return self.zero_pad_and_stack(self.feats[item]), self.valence[item], self.energy[item], self.danceability[item], l

    def __len__(self):
        return len(self.valence)


# In[8]:


m_specs = MultitaskDataset('../input/data/data/multitask_dataset/')
m_train_loader, m_val_loader = torch_train_val_split(m_specs, 32 , 32, val_size=.33)


# ## LSTM (5)

# In[9]:


from scipy.stats import spearmanr


# In[10]:


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


# In[11]:


input_dim = 140
rnn_size = 64
output_dim = 1
num_layers = 2
bidirectional = True
dropout = 0.2

m_lstm = BasicLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
m_lstm.to(device)

my_patience = 3

epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(m_lstm.parameters(), weight_decay=0.05)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_lstm.train()
    loss_sum = 0.0
    batches = 0
    for features, valence, _, _, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_lstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), valence.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_lstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, valence, _, _, lengths in m_val_loader:
            outputs = m_lstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), valence.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_lstm, "m_val_lstm"):
        print('Early Stopping!')
        break


# In[12]:


input_dim = 140
rnn_size = 64
output_dim = 1
num_layers = 2
bidirectional = True
dropout = 0.2

m_lstm = BasicLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
m_lstm.to(device)

my_patience = 3

epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(m_lstm.parameters(), weight_decay=0.05)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_lstm.train()
    loss_sum = 0.0
    batches = 0
    for features, _, energy, _, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_lstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), energy.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_lstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, _, energy, _, lengths in m_val_loader:
            outputs = m_lstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), energy.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_lstm, "m_en_lstm"):
        print('Early Stopping!')
        break


# In[13]:


input_dim = 140
rnn_size = 64
output_dim = 1
num_layers = 2
bidirectional = True
dropout = 0.2

m_lstm = BasicLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
m_lstm.to(device)

my_patience = 3

epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(m_lstm.parameters(), weight_decay=0.05)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_lstm.train()
    loss_sum = 0.0
    batches = 0
    for features, _, _, dance, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_lstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), dance.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_lstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, _, _, dance, lengths in m_val_loader:
            outputs = m_lstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), dance.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_lstm, "m_dan_lstm"):
        print('Early Stopping!')
        break


# In[14]:


input_dim = 140
rnn_size = 64
output_dim = 1
num_layers = 2
bidirectional = True
dropout = 0.2

m_lstm = BasicLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
m_lstm.to(device)

my_patience = 3

epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(m_lstm.parameters(), weight_decay=0.05)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_lstm.train()
    loss_sum = 0.0
    batches = 0
    for features, _, _, dance, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_lstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), dance.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_lstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, _, _, dance, lengths in m_val_loader:
            outputs = m_lstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), dance.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_lstm, "m_dan_lstm"):
        print('Early Stopping!')
        break


# ## CNN-LSTM (7)

# In[15]:


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


# In[16]:


input_dim = 140
rnn_size = 64
output_dim = 1
num_layers = 2
bidirectional = True
dropout = 0.2

m_cnnlstm = MyCNNLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
m_cnnlstm.to(device)

my_patience = 3

epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(m_cnnlstm.parameters(), weight_decay=0.05)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_cnnlstm.train()
    loss_sum = 0.0
    batches = 0
    for features, val, _, _, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_cnnlstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), val.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_cnnlstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, val, _, _, lengths in m_val_loader:
            outputs = m_cnnlstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), val.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_cnnlstm, "m_val_cnnlstm"):
        print('Early Stopping!')
        break


# In[17]:


input_dim = 140
rnn_size = 64
output_dim = 1
num_layers = 2
bidirectional = True
dropout = 0.2

m_cnnlstm = MyCNNLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
m_cnnlstm.to(device)

my_patience = 3

epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(m_cnnlstm.parameters(), weight_decay=0.05)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_cnnlstm.train()
    loss_sum = 0.0
    batches = 0
    for features, _, dan, _, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_cnnlstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), dan.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_cnnlstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, _, dan, _, lengths in m_val_loader:
            outputs = m_cnnlstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), dan.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_cnnlstm, "m_dan_cnnlstm"):
        print('Early Stopping!')
        break


# In[18]:


input_dim = 140
rnn_size = 64
output_dim = 1
num_layers = 2
bidirectional = True
dropout = 0.2

m_cnnlstm = MyCNNLSTM(input_dim, rnn_size, output_dim, num_layers, bidirectional=bidirectional, dropout=dropout)
m_cnnlstm.to(device)

my_patience = 3

epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(m_cnnlstm.parameters(), weight_decay=0.05)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_cnnlstm.train()
    loss_sum = 0.0
    batches = 0
    for features, _, _, en, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_cnnlstm(features.to(device), lengths.to(device))
        loss = criterion(outputs.squeeze(), en.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_cnnlstm.eval()
    loss_sum = 0.0
    accuracy_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, _, _, en, lengths in m_val_loader:
            outputs = m_cnnlstm(features.to(device), lengths.to(device))
            loss = criterion(outputs.squeeze(), en.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_cnnlstm, "m_en_cnnlstm"):
        print('Early Stopping!')
        break


# In[19]:


m_val = torch.load('best_m_val_cnnlstm.pt')
m_en = torch.load('best_m_en_cnnlstm.pt')
m_dan = torch.load('best_m_dan_cnnlstm.pt')
    
m_val.eval()
accuracy_sum = 0.0
batches = 0
with torch.no_grad():
    for features, val, _, _, lengths in m_val_loader:
        outputs = m_val(features.to(device), lengths.to(device))
        acc, _ = spearmanr(outputs.cpu(), val.cpu())
        accuracy_sum += acc
        batches += 1
acc_val = accuracy_sum / batches

m_en.eval()
accuracy_sum = 0.0
batches = 0
with torch.no_grad():
    for features, _, en, _, lengths in m_val_loader:
        outputs = m_en(features.to(device), lengths.to(device))
        acc, _ = spearmanr(outputs.cpu(), en.cpu())
        accuracy_sum += acc
        batches += 1
acc_en = accuracy_sum / batches

m_dan.eval()
accuracy_sum = 0.0
batches = 0
with torch.no_grad():
    for features, _, _, dan, lengths in m_val_loader:
        outputs = m_dan(features.to(device), lengths.to(device))
        acc, _ = spearmanr(outputs.cpu(), dan.cpu())
        accuracy_sum += acc
        batches += 1
acc_dan = accuracy_sum / batches

print((acc_val + acc_en + acc_dan)/3)


# ## CNN (9)

# In[20]:


input_dim1 = 1296
input_dim2 = 140
output_dim = 1

m_cnn = MyCNN(input_dim1, input_dim2, output_dim)
m_cnn.to(device)

my_patience = 3
epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(cnn.parameters(), weight_decay=0.5)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_cnn.train()
    loss_sum = 0.0
    batches = 0
    for features, val, _, _, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_cnn(features[:, None].to(device))
        loss = criterion(outputs.squeeze(), val.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_cnn.eval()
    loss_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, val, _, _, lengths in m_val_loader:
            outputs = m_cnn(features[:, None].to(device))
            loss = criterion(outputs.squeeze(), val.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_cnn, "m_val_cnn"):
        print('Early Stopping!')
        break


# In[21]:


input_dim1 = 1296
input_dim2 = 140
output_dim = 1

m_cnn = MyCNN(input_dim1, input_dim2, output_dim)
m_cnn.to(device)

my_patience = 3
epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(cnn.parameters(), weight_decay=0.5)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_cnn.train()
    loss_sum = 0.0
    batches = 0
    for features, _, en, _, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_cnn(features[:, None].to(device))
        loss = criterion(outputs.squeeze(), en.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_cnn.eval()
    loss_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, _, en, _, lengths in m_val_loader:
            outputs = m_cnn(features[:, None].to(device))
            loss = criterion(outputs.squeeze(), en.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_cnn, "m_en_cnn"):
        print('Early Stopping!')
        break


# In[22]:


input_dim1 = 1296
input_dim2 = 140
output_dim = 1

m_cnn = MyCNN(input_dim1, input_dim2, output_dim)
m_cnn.to(device)

my_patience = 3
epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(cnn.parameters(), weight_decay=0.5)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_cnn.train()
    loss_sum = 0.0
    batches = 0
    for features, _, _, dan, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_cnn(features[:, None].to(device))
        loss = criterion(outputs.squeeze(), dan.to(device))
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_cnn.eval()
    loss_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, _, _, dan, lengths in m_val_loader:
            outputs = m_cnn(features[:, None].to(device))
            loss = criterion(outputs.squeeze(), dan.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_cnn, "m_dan_cnn"):
        print('Early Stopping!')
        break


# In[23]:


m_val = torch.load('best_m_val_cnn.pt')
m_en = torch.load('best_m_en_cnn.pt')
m_dan = torch.load('best_m_dan_cnn.pt')
    
m_val.eval()
accuracy_sum = 0.0
batches = 0
with torch.no_grad():
    for features, val, _, _, lengths in m_val_loader:
        outputs = m_val(features[:, None].to(device))
        acc, _ = spearmanr(outputs.cpu(), val.cpu())
        accuracy_sum += acc
        batches += 1
acc_val = accuracy_sum / batches

m_en.eval()
accuracy_sum = 0.0
batches = 0
with torch.no_grad():
    for features, _, en, _, lengths in m_val_loader:
        outputs = m_en(features[:, None].to(device))
        acc, _ = spearmanr(outputs.cpu(), en.cpu())
        accuracy_sum += acc
        batches += 1
acc_en = accuracy_sum / batches

m_dan.eval()
accuracy_sum = 0.0
batches = 0
with torch.no_grad():
    for features, _, _, dan, lengths in m_val_loader:
        outputs = m_dan(features[:, None].to(device))
        acc, _ = spearmanr(outputs.cpu(), dan.cpu())
        accuracy_sum += acc
        batches += 1
acc_dan = accuracy_sum / batches

print((acc_val + acc_en + acc_dan)/3)


# ## Step 11a - Transfer Learning
# Για το transfer learning διαβάσαμε τις πηγές που δίνονται από την εκφώνηση από τις οποίες προκύπτουν συνοπτικά τα εξής.
# Εάν σε ένα πρόβλημα ταξινόμησης δε διαθέτουμε αρκετά δεδομένα για το συγκεκριμένο πρόβλημα, αλλά υπάρχει ένα μεγάλο dataset για κάποιο συναφές πρόβλημα (όπου συναφές σημαίνει το input να είναι ίδιας μορφής -π.χ. εικόνα-εικόνα, ήχος-ήχος) μπορούμε να χρησιμοποιήσουμε το μεγάλο dataset για την εκπαίδευση του μοντέλου του αρχικού προβλήματος. Συγκεκριμένα, έχει παρατηρηθεί ότι τα πρώτα layers σε ένα δίκτυο συνήθως εκτελούν κάποιες πολύ βασικές λειτουργίες που είναι κοινές σε ένα μεγάλο εύρος προβλημάτων (π.χ. στις εικόνες τα φίλτρα Gabor). Επομένως η εκπαίδευση μπορεί να γίνει μια φορά και να εφαρμοστεί σε πολλά δίκτυα. Από το γεγονός αυτό είδαμε ότι εκπαιδεύοντας τα τελευταία layers, που είναι πιο specific στο εκάστοτε πρόβλημα, μπορούμε να έχουμε καλύτερα αποτελέσματα, καθώς ουσιαστικά είναι σα να αρχικοποιούμε το δίκτυο όχι σε random τιμές, αλλά σε τιμές πολύ κοντά στις επιθυμητές. 
# Αυτό θα κάνουμε και εδώ. Αρχικά εκπαιδεύουμε το μοντέλο στα δεδομένα του βήματος 9 και κρατάμε το μοντέλο με το καλύτερο accuracy. Στο βέλτιστο αυτό μοντέλο θα βασιστούμε για να δουλέψουμε στο multitask datset. Επαναφέρουμε τις τιμές των βαρών του τελευταίου sequential layer, ώστε το δίκτυο να "ξεχάσει" την specific εκπαίδευση που πήρε στο spectrogram dataset και να εξειδικευτεί στο multitask dataset. Θέτουμε δηλαδή τις τιμές των σε random αριθμούς για το τελευταίο sequential layer του CNN καθώς και για τα 2 fully connected. Επίσης, προσθέτουμε ένα fully connected layer, καθώς πλέον δεν έχουμε 10 εξόδους, αλλα μία στην οποία και θέλουμε regression. Θα χρησιμοποιήσουμε επίσης τη σιγμοειδή συνάρτηση ώστε η έξοδος να κυμαίνεται μεταξύ 0 και 1 όπως στο πρόβλημα μας.

# In[24]:


class Transfer(torch.nn.Module):
    def __init__(self, old):
        super(Transfer, self).__init__()
        self.new_layer = nn.Sequential(nn.Linear(10, 1),
                     nn.Sigmoid())
        self.old = old

    def forward(self, x):
        return self.new_layer(self.old.forward(x))
    


# In[25]:


cnn = torch.load('best_cnn.pt')
cnn.state_dict()['layer4.0.weight'].data.random_()
cnn.state_dict()['fc1.weight'].data.random_()
cnn.state_dict()['fc2.weight'].data.random_()

m_cnn = Transfer(cnn)

m_cnn.to(device)


# In[26]:


my_patience = 3
epochs = 25

criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(cnn.parameters(), weight_decay=0.5)

patience = [my_patience]
min_loss = [100]
train_losses = []
validation_losses = []
for epoch in range(epochs):
    m_cnn.train()
    loss_sum = 0.0
    batches = 0
    for features, val, _, _, lengths in m_train_loader:
        optimizer.zero_grad()
        outputs = m_cnn(features[:, None].to(device))
        loss = criterion(outputs.squeeze(), val.to(device))
        loss.backward()
        optimizer.step()
        loss_sum += loss.item()
        batches += 1
    train_loss = loss_sum / batches
    
    m_cnn.eval()
    loss_sum = 0.0
    batches = 0
    with torch.no_grad():
        for features, val, _, _, lengths in m_val_loader:
            outputs = m_cnn(features[:, None].to(device))
            loss = criterion(outputs.squeeze(), val.to(device))
            loss_sum += loss.item()
            batches += 1
    validation_loss = loss_sum / batches
    loss = [validation_loss]
    print('Epoch {}: Train Loss = {}, Validation Loss = {}'.format(epoch, train_loss, validation_loss))
    train_losses.append(train_loss)
    validation_losses.append(validation_loss)
    if stop_early(patience, loss, min_loss, m_cnn, "transfer_cnn"):
        print('Early Stopping!')
        break


# In[27]:


transfer = torch.load('best_transfer_cnn.pt')

transfer.eval()
accuracy_sum = 0.0
batches = 0
with torch.no_grad():
    for features, val, _, _, lengths in m_val_loader:
        outputs = transfer(features[:, None].to(device))
        acc, _ = spearmanr(outputs.cpu(), val.cpu())
        accuracy_sum += acc
        batches += 1
acc_val = accuracy_sum / batches

print (acc_val)

