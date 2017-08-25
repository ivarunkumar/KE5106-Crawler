# Import Library
import sklearn
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import math
import json
import csv

########


########


########

def fTrainDataProcess (csv):
	column_names = ['userName','memberSince','ageGroup','gender','homeTown','points','rating','Label']
	df = pd.read_csv(csv, delimiter=',', encoding="ISO-8859-1", header=None, sep=',', names=column_names)

	for column in df.columns:
		if df[column].dtype == type(object):
			le = preprocessing.LabelEncoder()
			df[column] = le.fit_transform(df[column])

	array = df.values

	X = array[:,0:7]
	y = array[:,7]
	scaler = MinMaxScaler(feature_range=(0, 1))
	rescaledX = scaler.fit_transform(X)
	# summarize transformed data
	np.set_printoptions(precision=3)
	print(rescaledX[0:7,:])

	print("XXXXX:",rescaledX)
	print("YYYYYY:",y)	

	fML_SVM_Make_PredModel(rescaledX, y)	

def fML_SVM_Make_PredModel(X, y):    # Model # total attributes + target
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)
		
	vSVMML = SVC(probability=True)
	vSVMML.fit(X_train, y_train)
	SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
			decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
			max_iter=-1, probability=True, random_state=None, shrinking=True,
			tol=0.001, verbose=False)
		
	y_pred = vSVMML.predict(X_test)
	
	#print accuracy_score(y_test, pred)
	print(recall_score(y_test, y_pred, average="macro"))    
	
	# Preserve the Model
	joblib.dump(vSVMML, 'Tripadvisor_R2_MLModel.pkl') 

	
def fML_SVM_Load_TestModel(i): # Data Set
	# Load the R2 Model for Traipadvisor
	vSVMML = joblib.load('Tripadvisor_R2_MLModel.pkl') 
	vTesting = i
	vTesting = np.array(vTesting).reshape((1, -1))
	
	vPredProb = vSVMML.predict(vTesting)
	print("test ",vPredProb)
	return vPredProb

#---------------------- Call Functions ----------------------

# Run the function to make a model
#vTrainData_X = [['1','2014','1','1','1','1','3'],
#['1','2014','1','2','2','2','4'],
#['1','2014','1','3','3','3','4']]

#vTrainData_Y = ['1','0','0']

#fML_SVM_Make_PredModel(vTrainData_X, vTrainData_Y)

# Run the function to make prediction for untested data
#vTesting = ['20','014','20','20','20','0','2']
#fML_SVM_Load_TestModel(vTesting)

#fML_SVM_Load_TestModel(vData)
fTrainDataProcess("Input_01.csv")





