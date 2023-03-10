
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Prints the summary of the dataset
def summarize_dataset(dataset):
    # Dimensions of the dataset
    print("Dimensions of the dataset : ", dataset.shape)

    # Take a peek at the data
    print(dataset.head(20)) # Prints the first 20 rows

    # Statistical summary
    print(dataset.describe())

    # Class distribution
    print(dataset.groupby('class').size())

# Visualizes the dataset
def visualize_dataset(dataset):
    # Univariate plots - Box and Whisker plots
    dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
    pyplot.show()

    # Univariate plots - Histograms
    dataset.hist()
    pyplot.show()

    # Multi-variate plots - Scatter plot matrix
    scatter_matrix(dataset)
    pyplot.show()

# Split-out validation dataset
def split_dataset(dataset):
    array = dataset.values
    X = array[:,0:4]
    y = array[:,4]
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)

    return X_train, X_validation, Y_train, Y_validation

# Identify best model to train the dataset
def analyze_models():
    # Spot Check Algorithms
    models = []
    models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC(gamma='auto')))

    # Evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
        results.append(cv_results)
        names.append(name)
        print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

    # Compare Algorithms
    pyplot.boxplot(results, labels=names)
    pyplot.title('Algorithm Comparison')
    pyplot.show()

def train_model():
    # Make predictions on validation dataset
    model = SVC(gamma='auto')
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)

    # Evaluate predictions
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

    return model


if __name__ == "__main__":
    # Loading the dataset
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
    url = "iris.csv"
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = read_csv(url, names=names)

    # summarize_dataset(dataset)

    # visualize_dataset(dataset)

    X_train, X_validation, Y_train, Y_validation = split_dataset(dataset)

    # analyze_models()

    model = train_model()






