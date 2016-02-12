import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.preprocessing import MultiLabelBinarizer
# from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib


def parseData(source, groups):
    sentences = []
    targets = []
    with open(source, 'r') as f:
        for line in f:
            sample = line.split('&&')
            sentences.append(sample[0].decode('iso-8859-1').encode('utf8'))
            targets.append(sample[1].strip())

    y = [groups[i] for i in targets]
    return np.asarray(sentences), np.asarray(y)


def buildClassifier(source, targets, stop_words):
    """
    returns the trained text classifier 

    :param source:      list of comments
    :param targets:     list of comment categories related to the comments in source
    :param stop_words:  list of stop words 
    """

    text_clf = Pipeline([('vect', CountVectorizer(stop_words=stop_words, max_df=1.0, min_df=2)), 
                        ('tfidf', TfidfTransformer()),
                        ('clf', SVC(decision_function_shape='ovr', kernel='linear'))])

    text_clf.fit(source, targets)

    return text_clf


def runExperiment(source, stop_words, groups, n_validation=10):
    """
    Split the samples parsed from source file into train set and test set randomly.
    The final accuracy will be caculated through cross validation

    """
    sentences, targets = parseData(source, groups)
    stop_words_list =[]
    with open(stop_words, 'r') as f:
        for line in f:
            stop_words_list.append(line.strip())

    acc_total = 0
    for i in xrange(n_validation):
        index = range(len(sentences))
        random.shuffle(index)
        train_index = index[0: int(len(index)*5/6)]
        test_index = index[int(len(index)*5/6): len(index)]

        x_train = sentences[train_index]
        y_train = targets[train_index]
        x_test = sentences[test_index]
        y_test = targets[test_index]

        clf = buildClassifier(x_train, y_train, stop_words_list)
        y_predict = clf.predict(x_test)

        acc_total += float(np.sum(y_predict == y_test)) / len(y_predict)

    acc = acc_total / float(n_validation)

    print '\nExperiemtn result: '
    print '--------------------------------------------------'
    print 'Averaged predicting accuracy on test set is: %f' % (acc)
    print '--------------------------------------------------'


def trainSaveClassifier(input_source, groups, stop_words, output_source):
    """
    Train and save text classifier to an output file
    """
    sentences, targets = parseData(input_source, groups)
    stop_words_list =[]
    with open(stop_words, 'r') as f:
        for line in f:
            stop_words_list.append(line.strip())

    clf = buildClassifier(sentences, targets, stop_words_list)

    joblib.dump(clf, output_source) 



def loadClassifier(modelFile):
    """
    Load classifier from a file
    """
    clf = joblib.load(modelFile)
    return clf 


def predictNew(clf, sentences, groups):
    """
    Use trained classifier to make predictions on new samples

    :param clf:             trained classifier (clould be loaded from the model file)
    :param sentences:       a list of new comments (must in the form of list)
    :param groups:          dictionary from commment categories to indexes e.g. {'positive': 0, 'negative': 1, 'neutral': 2, 'question': 3}
    """
    groups = dict((y,x) for x,y in groups.iteritems())
    predicted = clf.predict(sentences)
    group_predict = [groups[i] for i in predicted]
   
    return group_predict



if __name__ == "__main__":
 
    source = 'data/sample_balance.txt'
    stop_words = 'data/Nespresso_228.txt'
    groups = {'positive': 0, 'negative': 1, 'neutral': 2, 'question': 3}

    ## Run experiment using data from source file
    runExperiment(source, stop_words, groups)

    ## To train and save classifier, you only need to call this function
    trainSaveClassifier(source, groups, stop_words, 'result/text_clf.pkl')

    ## Load classifier from model file
    clf = loadClassifier('result/text_clf.pkl')

    ## predict on new comments using the trained model
    new_text = ['the coffee machine is terrible! @Nespresso', 
                '@l_benson @Nespresso @TheRawChocCo This looks so amazing!']
    predict = predictNew(clf, new_text, groups)

    print '\nPredictions on new comments: '
    print '--------------------------------------------------------------'
    for i in range(len(new_text)):
        print "'%s' ==> %s" % (new_text[i], predict[i])
    print '--------------------------------------------------------------'







