import time
from processing import datasetConstructor
from processing import modelManipulator
from pandas import read_csv

from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score,StratifiedKFold
from sklearn.linear_model import LogisticRegression



start = time.time()
print("The program is running...")


# hyper-parameters
nog = 15  # number of groups
spr = 256  # samples per group
nof = 3  # number of features
noss = 1024  # number of sifted samples

# ..............................................................................

# obter dataset para videos de treino....
file_rows = list()
features_file = datasetConstructor.set_up_features_file("processing/features_file.csv")
rel_path_videos = "../videos/train"
datasetConstructor.construct(rel_path_videos, nog, spr, noss, features_file, file_rows)
dataset_1 = read_csv("features_file.csv", header=None)
dsTuple_1 = datasetConstructor.get_train_and_test_sets(dataset_1, debug=True)


# obter dataset para videos de teste....
# avaliar mais uma vez (agora com dados toalmete novos)
#file_rows = list()
#features_file = datasetConstructor.set_up_features_file("processing/features_file.csv")
#rel_path_videos = "../videos/test"
#datasetConstructor.construct(rel_path_videos, nog, spr, noss, features_file, file_rows)
#dataset_2 = read_csv("features_file.csv", header=None)
#dsTuple_2 = datasetConstructor.get_features_label_values(dataset_1, debug=True)


# criar um modelo
nr_epochs = 100
nr_batches = 20
model = modelManipulator.construct(nof, nog, True)
# treinar e testar com dataset_1
model = modelManipulator.train_model(model, dsTuple_1, nr_epochs, nr_batches, 2)


# testar com dataset_1 e 2
print("...................................................................")
print("Nr. of epochs: ", nr_epochs)
print("Nr. of batches: ", nr_batches)
print("Nr. of groups: ", nog)
print("Nr. of samples per group: ", spr)
print("Nr. of features: ", nof)
print("Nr. of shifted samples:", noss)
modelManipulator.evaluate_model(model, dsTuple_1, 0)
#modelManipulator.evaluate_model_v2(model, dsTuple_2, 0)

# ..............................................................................

end = time.time()
print("Processing time: %.3f", (end - start)/60, "minutes")
