import kNN
import matplotlib
import matplotlib.pyplot as plt
from numpy import *
from os import listdir

group, labels = kNN.createDataSet()
print group
print labels
result = kNN.classify0([0, 0], group, labels, 3)
print result
result = kNN.classify0([1.5,1.5], group, labels, 3)
print result

datingDataMat, datingLabels = kNN.file2matrix('datingTestSet2.txt')
print 'datingDataMat = ', datingDataMat
print 'datingLabels[0:20] = ', datingLabels[0:20]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,1], datingDataMat[:,2], 15.0*array(datingLabels), 15.0*array(datingLabels))
plt.show()
#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111)
#ax2.scatter(datingDataMat[:,0], datingDataMat[:,1], 15.0*array(datingLabels), 15.0*array(datingLabels))
#plt.show()

normMat, ranges, minVals = kNN.autoNorm(datingDataMat)
print 'normMat = ', normMat
print 'ranges = ', ranges
print 'minVals = ', minVals

kNN.datingClassTest()
#kNN.classifyPerson()

testVector = kNN.img2vector('testDigits/0_13.txt')
print testVector.shape
print testVector

kNN.handwritingClassTest()
