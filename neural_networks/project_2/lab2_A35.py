#!/usr/bin/env python
# coding: utf-8

import pandas as pd

dataset_url = "https://drive.google.com/uc?export=download&id=1PdkVDENX12tQliCk_HtUnAUbfxXvnWuG"
# make direct link for drive docs this way https://www.labnol.org/internet/direct-links-for-google-drive/28356/
df_data_1 = pd.read_csv(dataset_url, sep='\t',  header=None, quoting=3, error_bad_lines=False)


import numpy as np

# βάλτε το seed που αντιστοιχεί στην ομάδα σας
team_seed_number = 35

movie_seeds_url = "https://drive.google.com/uc?export=download&id=1NkzL6rqv4DYxGY-XTKkmPqEoJ8fNbMk_"
df_data_2 = pd.read_csv(movie_seeds_url, header=None, error_bad_lines=False)

# επιλέγεται 
my_index = df_data_2.iloc[team_seed_number,:].values

titles = df_data_1.iloc[:, [2]].values[my_index] # movie titles (string)
categories = df_data_1.iloc[:, [3]].values[my_index] # movie categories (string)
bins = df_data_1.iloc[:, [4]]
catbins = bins[4].str.split(',', expand=True).values.astype(np.float)[my_index] # movie categories in binary form (1 feature per category)
summaries =  df_data_1.iloc[:, [5]].values[my_index] # movie summaries (string)
corpus = summaries[:,0].tolist() # list form of summaries


# - Ο πίνακας **titles** περιέχει τους τίτλους των ταινιών. Παράδειγμα: 'Sid and Nancy'.
# - O πίνακας **categories** περιέχει τις κατηγορίες (είδη) της ταινίας υπό τη μορφή string. Παράδειγμα: '"Tragedy",  "Indie",  "Punk rock",  "Addiction Drama",  "Cult",  "Musical",  "Drama",  "Biopic \[feature\]",  "Romantic drama",  "Romance Film",  "Biographical film"'. Παρατηρούμε ότι είναι μια comma separated λίστα strings, με κάθε string να είναι μια κατηγορία.
# - Ο πίνακας **catbins** περιλαμβάνει πάλι τις κατηγορίες των ταινιών αλλά σε δυαδική μορφή ([one hot encoding](https://hackernoon.com/what-is-one-hot-encoding-why-and-when-do-you-have-to-use-it-e3c6186d008f)). Έχει διαστάσεις 5.000 x 322 (όσες οι διαφορετικές κατηγορίες). Αν η ταινία ανήκει στο συγκεκριμένο είδος η αντίστοιχη στήλη παίρνει την τιμή 1, αλλιώς παίρνει την τιμή 0.
# - Ο πίνακας **summaries** και η λίστα **corpus** περιλαμβάνουν τις συνόψεις των ταινιών (η corpus είναι απλά ο summaries σε μορφή λίστας). Κάθε σύνοψη είναι ένα (συνήθως μεγάλο) string. Παράδειγμα: *'The film is based on the real story of a Soviet Internal Troops soldier who killed his entire unit  as a result of Dedovschina. The plot unfolds mostly on board of the prisoner transport rail car guarded by a unit of paramilitary conscripts.'*
# - Θεωρούμε ως **ID** της κάθε ταινίας τον αριθμό γραμμής της ή το αντίστοιχο στοιχείο της λίστας. Παράδειγμα: για να τυπώσουμε τη σύνοψη της ταινίας με `ID=99` (την εκατοστή) θα γράψουμε `print(corpus[99])`.

# In[6]:


ID = 99
print(titles[ID])
print(categories[ID])
print(catbins[ID])
print(corpus[ID])


# # Εφαρμογή 1. Υλοποίηση συστήματος συστάσεων ταινιών βασισμένο στο περιεχόμενο
# <img src="http://clture.org/wp-content/uploads/2015/12/Netflix-Streaming-End-of-Year-Posts.jpg" width="50%">

# Η πρώτη εφαρμογή που θα αναπτύξετε θα είναι ένα [σύστημα συστάσεων](https://en.wikipedia.org/wiki/Recommender_system) ταινιών βασισμένο στο περιεχόμενο (content based recommender system). Τα συστήματα συστάσεων στοχεύουν στο να προτείνουν αυτόματα στο χρήστη αντικείμενα από μια συλλογή τα οποία ιδανικά θέλουμε να βρει ενδιαφέροντα ο χρήστης. Η κατηγοριοποίηση των συστημάτων συστάσεων βασίζεται στο πώς γίνεται η επιλογή (filtering) των συστηνόμενων αντικειμένων. Οι δύο κύριες κατηγορίες είναι η συνεργατική διήθηση (collaborative filtering) όπου το σύστημα προτείνει στο χρήστη αντικείμενα που έχουν αξιολογηθεί θετικά από χρήστες που έχουν παρόμοιο με αυτόν ιστορικό αξιολογήσεων και η διήθηση με βάση το περιεχόμενο (content based filtering), όπου προτείνονται στο χρήστη αντικείμενα με παρόμοιο περιεχόμενο (με βάση κάποια χαρακτηριστικά) με αυτά που έχει προηγουμένως αξιολογήσει θετικά.
# 
# Το σύστημα συστάσεων που θα αναπτύξετε θα βασίζεται στο **περιεχόμενο** και συγκεκριμένα στις συνόψεις των ταινιών (corpus). 
# 

# ## Μετατροπή σε TFIDF
# 
# Το πρώτο βήμα θα είναι λοιπόν να μετατρέψετε το corpus σε αναπαράσταση tf-idf:

# ***
# ### Σχόλια
# Στο preprocessing θα κάνουμε τη δική μας συνάρτηση για tokenization, την οποία θα περάσουμε ως όρισμα στον vectorizer. Σε αυτήν περιέχονται διάφορα στάδια. 
# Αρχικά θέλουμε να διαγράψουμε από τη λίστα μας τα σημεία στίξης και μερικές συχνά χρησιμοποιούμενες λέξεις που δεν προσφέρουν σημασιολογική αξία στο κείμενο (stopwords). Συγκεκριμένα, για τα πολλαπλά σημεία στίξης σε μια λέξη χρησιμοποιούμε τη συνάρτηση thorough_filter. Επίσης αφαιρούμε τα πρώτα ονόματα από τις πλοκές των ταινιών όπου εμφανίζονται συχνά και δεν προσφέρουν κάποια πληροφορία συγγένειας και μπορούν να επηρεάσουν αρνητικά οδηγώντας σε προτάσεις με βάση το όνομα του πρωταγωνιστή! Αυτό γίνεται με το names corpus του nltk. Επίσης αφαιρούμε τους αριθμούς αφού δεν βοηθάνε όπως είδαμε στο dataset μας.
# 
# Μπορούμε επίσης να χρησιμοποιήσουμε δύο γλωσσολογικούς μετασχηματισμούς, είτε την αφαίρεση της κατάληξης (stemming), είτε τη λημματοποίηση (lemmatization), ώστε από λέξεις με ίδια βάση θα θεωρούμε μια ενιαία αναπαράσταση. Εδώ θα χρησιμοποιήσουμε μόνο stemming καθώς βελτιώνει την ανάκληση και θα παραλείψουμε το lemmatization καθώς δε μας έδωσε χρήσιμα αποτελέσματα.
# ***

# In[7]:


import nltk
from nltk.corpus import stopwords
from nltk.corpus import names
from nltk.stem.porter import PorterStemmer
import string

names = [word.lower() for word in list(names.words())]

stop_words = names + list(stopwords.words('english')) + list(string.punctuation)

def thorough_filter(words):
    filtered_words = []
    for word in words:
        pun = True
        for letter in word:
            if (letter in string.punctuation + "0123456789ø–—’“”"):
                pun = False
        if (pun and len(word)>1):
            filtered_words.append(word)
    return filtered_words

def mytoken(corpus):
    words = nltk.word_tokenize(corpus.lower())
    filtered_words = [word for word in words if word not in stop_words]
    filtered_words = thorough_filter(filtered_words)
    porter_stemmer = PorterStemmer()
    stem_words = [porter_stemmer.stem(word) for word in filtered_words]
    return stem_words


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_df=0.4, min_df=5, tokenizer=mytoken)
corpus_tf_idf = vectorizer.fit_transform(corpus)


# Η συνάρτηση [TfidfVectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) όπως καλείται εδώ **δεν είναι βελτιστοποιημένη**. Οι επιλογές των μεθόδων και παραμέτρων της μπορεί να έχουν **δραματική επίδραση στην ποιότητα των συστάσεων** και είναι διαφορετικές για κάθε dataset. Επίσης, οι επιλογές αυτές έχουν πολύ μεγάλη επίδραση και στη **διαστατικότητα και όγκο των δεδομένων**. Η διαστατικότητα των δεδομένων με τη σειρά της θα έχει πολύ μεγάλη επίδραση στους **χρόνους εκπαίδευσης**, ιδιαίτερα στη δεύτερη εφαρμογή της άσκησης. Ανατρέξτε στα notebooks του εργαστηρίου και στο [FAQ](https://docs.google.com/document/d/1jL4gRag_LHbVCYIt5XVJ53iJPb6RZWi02rT5mPXiqEU/edit?usp=sharing) των ασκήσεων.
# 

# In[10]:


print(corpus_tf_idf.shape)
#print(vectorizer.get_feature_names())


# ## Υλοποίηση του συστήματος συστάσεων
# 
# Το σύστημα συστάσεων που θα παραδώσετε θα είναι μια συνάρτηση `content_recommender` με δύο ορίσματα `target_movie` και `max_recommendations`. Στην `target_movie` περνάμε το ID μιας ταινίας-στόχου για την οποία μας ενδιαφέρει να βρούμε παρόμοιες ως προς το περιεχόμενο (τη σύνοψη) ταινίες, `max_recommendations` στο πλήθος.
# Υλοποιήστε τη συνάρτηση ως εξής: 
# - για την ταινία-στόχο, από το `corpus_tf_idf` υπολογίστε την [ομοιότητα συνημιτόνου](https://en.wikipedia.org/wiki/Cosine_similarity) της με όλες τις ταινίες της συλλογής σας
# - με βάση την ομοιότητα συνημιτόνου που υπολογίσατε, δημιουργήστε ταξινομημένο πίνακα από το μεγαλύτερο στο μικρότερο, με τα indices (`ID`) των ταινιών. Παράδειγμα: αν η ταινία με index 1 έχει ομοιότητα συνημιτόνου με 3 ταινίες \[0.2 1 0.6\] (έχει ομοιότητα 1 με τον εαύτό της) ο ταξινομημένος αυτός πίνακας indices θα είναι \[1 2 0\].
# - Για την ταινία-στόχο εκτυπώστε: id, τίτλο, σύνοψη, κατηγορίες (categories)
# - Για τις `max_recommendations` ταινίες (πλην της ίδιας της ταινίας-στόχου που έχει cosine similarity 1 με τον εαυτό της) με τη μεγαλύτερη ομοιότητα συνημιτόνου (σε φθίνουσα σειρά), τυπώστε σειρά σύστασης (1 πιο κοντινή, 2 η δεύτερη πιο κοντινή κλπ), id, τίτλο, σύνοψη, κατηγορίες (categories)
# 

# In[11]:


import scipy as sp

def content_recommender(target_movie, max_recommendations):
    sim = []
    movies = corpus_tf_idf.toarray()
    for other in movies:
        sim.append(sp.spatial.distance.cosine(movies[target_movie], other))
    sim = np.argsort(sim)
    return sim[1:max_recommendations+1]

target_movie = 269
max_recommendations = 10

rec = content_recommender(target_movie, max_recommendations)
print("*** Target Movie " + str(target_movie) + " ***")
print("Title: " + titles[target_movie])
print("Genres: " + categories[target_movie])
print("Summary: " + corpus[target_movie])
print("*** " + str(max_recommendations) + " most related movies based on content ***")
for idx,movie in enumerate(rec):
    print("*** Recommended movie No. " + str(idx+1) + " ***")
    print("Movie ID: " + str(movie))
    print("Title: " + titles[movie])
    print("Genres: " + categories[movie])
    print("Summary: " + corpus[movie])


# ## Βελτιστοποίηση
# 
# Αφού υλοποιήσετε τη συνάρτηση `content_recommender` χρησιμοποιήστε τη για να βελτιστοποιήσετε την `TfidfVectorizer`. Συγκεκριμένα, αρχικά μπορείτε να δείτε τι επιστρέφει το σύστημα για τυχαίες ταινίες-στόχους και για ένα μικρό `max_recommendations` (2 ή 3). Αν σε κάποιες ταινίες το σύστημα μοιάζει να επιστρέφει σημασιολογικά κοντινές ταινίες σημειώστε το `ID` τους. Δοκιμάστε στη συνέχεια να βελτιστοποιήσετε την `TfidfVectorizer` για τα συγκεκριμένα `ID` ώστε να επιστρέφονται σημασιολογικά κοντινές ταινίες για μεγαλύτερο αριθμό `max_recommendations`. Παράλληλα, όσο βελτιστοποιείτε την `TfidfVectorizer`, θα πρέπει να λαμβάνετε καλές συστάσεις για μεγαλύτερο αριθμό τυχαίων ταινιών. Μπορείτε επίσης να βελτιστοποιήσετε τη συνάρτηση παρατηρώντας πολλά φαινόμενα που το σύστημα εκλαμβάνει ως ομοιότητα περιεχομένου ενώ επί της ουσίας δεν είναι επιθυμητό να συνυπολογίζονται (δείτε σχετικά το [FAQ](https://docs.google.com/document/d/1jL4gRag_LHbVCYIt5XVJ53iJPb6RZWi02rT5mPXiqEU/edit?usp=sharing)). Ταυτόχρονα, μια άλλη κατεύθυνση της βελτιστοποίησης είναι να χρησιμοποιείτε τις παραμέτρους του `TfidfVectorizer` έτσι ώστε να μειώνονται οι διαστάσεις του Vector Space Model μέχρι το σημείο που θα αρχίσει να εμφανίζονται επιπτώσεις στην ποιότητα των συστάσεων. 
# 
# 
# 

# ## Επεξήγηση επιλογών και ποιοτική ερμηνεία
# 
# Σε markdown περιγράψτε πώς προχωρήσατε στις επιλογές σας για τη βελτιστοποίηση της `TfidfVectorizer`. Επίσης σε markdown δώστε 10 παραδείγματα (IDs) από τη συλλογή σας που επιστρέφουν καλά αποτελέσματα μέχρι `max_recommendations` (5 και παραπάνω) και σημειώστε συνοπτικά ποια είναι η θεματική που ενώνει τις ταινίες.
# 
# Δείτε [εδώ](https://pastebin.com/raw/ZEvg5t3z) ένα παράδειγμα εξόδου του βελτιστοποιημένου συστήματος συστάσεων για την ταίνία ["Q Planes"](https://en.wikipedia.org/wiki/Q_Planes) με την κλήση της συνάρτησης για κάποιο seed `content_recommender(529,3)`. Είναι φανερό ότι η κοινή θεματική των ταινιών είναι τα αεροπλάνα, οι πτήσεις, οι πιλότοι, ο πόλεμος.

# ***
# ### Σχόλια
# Υλοποιούμε τη συνάρτηση όπως ζητήθηκε, με απόσταση συνημιτόνου, ώστε να βρούμε τις "κοντινές" λέξεις. 
# Για να βρούμε τις κατάλληλες παραμέτρους στο vectorizer, δοκιμάσαμε διάφορες ταινίες-target, π.χ. 4, 6 κλπ και εμφανίζαμε 3 recommendations κάθε φορά. Αρχικά τα αποτελέσματα δεν ήταν ικανοποιητικά για τις περισσότερες, όμως βρήκαμε το target ID = 700 με 3 recommendations να δίνει σχετικά αποτελέσματα. Συγκεκριμένα, η αρχική ταινία αφορά δύο στρατιώτες και αναφέρει μεταξύ άλλων στην πλοκή κατοχή όπλων, στρατιωτικές επιθέσεις, φυλάκιση, καταστάσεις ομηριας κλπ.
# Οι 3 ταινίες που προτείνονται αφορούν όλες μαχητές, όπλα, βλέπουμε δηλαδή να επαναλαμβάνονται οι λέξεις 'weapon', 'fighter' και γενικά οι πλοκές τους είναι παρεμφερείς. Κρατώντας αυτό ως ένα ID που έδωσε καλά αποτελέσματα δοκιμάζουμε διάφορες τιμές για min_df και max_df στο `TfidfVectorizer`. Ξεκινήσαμε από τις τιμές min = 0.02 και max = 0.5, ως μια πρώτη προσέγγιση που θεωρήσαμε χονδρικά ρεαλιστική και προσαρμόσαμε βλέποντας τα αποτελέσματα απο το recommender. 
# Αρχικά δοκιμάσαμε με δεκαδικους, που μεταφράζονται ως ποσοστό επί του συνόλου, δηλαδή αν η λέξη εμφανίζεται σε ποσοστό από 50% και πάνω, θεωρούμε οτι είναι πολύ generic άρα δεν μεταφέρει κάποια σημαντική πληροφορία που να διαφοροποιεί την πλοκή. Αντιθέτως, αν μια λέξη είναι πολύ σπάνια δε θα είναι χρήσιμη εφόσον θα εμφανίζεται συμπτωματικά και θα αυξάνει το feature size μας με τις επακόλουθες δυσκολίες. Στο στάδιο που ακολούθησε δοκιμάσαμε διαφορετικές προσεγγίσεις ως προς το max και το min, δηλαδή είτε διαφορετικές τιμές ποσοστών, είτε απόλυτες τιμές εμφανίσεων, είτε μεικτές. Τελικά, για το min επιλέξαμε τιμή 5, δηλαδή οχι ποσοστό επί των εμφανίσεων, αλλα απόλυτο αριθμό εμφάνισης (αν η λέξη εχει εμφανιστεί 5 φορές). Με αυτό το σχήμα δοκιμάσαμε στο γνωστό μας ID=700 αν η αναζήτηση θα δώσει καλά αποτελέσματα πέρα των 3 που βρήκαμε αρχικά.
# Θέλουμε να επαληθεύσουμε ότι το μοντέλο μας είναι καλό. Έχοντας βρει οτι αυτή η αναζήτηση ανταποκρίνεται καλά στα 3 recommendations για το συγκεκριμένο target movie, δοκιμάζουμε με 5 recommendations και έχουμε ακόμη σχετικές ταινίες ('weapon', 'army') και επεκτείνουμε για 10 ταινίες. Για ολα τα αποτελέσματα έχουμε πολύ καλό συσχετισμό περιεχομένου, είτε που αφορούν όπλα, είτε φυλακές (π.χ. 10ο recommendation) είτε μαχητές (9ο recommendation). 
# 
# Σημειώνεται ότι για να αποφύγουμε το φαινόμενο που αναφέρεται στην εκφώνηση, δηλαδή να λαμβάνονται υπ όψιν ομοιότητες που δεν προσφέρουν στην πλοκή, έχουμε εφαρμόσει δύο βασικές μεθόδους. Η πρώτη αφορά τη συχνότητα εμφάνισης, επομένως φράσεις όπως στο παράδειγμα του FAQ ("The plot of this film is about…") περιμένουμε οτι θα περιοριστούν απο το max_df, εφόσον θα εμφανίζονται αρκετά συχνά (θεωρούμε περισσότερο από το ποσοστό που ορίσαμε). Η δεύτερη μέθοδος που εφαρμόζουμε υλοποιείται στο στάδιο του tokenization και είναι η αφαίρεση των ονομάτων. Πολλές φορές στην πλοκη αναφέρεται το όνομα του πρωταγωνιστή ως υποκείμενο κάποιας πρότασης αλλά αυτό σαν στοιχείο δεν συσχετίζει την πλοκή των ταινιών σημασιολογικά (είναι λεκτική ομοιότητα, αλλά όχι περιεχομένου).
# 
# ***
# 
# Στη συνέχεια θα δώσουμε 10 παραδείγματα απο ταινίες που πήραμε καλά recommendations, δηλαδη καλουμε 10 φορες τη συναρτηση με διαφορετικα inputs (διαφορετικα target και αριθμο recommendations (5-15)). Αφήνουμε το αποτέλεσμα στο output του notebook, αλλά λόγω μεγάλου όγκου κειμένου, θα σχολιάσουμε συνοπτικά τα αποτελέσματα, βλέποντας την πλοκή της ταινίας στόχου και τη θεματολογία που ακολουθούν τα recommendations, ώστε να ελέγξουμε αν επαληθεύεται η καλή υλοποίηση του Vectorizer.
# 
# ***

# In[12]:


n = 5
for target in [304, 106, 32, 726, 1097, 269, 806, 67, 460, 4307]: 
    target_movie = target
    max_recommendations = n
    n+=1

    rec = content_recommender(target_movie, max_recommendations)
    print("*** Target Movie " + str(target_movie) + " ***")
    print("Title: " + titles[target_movie])
    print("Genres: " + categories[target_movie])
    print("Summary: " + corpus[target_movie])
    print("*** " + str(max_recommendations) + " most related movies based on content ***")
    for idx,movie in enumerate(rec):
        print("*** Recommended movie No. " + str(idx+1) + " ***")
        print("Movie ID: " + str(movie))
        print("Title: " + titles[movie])
        print("Genres: " + categories[movie])
        print("Summary: " + corpus[movie])
    
    print('\n \n ************************** NEXT MOVIE *******************************\n \n')


# *** 
# ### Σχόλια
# Αναφέρονται συνοπτικά οι ταινίες που επιλέχθηκαν, με αύξον αριθμό recommendations στην παρένθεση, ξεκινώντας από 5. Αναφέρονται κάποιες λέξεις κλειδιά που προσδιορίζουν την πλοκή και τη θεματολογία της ταινίας και τη συνδέουν με όλα τα recommendations που μας έδωσε ο recommender.
# 
#     - ID 304 - high school - girls - teenage love stories (5)
#     - ID 106 - Football clubs - Soccer teams - Παίκτες ομάδων - φιλίες εντός ομάδων - πως το ποδόσφαιρο καθορίζει τη ζωή ενός νέου παίκτη (έχουμε recommendations και για basketball teams, για φιλίες σε ομάδες, για αθλητές και την επιρροή του αθλήματος στη ζωή τους κλπ) (6)
#     - ID 32 - Nazis - Jews. Εδώ έχουμε το 4ο recommendation με "κακό" περιεχόμενο, δηλαδή η θεματολογία δεν εμπίπτει στο αρχικό μας θέμα (διωγμοί εβραίων, γερμανικές επιθέσεις, ναζισμός κλπ). Με μια σύντομη εποπτεία στα summaries βλέπουμε οτι υπάρουν κοινές λεξεις (π.χ. play) που δεν αφορούν την πλοκή (οι ταινίες δεν αφορούν παιχνίδι ή παίκτες, αλλά χρησιμοποιείται ως εναλλακτική του perform - performance). (7)
#     - ID 726 - Sharks - Shark attacks - Ocean. Υπάρχουν βέβαια 2 recommendations που δεν έχουν κοινή θεματολογία, η μία ταινία έχει όνομα πρωταγωνιστή "Shark" και η δεύτερη αφορά loan sharks, δηλαδή υπάρχει λεκτική ομοιότητα αλλά η θεματολογία δεν αφορά πραγματικούς καρχαρίες όπως η αρχική ταινία (8)
#     - ID 1097 - divorce - wife - marriage (9)
#     - ID 269 - Πιλότοι - πτήσεις (10)
#     - ID 806 - Music - Music Bands - ταινίες με συγκροτήματα - συγκροτήματα που αντιμετωπίζουν προβλήματα - συναυλίες (11)
#     - ID 67 - Second World War - German soldiers - Allies (12)
#     - ID 460 - Ένα αεροπλάνο πέφτει στο οποίο επιβαίνουν παιδιά και ένας πιλότος τα ψάχνει μαζί με τη μητέρα τους, καθώς τα παιδιά προσπαθούν να επιβιώσουν. Εδώ έχουμε recommendations για ταινίες με πιλότους, αεροπλάνα κλπ (1-8, 10) αλλά και για ταινίες με παιδιά και οικογένειες, μητέρες κλπ. (13)
#     - ID 4307 - Dance - disco - music. Μια γυναίκα ανοίγει ένα ντίσκο χορευτικό μπαρ με έναν συνεργάτη που δεν εγκρίνει ο σύντροφος της. Στα recommendations έχουμε ταινίες για χορό, μουσική, συνεργασίες σε κλαμπ. (14)
#     
# ***
# 
# 

# ## Tip: persistence αντικειμένων με joblib.dump
# 
# H βιβλιοθήκη [joblib](https://pypi.python.org/pypi/joblib) της Python δίνει κάποιες εξαιρετικά χρήσιμες ιδιότητες στην ανάπτυξη κώδικα: pipelining, παραλληλισμό, caching και variable persistence. Τις τρεις πρώτες ιδιότητες τις είδαμε στην πρώτη άσκηση. Στην παρούσα άσκηση θα μας φανεί χρήσιμη η τέταρτη, το persistence των αντικειμένων. Συγκεκριμένα μπορούμε με:
# 
# ```python
# from sklearn.externals import joblib  
# joblib.dump(my_object, 'my_object.pkl') 
# ```
# 
# να αποθηκεύσουμε οποιοδήποτε αντικείμενο-μεταβλητή (εδώ το `my_object`) απευθείας πάνω στο filesystem ως αρχείο, το οποίο στη συνέχεια μπορούμε να ανακαλέσουμε ως εξής:
# 
# ```python
# my_object = joblib.load('my_object.pkl')
# ```
# 
# Μπορούμε έτσι να ανακαλέσουμε μεταβλητές ακόμα και αφού κλείσουμε και ξανανοίξουμε το notebook, χωρίς να χρειαστεί να ακολουθήσουμε ξανά όλα τα βήματα ένα - ένα για την παραγωγή τους, κάτι ιδιαίτερα χρήσιμο αν αυτή η διαδικασία είναι χρονοβόρα. Προσοχή: αυτό ισχύει μόνο στα Azure και Kaggle, στο Colab και στο IBM τα αρχεία εξαφανίζονται όταν ανακυκλώνεται ο πυρήνας και θα πρέπει να τα αποθηκεύετε τοπικά. Περισσότερα στο [FAQ](https://docs.google.com/document/d/1jL4gRag_LHbVCYIt5XVJ53iJPb6RZWi02rT5mPXiqEU/edit?usp=sharing).
# 
# Ας αποθηκεύσουμε το `corpus_tf_idf` και στη συνέχεια ας το ανακαλέσουμε.

# In[ ]:


from sklearn.externals import joblib
joblib.dump(corpus_tf_idf, 'corpus_tf_idf.pkl') 


# 
# 
# Μπορείτε με ένα απλό `!ls` να δείτε ότι το αρχείο `corpus_tf_idf.pkl` υπάρχει στο filesystem σας (== persistence):

# In[ ]:


get_ipython().system('ls -lh')


# και μπορούμε να τα διαβάσουμε με `joblib.load`

# In[9]:


from sklearn.externals import joblib
corpus_tf_idf = joblib.load('corpus_tf_idf.pkl')


# # Εφαρμογή 2.  Σημασιολογική απεικόνιση της συλλογής ταινιών με χρήση SOM
# <img src="http://visual-memory.co.uk/daniel/Documents/intgenre/Images/film-genres.jpg" width="35%">

# ## Δημιουργία dataset
# Στη δεύτερη εφαρμογή θα βασιστούμε στις τοπολογικές ιδιότητες των Self Organizing Maps (SOM) για να φτιάξουμε ενά χάρτη (grid) δύο διαστάσεων όπου θα απεικονίζονται όλες οι ταινίες της συλλογής της ομάδας με τρόπο χωρικά συνεκτικό ως προς το περιεχόμενο και κυρίως το είδος τους. 
# 
# Η `build_final_set` αρχικά μετατρέπει την αραιή αναπαράσταση tf-idf της εξόδου της `TfidfVectorizer()` σε πυκνή (η [αραιή αναπαράσταση](https://en.wikipedia.org/wiki/Sparse_matrix) έχει τιμές μόνο για τα μη μηδενικά στοιχεία). 
# 
# Στη συνέχεια ενώνει την πυκνή `dense_tf_idf` αναπαράσταση και τις binarized κατηγορίες `catbins` των ταινιών ως επιπλέον στήλες (χαρακτηριστικά). Συνεπώς, κάθε ταινία αναπαρίσταται στο Vector Space Model από τα χαρακτηριστικά του TFIDF και τις κατηγορίες της.
# 
# Τέλος, δέχεται ένα ορισμα για το πόσες ταινίες να επιστρέψει, με default τιμή όλες τις ταινίες (5000). Αυτό είναι χρήσιμο για να μπορείτε αν θέλετε να φτιάχνετε μικρότερα σύνολα δεδομένων ώστε να εκπαιδεύεται ταχύτερα το SOM.
# 
# Σημειώστε ότι το IBM Watson δείνει "Kernel dead" εάν δεν έχετε βελτιστοποιήσει το tfidf και μικρύνει τις διαστάσεις του dataset (πιθανότατα κάποια υπέρβαση μνήμης).

# In[13]:


size = 5000
def build_final_set(doc_limit = size, tf_idf_only=False):
    # convert sparse tf_idf to dense tf_idf representation
    #    dense_tf_idf = corpus_tf_idf.toarray()[0:doc_limit,:]
    dense_tf_idf = corpus_tf_idf[0:doc_limit,:].toarray()
    if tf_idf_only:
        # use only tf_idf
        final_set = dense_tf_idf
    else:
        # append the binary categories features horizontaly to the (dense) tf_idf features
        final_set = np.hstack((dense_tf_idf, catbins[0:doc_limit,:]))
        # η somoclu θέλει δεδομ΄ένα σε float32
    return np.array(final_set, dtype=np.float32)


# In[14]:


final_set = build_final_set()


# Τυπώνουμε τις διαστάσεις του τελικού dataset μας. Χωρίς βελτιστοποίηση του TFIDF θα έχουμε περίπου 50.000 χαρακτηριστικά.

# In[15]:


final_set.shape


# Με βάση την εμπειρία σας στην προετοιμασί των δεδομένων στην επιβλεπόμενη μάθηση, υπάρχει κάποιο βήμα προεπεξεργασίας που θα μπορούσε να εφαρμοστεί σε αυτό το dataset; 

# ## Εκπαίδευση χάρτη SOM
# 
# Θα δουλέψουμε με τη βιβλιοθήκη SOM ["Somoclu"](http://somoclu.readthedocs.io/en/stable/index.html). Εισάγουμε τις somoclu και matplotlib και λέμε στη matplotlib να τυπώνει εντός του notebook (κι όχι σε pop up window).

# In[17]:


# install somoclu
get_ipython().system('pip install --upgrade somoclu')
# import sompoclu, matplotlib
import somoclu
import matplotlib
# we will plot inside the notebook and not in separate window
get_ipython().run_line_magic('matplotlib', 'inline')


# Καταρχάς διαβάστε το [function reference](http://somoclu.readthedocs.io/en/stable/reference.html) του somoclu. Θα δoυλέψουμε με χάρτη τύπου planar, παραλληλόγραμμου σχήματος νευρώνων με τυχαία αρχικοποίηση (όλα αυτά είναι default). Μπορείτε να δοκιμάσετε διάφορα μεγέθη χάρτη ωστόσο όσο ο αριθμός των νευρώνων μεγαλώνει, μεγαλώνει και ο χρόνος εκπαίδευσης. Για το training δεν χρειάζεται να ξεπεράσετε τα 100 epochs. Σε γενικές γραμμές μπορούμε να βασιστούμε στις default παραμέτρους μέχρι να έχουμε τη δυνατότητα να οπτικοποιήσουμε και να αναλύσουμε ποιοτικά τα αποτελέσματα. Ξεκινήστε με ένα χάρτη 10 x 10, 100 epochs training και ένα υποσύνολο των ταινιών (π.χ. 2000). Χρησιμοποιήστε την `time` για να έχετε μια εικόνα των χρόνων εκπαίδευσης. Ενδεικτικά, με σωστή κωδικοποίηση tf-idf, μικροί χάρτες για λίγα δεδομένα (1000-2000) παίρνουν γύρω στο ένα λεπτό ενώ μεγαλύτεροι χάρτες με όλα τα δεδομένα μπορούν να πάρουν 10-15 λεπτά ή και περισσότερο.
# 

# In[ ]:


n_rows, n_columns = 20, 20
som = somoclu.Somoclu(n_columns, n_rows, compactsupport=False, initialization="pca", maptype="toroid")
get_ipython().run_line_magic('time', 'som.train(final_set, epochs=100)')


# ***
# ### Σχόλια
# ***
# Ξεκινήσαμε με 10x10 map και ανεβήκαμε μέχρι 25x25 παρατηρώντας τα αποτελέσματα και τη βελτίωση, αλλά βέβαια και το χρόνο εκπαίδευσης ο οποίος αυξανόταν σημαντικά. Θεωρήσαμε ότι δεν υπάρχει σημαντική βελτίωση μετά το 20x20 οπότε κρατήσαμε αυτή τη τιμή, ως ένα ικανοποιητικό σημείο τόσο για την ακρίβεια όσο και για το χρόνο εκτέλεσης. 
# Όλες οι δοκιμές έγιναν αρχικά για 1000-2000 δείγματα μέχρι να καταλήξουμε σε ιδανικές παραμέτρους και να τις εφαρμόσουμε στο σύνολο του dataset μας. Φυσικά, δείχνουμε στο output του notebook την τελική εκτέλεση για όλο το dataset. 
# Χρησιμοποιούμε 100 epochs, αυξάνοντας σταδιακά από τα 10 που έδινε το reference του Somoclu. Επίσης, εφαρμόσαμε PCA initialization ώστε να "βοηθήσουμε" το SOM να ξεκινήσει από μια εκτίμηση και να συγκλίνει γρηγορότερα. Συγκεκριμένα, αρχικοποιούμε με  διανύσματα από τον υποχώρο που δίνουν οι δύο πρώτες ιδιοτιμές του πίνακα συσχέτισης. 
# Επίσης, αντί για το default planar του Somoclu, βάζουμε toroid map καθώς βλέπουμε ότι έτσι οι γωνίες του χάρτη ενώνονται με την άλλη μεριά του. Επίσης, πειραματιστήκαμε και με το hexagonal αλλά τα αποτελέσματα δεν ήταν ικανοποιητικά, οπότε κρατήσαμε το toroid.
# 
# ***

# 
# ## Best matching units
# 
# Μετά από κάθε εκπαίδευση αποθηκεύστε σε μια μεταβλητή τα best matching units (bmus) για κάθε ταινία. Τα bmus μας δείχνουν σε ποιο νευρώνα ανήκει η κάθε ταινία. Προσοχή: η σύμβαση των συντεταγμένων των νευρώνων είναι (στήλη, γραμμή) δηλαδή το ανάποδο από την Python. Με χρήση της [np.unique](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.unique.html) (μια πολύ χρήσιμη συνάρτηση στην άσκηση) αποθηκεύστε τα μοναδικά best matching units και τους δείκτες τους (indices) προς τις ταινίες. Σημειώστε ότι μπορεί να έχετε λιγότερα μοναδικά bmus από αριθμό νευρώνων γιατί μπορεί σε κάποιους νευρώνες να μην έχουν ανατεθεί ταινίες. Ως αριθμό νευρώνα θα θεωρήσουμε τον αριθμό γραμμής στον πίνακα μοναδικών bmus.
# 

# In[19]:


bmus = som.bmus
print(bmus.shape)
ubmus, indices = np.unique(bmus, return_inverse=True, axis=0)
print(ubmus.shape)
print(indices)


# 
# ## Ομαδοποίηση (clustering)
# 
# Τυπικά, η ομαδοποίηση σε ένα χάρτη SOM προκύπτει από το unified distance matrix (U-matrix): για κάθε κόμβο υπολογίζεται η μέση απόστασή του από τους γειτονικούς κόμβους. Εάν χρησιμοποιηθεί μπλε χρώμα στις περιοχές του χάρτη όπου η τιμή αυτή είναι χαμηλή (μικρή απόσταση) και κόκκινο εκεί που η τιμή είναι υψηλή (μεγάλη απόσταση), τότε μπορούμε να πούμε ότι οι μπλε περιοχές αποτελούν clusters και οι κόκκινες αποτελούν σύνορα μεταξύ clusters.
# 
# To somoclu δίνει την επιπρόσθετη δυνατότητα να κάνουμε ομαδοποίηση των νευρώνων χρησιμοποιώντας οποιονδήποτε αλγόριθμο ομαδοποίησης του scikit-learn. Στην άσκηση θα χρησιμοποιήσουμε τον k-Means. Για τον αρχικό σας χάρτη δοκιμάστε ένα k=20 ή 25. Οι δύο προσεγγίσεις ομαδοποίησης είναι διαφορετικές, οπότε περιμένουμε τα αποτελέσματα να είναι κοντά αλλά όχι τα ίδια.
# 

# In[20]:


from sklearn.cluster import KMeans
algorithm = KMeans(20)
som.cluster(algorithm=algorithm)


# 
# ## Αποθήκευση του SOM
# 
# Επειδή η αρχικοποίηση του SOM γίνεται τυχαία και το clustering είναι και αυτό στοχαστική διαδικασία, οι θέσεις και οι ετικέτες των νευρώνων και των clusters θα είναι διαφορετικές κάθε φορά που τρέχετε τον χάρτη, ακόμα και με τις ίδιες παραμέτρους. Για να αποθηκεύσετε ένα συγκεκριμένο som και clustering χρησιμοποιήστε και πάλι την `joblib`. Μετά την ανάκληση ενός SOM θυμηθείτε να ακολουθήσετε τη διαδικασία για τα bmus.
# 

# In[ ]:


from sklearn.externals import joblib
joblib.dump(som, 'som.pkl') 


# In[18]:


som = joblib.load('som.pkl')
bmus = som.bmus
ubmus, indices = np.unique(bmus, return_inverse=True, axis=0)


# 
# ## Οπτικοποίηση U-matrix, clustering και μέγεθος clusters
# 
# Για την εκτύπωση του U-matrix χρησιμοποιήστε τη `view_umatrix` με ορίσματα `bestmatches=True` και `figsize=(15, 15)` ή `figsize=(20, 20)`. Τα διαφορετικά χρώματα που εμφανίζονται στους κόμβους αντιπροσωπεύουν τα διαφορετικά clusters που προκύπτουν από τον k-Means. Μπορείτε να εμφανίσετε τη λεζάντα του U-matrix με το όρισμα `colorbar`. Μην τυπώνετε τις ετικέτες (labels) των δειγμάτων, είναι πολύ μεγάλος ο αριθμός τους.
# 
# Για μια δεύτερη πιο ξεκάθαρη οπτικοποίηση του clustering τυπώστε απευθείας τη μεταβλητή `clusters`.
# 
# Τέλος, χρησιμοποιώντας πάλι την `np.unique` (με διαφορετικό όρισμα) και την `np.argsort` (υπάρχουν και άλλοι τρόποι υλοποίησης) εκτυπώστε τις ετικέτες των clusters (αριθμοί από 0 έως k-1) και τον αριθμό των νευρώνων σε κάθε cluster, με φθίνουσα ή αύξουσα σειρά ως προς τον αριθμό των νευρώνων. Ουσιαστικά είναι ένα εργαλείο για να βρίσκετε εύκολα τα μεγάλα και μικρά clusters. 
# 
# Ακολουθεί ένα μη βελτιστοποιημένο παράδειγμα για τις τρεις προηγούμενες εξόδους:
# 
# <img src="https://image.ibb.co/i0tsfR/umatrix_s.jpg" width="35%">
# <img src="https://image.ibb.co/nLgHEm/clusters.png" width="35%">
# 
# 

# In[21]:


som.view_umatrix(bestmatches=True, colorbar=True, figsize=(20, 20))


# In[22]:


print(som.clusters)


# In[23]:


import collections

l = som.clusters.flatten().tolist()
cnt = collections.Counter(l)
sl = sorted(l, key=cnt.get,reverse=True)
scnt = collections.Counter(sl)
print(list(scnt.keys()))
print(list(scnt.values()))


# 
# ## Σημασιολογική ερμηνεία των clusters
# 
# Προκειμένου να μελετήσουμε τις τοπολογικές ιδιότητες του SOM και το αν έχουν ενσωματώσει σημασιολογική πληροφορία για τις ταινίες διαμέσου της διανυσματικής αναπαράστασης με το tf-idf και των κατηγοριών, χρειαζόμαστε ένα κριτήριο ποιοτικής επισκόπησης των clusters. Θα υλοποιήσουμε το εξής κριτήριο: Λαμβάνουμε όρισμα έναν αριθμό (ετικέτα) cluster. Για το cluster αυτό βρίσκουμε όλους τους νευρώνες που του έχουν ανατεθεί από τον k-Means. Για όλους τους νευρώνες αυτούς βρίσκουμε όλες τις ταινίες που τους έχουν ανατεθεί (για τις οποίες αποτελούν bmus). Για όλες αυτές τις ταινίες τυπώνουμε ταξινομημένη τη συνολική στατιστική όλων των ειδών (κατηγοριών) και τις συχνότητές τους. Αν το cluster διαθέτει καλή συνοχή και εξειδίκευση, θα πρέπει κάποιες κατηγορίες να έχουν σαφώς μεγαλύτερη συχνότητα από τις υπόλοιπες. Θα μπορούμε τότε να αναθέσουμε αυτήν/ές την/τις κατηγορία/ες ως ετικέτες κινηματογραφικού είδους στο cluster.
# 
# Μπορείτε να υλοποιήσετε τη συνάρτηση αυτή όπως θέλετε. Μια πιθανή διαδικασία θα μπορούσε να είναι η ακόλουθη:
# 
# 1. Ορίζουμε συνάρτηση `print_categories_stats` που δέχεται ως είσοδο λίστα με ids ταινιών. Δημιουργούμε μια κενή λίστα συνολικών κατηγοριών. Στη συνέχεια, για κάθε ταινία επεξεργαζόμαστε το string `categories` ως εξής: δημιουργούμε μια λίστα διαχωρίζοντας το string κατάλληλα με την `split` και αφαιρούμε τα whitespaces μεταξύ ετικετών με την `strip`. Προσθέτουμε τη λίστα αυτή στη συνολική λίστα κατηγοριών με την `extend`. Τέλος χρησιμοποιούμε πάλι την `np.unique` για να μετρήσουμε συχνότητα μοναδικών ετικετών κατηγοριών και ταξινομούμε με την `np.argsort`. Τυπώνουμε τις κατηγορίες και τις συχνότητες εμφάνισης ταξινομημένα. Χρήσιμες μπορεί να σας φανούν και οι `np.ravel`, `np.nditer`, `np.array2string` και `zip`.
# 
# 2. Ορίζουμε τη βασική μας συνάρτηση `print_cluster_neurons_movies_report` που δέχεται ως όρισμα τον αριθμό ενός cluster. Με τη χρήση της `np.where` μπορούμε να βρούμε τις συντεταγμένες των bmus που αντιστοιχούν στο cluster και με την `column_stack` να φτιάξουμε έναν πίνακα bmus για το cluster. Προσοχή στη σειρά (στήλη - σειρά) στον πίνακα bmus. Για κάθε bmu αυτού του πίνακα ελέγχουμε αν υπάρχει στον πίνακα μοναδικών bmus που έχουμε υπολογίσει στην αρχή συνολικά και αν ναι προσθέτουμε το αντίστοιχο index του νευρώνα σε μια λίστα. Χρήσιμες μπορεί να είναι και οι `np.rollaxis`, `np.append`, `np.asscalar`. Επίσης πιθανώς να πρέπει να υλοποιήσετε ένα κριτήριο ομοιότητας μεταξύ ενός bmu και ενός μοναδικού bmu από τον αρχικό πίνακα bmus.
# 
# 3. Υλοποιούμε μια βοηθητική συνάρτηση `neuron_movies_report`. Λαμβάνει ένα σύνολο νευρώνων από την `print_cluster_neurons_movies_report` και μέσω της `indices` φτιάχνει μια λίστα με το σύνολο ταινιών που ανήκουν σε αυτούς τους νευρώνες. Στο τέλος καλεί με αυτή τη λίστα την `print_categories_stats` που τυπώνει τις στατιστικές των κατηγοριών.
# 
# Μπορείτε βέβαια να προσθέσετε οποιαδήποτε επιπλέον έξοδο σας βοηθάει. Μια χρήσιμη έξοδος είναι πόσοι νευρώνες ανήκουν στο cluster και σε πόσους και ποιους από αυτούς έχουν ανατεθεί ταινίες.
# 
# Θα επιτελούμε τη σημασιολογική ερμηνεία του χάρτη καλώντας την `print_cluster_neurons_movies_report` με τον αριθμός ενός cluster που μας ενδιαφέρει. 
# 
# Παράδειγμα εξόδου για ένα cluster (μη βελτιστοποιημένος χάρτης, ωστόσο βλέπετε ότι οι μεγάλες κατηγορίες έχουν σημασιολογική  συνάφεια):
# 
# ```
# Overall Cluster Genres stats:  
# [('"Horror"', 86), ('"Science Fiction"', 24), ('"B-movie"', 16), ('"Monster movie"', 10), ('"Creature Film"', 10), ('"Indie"', 9), ('"Zombie Film"', 9), ('"Slasher"', 8), ('"World cinema"', 8), ('"Sci-Fi Horror"', 7), ('"Natural horror films"', 6), ('"Supernatural"', 6), ('"Thriller"', 6), ('"Cult"', 5), ('"Black-and-white"', 5), ('"Japanese Movies"', 4), ('"Short Film"', 3), ('"Drama"', 3), ('"Psychological thriller"', 3), ('"Crime Fiction"', 3), ('"Monster"', 3), ('"Comedy"', 2), ('"Western"', 2), ('"Horror Comedy"', 2), ('"Archaeology"', 2), ('"Alien Film"', 2), ('"Teen"', 2), ('"Mystery"', 2), ('"Adventure"', 2), ('"Comedy film"', 2), ('"Combat Films"', 1), ('"Chinese Movies"', 1), ('"Action/Adventure"', 1), ('"Gothic Film"', 1), ('"Costume drama"', 1), ('"Disaster"', 1), ('"Docudrama"', 1), ('"Film adaptation"', 1), ('"Film noir"', 1), ('"Parody"', 1), ('"Period piece"', 1), ('"Action"', 1)]```
#    

# In[24]:


def print_categories_stats(id_list):
    genres = []
    for iid in id_list:
        cat = categories[iid][0].replace('"','')
        cat = cat.split(',')
        cat = [c.strip(" ") for c in cat]
        genres.extend(cat)
    cnt = collections.Counter(genres)
    sgenres = sorted(genres, key=cnt.get,reverse=True)
    scnt = collections.Counter(sgenres)
    print (list(zip(list(scnt.keys()),list(scnt.values()))))
        
        
def print_cluster_neurons_movies_report(cluster):
    neurons = []
    where = np.where(cluster == som.clusters)
    bmus = np.column_stack(where)
    bmus = np.flip(bmus,axis=1)
    for bmu in bmus:
        for idx,ubmu in enumerate(ubmus):
            if(np.array_equal(bmu,ubmu)):
                neurons.append(idx)
    neuron_movies_report(neurons)

def neuron_movies_report(neurons):
    movies = []
    for neuron in neurons:
        where = np.where(neuron == indices)[0].tolist()
        movies.extend(where)
    print_categories_stats(movies)


# In[25]:


for i in range(20):
    print_cluster_neurons_movies_report(i)
    print()


# ***
# ### Σχόλια
# Υλοποιήσαμε αυτό το βήμα όπως προτείνεται από την εκφώνηση (ταξινομούμε με την sorted αντί της np.unique - np.argsort).
# Ελέγχουμε αν κάθε bmu στο cluster αντιστοιχεί σε ενα μοναδικό bmu (δηλαδή βρίσκεται στον πίνακα ubmu που έχουμε πάρει με την np.unique). Με αυτή τη διαδικασία βλέπουμε ότι υπάρχει κατανομή στη συχνότητα εμφάνισης κάθε κατηγορίας (άρα το cluster μας έχει ικανοποιητική ακρίβεια). 
# ***

# 
# ## Tips για το SOM και το clustering
# 
# - Για την ομαδοποίηση ένα U-matrix καλό είναι να εμφανίζει και μπλε-πράσινες περιοχές (clusters) και κόκκινες περιοχές (ορίων). Παρατηρήστε ποια σχέση υπάρχει μεταξύ αριθμού ταινιών στο final set, μεγέθους grid και ποιότητας U-matrix.
# - Για το k του k-Means προσπαθήστε να προσεγγίζει σχετικά τα clusters του U-matrix (όπως είπαμε είναι διαφορετικοί μέθοδοι clustering). Μικρός αριθμός k δεν θα σέβεται τα όρια. Μεγάλος αριθμός θα δημιουργεί υπο-clusters εντός των clusters που φαίνονται στο U-matrix. Το τελευταίο δεν είναι απαραίτητα κακό, αλλά μεγαλώνει τον αριθμό clusters που πρέπει να αναλυθούν σημασιολογικά.
# - Σε μικρούς χάρτες και με μικρά final sets δοκιμάστε διαφορετικές παραμέτρους για την εκπαίδευση του SOM. Σημειώστε τυχόν παραμέτρους που επηρεάζουν την ποιότητα του clustering για το dataset σας ώστε να τις εφαρμόσετε στους μεγάλους χάρτες.
# - Κάποια τοπολογικά χαρακτηριστικά εμφανίζονται ήδη σε μικρούς χάρτες. Κάποια άλλα χρειάζονται μεγαλύτερους χάρτες. Δοκιμάστε μεγέθη 20x20, 25x25 ή και 30x30 και αντίστοιχη προσαρμογή των k. Όσο μεγαλώνουν οι χάρτες, μεγαλώνει η ανάλυση του χάρτη αλλά μεγαλώνει και ο αριθμός clusters που πρέπει να αναλυθούν.
# 

# ***
# ### Σχόλια
#  - Το U-matrix μας δείχνει το πλέγμα του SOM και το χρωματίζει ανάλογα το πόσο απέχουν οι νευρώνες εξόδου μεταξύ τους. Οι κόκκινες περιοχές δείχνουν περιοχές με μεγάλες αποστάσεις και οι μπλε περιοχές δείχνουν περιοχές με μικρές αποστάσεις. Στο U-matrix που σχηματίστηκε βλέπουμε ότι υπάρχει μια μπλε περιοχή και αρκετές πράσινες, αλλά υπάρχει και κόκκινη περιοχή, με κάποιες ενδιάμεσες (πορτοκαλί). Όσο μεγαλύτερο είναι το grid τόσο πιο αναλυτική είναι η πληροφορία που παίρνουμε.
#      
# 
#  - Για τον k-means δοκιμάζουμε διάφορες τιμές για τον αριθμό των clusters. Ανάμεσα στις τιμές 20 και 25 που προτάθηκαν από την εκφώνηση, κρατήσαμε την τιμή 20. Για k=25, αλλά και μεγαλύτερα, είδαμε ότι παίρνουμε πάρα πολλά είδη και από πολύ νωρίς παρατηρούμε διάσπαση, δηλαδή εμφανίζονται πάρα πολλές κατηγορίες ταινιών (μετά τις 10-15 πρώτες περίπου) που δεν διαφέρουν τόσο ουσιαστικά. Θεωρούμε πως αυτό έχει να κάνει με το dataset μας, αφού έχουμε πάρα πολλές ταινίες κατηγορίας Drama και όχι τόσο μεγάλη ποικιλία. Ενδεικτικά δίνουμε μια εκτέλεση που έγινε (για 20x20 map, kmeans k=25 clusters). Είναι σαφώς πιο αναλυτική αναπαράσταση του συνόλου, αλλά όχι τόσο πρακτική ώστε να μπορέσουμε να αναλύσουμε τα clusters σαν κατηγορίες. Να πούμε επίσης σε αυτό το σημείο ότι δεν χωρίσαμε τα δεδομένα σε παραπάνω από 20 κατηγορίες αφού ο U-matrix δείχνει πως μια διαμέριση σε περίπου τόσες κατηγορίες ανταποκρίνεται στη φύση του προβλήματος
# 
#         [('Drama', 185), ('World cinema', 23), ('Crime Fiction', 17), ('War film', 9), ('Indie', 9), ('Action/Adventure', 8), ('Family Film', 8), ('Chinese Movies', 7), ('Family Drama', 7), ('Television movie', 6), ('Horror', 5), ('Comedy film', 5), ('Musical', 5), ('Film adaptation', 4), ('Political drama', 4), ('Biographical film', 4), ('Melodrama', 3), ('Docudrama', 3), ('Short Film', 3), ('Period piece', 3), ('Epic', 3), ('Romantic drama', 3), ('Crime Drama', 3), ('Coming of age', 3), ('Documentary', 3), ('Historical drama', 3), ('Ensemble Film', 3), ('Silent film', 3), ('Adventure', 3), ("Children's/Family", 3), ('Mystery', 2), ('Creature Film', 2), ('Medical fiction', 2), ('Art film', 2), ('Tamil cinema', 2), ('Historical Epic', 2), ('Tollywood', 2), ('Juvenile Delinquency Film', 2), ('Biography', 2), ('Courtroom Drama', 2), ('Fantasy', 2), ('History', 2), ('Teen', 2), ('Western', 2), ('Action', 2), ('Marriage Drama', 2), ('Film noir', 1), ('Tragedy', 1), ('Sports', 1), ('Addiction Drama', 1), ('Historical fiction', 1), ('Filipino', 1), ('Existentialism', 1), ('Filipino Movies', 1), ('Childhood Drama', 1), ('Zombie Film', 1), ('Japanese Movies', 1), ('Music', 1), ('Slice of life story', 1), ('Christian film', 1), ('Psychological thriller', 1), ('Erotic Drama', 1), ('Gangster Film', 1), ('Biopic [feature]', 1), ('Crime Thriller', 1), ('Kitchen sink realism', 1), ('Dance', 1), ('Musical Drama', 1), ('British New Wave', 1), ('Propaganda film', 1), ('Road movie', 1), ('New Hollywood', 1), ('Revisionist Western', 1), ('Comedy-drama', 1), ('Domestic Comedy', 1), ('Escape Film', 1), ('Hagiography', 1), ("Children's", 1), ('Animation', 1), ('Holiday Film', 1), ('Christmas movie', 1), ('Punk rock', 1)]
# 
#  - Αναλύσαμε τη διαδιασία αυτή και σε προηγούμενο κελί σχολίων (συγκεκριμένα στο στάδιο της εκπαίδευσης όπου επιλέξαμε τις παραμέτρους). Από τη διαδικασία πειραματισμού σε ένα subset εξάγουμε το βέλτιστο μοντέλο εκπαίδευσης του SOM το οποίο εφαρμόσαμε. Καταλήξαμε στις τιμές:
#        -- 20x20 map
#        -- 100 epochs
#        -- PCA initialisation
#        -- toroid
# 
#  - Όπως έχει γίνει κατανοητό και σε προηγούμενα σημεία που σχολιάσαμε, πολύ μεγάλο μέγεθος χάρτη μας δίνει καλύτερη ανάλυση αλλά υπάρχουν σημαντικά μειονεκτήματα. Αρχικά ο χρόνος που απαιτείται για την εκπαίδευση αυξάνεται σημαντικά, σε σημείο που δεν είναι πια πρακτικός για το σύστημα μας. Επιπλέον, η πληροφορία που παίρνουμε για μεγαλύτερους χάρτες, όπως είπαμε προηγουμένως και για τον αριθμό των clusters στον KMeans, δεν είναι απαραίτητα επιθυμητή καθώς μπορεί να οδηγεί σε πολλά clusters που σημασιολογικά δεν είναι εύκολο να αναλυθούν (η κατηγοριοποίηση παύει να είναι ακριβής σε ωφέλιμο βαθμό και σχεδόν εκφυλίζεται στο σημείο που κάθε στοιχείο είναι μια κατηγορία, όπως είδαμε στο output του προηγούμενου βήματος).
# ***

# 
# 
# ## Ανάλυση τοπολογικών ιδιοτήτων χάρτη SOM
# 
# Μετά το πέρας της εκπαίδευσης και του clustering θα έχετε ένα χάρτη με τοπολογικές ιδιότητες ως προς τα είδη των ταίνιών της συλλογής σας, κάτι αντίστοιχο με την εικόνα στην αρχή της Εφαρμογής 2 αυτού του notebook (η συγκεκριμένη εικόνα είναι μόνο για εικονογράφιση, δεν έχει καμία σχέση με τη συλλογή δεδομένων και τις κατηγορίες μας).
# 
# Για τον τελικό χάρτη SOM που θα παράξετε για τη συλλογή σας, αναλύστε σε markdown με συγκεκριμένη αναφορά σε αριθμούς clusters και τη σημασιολογική ερμηνεία τους τις εξής τρεις τοπολογικές ιδιότητες του SOM: 
# 
# 1. Δεδομένα που έχουν μεγαλύτερη πυκνότητα πιθανότητας στο χώρο εισόδου τείνουν να απεικονίζονται με περισσότερους νευρώνες στο χώρο μειωμένης διαστατικότητας. Δώστε παραδείγματα από συχνές και λιγότερο συχνές κατηγορίες ταινιών. Χρησιμοποιήστε τις στατιστικές των κατηγοριών στη συλλογή σας και τον αριθμό κόμβων που χαρακτηρίζουν.
# 2. Μακρινά πρότυπα εισόδου τείνουν να απεικονίζονται απομακρυσμένα στο χάρτη. Υπάρχουν χαρακτηριστικές κατηγορίες ταινιών που ήδη από μικρούς χάρτες τείνουν να τοποθετούνται σε διαφορετικά ή απομονωμένα σημεία του χάρτη.
# 3. Κοντινά πρότυπα εισόδου τείνουν να απεικονίζονται κοντά στο χάρτη. Σε μεγάλους χάρτες εντοπίστε είδη ταινιών και κοντινά τους υποείδη.
# 
# Προφανώς τοποθέτηση σε 2 διαστάσεις που να σέβεται μια απόλυτη τοπολογία δεν είναι εφικτή, αφενός γιατί δεν υπάρχει κάποια απόλυτη εξ ορισμού για τα κινηματογραφικά είδη ακόμα και σε πολλές διαστάσεις, αφετέρου γιατί πραγματοποιούμε μείωση διαστατικότητας.
# 
# Εντοπίστε μεγάλα clusters και μικρά clusters που δεν έχουν σαφή χαρακτηριστικά. Εντοπίστε clusters συγκεκριμένων ειδών που μοιάζουν να μην έχουν τοπολογική συνάφεια με γύρω περιοχές. Προτείνετε πιθανές ερμηνείες.
# 
# 
# 
# Τέλος, εντοπίστε clusters που έχουν κατά την άποψή σας ιδιαίτερο ενδιαφέρον στη συλλογή της ομάδας σας (data exploration / discovery value) και σχολιάστε.
# 

# *** 
# ### Σχόλια
# 
# Αρχικά, από το output αντιγράφουμε τα clusters με τις ετικέτες τους και τον αριθμό των νευρώνων με τους οποίους εμφανίζονται, σε φθίνουσα σειρά. Έπειτα, τα clusters του som. Έτσι μπορούμε να δούμε καλύτερα συγκριτικά τα δεδομένα καθώς σχολιάζουμε.
# 
#     [3, 9, 4, 10, 8, 2, 13, 1, 11, 16, 15, 6, 12, 18, 5, 17, 0, 19, 7, 14]
#     [56, 38, 36, 24, 22, 21, 19, 19, 19, 19, 16, 16, 16, 14, 13, 12, 12, 11, 10, 7]
# 
#      [ 8 13 13 13 13 18  1  1  1  4  4 11 15 11 15 15  5  5  5  8]
#      [ 8  8 13 13  4 18  4  4  4  4  4  4 11 11 11 11  5  5  5  8]
#      [ 8  8  8 18 18 18 18  4  4  4  4  4 11 11 11 11 11  8  8  8]
#      [ 8  8  8 18 18 18 18  4  4  4  4  4  4 11 11 11 11  8  8  8]
#      [ 8  8 18 18 18  7  4  4  4  4  4  4  4 16 11 11 11  8  8  8]
#      [ 9  9 18  7  7  7 17 17  4 19 19 19 16 16 16 11 14 14  9  9]
#      [ 9  9  9  7  7  7 17 17 19 19 19 19 19 16 16 16 14 14  9  9]
#      [ 9  9  9  7  7  7 17 17 17 19 19 19 16 16 16 16 14 14  9  9]
#      [ 9  9  9  9  9 17 17 17 17  0  0  0 16 16 16 16 14  9  9  9]
#      [ 9  9  9  9  9  9 17  4  0  0  0  0 16 16 16 16  9  9  9  9]
#      [ 9  6  6  6  6  4  4  4  0  0  0  0  3  3  3  3  9  9  9  9]
#      [ 6  6  6  6  4  4  4  3  3  3  0  3  3  3  3  3  2  9  2  2]
#      [ 2  6  6  6  6  4  3  3  3  3  3  3  3  3  3  3  2  2  2  2]
#      [ 2  6  6  6 10  3  3  3  3  3  3  3  3  3  3  3  2  2  2  2]
#      [ 2  6 10 10 10 10  3  3  3  3  3  3  3  3  3 12 12  2  2  2]
#      [ 2 10 10 10 10 10 10 10  3  3  3  3  3  3 12 12 12 12  2  2]
#      [ 2  3 10 10 10 10 10 10  1  3  3  3  3  3 12 12 12 12 12 12]
#      [13 13 13 10 10 10 10  1  1  1  1  3 15 15 15 12 12 12  5 12]
#      [13 13 13 13 13 10 10  1  1  1  1  1 15 15 15 15 15  5  5  5]
#      [13 13 13 13 13  3  1  1  1  1  1  1 15 15 15 15 15  5  5  5]
#      
#      
#  1. Από τον πίνακα με τους νευρώνες βλέπουμε ότι περισσότερους έχει το cluster 3, ακολουθεί το 9, το 4 κλπ. Από τα cluster_neurons_movies_report βλέπουμε ότι το 
#          - cluster 3  ξεκινάει με ('Drama', 903), ('Romance Film', 120), 
#          - το 9 με ('Comedy', 486), ('Black-and-white', 101), 
#          - το 4 με ('Comedy film', 86), ('Romance Film', 66). 
#     Άρα, βλέπουμε ότι τα Drama, Comedy, Romance, που είναι πολύ συχνές κατηγορίες, με μεγάλο πλήθος ταινιών, έχουν και τους περισσότερους νευρώνες. Όσον αφορά τα clusters με τους λιγότερους νευρώνες, δηλαδή το 7 και 14, βλέπουμε
#          -  ('Family Film', 101), ('Animation', 100), ('Short Film', 95), ('Comedy', 67), ('Comedy film', 24), ('Black-and-white', 14), ('Musical', 6), ("Children's/Family", 6), ('Fantasy', 4), ("Children's", 3) 
#          - ('Action', 174), ('Drama', 140), ('Adventure', 124), ('Action/Adventure', 81), ('War film', 43), ('Romance Film', 31)
#          
#          
#          
# 2. Ένα παράδειγμα είναι τα clusters 10 και 11. Στο χάρτη βλέπουμε το 10 κάτω αριστερά, ενώ το 11 πάνω δεξιά, είναι δηλαδή εντελώς απομακρυσμένα. Πράγματι, βλέποντας τις κατηγορίες ταινιών σε αυτά τα clusters είναι 
#         - cluster 10 ('Drama', 283), ('Romance Film', 282), ('Romantic drama', 269), ('World cinema', 134), ('Comedy', 59), ('Period piece', 47), ('Romantic comedy', 46),
#         - cluster 11 ('Thriller', 195), ('Horror', 84), ('Psychological thriller', 41), ('Mystery', 30), ('Science Fiction', 30), ('Crime Thriller', 25),
#    Πρόκειται δηλαδή για κατηγορίες που είναι πολύ διαφορετικές (Romance - Horror) και είναι αναμενόμενο τοπολογικά να είναι απομακρισμένες. Ένα ακόμη παράδειγμα ειναι το 5 που βρίσκεται κάτω δεξιά, πάνω δεξιά με το 7 που βρίσκεται στη μέση και προς τα πάνω αριστερά, όπου 
#        - cluster 5 ('Action', 129), ('Thriller', 128), ('Action/Adventure', 105), ('Crime Fiction', 95), 
#        - cluster 7 ('Family Film', 101), ('Animation', 100), ('Short Film', 95), ('Comedy', 67), ('Comedy film', 24), ('Black-and-white', 14), ('Musical', 6), ("Children's/Family", 6)
#    Είναι προφανές ότι οι ταινίες θρίλερ-δράσεις είναι πολύ μακριά σημασιολογικά-θεματολογικά από παιδικές ταινίες κινουμένων σχεδίων-κωμωδίες.
# 
# 
# 3. Θα εξετάσουμε το cluster 12 που βρίσκεται κάτω δεξιά. Βλέπουμε ότι έχει σύνορα με 3, 2, 5, 15.
#         - cluster 12 ('Crime Fiction', 160), ('Drama', 158), ('Thriller', 45), ('Indie', 33), ('Action', 29), ('Crime Drama', 28), ('Black-and-white', 25), ('Film noir', 21)
#         
#         
#         - cluster 3 ('Drama', 903), ('Romance Film', 120), ('Black-and-white', 64), ('War film', 57), ('Indie', 51)
#         - cluster 15 ('Thriller', 202), ('Drama', 171), ('Mystery', 115), ('Crime Thriller', 88), ('Crime Fiction', 74), ('Psychological thriller', 64), ('Horror', 34), ('Suspense', 32)
#         - cluster 2 ('Drama', 212), ('Comedy', 210), ('Comedy-drama', 55), ('Indie', 52), ('Romance Film', 43), ('Black comedy', 30), ('World cinema', 21),
#         - cluster 5('Action', 129), ('Thriller', 128), ('Action/Adventure', 105), ('Crime Fiction', 95), ('Drama', 55), ('Crime Thriller', 34), ('Action Thrillers', 34),
#         
# Με το 3 υπάρχει κοινό το Drama, Black-and-White, με το 15 το Thriller, Crime, με το 2 το Drama, με το 5 το Thriller, Drama, Action κλπ. Αν εξετάσουμε όλες τις γειτνιάσεις στο χάρτη θα βρούμε κοινές κατηγορίες ταινιών. Φυσικά, αυτό δεν είναι απόλυτο για τους λόγους που εξηγεί η εκφώνηση ως προς την κατηγοριοποίηση των ταινιών, αλλά όπως είδαμε από τα παραδείγματα που παρουσιάσαμε, υπάρχει μια ικανοποιητικά καλή προσέγγιση από το χάρτη.       
# 
# Το cluster 0, που είναι σχετικά μικρό όπως βλέπουμε από τον αριθμό των νευρώνων που έχει (12), 
# έχει τα είδη ('Silent film', 105), ('Black-and-white', 94), ('Drama', 44), ('Indie', 35), αλλά ενώ συνορεύει με το 19, βλέπουμε ότι οι κατηγορίες ταινιών δεν έχουν κάποια εμφανή συνάφεια ('Family Film', 119), ('Adventure', 108), ('Fantasy', 77), ('Animation', 62), ("Children's/Family", 56). Παρατηρούμε επίσης ότι το cluster 19 είναι επίσης ένα cluster με μικρό αριθμό νευρώνων (11). Η έλλειψη συνάφειας μεταξύ τους πιθανά να οφείλεται στη μικρότερη πυκνότητα πιθανότητας που έχουν εξ αρχής στο χώρο εισόδου τα δύο συγκεκριμένα clusters.
# 
# Για τον τοπολογικό μας χάρτη έχει ιδιαίτερο ενδιαφέρον το cluster 9 το οποίο είναι στα δεξιά και τα αριστερά του χάρτη, με το οποίο βλέπουμε πως ο toroid map που εφαρμόσαμε έχει "ενώσει" τις άκρες. 
# ***