import random
import re

class loteria:
    def generateNumbers(self, lowestValue = 1, maximunValue =  58):
        return list(range(lowestValue, maximunValue))

    def getSetOfWinnerNumbers(self, lowestValue = 1, maximunValue =  58, setOfNumbers  =  8):
        setOfPossibleNumbers =  self.generateNumbers(lowestValue, maximunValue)
        setOfWinnerNumber    =  set()

        if setOfNumbers > maximunValue:
            return "EL numero de numeros aleatorios que necesitas es superior al set de numeros posible"

        for index in range(0,setOfNumbers):
            possibleWinnerNumber =  random.choice(setOfPossibleNumbers)
            setOfWinnerNumber.add(possibleWinnerNumber)
            setOfPossibleNumbers.remove(possibleWinnerNumber)

        return str(sorted(list(setOfWinnerNumber))).replace('[', '').replace(']', '')

    def getSetOfWinnerNumbersStr(self, lowestValue = 1, maximunValue =  58, setOfNumbers  =  8):
        setOfPossibleNumbers        =   self.getSetOfWinnerNumbers(lowestValue, maximunValue, setOfNumbers)
        setOfPossibleNumbersStr     =   map(self.numberToString, setOfPossibleNumbers)
        return list(setOfPossibleNumbersStr)

    def numberToString(self, number):
        group_size          = 3
        finalNumberString   = ''
        basicNames          = {'^1$':' uno ', '^2$':' dos', '^3$':' tres ', '^4$':' cuatro', '^5$':' cinco', '^6$':' seis', '^7$':' siete',
            '^8$':' ocho', '^9$':' nueve', '^10$':' diez', '^11$':' once', '^12$':' doce', '^13$':' trece', '^14$':' catorce',
            '^15$':' quince', '^16$':' dieciséis', '^17$':' diecisiete', '^18$':' dieciocho', '^19$':' diecinueve',
            '^20$':' veinte', '^2[1-9]$':' veinti', '^30$':' treinta', '^3[1-9]$':' treinta y ', '^40$':' cuarenta',
            '^4[1-9]$': ' cuarenta y ', '^50$':' cincuenta', '^5[1-9]$':' cincuenta y ', '^60$': ' sesenta', '^6[1-9]$':' sesenta y ',
            '^70$' : ' setenta', '^7[1-9]$':' setenta y ', '^80$' : ' ochenta', '^8[1-9]$' : ' ochenta y ', '^90$' : ' noventa',
            '^9[1-9]$': ' noventa y ', '^100$' : ' cien', '^1[0-9][1-9]$' : ' ciento ', '^2[0-9][0-9]$' : ' docientos ',
            '^3[0-9][0-9]': 'trecientos', '^4[0-9][0-9]$' : ' cuatrocientos ', '^5[0-9][0-9]$' : ' quinientos ',  '^6[0-9][0-9]$' : ' seicientos ',
            '^7[0-9][0-9]$': ' setecientos ', '^8[0-9][0-9]$' : ' ochocientos ',  '^9[0-9][0-9]$' : ' novecientos ' }

        groupLastName       = {0 : '', 1 : ' mil ', 2 : ' millones '}

        #Por ahora solo hasta 999,999
        strNumber      = str( number )
        numberLen      = len( strNumber )
        moduleGroup3   = numberLen  % group_size
        if moduleGroup3 is not  0:
            extraCharacters     =   (group_size * (int(numberLen / group_size )+ 1)) - numberLen
            strNumber           = '*' * int(extraCharacters) + strNumber
            numberLen           = numberLen + extraCharacters

        numberIngroups  = self.getGroupsDivision(strNumber, group_size)

        numberIngroups.reverse()

        for groupIndex  in range(0, len (numberIngroups)):
            groupLastNameStr       =  groupLastName[groupIndex]
            finalNumberString   = '{0}{1}'.format(self.getGroupNames(basicNames, numberIngroups[groupIndex], groupLastNameStr )  , finalNumberString)
        return self.cleanString(finalNumberString)

    def getGroupNumber(self, strNumber, group_size):
        return int( len(strNumber) / group_size )

    def getGroupNames(self, basicNamesColl, strNumberInGroupOfThree, groupLastName):
        numberStr = ''
        for iteration in range(0,3):
            numberStr = '{0}{1}'.format(numberStr, self.getRegExResult( strNumberInGroupOfThree ,basicNamesColl) )
            if (len(strNumberInGroupOfThree) >= 1):
                strNumberInGroupOfThree   = strNumberInGroupOfThree[1:]
        return '{0}{1}'.format(numberStr, groupLastName)

    def getRegExResult(self, strToCompare, basicNamesColl ):
        regExList = basicNamesColl.keys()

        for regEx in regExList:
            if re.search(regEx , strToCompare):

                return basicNamesColl[regEx]
        return ''

    def getGroupsDivision(self, stringNumber, groupSize):
        groups          = self.getGroupNumber(stringNumber, groupSize )
        leftLimit       =  0
        rightLimit      = groupSize
        numberIngroups  = []
        for groupsIndex in  range(0, groups):
            numberIngroups.append(stringNumber[leftLimit:rightLimit])
            leftLimit   = rightLimit
            rightLimit  = rightLimit  + groupSize
        return numberIngroups

    def cleanString(self, stringNumber):
        stringNumber  = ' '.join(stringNumber.split())
        stringNumber  = stringNumber.strip()
        stringNumber  = re.sub('^uno mil', 'mil', stringNumber)
        stringNumber  = re.sub('once uno', 'once', stringNumber)
        stringNumber  = re.sub('doce dos', 'doce', stringNumber)
        stringNumber  = re.sub('trece tres', 'trece', stringNumber)
        stringNumber  = re.sub('catorce cuatro', 'cuatro', stringNumber)
        stringNumber  = re.sub('quince cinco', 'quince', stringNumber)
        stringNumber  = re.sub('dieciséis seis', 'dieciséis',stringNumber)
        stringNumber  = re.sub('diecisiete siete', 'diecisiete',stringNumber)
        stringNumber  = re.sub('dieciocho ocho' , 'dieciocho', stringNumber)
        stringNumber  = re.sub('diecinueve nueve', 'diecinueve', stringNumber)
        stringNumber  = re.sub('(?<=veinti) ', '', stringNumber)
        return stringNumber.capitalize()


    def sorteoNumbers(self, sorteoName):
        maxNumber = 56 #Melate es default
        if 'revanchita' in  sorteoName or 'melate' in sorteoName or 'revancha' in sorteoName:
            maxNumber       = 56
            setOfNumbers    = 8
        if 'chispa' in  sorteoName:
            maxNumber       = 28
            setOfNumbers    = 5
        return self.getSetOfWinnerNumbers(maximunValue =  maxNumber, setOfNumbers  =  setOfNumbers)



if __name__ == "__main__":
    lot             = loteria()
    print('Sorteo 05 : {}'.format(lot.numberToString(5)))
    print(lot.getSetOfWinnerNumbersStr())
    #print(lot.getGroupsDivision('**1101', 3))
