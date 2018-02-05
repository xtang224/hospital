from numpy import *
import operator
from os import listdir

def createDataSet():
   group = array([[1.0,1.1], [1.0,1.0], [0,0], [0,0.1]])
   labels = ['A', 'A', 'B', 'B']
   return group, labels

def classify0(inX, dataSet, labels, k):
   #print 'dataSet = ', dataSet
   dataSetSize = dataSet.shape[0]
   #print 'dataSetSize = ', dataSetSize
   #beginning of calculating the distance
   repMat = tile(inX, (dataSetSize,1)) 
   #print 'repMat = ', repMat
   diffMat = repMat - dataSet
   #print 'tile(inX, (dataSetSize,1)) = ', tile(inX, (dataSetSize,1))
   #print 'diffMat = ', diffMat
   sqDiffMat = diffMat ** 2
   sqDistances = sqDiffMat.sum(axis=1)
   #print 'sqDistances = ', sqDistances
   distances = sqDistances ** 0.5
   #print 'distances = ', distances
   #ending of calculating the distance
   sortedDistIndices = distances.argsort()
   #print 'sortedDistIndices = ', sortedDistIndices
   classCount = {}
   for i in range(k):
      #print 'sortedDistIndices[i] = ', sortedDistIndices[i]
      voteIlabel = labels[sortedDistIndices[i]]
      #print 'voteIlabel = ', voteIlabel
      #print 'classCount.get(voteIlabel,0) = ', classCount.get(voteIlabel,0)
      classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 #choose the k nearest neighbors
      #print 'classCount = ', classCount
   #print 'classCount = ', classCount
   sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True) #sort
   #print 'sortedClassCount = ', sortedClassCount
   return sortedClassCount[0][0]

def file2matrix(filename):
   fr = open(filename)
   arrayOLines = fr.readlines()
   numberOfLines = len(arrayOLines)
   returnMat = zeros((numberOfLines, 6))
   classLabelVector = []
   index = 0
   for line in arrayOLines:
      line = line.strip()
      listFromLine = line.split('\t')
      returnMat[index,:] = listFromLine[0:6]
      classLabelVector.append(int(listFromLine[-1]))
      index += 1
   return returnMat, classLabelVector

def file2matrix_s(filename):
   fr = open(filename)
   arrayOLines = fr.readlines()
   numberOfLines = len(arrayOLines)
   returnMat = zeros((numberOfLines, 3))
   classLabelVector = []
   index = 0
   for line in arrayOLines:
      line = line.strip()
      listFromLine = line.split('\t')
      returnMat[index,:] = listFromLine[0:3]
      classLabelVector.append(listFromLine[-1])
      index += 1
   return returnMat, classLabelVector    

def autoNorm(dataSet):
   minVals = dataSet.min(0)
   maxVals = dataSet.max(0)
   print 'minVals = ', minVals
   print 'maxVals = ', maxVals
   ranges = maxVals - minVals
   normDataSet = zeros(shape(dataSet))
   m = dataSet.shape[0]
   normDataset = dataSet - tile(minVals, (m,1))
   normDataSet = normDataSet / tile(ranges, (m,1))
   return normDataSet, ranges, minVals

def datingClassTest():
   hoRatio = 0.10
   datingDataMat, datingLabels = file2matrix_s('datingTestSet.txt')
   normMat, ranges, minVals = autoNorm(datingDataMat)
   m = normMat.shape[0]
   numTestVecs = int(m*hoRatio)
   errorCount = 0.0
   for i in range(numTestVecs):
      classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m], 3)
      print "the classifier came back with: %s, the real answer is: %s" % (classifierResult, datingLabels[i])
      if (classifierResult != datingLabels[i]):
         errorCount += 1.0
   print "the total error rate is: %f" % (errorCount / float(m))

def classifyPerson():
   resultList = ['not at all', 'in small doses', 'in large doses']
   percentTats = float(raw_input("percentage of time spent playing video games?"))
   ffMiles = float(raw_input("frequent flier miles earned per year?"))
   iceCream = float(raw_input("liters of ice cream consumed per year?"))
   datingDataMat, datingLabels = file2matrix_s('datingTestSet.txt')
   normMat, ranges, minVals = autoNorm(datingDataMat)
   inArr = array([ffMiles, percentTats, iceCream])
   classifierResult = classify0((inArr-minVals)/ranges, normMat, datingLabels, 3)
   print "You will probably like this person: %s" % classifierResult

def img2vector(filename):
   returnVect = zeros((1, 1024))
   fr = open(filename)
   for i in range(32):
      lineStr = fr.readline()
      for j in range(32):
         returnVect[0, 32*i+j] = int(lineStr[j])
   return returnVect

def handwritingClassTest():
   hwLabels = []
   trainingFileList = listdir('trainingDigits')
   m = len(trainingFileList)
   trainingMat = zeros((m,1024))
   for i in range(m):
      fileNameStr = trainingFileList[i]
      fileStr = fileNameStr.split('.')[0]
      classNumStr = int(fileStr.split('_')[0])
      hwLabels.append(classNumStr)
      trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
   testFileList = listdir('testDigits')
   errorCount = 0.0
   mTest = len(testFileList)
   for i in range(mTest):
      fileNameStr = testFileList[i]
      fileStr = fileNameStr.split('.')[0]
      classNumStr = int(fileStr.split('_')[0])
      vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
      classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
      print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
      if (classifierResult != classNumStr):
         errorCount += 1.0
   print "the total error rate is: %f" % (errorCount / float(mTest))

