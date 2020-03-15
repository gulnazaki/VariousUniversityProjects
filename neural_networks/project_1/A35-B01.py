#!/usr/bin/env python
# coding: utf-8

# In[68]:


import warnings 
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix,f1_score, precision_recall_fscore_support
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
from imblearn.pipeline import Pipeline
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score, cross_validate, GridSearchCV
from sklearn.utils import shuffle
import time


# ## Α. Στοιχεία ομάδας
# ***

#      Ομάδα Α35
#    
#    
#  
#  - Μελίστας Θωμάς - 03114149
#  - Κουμούτσου Δήμητρα - 03114022
#         
#  Datasets S02,B01

# ## Β. Εισαγωγή του dataset
# ***

# 1. Το dataset που μας δίνεται περιγράφει μετρήσεις ενός τηλεσκοπίου παρατήρησης σωματιδίων gamma. Το τηλεσκόπιο ανιχνεύει ενέργειες σωματιδίων χρησιμοποιώντας τη μέθοδο Monte Carlo. Τα σωματίδια (φωτόνια Cherenkov) αφήνουν το ίχνος τους στην κάμερα του τηλεσκοπίου. Σκοπός είναι να διαχωριστεί η ακτινοβολία σε αυτή που οφείλεται σε σήματα gamma ακτινοβολίας και σε αυτή που οφείλεται σε κοσμικές ακτίνες και αποτελεί background noise. Ανάλογα με τον σχηματισμό της ακτινοβολίας πάνω στο επίπεδο της κάμερας μπορούμε να ταξινομήσουμε τα δείγματα. Έτσι τα χαρακτηριστικά που δίνονται αφορούν το σχήμα της έλλειψης που παρατηρείται καθώς και την ενέργεια.
# 
# 2. Τα δείγματα είναι 19019, τα χαρακτηριστικά είναι 10 στην ουσία αφού το 11ο είναι η κλάση του δείγματος (gamma or hadron) και τα χαρακτηριστικά είναι συνεχείς τιμές (δεκαδικοί) που αναφέρονται σε γεωμετρικά και ενεργειακά χαρακτηριστικά και είναι mm, degrees ή ratios. Δεν υπάρχουν μη διατεταγμένα χαρακτηριστικά.
# 
# 3. Δέν υπάρχουν επικεφαλίδες, ούτε αρίθμηση των δειγμάτων.
# 
# 4. Το 11ο χαρακτηριστικό είναι το εκάστοτε label. Άρα η 11η κολώνα.
# 
# 5. Δεν χρειάστηκε κάποια επεξεργασία στο text αρχείο μας.
# 
# 6. Δεν απουσιάζει καμία τιμή από το dataset
# 
# 7. Έχουμε 2 κλάσεις όπως αναφέραμε και προηγουμένως. Το dataset δεν είναι ισορροπημένο και για την ακρίβεια όπως φαίνεται παρακάτω που υπολογίστηκε οι λόγοι είναι: 
#                                                    Percentage of 0 (hadron) (background) = 35.16483516483517 %
#                                                    Percentage of 1 (gamma) (event) = 64.83516483516483 %
# 
# 8. Χωρίζουμε σε train και test σε αναλογία 70-30 όπως ζητείται από την εκφώνηση.

# In[47]:


data = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/magic/magic04.data")
features = data.iloc[:,:10].values
labels = data.iloc[:,10]
mapping = {'h': 0, 'g': 1}
labels = labels.replace(mapping)
labels = labels.values.flatten()


# In[48]:


count = np.bincount(labels)
perc = count / len(labels)
print("Percentage of 0 (hadron) (background) =",perc[0]*100,"%")
print("Percentage of 1 (gamma) (event) =",perc[1]*100,"%")


# In[49]:


X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size = 0.3, random_state = 1312)


# ## Γ. Baseline classification

# Πρώτα θα χρησιμοποιήσουμε τους Dummy classifiers

# In[50]:


f1_micro_base = {}
f1_macro_base = {}


# In[51]:


dc_uniform = DummyClassifier(strategy="uniform")
dc_constant_0 = DummyClassifier(strategy="constant", constant=0)
dc_constant_1 = DummyClassifier(strategy="constant", constant=1)
dc_most_frequent = DummyClassifier(strategy="most_frequent")
dc_stratified = DummyClassifier(strategy="stratified")


# ###### Uniform

# In[86]:


model = dc_uniform.fit(X_train, y_train)
pred = model.predict(X_test)
confusion = confusion_matrix(y_test, pred)
f1_micro_base['uni'] = f1_score(y_test, pred, average="micro")
f1_macro_base['uni'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro_base['uni'])
print("F1_macro score: ", f1_macro_base['uni'], "\n")
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# ###### Constant 0

# In[88]:


model = dc_constant_0.fit(X_train, y_train)
pred = model.predict(X_test)
confusion = confusion_matrix(y_test, pred)
f1_micro_base['cons_0'] = f1_score(y_test, pred, average="micro")
f1_macro_base['cons_0'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro_base['cons_0'])
print("F1_macro score: ", f1_macro_base['cons_0'], "\n")
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# ###### Constant 1

# In[89]:


model = dc_constant_1.fit(X_train, y_train)
pred = model.predict(X_test)
confusion = confusion_matrix(y_test, pred)
f1_micro_base['cons_1'] = f1_score(y_test, pred, average="micro")
f1_macro_base['cons_1'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro_base['cons_1'])
print("F1_macro score: ", f1_macro_base['cons_1'], "\n")
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# ###### Most Frequent

# In[90]:


model = dc_most_frequent.fit(X_train, y_train)
pred = model.predict(X_test)
confusion = confusion_matrix(y_test, pred)
f1_micro_base['most_fr'] = f1_score(y_test, pred, average="micro")
f1_macro_base['most_fr'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro_base['most_fr'])
print("F1_macro score: ", f1_macro_base['most_fr'], "\n")
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# ###### Stratified

# In[91]:


model = dc_stratified.fit(X_train, y_train)
pred = model.predict(X_test)
confusion = confusion_matrix(y_test, pred)
f1_micro_base['strat'] = f1_score(y_test, pred, average="micro")
f1_macro_base['strat'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro_base['strat'])
print("F1_macro score: ", f1_macro_base['strat'], "\n")
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# ###### Gaussian Naive Bayes Classifier

# In[99]:


gnb = GaussianNB()
gnb.fit(X_train,y_train)
pred = gnb.predict(X_test)
confusion = confusion_matrix(y_test, pred)
f1_micro_base['gnb'] = f1_score(y_test, pred, average="micro")
f1_macro_base['gnb'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro_base['gnb'])
print("F1_macro score: ", f1_macro_base['gnb'], "\n")
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# ###### kNN

# In[100]:


kNN = KNeighborsClassifier()
kNN.fit(X_train,y_train)
pred = kNN.predict(X_test)
confusion = confusion_matrix(y_test, pred)
f1_micro_base['kNN'] = f1_score(y_test, pred, average="micro")
f1_macro_base['kNN'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro_base['kNN'])
print("F1_macro score: ", f1_macro_base['kNN'], "\n")
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# ###### Multi Layer Perceptron Classifier

# In[101]:


mlp = MLPClassifier()
mlp.fit(X_train,y_train)
pred = mlp.predict(X_test)
confusion = confusion_matrix(y_test, pred)
f1_micro_base['mlp'] = f1_score(y_test, pred, average="micro")
f1_macro_base['mlp'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro_base['mlp'])
print("F1_macro score: ", f1_macro_base['mlp'], "\n")
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# ###### Bar Plots για F1 Micro και F1 Macro μετρικές

# In[60]:


clas = list(f1_micro_base.keys())
values = list(f1_micro_base.values())
y_pos = np.arange(len(clas))

plt.bar(y_pos, values)
plt.title('F1-Micro Scores')
plt.xlabel('Classifiers')
plt.ylabel('Scores')
plt.xticks(y_pos, clas)

plt.show()


# In[61]:


clas = list(f1_macro_base.keys())
values = list(f1_macro_base.values())
y_pos = np.arange(len(clas))

plt.bar(y_pos, values)
plt.title('F1-Macro Scores')
plt.xlabel('Classifiers')
plt.ylabel('Scores')
plt.xticks(y_pos, clas)

plt.show()


# Θα σχολιάσουμε εδώ τα παραπάνω αποτελέσματα.
# 
# Αρχικά από τα confusion matrices και τις μετρικές precision και recall βγάζουμε τα εξής συμπεράσματα. Όσον αφορά τους dummy ταξινομητές ο uniform κρατάει και τις 2 μετρικές πολύ κοντά στο 50%. Ιδανικά θα είχαμε ίσα αθροίσματα κατά μήκος των 2 κολώνων αφού οι προβλέψεις γίνονται τυχαία με σκοπό να μην έχουμε κάποια προκατάληψη. Στο constant 0 και constant 1 προβλέπουμε πάντα την αντίστοιχη κλάση έτσι τα στοιχεία στην άλλη στήλη είναι 0. Όσον αφορά τις micro μετρικές έχουμε ίδιες τιμές στα f1, precision και recall οι οποίες είναι και το ποσοστό της αντίστοιχης κλάσης στο dataset μας. Το recall στην macro μετρική είναι αυστηρά 50% επίσης, απολύτως λογικό αφού το άθροισμα στη στήλη είναι 100% και διαιρούμε με 2 συνολικά κατηγορίες. Το precision είναι μικρότερο στο constant 0 αφού μικρότερο μέρος ανήκει στην κατηγορία αυτή. Για τον most_frequent έχουμε ακριβώς τα ίδια με το constant 1 αφού η κλάση 1 είναι η συχνότερη. Για τον stratified dummy έχουμε στη micro αλλά και στην macro ίδιο precision και recall (συνεπώς και f1) λογικό αφού ο classifier διαλέγει με πιθανότητα ίση με το ποσοστό της εκάστοτε κλάσης στο dataset (παρατηρείται σε κάθε micro μετρική). Στις micro μετρικές έχουμε μεγαλύτερα ποσοστά αφού δίνουμε μεγαλύτερη βαρύτητα στην πιο συχνή κλάση. Το confusion matrix επίσης έχει άθροισμα κολώνας τον αριθμό των δειγμάτων από κάθε κατηγορία. Στον Gaussian Naive Bayes βλέπουμε πολύ καλύερα αποτελέσματα όπως είναι λογικό. Βλέπουμε επίσης μια προτίμηση προς την κλάση 1 που έχει να κάνει και με το ότι στηρίζεται στις a priori πιθανότητες, έτσι τα false positive είναι πολύ περισσότερα από τα false negative. Στους kNN και MLP classifiers επίσης βλέπουμε πολύ καλύτερα αποτελέσματα με τον MLP να είναι καλύτερος αλλά και να έχει πιο ισορροπημένα False Positive και False Negative αφού δεν επηρεάζεται από το unbalanced dataset σε μεροληψία. Στην ουσία κάνει στατιστικά περισσότερες λάθος προβλέψεις στα events και δίνει λίγα false positives. (κάτι που διαβάζοντας την περιγραφή του dataset είναι και αυτό που μας ενδιαφέρει περισσότερο, δηλαδή θέλουμε μεγάλο precision).
# 
# Στα bar plots βλέπουμε συνοπτικά όσα περιγρέψαμε εδώ. Μόνη εμφανής διαφορά μεταξύ micro kai macro οι μετρικές για constant και most frequent dummies.

# ## Δ. Βελτιστοποίηση ταξινομητών

# Δημιουργούμε ένα μικρότερο testset το οποίο θα χρησιμοποιήσουμε σε απαιτητικούς υπολογισμούς και θα μας δώσει μια γενική κατεύθυνση για τις υπερπαραμέτρους.

# In[62]:


small_X, small_y = shuffle(X_train, y_train, random_state = 1312)
samples = 500
small_X = small_X[0:samples-1,:]
small_y = small_y[0:samples-1]


# Βλέπουμε ότι έχουμε πολύ λίγα features σε σχέση με τα δεδομένα μας κάτι που δείχνει ότι δεν χρειαζόμαστε μείωση διαστατικότητας. Τυπώνουμε επίσης τις κανονικοποιημένες διασπορές και βλέπουμε ότι δεν έχει νόημα να χρησιμοποιήσουμε variance threshold.

# In[63]:


print(len(y_train))
print(len(X_train[0]))
min_max_scaler = MinMaxScaler()
X_minmax = min_max_scaler.fit_transform(X_train)
Xvar = np.var(X_minmax, axis=0)
print(Xvar)


# In[64]:


micro_estimator = {}
macro_estimator = {}


# In[70]:


f1_micro = {}
f1_macro = {}


# Όσον αφορά τους dummy classifiers είναι προφανές ότι κανένας δεν έχει υπερπαραμέτρους αλλά και ότι κανένας δεν επηρεάζεται από το data preprocessing που γίνεται στα train δεδομένα εκτός ίσως από το sampling το οποίο επηρεάζει ελάχιστα το ποσοστό του stratify dummy αφού είναι πιο ισορροπημένα τα δείγματα. Και όπως βλέπουμε εδώ δίνει χειρότερα αποτελέσματα αφού θεωρεί ισοπίθανες τις 2 κατηγορίες ενώ στο test set δεν είναι.

# In[135]:


ros = RandomOverSampler(random_state=1312)
X_resampled, y_resampled = ros.fit_sample(X_train,y_train)
model = dc_stratified.fit(X_resampled, y_resampled)
pred = model.predict(X_test)
confusion = confusion_matrix(y_test, pred)

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_score(y_test, pred, average="micro"), "\n")
print("F1_macro score: ", f1_score(y_test, pred, average="micro"), "\n")


# In[136]:


f1_micro['uni'] = f1_micro_base['uni']
f1_macro['uni'] = f1_macro_base['uni']
f1_micro['cons_0'] = f1_micro_base['cons_0']
f1_macro['cons_0'] = f1_macro_base['cons_0']
f1_micro['cons_1'] = f1_micro_base['cons_1']
f1_macro['cons_1'] = f1_macro_base['cons_1']
f1_micro['most_fr'] = f1_micro_base['most_fr']
f1_macro['most_fr'] = f1_macro_base['most_fr']
f1_micro['strat'] = f1_score(y_test, pred, average="micro")
f1_macro['strat'] = f1_score(y_test, pred, average="macro")


# ###### Gaussian Naive Bayes Classifier

# Στον GNB δεν έχουμε κάποια υπερπαράμετρο (πέρα από το var_smoothing που δεν μας απασχολεί), οπότε θα περιοριστούμε στην βελτιστοποίηση της προεπεξεργασίας. Αρχικοποιούμε τους διάφορους ταξινομητές-μετασχηματιστές και ορίζουμε τα βήματα του pipeline, το pipeline και τις διάφορες περιπτώσεις που θα εξετάσει ο GridSearchCV. Θα εξετάσουμε Standard και MinMax Scaler ή κανέναν, OverSampler, UnderSampler ή κανέναν και διάφορες τιμές για το PCA. Για μετρική το f1 micro και παρακάτω το f1 macro. Για το PCA δώθηκαν οι τιμές : [2, 4, 6, 8, 10] και καλύτερη θεωρήθηκε το 6, μετά κάναμε πιο κοντινή αναζήτηση και καταλήξαμε σε 5 components.

# In[67]:


scaler = StandardScaler()
sampler = RandomOverSampler()
pca = PCA()
clf = GaussianNB()

pipe = Pipeline(steps=[('scaler', scaler), ('sampler', sampler), ('pca', pca), ('gnb', clf)], memory ='tmp')

dictionary = dict(
                scaler=[StandardScaler(), MinMaxScaler(), None],
                sampler=[RandomOverSampler(), RandomUnderSampler(), None], 
                pca__n_components=[4, 5, 6]
               )

micro_estimator['gnb'] = GridSearchCV(pipe, dictionary, n_jobs=-1, cv=5, scoring='f1_micro')
micro_estimator['gnb'].fit(X_train, y_train)
print(micro_estimator['gnb'].best_estimator_)   
print(micro_estimator['gnb'].best_params_)


# In[74]:


model = micro_estimator['gnb'].best_estimator_
start_time = time.time()
model.fit(X_train,y_train)
print("Χρόνος fit: %s seconds" % (time.time() - start_time))
start_time = time.time()
pred = model.predict(X_test)
print("Χρόνος predict: %s seconds" % (time.time() - start_time))
confusion = confusion_matrix(y_test, pred)
f1_micro['gnb'] = f1_score(y_test, pred, average="micro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro['gnb'])
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")


# Για τη βελτιστοποίηση της f1 macro μετρικής πάλι 5 components κρίνονται κατάλληλα και εδώ βλέπουμε ότι χρησιμοποιείται Undersampling για καλύτερα αποτελέσματα.

# In[73]:


scaler = StandardScaler()
sampler = RandomOverSampler()
pca = PCA()
clf = GaussianNB()

pipe = Pipeline(steps=[('scaler', scaler), ('sampler', sampler), ('pca', pca), ('gnb', clf)], memory ='tmp')

dictionary = dict(
                scaler=[StandardScaler(), MinMaxScaler(), None],
                sampler=[RandomOverSampler(), RandomUnderSampler(), None], 
                pca__n_components=[4, 5, 6]
               )

macro_estimator['gnb'] = GridSearchCV(pipe, dictionary, n_jobs=-1, cv=5, scoring='f1_macro')
macro_estimator['gnb'].fit(X_train, y_train)
print(macro_estimator['gnb'].best_estimator_)   
print(macro_estimator['gnb'].best_params_)


# In[129]:


model = macro_estimator['gnb'].best_estimator_
start_time = time.time()
model.fit(X_train,y_train)
print("Χρόνος fit: %s seconds" % (time.time() - start_time))
start_time = time.time()
pred = model.predict(X_test)
print("Χρόνος predict: %s seconds" % (time.time() - start_time))
confusion = confusion_matrix(y_test, pred)
f1_macro['gnb'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_macro score:", f1_macro['gnb'])
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# Βλέπουμε ότι έχουμε πολύ μικρούς χρόνους για τον GNB έναν classifier που θεωρείται πολύ ελαφρύς υπολογιστικά. Βελτιστοποίση για micro βλέπουμε στο confusion matrix ότι δίνει λιγότερο ισορροπημένα mispredictions από αυτή για macro κάτι που εξηγήθηκε στο πάνω μέρος.

# ###### kNN

# Στον Κ Νearest Νeighbors Classifier θα βρούμε βέλτιστες τιμές για 3 υπερπαραμέτρους του. n_neighbors: ο αριθμός των γειτόνων που λαμβάνονται υπόψιν. Στο baseline χρησιμοποιήθηκε η default τιμή 5 γείτονες.
# weights: 'uniform', 'distance', επηρρεάζει το 'βάρος' κοντινού κόμβου στην αποτίμηση του τελικού αποτελέσματος. 'uniform' σημαίνει το ίδιο βάρος για κάθε γείτονα και 'distance' σημαίνει ότι το βάρος επηρεάζεται από την απόσταση που έχει ένα σημείο σε σχέση με αυτό που μελετάται. Default uniform
# metric: καθορίζει τον τρόπο υπολογισμού της απόστασης μεταξύ σημείων. Θα μελετήσουμε τις μετρικές : 'euclidean', 'manhattan', 'chebyshev'. Default euclidean
# 
# Επειδή έχει κάποιο υπολογιστικό κόστος ο αλγόριθμος ξεκινήσαμε με όλες τις παραμέτρους και για προεπεξεργασία (αναφέρθηκαν παραπάνω) και χρησιμοποιήσαμε ένα μέρος του dataset. Όσον αφορά τη μεταβλητή neighbors ξεκινήσαμε στο διάστημα 1- 15 και εμβαθύναμε ανάλογα με τα αποτελέσματα.

# In[76]:


scaler = StandardScaler()
sampler = RandomOverSampler()
pca = PCA()
clf = KNeighborsClassifier()

pipe = Pipeline(steps=[('scaler', scaler), ('sampler', sampler), ('pca', pca), ('knn', clf)], memory ='tmp')

dictionary = dict(
                scaler=[MinMaxScaler()],
                sampler=[None], 
                pca__n_components=[9, 10],
                knn__n_neighbors=[11, 13],
                knn__weights=['uniform'],
                knn__metric=['euclidean']
               )

micro_estimator['knn'] = GridSearchCV(pipe, dictionary, n_jobs=-1, cv=5, scoring='f1_micro')
micro_estimator['knn'].fit(X_train, y_train)
print(micro_estimator['knn'].best_estimator_)   
print(micro_estimator['knn'].best_params_)


# In[77]:


model = micro_estimator['knn'].best_estimator_
start_time = time.time()
model.fit(X_train,y_train)
print("Χρόνος fit: %s seconds" % (time.time() - start_time))
start_time = time.time()
pred = model.predict(X_test)
print("Χρόνος predict: %s seconds" % (time.time() - start_time))
confusion = confusion_matrix(y_test, pred)
f1_micro['knn'] = f1_score(y_test, pred, average="micro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro['knn'])
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")


# Βλέπουμε ότι για την macro μετρική προτιμούμε λιγότερους γείτονες (9 αντί για 11) και έχουμε χειρότερα αποτελέσματα που όπως βλέπουμε από τα confusion matrices οφείλονται σε λιγότερες σωστές προβλέψεις της κατηγορίας 1 (gamma).

# In[78]:


scaler = StandardScaler()
sampler = RandomOverSampler()
pca = PCA()
clf = KNeighborsClassifier()

pipe = Pipeline(steps=[('scaler', scaler), ('sampler', sampler), ('pca', pca), ('knn', clf)], memory ='tmp')

dictionary = dict(
                scaler=[MinMaxScaler()],
                sampler=[None], 
                pca__n_components=[9, 10],
                knn__n_neighbors=[7, 9, 11],
                knn__weights=['uniform'],
                knn__metric=['euclidean']
               )

macro_estimator['knn'] = GridSearchCV(pipe, dictionary, n_jobs=-1, cv=5, scoring='f1_macro')
macro_estimator['knn'].fit(X_train, y_train)
print(macro_estimator['knn'].best_estimator_)   
print(macro_estimator['knn'].best_params_)


# In[130]:


model = macro_estimator['knn'].best_estimator_
start_time = time.time()
model.fit(X_train,y_train)
print("Χρόνος fit: %s seconds" % (time.time() - start_time))
start_time = time.time()
pred = model.predict(X_test)
print("Χρόνος predict: %s seconds" % (time.time() - start_time))
confusion = confusion_matrix(y_test, pred)
f1_macro['knn'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_macro score:", f1_macro['knn'])
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# Οι χρόνοι εδώ είναι επίσης μικροί αλά βλέπουμε αντίθετη συμπεριφορά με πριν. Στον gaussian το fit έπαιρνε πολύ περισσότερο χρόνο από το predict ενώ εδώ συμβαίνει το αντίθετο. Αυτό είναι εύλογο αν αναλογιστεί κανείς το ότι ο gaussian για να κάνει fit πρέπει να υπολογίσει πολλές πιθανότητες και για να κάνει predict απλά να κάνει κάποιες πράξεις στα ήδη γνωστά δεδομένα ενώ ο knn κάνει το μεγαλύτερο μέρος της δουλειάς κατα την πρόβλεψη (υπολογισμοί αποστάσεων κλπ).

# ###### Multi Layer Perceptron Classifier

# Για το MLP θα ασχοληθούμε με την εύρεση βέλτιστων τιμών για 6 υπερπαραμέτρους του:
# 1. hidden_layer_sizes :
# 2. solver :
# 3. activation :
# 4. alpha :
# 5. learning_rate :
# 6. max_iter :
# Η υπερπαράμετρος activation αφορά τη συνάρτηση ενεργοποίησης που χρησιμοποιείται στο layer.
# Η υπερπαράμετρος solver αφορά τον τρόπο βελτιστοποίησης των βάρών του layer.
# Η υπερπαράμετρος alpha ή αλλιώς L2 regularization term κανονικοποιεί το μοντέλο μας, δηλαδή το κάνει πιο απλό. Έχουμε trade-off σχέση αφού για μικρές τιμές κάνουμε overfitting ενώ για μεγάλες underfitting στο μοντέλο.
# Η υπερπαράπμετρος max_iter αφορά το πόσες εκτιμήσεις θα γίνουν, ιδανικά θέλουμε να είναι όσο μεγαλύτερη γίνεται εφόσον δεν κινδυνεύουμε από overfitting.
# Το learning_rate μπορεί να δηλώνει σταθερό ρυθμό εκπαίδευσης η όχι και τρόπο μεταβολής του. 
# Τέλος, το μέγεθος του hidden layer θέλουμε να είναι όσο μεγαλύτερο γίνεται αλλά θα πρέπει να συνοδεύεται και με αύξηση του max_iter. Όμως δεν θέλουμε να γίνει πολύ μεγάλο γιατί ενδέχεται το μοντέλο μας να είναι υπερβολικά πολύπλοκο. Επίσης είδαμε και από αυτό το μέρος ότι ναι μεν η αύξηση του δίνει καλύτερα αποτελέσματα όμως από ένα σημείο και μετά δεν προσφέρει παρά ελάχιστη βελτίωση και υπολογιστικά κοστίζει υπερβολικά πολυ.
# 
# Επειδή, οι χρόνοι για το MLP είναι απαγορευτικοί για ολόκληρο το dataset χρησιμοποιήσαμε πάλι μέρος του και γενικέυσαμε κατάλληλα. Αρχικά ξεκινήσαμε με όλους τους solver, όλες τις activation functions, τα learning rates και για hidden_layer_size από 10 μέχρι 210 με βήμα 50 επαναλάβαμε πολλές φορές και συνεχίσαμε με h_l_s από 80 μέχρι 120. Για το alpha χρησιμοποίηθηκαν τιμλές 0,0001 0,001 0,01 0,1 ενώ για max_iterations από 50 μέχρι 350 με βήμα 100. Όταν καταλήξαμε σε solver, activation, alpha, learning rate μεγαλώσαμε το sample trainset και προσπαθήσαμε να βρούμε με μεγαλύτερη ακρίβεια size και iterations όπου καταλήξαμε στο ότι για 100 neurons και 400 iterations έχουμε καλά αποτελέσματα αφού συμβαίνει συνήθως σύγκλιση ενώ για μεγαλύτερους ριθμούς έχουμε αμελητέα βελτίωση.

# In[81]:


scaler = StandardScaler()
sampler = RandomOverSampler()
pca = PCA()
clf = MLPClassifier()

pipe = Pipeline(steps=[('scaler', scaler), ('sampler', sampler), ('pca', pca), ('mlp', clf)], memory ='tmp')

dictionary = dict(
                scaler=[None],
                sampler=[RandomOverSampler()], 
                pca__n_components=[10],
                mlp__hidden_layer_sizes=[(100,)],
                mlp__solver=['adam'],
                mlp__activation=['logistic'],
                mlp__alpha=[0.001] ,
                mlp__learning_rate=['adaptive'],
                mlp__max_iter=[ 400] ,
               )

micro_estimator['mlp'] = GridSearchCV(pipe, dictionary, n_jobs=-1, cv=5, scoring='f1_micro', verbose=10)
micro_estimator['mlp'].fit(X_train, y_train)
print(micro_estimator['mlp'].best_estimator_)   
print(micro_estimator['mlp'].best_params_)


# In[82]:


model = micro_estimator['mlp'].best_estimator_
start_time = time.time()
model.fit(X_train,y_train)
print("Χρόνος fit: %s seconds" % (time.time() - start_time))
start_time = time.time()
pred = model.predict(X_test)
print("Χρόνος predict: %s seconds" % (time.time() - start_time))
confusion = confusion_matrix(y_test, pred)
f1_micro['mlp'] = f1_score(y_test, pred, average="micro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_micro score:", f1_micro['mlp'])
print(precision_recall_fscore_support(y_test, pred, average='micro'), "\n")


# Να τονιστεί σε αυτό το σημείο ότι στο MLP έχουμε προτίμηση για τη διαδικασία του oversampling στο preprocessing και στις 2 μετρικές.
# 
# Για την f1 macro έχουμε σχεδόν ίδιες παραμέτρους μόνο που βλέπουμε ότι και για μικρότερο hidden layer size έχουμε καλά αποτελέσματα.

# In[83]:


scaler = StandardScaler()
sampler = RandomOverSampler()
pca = PCA()
clf = MLPClassifier()

pipe = Pipeline(steps=[('scaler', scaler), ('sampler', sampler), ('pca', pca), ('mlp', clf)], memory ='tmp')

dictionary = dict(
                scaler=[None],
                sampler=[RandomOverSampler()], 
                pca__n_components=[10],
                mlp__hidden_layer_sizes=[(40,)],
                mlp__solver=['adam'],
                mlp__activation=['logistic'],
                mlp__alpha=[0.01] ,
                mlp__learning_rate=['invscaling'],
                mlp__max_iter=[300] ,
               )

macro_estimator['mlp'] = GridSearchCV(pipe, dictionary, n_jobs=-1, cv=5, scoring='f1_macro', verbose=10)
macro_estimator['mlp'].fit(X_train, y_train)
print(macro_estimator['mlp'].best_estimator_)   
print(macro_estimator['mlp'].best_params_)


# In[84]:


model = macro_estimator['mlp'].best_estimator_
start_time = time.time()
model.fit(X_train,y_train)
print("Χρόνος fit: %s seconds" % (time.time() - start_time))
start_time = time.time()
pred = model.predict(X_test)
print("Χρόνος predict: %s seconds" % (time.time() - start_time))
confusion = confusion_matrix(y_test, pred)
f1_macro['mlp'] = f1_score(y_test, pred, average="macro")

print("Confusion matrix:\n" ,confusion, "\n")
print("F1_macro score:", f1_macro['mlp'])
print(precision_recall_fscore_support(y_test, pred, average='macro'), "\n")


# Βλέπουμε παρεμφερή αποτελέσματα στις δύο μετρικές και στο confusion matrix του βέλτιστου macro πιο πολλές σωστές προβλέψεις και για τις 2 κατηγορίες και λιγότερα false positives που είναι και αυτό που μας ενδιαφέρει αρκετά σύμφωνα με το dataset.
# 
# Όσον αφορά τους χρόνους είναι εμφανές ότι ο MLP είναι ο πιο κοστοβόρος classifier (στην εκπαίδευση όχι στην πρόβλεψη) και επίσης βλεπουμε τη σημασία του hidden layer size αλλά και του max_iterations στον χρόνο εκπαίδευσης αφού για διπλάσιο size και 100 περισσότερα iterations ο micro mlp δηλαδή χρειάζεται σχεδόν 8πλάσιο χρόνο.

# ### Στην συνέχεια θα σχεδιάσουμε τα bar plot σύγκρισης για τα f1 micro και f1 macro μεταξύ των διαφορετικών classifiers και θα δείξουμε και τη διαφορά για optimised και baseline.

# In[137]:


clas = list(f1_micro_base.keys())
values_b = list(f1_micro_base.values())
values_o = list(f1_micro.values())
y_pos = np.arange(len(clas))
width = 0.3

fig, ax = plt.subplots()
ax.bar(y_pos, values_b, width)
ax.bar(y_pos + width, values_o, width)

plt.title('F1-Micro Scores')
plt.xlabel('Classifiers')
plt.ylabel('Scores')
plt.xticks(y_pos, clas)

plt.show()


# In[138]:


clas = list(f1_macro_base.keys())
values_b = list(f1_macro_base.values())
values_o = list(f1_macro.values())
y_pos = np.arange(len(clas))
width = 0.3

fig, ax = plt.subplots()
ax.bar(y_pos, values_b, width)
ax.bar(y_pos + width, values_o, width)

plt.title('F1-Macro Scores')
plt.xlabel('Classifiers')
plt.ylabel('Scores')
plt.xticks(y_pos, clas)

plt.show()


# Οι μετρικές για τους πρώτους 4 dummy είναι ίδια όπως προείπαμε. Για τον startified παρατηρούμε μείωση στο micro και αμελητέα αύξηση στο macro μετά από oversampling. Για τους υπόλοιπους βλέπουμε σαφή βελτίωση μετά την βελτιστοποίση και διατήρηση μεταξύ του ανταγωνισμού των classifiers.

# ### Πίνακες μεταβολής επίδοσης

# In[147]:


micro_d = {}
for i in f1_micro_base.keys():
    micro_d[i] = [f1_micro[i] - f1_micro_base[i]]
    
macro_d = {}
for i in f1_macro_base.keys():
    macro_d[i] = [f1_macro[i] - f1_macro_base[i]]

    
for i in f1_micro_base.keys():
    print('\n', i)
    print('\n f1-micro change ', 100 * micro_d[i][0], '%')
    print('\n f1-macro change ', 100 * macro_d[i][0], '%')


# Βλέπουμε ότι η μεγαλύτερη αλλαγή έχει συντελεστεί στην macro μετρική του πλέον optimised gaussian. Χρησιμοποιήθηκε MinMaxScaling, UnderSampling και PCA ανάλυση σε κύριες συνιστώσες κάτι που βελτίωσε σημαντικά την απόδοση του. Η πτώση στην απόδοση του stratified αναλύθηκε πιο πάνω. Βλέπουμε μικρή αλλαγή στον kNN αφού οι default τιμές του ήταν ίδιες και κάποιες άλλες αρκετά κοντά στις βέλτιστες. Στον MLP παρατηρούμε επίσης μικρή βελτίωση ειδικά στη μετρική micro ο λόγος είναι όμως οτι πήγαινε αρκετά καλα ήδη οπότε υπήρχαν μικρά περιθώρια βελτίωσης.
# 
# Να ειπωθεί σε αυτό το σημείο ότι ο λόγος που o MLP αλλά και άλλοι classifiers δεν δίνουν πολύ καλές αποδόσεις (πάνω απο 90% δηλαδή) είναι ότι ο αριθμός των χαρακτηριστικών (10) είναι υπερβολικά μικρός για ένα πρόβλημα με dataset 19019 δειγμάτων
