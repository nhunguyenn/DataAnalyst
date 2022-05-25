from asyncio.windows_events import NULL
from socket import socket
from tkinter import N
from bs4 import BeautifulSoup as BS
import urllib.request
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import requests
import matplotlib.pyplot as plt

def getData(code_stock):
    year = 2021
    Quanter = []
    TaiSanNganHan = []
    TaiSanDaiHan = []
    TongCongTaiSan = []
    TongCongNguonVon=[]
    while year>2000:
        if  dowData(code_stock, year) != 0:
            for i in dowData(code_stock, year)[0]:
                Quanter.append(i)
            for i in dowData(code_stock, year)[1]:
                TaiSanNganHan.append(float(replaceNumber(i)))
            for i in dowData(code_stock, year)[2]:
                TaiSanDaiHan.append(float(replaceNumber(i)))
            for i in dowData(code_stock, year)[3]:
                TongCongTaiSan.append(float(replaceNumber(i)))
            for i in dowData(code_stock, year)[4]:
                TongCongNguonVon.append(float(replaceNumber(i)))
        else:
            break
        year = year-1
    return Quanter, TaiSanNganHan, TaiSanDaiHan, TongCongTaiSan, TongCongNguonVon

def replaceNumber(i):
    if i == '':
        return 0
    return i.replace(',', '')

def dowData(code_stock, year):
    url =  f'https://www.cophieu68.vn/financial.php?id={code_stock}&view=&year={year}'
    page = urllib.request.urlopen(url)
    soup = BS(page, 'html.parser')

    Quanter = soup.find('div', id= 'right_col').find('table', class_ = 'table_finance').find_all('tr')[0].find_all('td')
    QuanterTemp = []
    for i in range(2,len(Quanter)):
        QuanterTemp.append((Quanter[i].get_text()))
    if ('Năm 2020'in QuanterTemp) or (len(QuanterTemp)== 0):
        return 0 
    NganHan = soup.find('div', id= 'right_col').find('table', class_ = 'table_finance').find_all('tr')[1].find_all('td')
    DaiHan = soup.find('div', id= 'right_col').find('table', class_ = 'table_finance').find_all('tr')[4].find_all('td')
    TongCongTaiSan = soup.find('div', id= 'right_col').find('table', class_ = 'table_finance').find_all('tr')[7].find_all('td')
    TongCongNguonVon = soup.find('div', id= 'right_col').find('table', class_ = 'table_finance').find_all('tr')[10].find_all('td')
    NganHanTemp = []
    DaiHanTemp = []
    TongCongTaiSanTemp = []
    TongCongNguonVonTemp = []
    for i in range(2,len(Quanter)):
        NganHanTemp.append(NganHan[i].get_text())
        DaiHanTemp.append(DaiHan[i].get_text())
        TongCongTaiSanTemp.append(TongCongTaiSan[i].get_text())
        TongCongNguonVonTemp.append(TongCongNguonVon[i].get_text())
    QuanterTemp.reverse()
    NganHanTemp.reverse()
    DaiHanTemp.reverse()
    TongCongTaiSanTemp.reverse()
    TongCongNguonVonTemp.reverse()

    return QuanterTemp, NganHanTemp, DaiHanTemp, TongCongTaiSanTemp, TongCongNguonVonTemp


print(getData('HPG'))

def drawChart(code_stock):
    Data = getData(code_stock)
    Quanter = np.array(Data[0])
    TaiSanNganHan = np.array(Data[1])
    TaiSanDaiHan = np.array(Data[2])
    TongCongTaiSan = np.array(Data[3])
    TongCongNguonVon = np.array(Data[4])
    plt.bar(Quanter, TaiSanNganHan, 0.6, label='Tài sản ngắn hạn')
    plt.bar(Quanter, TaiSanDaiHan, 0.6, bottom=TaiSanNganHan,label='Tài sản dài hạn')
    plt.bar(Quanter, TongCongTaiSan, 0.6, bottom=TaiSanNganHan+TaiSanDaiHan,label='Tổng cộng tài sản')
    plt.bar(Quanter, TongCongNguonVon, 0.6, bottom=TaiSanNganHan+TaiSanDaiHan+TongCongTaiSan,label='Tổng cộng nguồn vốn')
    plt.setp(plt.gca().get_xticklabels(), rotation=50, horizontalalignment='right')
    plt.ylabel('Tỷ đồng')
    plt.title('TỔNG CƠ CẤU TÀI SẢN CÔNG TY QUA TỪNG QUÝ')
    plt.legend()
    plt.show()

drawChart('HPG')


