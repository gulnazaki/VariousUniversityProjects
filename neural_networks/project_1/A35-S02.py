#!/usr/bin/env python
# coding: utf-8

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

# ## Α. Εισαγωγή του dataset
# ***

#    ### 1.  Σύντομη παρουσίαση του dataset
#         
# Το dataset μας αφορά τα δεδομένα που συλλέχθηκαν κατά τη διάρκεια μιας μελέτης εγκεφαλογραφήματος. Συγκεκριμένα, ένας νεαρός άντρας έκανε 5 εγκεφαλογραφήματα. Αρχικά βρισκόταν σε κατάσταση ηρεμίας, έπειτα του ζητήθηκε να σκεφτεί ότι κουνάει το δεξί του αντίχειρα και στην αρχή και το τέλος της "κίνησης" ακούστηκε ένας ήχος ("μπιπ"). Το πείραμα συνεχίζεται για 30 λεπτά και τα δεδομένα συλλέχθηκαν για 5 δοκιμές από την κάθε κατάσταση. 
# 
# 

# In[1]:


import pandas as pd
import numpy as np
import warnings 
warnings.filterwarnings('ignore')


# In[2]:


#1-4
df = pd.read_csv("plrx.txt", header=None, sep='\t' )


#    ### 2.  Αριθμός δειγμάτων και χαρακτηριστικών, είδος χαρακτηριστικών, μη διατεταγμένα χαρακτηριστικά.
# Όπως βλέπουμε από τις διαστάσεις του πίνακα, έχουμε 182 γραμμές και 13 στήλες. Επομένως, έχουμε 182 δείγματα και 12 χαρακτηριστικά (που αντιστοιχούν σε συντελεστές wavelets) καθώς και η τελευταία στήλη είναι η πνευματική κατάσταση από το σήμα που καταγράφηκε στο εγκεφαλογράφημα (Planning (during imagination of motor act) / Relax state). 
# 

# In[3]:


print(df.shape)


#    ### 3.  Επικεφαλίδες, αρίθμηση γραμμών
#         
# Τυπώνοντας βλέπουμε ότι δεν υπάρχει επικεφαλίδα ούτε αρίθμηση στα δείγματα.

# In[4]:


print(df)


#   ### 4.   Ετικέτες των κλάσεων
#         
# Όπως είπαμε και προηγουμένως οι δύο καταστάσεις (Planning /  Relax) βρίσκονται στη 13η στήλη του πίνακα και κωδικοποιούνται με τους αριθμούς 1.0 , 2.0 αντίστοιχα. Χωρίζουμε τα χαρακτηριστικά από τις καταστάσεις σε δύο πίνακες. 

# In[5]:


#5 Το αρχείο έχει μόνο αριθμητικές τιμές άρα μπορεί να μετατραπεί απευθείας σε numpy array
np_data = df.values
features = np_data[:,0:12]
labels = np_data[:,12].astype(int) # για να δουλέψει η bincount πρέπει να κάνουμε cast τα labels από float σε int

print(features.shape)
print(labels.shape)


#   ###  5.   Μετατροπές
#         
# Είναι βολικότερο για την υλοποίηση του κώδικα να δουλεύουμε με binary τιμές, επομένως τροποποιούμε ελαφρά την κωδικοποίηση του αρχείου. Αλλάζουμε τις τιμές 1,2 σε 0,1.

# In[6]:


labels = labels - 1 


#   ###  6.   Απουσιάζουσες τιμές
#         
# Δεν απουσιάζουν τιμές από το dataset.

#  ###   7.  Αριθμός των κλάσεων, ποσοστά δειγμάτων τους επί του συνόλου, Ισορροπία dataset.
#         
# 2 κλάσεις όπως αναφέρθηκε και πριν (1,2). Με 130(1) και 52(2) δείγματα αντίστοιχα. Ποσοστιαία οι τιμές αυτές αντιστοιχούν περίπου σε 71.4 και 28.5, άρα εφόσον το όριο που δίνεται από την εκφώνηση για binary dataset είναι 60-40, το dataset μας δεν θεωρείται ισορροπημένο. Το χαρακτηριστικό αυτό θα αντιμετωπιστεί στη συνέχεια της άσκησης.

# In[7]:


frequencies = np.bincount(labels)
print("class frequencies: ", frequencies)
total_samples = frequencies.sum()
print("total samples: ", total_samples)
percentage = (frequencies / total_samples) * 100
print("class percentage: ", percentage)


#  ###   8.  Διαχωρισμός train, test.
#         
# Χωρίζουμε το dataset σε train set και test set με αναλογία 80-20, ώστε να έχουμε αρκετά δεδομένα για την εκπαίδευση του μοντέλου αλλά και ένα ικανοποιητικό test set για να δοκιμάσουμε το μοντέλο μας τελικά. 

# In[8]:


from sklearn.model_selection import train_test_split
train, test, train_labels, test_labels = train_test_split(features, labels, test_size=0.2)


# ## Γ. Baseline classification
# ***

#   ### 1. Classification
#   Φτιάχνουμε τους 6 classifiers (5 dummy + 1 k-Nearest Neighbors) και εκπαιδεύουμε στο train set. Έπειτα, κάνουμε εκτίμηση για το test set και κρατάμε τον πίνακα σύγχυσης (confusion matrix) καθώς και τιμές για τα average f1-micro και macro, που θα χρησιμοποιήσουμε αργότερα για να συγκρίνουμε με τη βελτιστοποιημένη εκδοχή.

# In[9]:


from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report


classifiers = []
dc_uniform = DummyClassifier(strategy="uniform")
dc_constant_0 = DummyClassifier(strategy="constant", constant=0)
dc_constant_1 = DummyClassifier(strategy="constant", constant=1)
dc_most_frequent = DummyClassifier(strategy="most_frequent")
dc_stratified = DummyClassifier(strategy="stratified")
knn = KNeighborsClassifier(n_neighbors=5)

classifiers.append(dc_uniform)
classifiers.append(dc_constant_0)
classifiers.append(dc_constant_1)
classifiers.append(dc_most_frequent)
classifiers.append(dc_stratified)
classifiers.append(knn)

model = []
pred = []
for i in classifiers:
    c = i.fit(train, train_labels)
    model.append(c)
    
for i in model:
    pred.append(i.predict(test))

conf_matrix = []
f1_micro = []
f1_macro = []
class_report = []
for i in pred:
    conf_matrix.append(confusion_matrix(test_labels, i))
    f1_micro.append(f1_score(test_labels, i, average="micro"))
    f1_macro.append(f1_score(test_labels, i, average="macro"))
    class_report.append(classification_report(test_labels, i))

for i, c in enumerate(classifiers):
    print(c)
    print('\n Confusion matrix is: \n', conf_matrix[i])
    print('\n F1-micro Average Score is ', f1_micro[i])
    print('\n F1-macro Average Score is ', f1_macro[i])
    print('\n', class_report[i])
    print("===========================================================================================================\n")


#    ***
#    ### 2. Bar plots
#    Για τα f1-micro και f1-macro (average) φτιάχνουμε δύο bar plots. Στον άξονα x έχουμε τους ταξινομητές και στον άξονα y την τιμή για κάθε αντίστοιχη μετρική. 
#    ***

# In[20]:


import matplotlib.pyplot as plt

clas = ['uni','con0', 'con1', 'mf', 'str','knn']
y_pos = np.arange(len(clas))

plt.bar(y_pos, f1_micro)
plt.title('F1-Micro Scores')
plt.xlabel('Classifiers')
plt.ylabel('Scores')
plt.xticks(y_pos, clas)

plt.show()


# In[11]:


plt.bar(y_pos, f1_macro)
plt.title('F1-Macro Scores')
plt.xlabel('Classifiers')
plt.ylabel('Scores')
plt.xticks(y_pos, clas)

plt.show()


# ***
# ### 3. Σχολιασμός
# Παρατηρούμε από τα bar plots ότι ως προς την f1-micro καλύτερο αποτέλεσμα δίνουν οι dummy με strategies constant 0 και most frequent καθώς και ο kNN, ενώ για την f1-macro είναι σαφώς καλύτερος ο kNN. Πάντως στον macro έχουμε  ελαφρώς χειρότερες τιμές σε σχέση με τον micro για όλους τους classifiers, γεγονός που οφείλεται στο ότι το dataset δεν είναι ισορροπημένο και η κλάση 0 είναι μεγαλύτερη σε αριθμό δειγμάτων.
# 
#    Σχετικά με τα confusion matrix και τις τιμές που έδωσε το classification report (precision, recall, f1-macro metrics) μπορούμε να βγάλουμε διάφορα συμπεράσματα. Ξεκινώντας από το πιο εμφανές, δηλαδή τις μηδενικές γραμμές στους dummy with constant strategy. Βλέπουμε ότι ανάλογα με την τιμή του constant έχουμε μια μηδενική γραμμή, δηλαδή για constant 0 η κλάση 1 είναι μηδενική και αντιστρόφως. Αυτό ήταν αναμενόμενο καθώς ο constant 1 διαλέγει πάντα την 2η κλάση κλπ. Για την uniform γνωρίζουμε ότι πάντοτε η επιλογή θα είναι τυχαία και ομοιόμορφη, γεγονός που φαίνεται και από τα αριθμητικά αποτελέσματα, αφού έχει τις πιο "ομαλές" κατανομές. Για τον most frequent και τον stratified γνωρίζουμε ότι πρόκειται για δύο  ταξινομητές που βασίζονται στο συχνότερο και στην κατανομή συχνοτήτων αντιστοίχως. Έχουμε πει και προηγουμένως ότι η κλάση 0 έχει περισσότερα δείγματα από την 1, άρα είναι αναμενόμενο να έχουμε μεγαλύτερες τιμές στην κλάση 0. Ειδικά για τον most frequent, έχουμε τη μηδενική γραμμή για την κλάση 1 ακριβώς όπως στον constant 0 (αφού το most frequent είναι το 0, άρα ουσιαστικά λειτουγούν όμοια).
#     
#    Τα ίδια συμπεράσματα μπορούμε να πάρουμε κοιτάζοντας και τους πίνακες σύγχυσης. Για το confusion matrix μπορούμε να δούμε αναλυτικά ποιες προβλέψεις έγιναν από τον ταξινομητή. Για τους ίδιους λόγους που εξηγήθηκαν παραπάνω, η μία στήλη του πίνακα είναι μηδενική για τους constant 0, constant 1 και most frequent (η αντίστοιχη της μηδενικής γραμμής που αναλύσαμε). Όπως γνωρίζουμε το άθροισμα των κελιών του cm αθροίζεται στο σύνολο των δειγμάτων του test set (εδώ 37). Η κατανομή των κλάσεων 0 και 1, όπως δείξαμε και κατά την εισαγωγή του dataset είναι μη ομοιόμορφη, και βλέπουμε πως χωρίζονται τα δείγματα στα classification report, στη στήλη support. 

# ## Βελτιστοποίηση ταξινομητών
# ***

# ***
# ### 1. Βελτιστοποίηση
# Υπερπαραμέτρους έχει μόνο ο kNN, την παράμετρο k (τον αριθμό των neighbors). Τα υπόλοιπα στάδια αφορούν την προεπεξεργασία των δεδομένων, με τη σειρά threshold -> scaling -> oversampling -> PCA -> estimator. Για κάθε συνδυασμό παραμέτρων κρατάμε τις μετρικές f1-micro και f1-macro. Από τις τιμές αυτές κρατάμε τη μέγιστη τιμή και το index της (δηλαδή σε ποιο συνδυασμό παραμέτρων αντιστοιχεί) και η συνάρτηση τα επιστρέφει.
# ***

# In[12]:


from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score


# function keywithmaxval taken from stackoverflow
# reads a dictionary with integer values
# returns the key of the max value
# modified to return value as well
def keywithmaxval(d):
    v=list(d.values())
    k=list(d.keys())
    return [ k[v.index(max(v))], max(v)]

def my_CV(params, train):
    f1_micro_params = {}
    f1_macro_params = {}

    for k in (params.get("knn")):
        for sel in (params.get("selector")):
            if (sel=="n"):
                train_reduced = train
            else:
                train_reduced = sel.fit_transform(train)
        
            for scal in (params.get("scaler")):
                if (scal=="n"):
                    train_scaled = train_reduced
                else:
                    scaler = scal().fit(train)
                    train_scaled = scaler.transform(train_reduced)
            
                for sam in (params.get("sampler")):
                    if (sam=="n"):
                        train_scaled_sampled = train_scaled
                        train_labels_sampled = train_labels
                    else:
                        train_scaled_sampled, train_labels_sampled = sam.fit_sample(train_scaled,train_labels)
                
                    for n in (params.get("pca")):
                        pca = PCA(n_components=n)
                        trainPCA = pca.fit_transform(train_scaled_sampled)

                        knn = KNeighborsClassifier(n_neighbors=k)
                        scores_mic = cross_val_score(knn, trainPCA, train_labels_sampled, cv=10, scoring='f1_micro')
                        f1_micro_params[(sel, scal, sam, n, k)] = scores_mic.mean()
                        scores_mac = cross_val_score(knn, trainPCA, train_labels_sampled, cv=10, scoring='f1_macro')
                        f1_macro_params[(sel, scal, sam, n, k)] = scores_mac.mean()
                 
    [opt_mic, max_mic] = keywithmaxval(f1_micro_params)
    [opt_mac, max_mac] = keywithmaxval(f1_macro_params)
                
    optimal_params = [opt_mic, opt_mac]
    optimal_scores = [max_mic, max_mac]
    
    return [optimal_params, optimal_scores]


# Ορίζουμε το πεδίο αναζήτησης για τις παραμέτρους. 
# 
# Για τα selector, scaler, sampler ορίζουμε και την τιμή "n" που αντιστοιχεί στη μη-χρήση αυτού του σταδίου. Για τον scaler χρησιμοποιούμε το Standard Scaler ή τον MinMax, για τον sampler Oversampling ή Undersampling. 
# 
# Για το PCA, εφόσον θέλουμε να μειώσουμε τις διαστάσεις, η μέγιστη τιμή θα είναι 12 (δηλαδή όσες είχαμε αρχικά) και η ελάχιστη προφανώς 2. 
# 
# Όσον αφορά τις τιμές για τον kNN, δοκιμάσαμε αρχικά τιμές μεταξύ 1-50, οι τιμές ήταν χαμηλές επομένως προσαρμόσαμε σταδιακά το διάστημα καταλήγοντας στο (1,10). Καλούμε τη συνάρτηση και έχουμε τις βέλτιστες παραμέτρους στην μεταβλητή params.

# In[13]:


params = { 
    "selector" : [VarianceThreshold(), "n"],
    "scaler" : [preprocessing.StandardScaler, preprocessing.MinMaxScaler, "n"], 
    "sampler" : [RandomOverSampler(random_state=0), RandomUnderSampler(random_state=0), "n"],
    "pca" : [i for i in range(2,13)], 
    "knn" : list(filter(lambda x: x % 2 != 0, list(range(1, 10)))) #ξεκινησα απο (1,50) και περιορισα στο 1,10
    }

[params, scores] = my_CV(params, train)


# In[14]:


print('Best model with f1-micro: \n' + str(params[0]) + '\n')
print('Score is: ' + str(scores[0]) + '\n')
      
print('Best model with f1-macro: \n' + str(params[1]) + '\n')
print('Score is: ' + str(scores[1]) + '\n')


# Βλέπουμε ότι το καλύτερο αποτέλεσμα με βάση τη μετρική f1-micro είναι VarianceThreshold, scaling με τον MinMax, Oversampling, αριθμός διανυσμάτων για τη μέθοδο PCA =7, δηλαδή μείωση των διαστάσεων σε 7, και υπερπαράμετρος για το kNN =1, δηλαδή μόνο ο κοντινότερος neighbor θα χρησιμοποιείται για την εκτίμηση. Με αυτό το μοντέλο έχουμε τιμή για το f1-micro = 0.864
# 
# Για καλύτερο αποτέλεσμα με βάση τη macro τα αποτελέσματα είναι παρόμοια, με μόνη διαφορά τον αριθμό των διαστάσεων στην PCA, που εδώ είναι 8. Το σκορ σε αυτή την περίπτωση είναι 0.862 (σχεδόν ίδιο με το micro).

# Φτιάχνουμε μια δική μας υλοποίηση για την pipeline, η οποία παίρνει στο input τις παραμέτρους για την προεπεξεργασία των δεδομένων, τα σύνολο train και test με τα αντίστοιχα labels, καθώς και τον estimator που θα χρησιμοποιηθεί. Σημειώνεται ότι, όπως και στην προηγούμενη συνάρτηση, όλα τα parameters και ο estimator πρέπει να έχουν οριστεί πριν την κλήση της συνάρτησης (δεν περνιούνται σαν string argument). Ο διαχωρισμός train-test διατηρείται όπως πριν και δεν κάνουμε ξανά split καθώς θέλουμε να συγκρίνουμε με τις προηγούμενες τιμές για τις μετρικές (πριν την προεπεξεργασία και τη βελτιστοποίηση, στο baseline).

# In[15]:


def my_pipeline(params, train, train_labels, test, test_labels, estimator):
    selector = params[0]
    scaler = params[1]
    sampler = params[2]
    n = params[3]
    k = params[4]
    
    if (selector=="n"):
        train_reduced = train
        test_reduced = test
    else:
        train_reduced = selector.fit_transform(train)
        test_reduced = selector.transform(test)
    
    if (scaler=="n"):
        train_scaled = train_reduced
        test_scaled = test_reduced
    else:
        scaler = scaler().fit(train)
        train_scaled = scaler.transform(train_reduced)
        test_scaled = scaler.transform(test_reduced)
    
    if (sampler=="n"):
        train_scaled_sampled = train_scaled
        train_labels_sampled = train_labels
    else:
        train_scaled_sampled, train_labels_sampled = sampler.fit_sample(train_scaled,train_labels)
    
    pca = PCA(n_components=n)
    trainPCA = pca.fit_transform(train_scaled_sampled)
    testPCA = pca.fit_transform(test_scaled)
    
    if (type(estimator) == type(KNeighborsClassifier())):
        estimator = KNeighborsClassifier(n_neighbors=k)
    pipe = [estimator, trainPCA, testPCA, train_labels_sampled, test_labels]
    return pipe


# Τρέχουμε τη συνάρτηση για όλους τους classifiers και παίρνουμε τις μέγιστες παραμέτρους για κάθε μια. Στη συνέχεια εκπαιδεύουμε το μοντέλο στα train δεδομένα και κάνουμε εκτίμηση στα test. Κρατάμε για όλες αυτές τις διαδικασίες τους αντίστοιχους χρόνους και εμφανίζουμε τις μετρικές (classification report, confusion matrix κλπ) σε κάθε περίπτωση.

# In[16]:


import time

micro_opt = []
macro_opt = []
fit_time = []
pred_time = []
estims = []

for i, estimator in enumerate(classifiers):
    print('For estimator: ' + str(estimator) + '\n')

    pipe = my_pipeline(params[0], train, train_labels, test, test_labels, estimator)
    
    estims.append(pipe[0])
    X_train = pipe[1]
    X_test = pipe[2]
    y_train = pipe[3]
    y_test = pipe[4]
    
    fit_start = time.time()
    model = pipe[0].fit(X_train, y_train) #pipe.fit(trainPCA, train_labels_sampled)
    fit_end = time.time()
    fit_time.append(fit_end - fit_start)
    print('Fit time was: %s seconds \n' % (fit_time[i]))
    
    pred_start = time.time()
    pred = pipe[0].predict(X_test) #pipe.predict(testPCA)
    pred_end = time.time()
    pred_time.append(pred_end - pred_start)

    print('Predict time was: %s seconds \n' % pred_time[i])
    
    print("Confusion matrix: \n" + str(confusion_matrix(y_test, pred))+ '\n')
    
    micro_opt.append(f1_score(y_test, pred, average="micro"))
    print("f1-micro : " + str(micro_opt[i]) + '\n')
    
    macro_opt.append(f1_score(y_test, pred, average="macro"))
    print("f1-macro : " + str(macro_opt[i]) + '\n')
    
    print(classification_report(y_test, pred)) #classification_report( test_labels_sampled, pred)
    print("===========================================================================================================\n")


# ***
# ### 2. Χρόνοι εκτέλεσης
# Τυπώνουμε ξεχωριστά ξανά τους χρόνους που απαιτούνται για κάθε διαδικασία (fit/predict) σε κάθε ταξινομητή.
# ***

# In[17]:


d = {}
for i, keys in enumerate(estims):
    d[keys] = [fit_time[i], pred_time[i]]

for x in d:
    print ('\n', x)
    print('\n Fit time: %s', d[x][0])
    print('\n Predict time: %s', d[x][1])


# ***
# ### 3. Bar plots
# Εμφανίζουμε σε bar plots τα αποτελέσματα του f1-score για την ταξινόμηση με τις βέλτιστες παραμέτρους. Με ανοιχτό πράσινο έχουμε τις αρχικές τιμές και με σκούρο τις νέες.
# ***

# In[18]:


clas = ['uni','con0', 'con1', 'mf', 'str','knn']
y_pos = np.arange(len(clas))
width = 0.3

fig, ax = plt.subplots()
ax.bar(y_pos, f1_micro, width, color = 'c')
ax.bar(y_pos + width, micro_opt ,width, color = 'g')

plt.title('F1-Micro Scores')
plt.xlabel('Classifiers')
plt.ylabel('Scores')
plt.xticks(y_pos, clas)
plt.show()


fig, ax = plt.subplots()
ax.bar(y_pos, f1_macro, width, color = 'c')
ax.bar(y_pos + width, macro_opt ,width ,color = 'g')

plt.title('F1-Macro Scores')
plt.xlabel('Classifiers')
plt.ylabel('Scores')
plt.xticks(y_pos, clas)
plt.show()


# *** 
# ### 4. Μεταβολή επίδοσης
# Για καλύτερη σύγκριση, υπολογίζουμε (επί τοις εκατό) τη διαφορά των μετρικών f1-micro average, f1-macro average.
# ***

# In[19]:


micro_d = {}
for i, keys in enumerate(estims):
    micro_d[keys] = [micro_opt[i] - f1_micro[i]]
    
macro_d = {}
for i, keys in enumerate(estims):
    macro_d[keys] = [macro_opt[i] - f1_macro[i]]

    
for x in micro_d:
    print('\n', x)
    print('\n f1-micro change ', 100 * micro_d[x][0], '%')
    print('\n f1-macro change ', 100 * macro_d[x][0], '%')


# ***
# ### 5. Σχολιασμός
# 
# ##### Plots, precision, recall, f1-scores, confusion matrices, μεταβολή απόδοσης
# Αρχικά, μπορούμε εποπτικά να πάρουμε τη γενική εικόνα από τα plots, όπου εύκολα βλέπουμε ποιοι ταξινομητές βελτιώθηκαν και πόσο. Πρώτα παρατηρούμε ότι οι constant 0,1 και most frequent δεν εμφάνισαν καμία βελτίωση. Μάλιστα, από τον πίνακα μεταβολής απόδοσης βλέπουμε ότι η μεταβολή ήταν 0. Αυτό ήταν αναμενόμενο, καθώς ο τρόπος με τον οποίο επιλέγουν δεν επιδέχεται βελτίωση (εξηγήσαμε τον τρόπο επιλογής στο σχολιασμό του baseline). Στα confusion matrices και τα precision - recall εμφανίζονται και πάλι οι μηδενικές γραμμές. Γενικά, τα αποτελέσματα ως προς τις ποιοτικές διαφορές μεταξύ ταξινομητών δεν έχουν αλλάξει σε σχέση με αυτά που πήραμε από το baseline. Θα εστιάσουμε στις μεταβολές από τη βελτιστοποίηση. 
# 
# Με τη βελτιστοποίηση των παραμέτρων και το preprocessing των δεδομένων έχουμε εξομαλύνει κάποιες ιδιαιτερότητες που είχε το dataset, ώστε να μην επηρεάζονται τα αποτελέσματα του prediction. 
# Μεγαλύτερη βελτίωση έχουμε στα macro scores, αναμενόμενο λόγω του preprocessing στα δεδομένα που έχει εξομαλύνει τις μεγάλες αποκλείσεις τα δέιγματα που είχαμε αρχικά. Και για τις δύο μετρικές έχουμε καλύτερη βελτίωση στον kNN για τον οποίο έχουμε βελτιστοποιήσει και την υπερπαράμετρο του.  Συγκεκριμένα βλέπουμε ότι ο kNN είχε βέλτιση παράμετρο k = 1. Αυτό σημαίνει ότι ταξινομεί καλύτερα τα αποκλείνονται δείγματα και έχει χαμηλότερη απόκλιση. Παρατηρούμε, όντως, ότι ο kNN έχει επιτύχει πολύ καλά αποτελέσματα και μάλιστα δίνει το μέγιστο f1 average score τόσο στο micro όσο και στο macro metric. 
# 
# Για τις μεταβολές της απόδοσης, γενικά βλέπουμε βελτίωση, ειδικά στον kNN. Βέβαια, στην περίπτωση του dummy stratified η απόδοση έπεσε. Αυτό μπορεί να οφείλεται σε διάφορες αιτίες, αποκλίσεις του test set από το train set κλπ. Γενικά, οι dummy ταξινομητές είναι μη παραμετρικοί, επομένως όπως γνωρίζουμε είναι πιο επιρρεπείς στο overfitting, δηλαδή προσαρμόζονται υπερβολικά στα train δεδομένα και τελικά αδυνατούν να γενικεύσουν το μοντέλο τους όταν γίνεται η εκτίμηση στα test. Γενικά, οι dummy ταξινομητές απαιτούν συγκεκριμένες κατανομές στα δεδομένα ώστε να δουλέψουν ιδανικά, πράγμα το οποίο φυσικά δεν ισχύει για πραγματικά datasets όπως αυτό που εξετάζουμε. 
# 
# 
# ##### Χρόνοι εκτέλεσης 
# Βλέπουμε με την πρώτη ματιά στον πίνακα των χρόνων εκτέλεσης ότι οι χρόνοι για την εκπαίδευση είναι πολύ μικρότεροι από τους χρόνους εκτίμησης. Θα εστιάσουμε όμως περισσότερο το σχολιασμό στις αποκλίσεις των χρόνων μεταξύ ταξινομητών. 
# 
# Σε αυτό το σημείο είναι ξεκάθαρο ότι ο kNN έχει σημαντικά καλύτερους χρόνους από όλους τους dummies. Η διαφορά αυτή έγκειται στη βασική διαφορά τους, ότι ο kNN είναι παραμετρικός, ενώ οι dummies μη παραμετρικοί. Οι μη παραμετρικοί είναι πιο αργοί συγκριτικά. Συγκεκριμένα, βλέπουμε ότι ο kNN έχει αμελητέο χρόνο εκπαίδευσης. Αυτό είναι αναμενόμενο καθώς από τη φύση του ο kNN βασίζεται στον υπολογισμό των αποστάσεων κάθε στοιχείου προς ταξινόμηση με τα γνωστά δείγματα από το train set, άρα απαιτεί χώρο για την αποθήκευση τους, αλλά όχι πολύ χρόνο για εκπαίδευση. Επίσης, επειδή εδώ κρατήσαμε (από τις βέλτιστες παραμέτρους) μόνο ένα γείτονα για τον υπολογισμό, και η φάση εκτίμησης είναι γρήγορη. 

# In[ ]:




