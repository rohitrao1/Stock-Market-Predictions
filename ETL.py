import os
import csv
import pprint
import pandas as pd

# GDP is quaterly so converting it to monthly data
def parseGDP(file):
    missedMonths = [['02','03'], ['05','06'], ['08','09'], ['11','12']]
    gdpDic = {}
    with open(file, 'r') as gdpcsv:
        csvreader = csv.reader(gdpcsv)
        next(csvreader)
        cnt = 0
        for row in csvreader:
            if cnt == 4:
                cnt = 0
            dt = row[0].split("-")
            year = dt[0]
            month = dt[1]
            gdpDic[year+"-"+month] = round(float(row[1]),2)
            for item in missedMonths[cnt]:
                gdpDic[year+"-"+item] = round(float(row[1]),2)
            cnt += 1
    return gdpDic

def parseMonthlyRates(file):
    dic = {}
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            dt = row[0].split("-")
            year = dt[0]
            month = dt[1]
            dic[year+"-"+month] = round(float(row[1]),2)
    return dic

def parseDailyIndex(file):
    dicIndex = {}
    dicDayCount = {}
    dicAvgIndex = {}
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        current_key = ""
        previous_key = ""
        for row in csvreader:
            dt = row[0].split("-")
            year = dt[0]
            month = dt[1]
            current_key = year+"-"+month
            if current_key not in dicIndex:
                dicIndex[current_key] = round(float(row[4]),2)
                dicDayCount[current_key] = 1
            else:
                dicIndex[current_key] += round(float(row[4]),2)
                dicDayCount[current_key] += 1
            if previous_key != current_key and previous_key != "":
                dicAvgIndex[previous_key] = round(dicIndex[previous_key]/dicDayCount[previous_key],2)
            previous_key = current_key
        dicAvgIndex[current_key] = round(dicIndex[current_key]/dicDayCount[current_key],2)
    return dicAvgIndex

#merge dicts to single 
def mergeDatasets(n, dataDicts):
    df1 = pd.DataFrame(list(dataDicts[0].items()), columns=['Month', 'Value0'])
    for i in range(1,n):
        df = pd.DataFrame(list(dataDicts[i].items()), columns=['Month', 'Value'+str(i)])
        df1 = pd.merge(df1, df, how='inner', on =['Month'])
    return df1

gdp = parseGDP("v_GDP.csv")
bankRates = parseMonthlyRates("v_BankPrimeLoanRate.csv")
cpi = parseMonthlyRates("v_ConsumerPriceIndex.csv")
fedRate = parseMonthlyRates("v_FederalFundRate.csv")
ipi = parseMonthlyRates("v_IndustrialProductionIndex.csv")
unEmpRate = parseMonthlyRates("v_UnemploymentRate.csv")

sp500 = parseDailyIndex("o_SP500.csv")
dowJones = parseDailyIndex("o_DowJonesIndustrialAverage.csv")
ls = [gdp, bankRates, cpi, fedRate, ipi, unEmpRate, sp500, dowJones]
lenLs = len(ls)


df = mergeDatasets(lenLs, ls)
print(df)

df = df.rename(columns={
    'Value0': 'GDP', 
    'Value1': 'BankRate',
    'Value2': 'CPI',
    'Value3': 'FederalRate',
    'Value4': 'IPI',
    'Value5': 'UnEmpRate',
    'Value6': 'SP500',
    'Value7': 'DowJones'
    })
df.to_csv('MarketData.csv', index=False)