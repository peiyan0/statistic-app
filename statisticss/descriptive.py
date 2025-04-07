def mean(data):
    return sum(data)/ len(data)

def median(data):
    sortedData = sorted(data)
    middle = len(data)//2
    if len(data)%2 == 0:
        return (sortedData[middle-1] + sortedData[middle]) /2
    else:
        return sortedData[middle]

from collections import Counter
def mode(data):
    count = Counter(data)
    maxCount = max(list(count.values()))
    modes = [key for key, value in list(count.items()) if value == maxCount]
    return modes

def range(data):
    return max(data) - min(data)

def variance(data):
    meanVal = sum(data)/len(data)
    return sum((x - meanVal) ** 2 for x in data) / len(data)
def std_dev(data):
    return variance(data) ** 0.5

def quartile(data):
    sortedList = sorted(data)
    Q1 = sortedList[int(len(sortedList)*0.25)]
    Q3 = sortedList[int(len(sortedList)*0.75)]
    Q2 = median(sortedList)
    print("First quartile: ",Q1)
    print("Second quartile: ",Q2)
    print("Third quartile: ",Q3)
    IQR = Q3 - Q1
    print("Interquartile Range is " + str(IQR))

    mildLowerBound = Q1 - (1.5 * IQR)
    extremeLowerBound = Q1 - (3 * IQR)
    mildUpperBound = Q3 + (1.5 * IQR)
    extremeUpperBound = Q3 + (1.5 * IQR)
    outliers = [i for i in data if i < extremeLowerBound or  i  > extremeUpperBound]
    print("Outliers: ",outliers)
    return

def result(data):
    print("Descriptive Statistics: ")
    print("Mean: ",mean(data))
    print("Median: ",median(data))
    print("Mode: ",mode(data))
    print("Range: ",range(data))
    print("Variance: ",variance(data))
    print("Standard deviation: ",std_dev(data))
    quartile(data)
    print('------------------------')
    return
