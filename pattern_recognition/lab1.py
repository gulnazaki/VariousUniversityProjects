#!/usr/bin/env python
# coding: utf-8


# ## Step 1

# Import numpy and matplotlib.

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# Read train and test files from given material and convert to numpy arrays with numpy.loadtxt
# The data files should be in the path given in the c variable. For a different path (c) should be altered.

# In[2]:


c = 'pr_lab1_2016-17_data/train.txt'
train_data = np.loadtxt(c)
#print(train_data)


# In[3]:


c = 'pr_lab1_2016-17_data/test.txt'
test_data = np.loadtxt(c)
#print(test_data)


# Each row has the target in the first column (target)
# and the characteristics in the following 256 columns (features).
# y_test and y_train are 1-d np arrays (n_samples x1)
# X_test and X_train are (n_samples x n_features)

# In[4]:


y_train = train_data[:,0]
X_train = train_data[:,1:]

y_test = test_data[:,0]
X_test = test_data[:,1:]

#print(y_train)
#print(X_train)


# ## Step 2

# Keep digit from line 131. Reshape from 256 to 16x16 and plot.

# In[5]:


n = X_train[131,:]
n131 = np.reshape(n, (16,16))
#print(n)
#print(np.shape(n))

plt.imshow(n131)


# ## Step 3

# Plot a random sample from each label (digit). 
# We use an array ("seen") with 10 samples (initialised to 0), corresponding to the 10 digits (0-9). We keep the values that have already been found (setting value to 1 for each found digit).
# We iterate in y_train array and keep the index of the digit (its index in the X array) and the number it represents (0-9). idx is used to look up the digit in X and num to plot in ascending order.
# We plot in the same figure with add_subplot.
# Each subplot is 16x16.

# In[6]:


seen = np.zeros(10)
fig = plt.figure(figsize=(20,20))
for idx,num in enumerate(y_train):
    if not seen[int(num)]:
        x = fig.add_subplot(16,16,int(num)+1)
        n = X_train[idx,:]
        n = np.reshape(n, (16,16))
        x.imshow(n)
        seen[int(num)] = 1


# ## Step 4

# Compute mean of features for pixel (10,10) of digit 0.
# For each "0" found, store pixel (10,10) in list. Pixel (10,10) is equal to index 170, because features are stored in (n) x 256 form. 
# Mean value is computed with numpy.mean function. 

# In[7]:


lis = []

for idx,num in enumerate(y_train):
    if int(num)==0:
        lis.append(X_train[idx,170])

arr = np.array(lis)
mean = np.mean(arr)  
print(mean)


# 
# ## Step 5

# Variance is computed with numpy.var function.

# In[8]:


var = np.var(arr)
print(var)


# ## Step 6

# Compute mean value and variance of "0" digit. 
# For each "0", we now store all the pixels in list. When list is complete, we transform to numpy array. Mean and var are computed with argument -axis=0, because each column represents a pixel. 

# In[9]:


lis = []

for idx,num in enumerate(y_train):
    if int(num)==0:
        lis.append(X_train[idx,:])

arr = np.array(lis)

mean = np.mean(arr, axis=0)  
mean = np.reshape(mean, (16,16))

var = np.var(arr, axis=0)
var = np.reshape(var, (16,16))


# ## Step 7

# Show digit "0" with mean values. 

# In[10]:


plt.imshow(mean)


# ## Step 8

# Show digit "0" with variance.
# Unlike the mean value image, we have higher variance values on the inner and outer surface of the "0". This is expected as the inner and outer borders represent the pixels which are most likely to vary amongst different representations, while the "core" is roughly the same in every image.

# In[11]:


plt.imshow(var)


# ## Step 9

# We compute the mean and variance for all digits. 
# We create a list of 10 lists ("lis"), one list for each digit, where the features are stored. meanlist and varlist are 10x256 respectively, and each 1x256 vector has the mean and variance values for a digit. List indexes match the digit value.
# Plot and subplot are used similar to Step 3.

# In[12]:


fig = plt.figure(figsize=(20,20))
meanlist = []
varlist = []
lis = [[] for i in range(10)]

for idx,num in enumerate(y_train):
    lis[int(num)].append(X_train[idx,:])
            
arr = np.array(lis)
    
for i in range(10):
    fig.add_subplot(16,16,i+1)
    
    mean = np.mean(arr[i], axis=0)
    meanlist.append(mean)
    mean = np.reshape(mean, (16,16))
    
    var = np.var(arr[i], axis=0)
    varlist.append(var)
    var = np.reshape(var, (16,16))
    plt.imshow(mean)


# ## Step 10

# To classify digit 101 we keep its features (vector n)
# For each digit, we have its mean value stores in meanlist. Each digit's mean value is stored in a vector (u). We calculate the euclidean distance of the two vectors. The minimum distance represents the most probable prediction. 
# Result is the index of the list where the minimum distance was found. 

# In[13]:


n = X_test[101,:]
distlist = []

for i in range(10):
    u = meanlist[i]
    u = np.array(u)
    dist =  np.linalg.norm(n-u)
    distlist.append(dist)
    
res = distlist.index(min(distlist))
print(res)


# Show actual value of digit 101.
# We conclude that our classification was not correct. The correct value is "6" and using the euclidean distance we got 0. The result can be justified by the similarity in the shape of the two digits. We show the two images (digit 101 from train set and "0" from its mean values) to highlight the similarity, in terms of round shape and position of the curves. The specific 6 (digit 101) has a slight elevation in its curve, unlike the 6 from the mean value, which is probably why the euclidean distance was bigger, thus classified it as a zero. 

# In[14]:


print("Actual value of digit 101 is: " + str(y_test[101]))

plt.figure(1)
plt.imshow(np.reshape(X_test[101], (16,16)))

plt.figure(2)
plt.imshow(np.reshape(meanlist[0], (16,16)))


# 
# ## Step 11

# (a) Repeat same procedure for all values of X_test and store results in list.

# In[15]:


resultlist = []

for n in X_test:
    distlist = []

    for i in range(10):
        u = meanlist[i]
        u = np.array(u)
        dist =  np.linalg.norm(n-u)
        distlist.append(dist)
    
    res = distlist.index(min(distlist))
    resultlist.append(res)


# (b) Compare values from resultlist (estimated values) and y_test (true values). Using the zip function we create tuples that have the (true,estimated) values. If the two elements in each tuple are the same, the classification was correct. For each correct value "correct" counter is increased. Final accuracy is correct values/all values. 

# In[16]:


correct = 0
acc = zip(y_test,resultlist)
for i in acc:
    if(int(i[0]) == i[1]):
        correct+=1
accuracy = correct/len(y_test)
print(accuracy)


# 
# ## Step 12

# Using given code as template, we create a Euclidean Classifier. 
# fit is implemented according to Step 9, using a list of lists for all the digits. It returns self (as it always should) and creates the self.X_mean_ which is a list with all the mean values for the 256 features.
# predict is implemented according to Step 11(a), calculating the euclidean distance of each digit to each vector in meanlist. It returns a list of the classifier's predictions.
# score is implemented according to Step 11(b), by counting all the correctly classified digits. it returns the accuracy percentage by cross checking ground truths and predictions (it uses the predict method we implemented above). 

# In[17]:


from sklearn.base import BaseEstimator, ClassifierMixin

class EuclideanClassifier(BaseEstimator, ClassifierMixin):  
    """Classify samples based on the distance from the mean feature value"""

    def __init__(self):
        self.X_mean_ = None


    def fit(self, X, y):
        self.X_mean_ = []
        lis = [[] for i in range(10)]

        for idx,num in enumerate(y):
            lis[int(num)].append(X[idx,:])
            
        arr = np.array(lis)
    
        for i in range(10):
            mean = np.mean(arr[i], axis=0)
            self.X_mean_.append(mean)
        return self


    def predict(self, X):
        resultlist = []

        for n in X:
            distlist = []

            for i in range(10):
                u = self.X_mean_[i]
                dist =  np.linalg.norm(n-u)
                distlist.append(dist)
    
            res = distlist.index(min(distlist))
            resultlist.append(res)
        
        return resultlist;
        
        
    def score(self, X, y):
        correct = 0
        acc = zip(y,self.predict(X))
        for i in acc:
            if(int(i[0]) == i[1]):
                correct+=1
        return correct/len(y)


# 
# ## Step 13

# ####  (a) Computer score of the Euclidean Classifier using 5-fold cross-validation. 
# Using cross_val_score we use the Classifier from Step 12 and the train set and we split it 5 times. We get the scores and compute a mean value for the error estimation. We use 100 for a random state, but by altering the value and observing the scores we can conclude that there was no significant difference and our error estimate is reliable because of cross validating the train set

# In[18]:


from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

scores = cross_val_score(EuclideanClassifier(), X_train, y_train, 
                         cv=KFold(n_splits=5, random_state=100), 
                         scoring="accuracy")
print("CV error = %f +-%f" % (np.mean(scores), np.std(scores)))


# #### (b) Plot the Decision Surface of the Euclidean Classifier.
# Using the given code from Lab 0.3 we adapt it for 10 classes (0-9 digits). We use ten colors to color the decision surface and only two dimensions (two features). 
# So at the first plot we select randomly 2 pixels (features) to plot the decision surface of the classifier pixel (5,8) and (7,3) and for the second plot we use a PCA with two components.
# It is obvious that PCA gives much better results, because we have two linearly uncorrelated variables (components) and we can safely reduce the number of our dimensions to two. Also we scale our data before PCA for better results

# In[19]:


from matplotlib.colors import ListedColormap
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X_train)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

X_new = X_train[:,[88,115]]

def plot_clf(clf, X, y, labels):
    colours =  ['xkcd:red', 'xkcd:green', 'xkcd:blue', 'xkcd:pink', 'xkcd:brown',
               'xkcd:purple', 'xkcd:orange', 'xkcd:yellow', 'xkcd:cyan', 'xkcd:black']
    pca_cmap = ListedColormap(colours, name='pca_cmap')
    plt.register_cmap(cmap=pca_cmap)
    
    fig, ax = plt.subplots(figsize=(20,20))
    # title for the plots
    title = ('Decision surface of Classifier')
    # Set-up grid for plotting.
    X0, X1 = X[:, 0], X[:, 1]
    
    x_min, x_max = X0.min() - 0.1, X0.max() + 0.1
    y_min, y_max = X1.min() - 0.1, X1.max() + 0.1
    
    xx, yy = np.meshgrid(np.arange(x_min, x_max, .05),
                         np.arange(y_min, y_max, .05))
    
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = np.array(Z)
    Z = Z.reshape(xx.shape)
    
    out = ax.contourf(xx, yy, Z, 10, cmap=pca_cmap, alpha=0.8)
    
    for label, colour in zip(labels,colours):
        ax.scatter(X0[y == label], X1[y == label],
        c=colour, label=label,
        s=2, alpha=0.9)
    
    ax.set_ylabel("Dimension 2")
    ax.set_xlabel("Dimension 1")
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_title(title)
    ax.legend()
    plt.show()


# In[33]:


clf1 = EuclideanClassifier()
clf1.fit(X_new, y_train)
plot_clf(clf1, X_new, y_train, [0,1,2,3,4,5,6,7,8,9])


# In[21]:


clf2 = EuclideanClassifier()
clf2.fit(X_pca, y_train)
plot_clf(clf2, X_pca, y_train, [0,1,2,3,4,5,6,7,8,9])


# #### (c)  Plot the Learning Curve of the Euclidean Classifier.
# We plot the test score and the training score as we split the data with a 5-fold cross-validation strategy, so as to an estimation of our model's behaviour. We see that after a certain point, roughly at 4000 samples, the two lines, training and cross-validation scores are almost aligned. That indicates that giving the model more data improves the behaviour up to a point, but after that more data will make no difference. In fact, going over that number in data will be counter-effective as the time consumption can be significant. Our model could be ameliorated by adding more features, which would make it more precise, but giving a dataset with more than ~5000 instances is no use.
# Actually we can see that after 2000 examples cross-validation score remains the same and training score is droping slightly. That's something we expect because we don't train a neural network which would explain a bigger incline with more samples.

# In[22]:


from sklearn.model_selection import learning_curve

train_sizes, train_scores, test_scores = learning_curve(
    EuclideanClassifier(), X_train, y_train, cv=5, n_jobs=-1, 
    train_sizes=np.linspace(.1, 1.0, 5))


# In[23]:


def plot_learning_curve(train_scores, test_scores, train_sizes, ylim=(0, 1)):
    plt.figure()
    plt.title("Learning Curve")
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")

    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

plot_learning_curve(train_scores, test_scores, train_sizes, ylim=(.6, 1))


# 
# ## Step 14

# For the a-priory probabilities, we count the apparitions of each digit in the train set, and store in an array of 10 counters, one for each digit. We divide with the sum and get the percentage.

# In[24]:


a_priori = np.zeros(10)
for i in y_train:
    a_priori[int(i)]+=1
a_priori = np.true_divide(a_priori, a_priori.sum(axis=0, keepdims=True))
print(a_priori)


# 
# ## Step 15

# #### (a) Construct a Bayesian Classifier, compatible with scikit-learn.
# The constructor creates the arrays. Then, they are assigned to the values from the mean and var lists, and the a-priory probabilities calculated in Step 14. 
# The 'fit' method is conditional so as to adapt to step 15. In this step we  use the variance for each pixel as was calculated in the prepare lab. The variance array has some zero values that result in a division error, so we add a small value that allows the calculations to be done.
# In the predict function, we implement the Gaussian Naive Bayes distribution. We use log to simplify calculations and convert multiplications to sums, in given relation ![Screen%20Shot%202018-11-01%20at%2001.13.15.png](attachment:Screen%20Shot%202018-11-01%20at%2001.13.15.png)
# We calculate the Maximum A Posteriori (MAP) estimation. The likelihood of the features is assumed to be Gaussian: 
# ![Screen%20Shot%202018-11-01%20at%2001.37.49.png](attachment:Screen%20Shot%202018-11-01%20at%2001.37.49.png)
# The mean and variance values for each pixel are taken from the respective arrays.
# 
# #### (b) Calculating the score.
# The score is calculated in the same way as Step 12, by counting all the correctly classified digits and returns the accuracy percentage by cross checking ground truths and predictions. 

# In[25]:


class MyNB(BaseEstimator, ClassifierMixin):  
    """Classify samples using our own Naive Bayes Classifier"""

    def __init__(self):
        self.X_mean_ = None
        self.X_var_ = None
        self.a_priori_ = None


    def fit(self, var="else", var_smooth=0.001):
        self.X_mean_ = np.array(meanlist)
        if (var == 1):
            self.X_var_ = np.ones((10,256))
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

            for i in range(10):
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
            if(int(i[0]) == i[1]):
                correct+=1
        return correct/len(y)


# We create our Naive Bayes Estimator and call the fit method. We use the test dataset (given as a parameter to the 'score' method) to get a score for the classification using our estimator.

# In[26]:


mnb = MyNB()
mnb.fit()
print (mnb.score(X_test,y_test))


# #### (c) Compare our implementation with the scikit-learn one.
# We import GaussianNB and train our model using the train set. Then we calculate the score on the test set, like we did with our implementation.
# The score results are similar, around 75%. We see that our implementation of the Bayes Classifier gives a significantly better score (~6 %).

# In[27]:


from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train,y_train)
print (gnb.score(X_test,y_test))


# 
# ## Step 16

# We call the 'fit' method of the classifier with our own estimator, with the var value set to 1, so the if-condition decides on using an array of ones instead of the variance array. 
# The new score of the test set if slightly but not insignificantly better, with an increase of ~4%.

# In[28]:


mnb.fit(1)
print (mnb.score(X_test,y_test))


# 
# ## Step 17

# We compare three classifiers, the Naive Bayes from the previous steps, Nearest neighbors and SVC. In the SVC classifier we try different kernels (linear, polynomial, Radial basis function, sigmoid). 
# The latter gives the best score (with the polynomial kernel), but both the kNeighbors and the SVC are significantly better than the Bayes Classifier. The classification report for each method shows that our classifier is better than the scikit one. Still, the KNeighbors and the SVC are superior both in terms of recall and precision.

# In[29]:


from sklearn.neighbors import KNeighborsClassifier
knc = KNeighborsClassifier()
knc.fit(X_train,y_train)
print (knc.score(X_test,y_test))


# In[30]:


from sklearn.svm import SVC
svc = {}
for i in ['linear', 'poly', 'rbf', 'sigmoid']:
    svc[i] = SVC(kernel=i, gamma='auto',probability=True)
    svc[i].fit(X_train,y_train)
    print (svc[i].score(X_test,y_test))


# In[31]:


from sklearn.metrics import classification_report
for i in [mnb,gnb,knc]:
    predictions = i.predict(X_test)
    print('Classification for ' + str(i) + '\n')
    print(classification_report(y_test, predictions))
    
for i in ['linear', 'poly', 'rbf', 'sigmoid']:
    predictions = svc[i].predict(X_test)
    print('Classification for SVC with ' + i + ' kernel \n')
    print(classification_report(y_test, predictions))


# 
# ## Step 18

# #### (a) 
# Using the VotingClassifier we combine some classifiers in hard and soft voting. We combine the KNeighbors, the liner kernel SVC and the polynomial SVC. These three were selected according to the classification results from the metaclassifier. They have different kinds of mistakes, so if one of them fails repeatedly in classifing a digit, another one will give a correct prediction. It is crucial that we have an odd number of classifiers combined so that they do not come to a draw about a result, because one result will always be outnumbered.

# In[34]:


from sklearn.ensemble import VotingClassifier


vclf1 = VotingClassifier(estimators=[('knn', knc), ('lsvc', svc['linear']), ('psvc', svc['poly'])], voting='hard')
vclf1.fit(X_train,y_train)
print (vclf1.score(X_test,y_test))

vclf2 = VotingClassifier(estimators=[('knn', knc), ('lsvc', svc['linear']), ('psvc', svc['poly'])], voting='soft')
vclf2.fit(X_train,y_train)
print (vclf2.score(X_test,y_test))


# #### (b) 
# We create an ensemble with the KNeighbors Classifier.

# In[36]:


from sklearn.ensemble import BaggingClassifier
bagging = BaggingClassifier(knc)
bagging.fit(X_train,y_train)
print (bagging.score(X_test,y_test))


# 
# ## Step 19

# #### (a) Create a dataloader.
# We implement the DigitDataset as a class where the data is initialised as a tuple list of digits and pixels. The train and test sets are converted to tensors (corresponding types), processed in our class DigitDataset and then sent to DataLoader to be more easily iterated and splitted in batches of a certain size. 

# In[37]:


import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

EPOCHS = 500
BATCH_SZ = 30

class DigitDataset(Dataset):
    """Handwritten digits dataset."""

    def __init__(self, X, y):
        self.data = list(zip(X, y))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    
train_data = DigitDataset(torch.from_numpy(X_train).type(torch.FloatTensor), torch.from_numpy(y_train).type(torch.LongTensor))
test_data = DigitDataset(torch.from_numpy(X_test).type(torch.FloatTensor), torch.from_numpy(y_test).type(torch.LongTensor))


train_dl = DataLoader(train_data, batch_size=BATCH_SZ, shuffle=True)
test_dl = DataLoader(test_data, batch_size=BATCH_SZ, shuffle=True)


# #### (b) Create a fully connected neural network
# We decided on using a 3-layer neural network (one input, one hidden and one output layer). We use two activation functions, a sigmoid function in the hidden layer and a softmax for the output layer. We have experimenting with two hidden layers but we saw negligible differences, also the number of neurons that gives us the best results is fifty in the hidden layer. When it comes to the activations functions we used softmax to see the possibility of each class in the output layer and we saw best results with sigmoid rather than reLU or tanh in the hidden layer. Also lr=1e-1 for the optimizer gave best results.

# In[38]:


import torch.nn.functional as F
import torch.optim as optim

class MyNN(torch.nn.Module):
    def __init__(self, input_D, hidden_D, output_D):
        super().__init__()
        self.linear1 = torch.nn.Linear(input_D, hidden_D)
        self.linear2 = torch.nn.Linear(hidden_D, output_D)

    def forward(self, X):
        h_sigm = torch.sigmoid(self.linear1(X))
        o_softm = F.softmax(self.linear2(h_sigm))
        return o_softm


# In[39]:


criterion = torch.nn.CrossEntropyLoss()

mynn = MyNN(256,50,10)

optimizer = optim.SGD(list(mynn.parameters()), lr=1e-1)


# In[40]:


mynn.train()
for epoch in range(EPOCHS):
    running_average_loss = 0
    for i, data in enumerate(train_dl):
        X_batch, y_batch = data
        optimizer.zero_grad()
        out = mynn(X_batch)
        loss = criterion(out, y_batch)
        loss.backward()
        optimizer.step()
        
        running_average_loss += loss.detach().item()
        if i % 100 == 0:
            print("Epoch: {} \t Batch: {} \t Loss {}".format(epoch, i, float(running_average_loss) / (i + 1)))


# In[41]:


mynn.eval()
acc = 0
n_samples = 0
with torch.no_grad():
    for i, data in enumerate(test_dl):
        X_batch, y_batch = data
        out = mynn(X_batch)
        val, y_pred = out.max(1)
        acc += (y_batch == y_pred).sum().detach().item()
        n_samples += BATCH_SZ

print(acc / n_samples)


# #### (c) Train and Evaluate
# Using the train_test_split function we split our train data to 85% for training and 15% to evaluating our NN. We create a sklearn compatible classifier that trains our nn in the fit function, using CrossEntropy as our loss function and SGD optimization. We pass epochs and batch size as arguments, we choose 500 epochs because after that our classifier gets no better and the risk for overfitting is big. The predict function gives predictions for each batch and using the score function we can evaluate our model by looking at the validate set accuracy.

#  #### Version compatible with scikit-learn
#     

# In[42]:


class MyNNClassifier(BaseEstimator, ClassifierMixin):  

    def __init__(self, hidden_d, epochs, batch_size):
        self.hidden_d = hidden_d
        self.epochs = epochs
        self.batch_size = batch_size
        self.net = None
        
    def fit(self, X, y):
        self.net = MyNN(256, self.hidden_d, 10)
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = optim.SGD(list(self.net.parameters()), lr=1e-1)
        train_data = DigitDataset(torch.from_numpy(X).type(torch.FloatTensor), torch.from_numpy(y).type(torch.LongTensor))
        train_dl = DataLoader(train_data, batch_size=self.batch_size, shuffle=True)
        self.net.train()
        for epoch in range(self.epochs):
            running_average_loss = 0
            for i, data in enumerate(train_dl):
                X_batch, y_batch = data
                optimizer.zero_grad()
                out = self.net(X_batch)
                loss = criterion(out, y_batch)
                loss.backward()
                optimizer.step()

                running_average_loss += loss.detach().item()
                if i == 0 and epoch % 100 == 0:
                    print("Epoch: {} \t Batch: {} \t Loss {}".format(epoch, i, float(running_average_loss) / (i + 1)))
        
    def predict(self, X):
        out = self.net(X)
        val, y_pred = out.max(1)
        return y_pred

    def score(self, X, y):
        test_data = DigitDataset(torch.from_numpy(X).type(torch.FloatTensor), torch.from_numpy(y).type(torch.LongTensor))
        test_dl = DataLoader(test_data, batch_size=self.batch_size)
        self.net.eval()
        acc = 0
        n_samples = 0
        with torch.no_grad():
            for i, data in enumerate(test_dl):
                X_batch, y_batch = data
                acc += (y_batch == self.predict(X_batch)).sum().detach().item()
                n_samples += self.batch_size

        return(acc / n_samples)


# In[44]:


X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.15)

mynnclf =  MyNNClassifier(50, 500, 30)
mynnclf.fit(X_tr,y_tr)
print (mynnclf.score(X_val,y_val))


# 
# #### (d)Test data: accuracy 

# In[45]:


print (mynnclf.score(X_test,y_test))


# In[ ]:




