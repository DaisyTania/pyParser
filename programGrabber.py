import json

def instituteFileNames():
    safu = 'rawData/idSAFU.csv'
    mgu = 'rawData/idMGU.csv'
    hse = 'rawData/idHSE.csv'
    svfu = 'rawData/idsvfu.csv'
    tsu = 'rawData/idTSU.csv'
    urfu = 'rawData/idURFU.csv'
    return [safu,mgu,hse,svfu,tsu,urfu]

def instituteFileNamesBored():
    safu = 'filtered/idSAFUBored.csv'
    mgu = 'filtered/idMGUBored.csv'
    hse = 'filtered/idHSEBored.csv'
    svfu = 'filtered/idsvfuBored.csv'
    tsu = 'filtered/idTSUBored.csv'
    urfu = 'filtered/idURFUBored.csv'
    return [safu,mgu,hse,svfu,tsu,urfu]

def csvParse(index):
    file = instituteFileNames()[index]
    print(file)
    boredInstitutes = instituteFileNamesBored()[index]
    fo = open(file,'r')#fileOpen
    fw = open(boredInstitutes, 'a')#fileWrite(Append rows to the file)
    try:
        for line in fo:
            splitted = line.split(';')
            writeLine = splitted[0]+';'+splitted[25]+';'+splitted[42]+';'+splitted[9]+';'+splitted[43]
            fw.write(writeLine)
    except Exception as err:
        print('SmthWrong in '+ fo.name)
        print(err)
    fo.close()
    fw.close()
    print("DONE")

def occupationDecode(index):
    decodeFileName = instituteFileNamesBored()[index]
    workList = list()
    schoolList = list()
    universityList = list()
    ListsArray = [workList, schoolList, universityList] #Array which contains lists: 0 - work, 1 - school, 2 - university
    
    fo = open(decodeFileName, 'r')
    try:
        for idx,line in enumerate(fo):            
            scplittedLine = line.split(';')
            splittedOccupation = scplittedLine[1].split(',',1)

            if splittedOccupation[0] == 'university':
                ListsArray[2].append(splittedOccupation[1])
            elif splittedOccupation[0] == 'work':
                ListsArray[0].append(splittedOccupation[1])
            elif splittedOccupation[0] == 'school':
                ListsArray[1].append(splittedOccupation[1])
    except Exception as Error:
        print(Error)
        print(idx)
    fo.close()
    return ListsArray

def isJsonString(str):
    if len(str)>2 and str[:2]=='[{':
        return True
    else:
        return False

def schoolsToList(index):
    decodeFileName = instituteFileNamesBored()[index]
    fo = open(decodeFileName,'r')
    SchoolsList = list()
    try:
        for line in fo:
            splittedLine = line.split(';')
            jsonSchool = splittedLine[2].replace("'",'"')
            if isJsonString(jsonSchool):
                decodedSchool = json.loads(jsonSchool)
                SchoolsList.append(decodedSchool)
            else:
                continue
    except Exception as identifier:
        print(identifier)
    fo.close()
    return SchoolsList

def universitiesToList(index):
    decodeFileName = instituteFileNamesBored()[index]
    fo = open(decodeFileName,'r')
    UniverList = list()
    dCounter = 0 ##Debug Variable
    try:
        for idx,line in enumerate(fo):
            splittedLine = line.split(';')
            jsonUniversity = splittedLine[4].replace("'",'"')
            if isJsonString(jsonUniversity):
                try:
                    UniverList.append(json.loads(jsonUniversity))
                except json.JSONDecodeError as ErrorMsg:
                    UniverList.append('ditryJson.Error')
                    dCounter += 1
                    print("%s|| Index: %s, Dirty string number: %s" % (ErrorMsg, idx, dCounter))
            else:
                continue
    except Exception as Error:
        print(Error)
    fo.close()
    return UniverList

def careerDecode(index):
    decodeFileName = instituteFileNamesBored()[index]
    fo = open(decodeFileName,'r')
    CareerList = list()
    dCounter = 0 ##Debug value
    try:
        for idx,line in enumerate(fo):
            splittedLine = line.split(';')
            jsonCareer = splittedLine[3].replace("'",'"')
            if isJsonString(jsonCareer):
                try:
                    CareerList.append(json.loads(jsonCareer))
                except json.JSONDecodeError as ErrorMsg:
                    CareerList.append('dirtyJson.error')
                    dCounter+=1
                    print("%s|| Index: %s, Dirty string number: %s" % (ErrorMsg, idx, dCounter))    
            else:
                continue
    except Exception as Error:
        print(Error)
    fo.close()
    return CareerList

def getFullRows(fileIndex):
    fileNameToDecode = instituteFileNamesBored()[fileIndex]
    fo = open(fileNameToDecode,'r')
    RowsList = list()
    dCounter = 0 #Debug Value
    try:
        for idx,line in enumerate(fo):
            entityDict = {}
            splittedLine = line.split(';')
            splittedOccupation = splittedLine[1].split(',',1) 
            jsonSchool = splittedLine[2].replace("'",'"')
            jsonUniversity = splittedLine[4].replace("'",'"')
            jsonCareer = splittedLine[3].replace("'",'"')                       
            entityDict['ID'] = splittedLine[0]
            if len(splittedOccupation)>1:
                entityDict['OCCUPATION'] = {splittedOccupation[0]:splittedOccupation[1]}
            else:
                entityDict['OCCUPATION'] = {splittedOccupation[0]:'occupation'}

            if isJsonString(jsonSchool):
                try:
                    entityDict['SCHOOLS'] = json.loads(jsonSchool)
                except Exception as ErrorMsg:                    
                    entityDict['SCHOOLS'] = 'bad json'
                    print("%s found + %s" % (ErrorMsg, 'bad JSON'))
            else:
                entityDict['SCHOOLS'] = 'not json'

            if isJsonString(jsonUniversity):
                try:
                    entityDict['UNIVERSITY'] = json.loads(jsonUniversity)
                except json.JSONDecodeError as ErrorMsg:
                    entityDict['UNIVERSITY'] = 'bad json'
                    dCounter += 1
                    print("%s|| Index: %s, Dirty string number: %s" % (ErrorMsg, idx, dCounter))
            else:
                entityDict['UNIVERSITY'] = 'not json'
            
            if isJsonString(jsonCareer):
                try:
                    entityDict['CAREER'] = json.loads(jsonCareer)
                except json.JSONDecodeError as ErrorMsg:
                    entityDict['CAREER'] = 'bad json'
                    dCounter+=1
                    print("%s|| Index: %s, Dirty string number: %s" % (ErrorMsg, idx, dCounter))    
            else:
                entityDict['CAREER'] = 'not json'
            
            RowsList.append(entityDict)

    except Exception as Error:
        print("%s, || Index: %s" % (Error,idx))
    finally:
        fo.close()
    return RowsList

if __name__ == "__main__":
    #schoolsList = schoolsToList(0)
    #universityList = universitiesToList(0)
    rows = getFullRows(0)
    ##careerList = careerDecode(0)
    #variable = occupationDecode(0)
    ##csvParse(0)