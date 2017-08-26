# Import Library
import sklearn
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
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
	column_names = ['1','2,','3','4,','5','6','7','8','9','10','11','12,','13','14,','15','16','17','18','19','20','21','22,','23','24','25','26','27','28','29','30','31','32,','33','34','35','36','37','38','39','40','41','42']
	df = pd.read_csv(csv, delimiter=',', encoding="ISO-8859-1", header=None, sep=',', names=column_names)

	for column in df.columns:
		if df[column].dtype == type(object):
			le = preprocessing.LabelEncoder()
			df[column] = le.fit_transform(df[column])

	array = df.values

	X = array[:,0:41]
	y = array[:,41]
	#scaler = MinMaxScaler(feature_range=(0, 1))
	#rescaledX = scaler.fit_transform(X)
	# summarize transformed data
	#np.set_printoptions(precision=3)
	#print(rescaledX[0:41,:])

	print("XXXXX:",X)
	print("YYYYYY:",y)	

	fML_SVM_Make_PredModel(X, y)	

def fML_SVM_Make_PredModel(X, y):    # Model # total attributes + target
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)
		
	#vSVMML = SVC(probability=True)
	
	vSVMML= SVC(probability=True, C=1000)
	
	vSVMML.fit(X_train, y_train)
		
	y_pred = vSVMML.predict(X_test)
	
	#print accuracy_score(y_test, pred)
	print(recall_score(y_test, y_pred, average="macro"))    
	
	# Preserve the Model
	joblib.dump(vSVMML, 'Tripadvisor_R2_MLModel.pkl') 

	
def fML_SVM_Load_TestModel(i): # Data Set
	# Load the R2 Model for Traipadvisor
	vSVMML = joblib.load('resources/Tripadvisor_R2_MLModel.pkl') 
	
	#scaler = MinMaxScaler(feature_range=(0, 1))
	#rescaledX = scaler.fit_transform(i)
	vTesting = i
	vTesting = np.array(vTesting).reshape((1, -1))
	
	vPredProb1 = vSVMML.predict(vTesting)
	vPredProb2 = vSVMML.predict_proba(vTesting)
	#print("Predicted :  ",vPredProb1)
	#print("Predict Probabilities : ",vPredProb2)
	
	
	
	
	return (vPredProb1, vPredProb2)

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
#vData = ['5','4','2','13631','6','39','18','48','34','8','1','1','0','0','1','0','1','0','0','0','0','0','1','0','0','0','0','0','0','0','109','34','56','32','21','0','0','43','22','44','0']
#vData = ['9','3','2','11343','6','37','19','38','16','4','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','79','28','58','10','9','0','2','30','16','33','0']
vData = ['3','0','0','2677','4','20','3','15','5','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','24','1','9','10','5','0','0','8','1','15','0']
#vData = ['5','4','2','13631','6','39','18','48','34','8','1','1','0','0','1','0','1','0','0','0','0','0','1','0','0','0','0','0','0','0','109','34','56','32','21','0','0','43','22','44','0']
#####fML_SVM_Load_TestModel(vData)
#fTrainDataProcess("R2Dumping_02.csv")





