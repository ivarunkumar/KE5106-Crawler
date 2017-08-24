from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.datasets import make_classification  # Delete once own data ready

# We use a utility to generate artificial classification data.
X, y = make_classification(n_samples=1000, n_informative=10, n_classes=3) # Delete once own data ready
X1 = make_classification(n_samples=20, n_informative=10, n_classes=3) # Delete once own data ready

def fML_SVM_Make_PredModel(X, y):
	# Setup the Model
	sss = StratifiedShuffleSplit(y, n_iter=3, test_size=0.5, random_state=0)
	
	for train_idx, test_idx in sss:
		X_train, X_test, y_train, y_test = X[train_idx], X[test_idx], y[train_idx], y[test_idx]
		
		print ("X_train",X_train)
		print ("X_test",X_test)
		print ("y_train",y_train)
		print ("y_test",y_test)
		
		vSVMML = SVC(probability=True)
		vSVMML.fit(X_train, y_train)
		SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
			decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
			max_iter=-1, probability=True, random_state=None, shrinking=True,
			tol=0.001, verbose=False)
		
		y_pred = vSVMML.predict(X_test)
		# print(accuracy_score(y_test, y_pred, normalize=False))
		# print(f1_score(y_test, y_pred, average="macro"))
		# print(precision_score(y_test, y_pred, average="macro"))
		print(recall_score(y_test, y_pred, average="macro"))    
	
	# Preserve the Model
	joblib.dump(vSVMML, 'Tripadvisor_R2_MLModel.pkl') 
	# print(vSVMML.predict([[0, 0, 0, 0]]))

	
def fML_SVM_Load_TestModel(X):
	# Load the R2 Model for Traipadvisor
	vSVMML = joblib.load('Tripadvisor_R2_MLModel.pkl') 
	
	vContainer = [];
	vLengthOfX = len(X)
	
	for i in range(vLengthOfX):
		vPredProb = vSVMML.predict_proba(X[i])
		
		vContainer.append(vPredProb)
		
	# print(vSVMML.predict([[0, 0.5, 0, 0]]))
	return vContainer
	
fML_SVM_Make_PredModel(X, y)
print ("Probability:", fML_SVM_Load_TestModel(X1))






