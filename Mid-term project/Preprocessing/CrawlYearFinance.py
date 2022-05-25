
from bs4 import BeautifulSoup as BS
import urllib.request
import matplotlib.pyplot as plt

# Lấy dữ về và lưu vào các list
def downData(code_stock):
    # Tìm kiếm đường link đến trang web có bảng dữ liệu cần lấy
    url =  f'https://www.cophieu68.vn/financial.php?id={code_stock}&year=-1&view='

    page = urllib.request.urlopen(url)
    soup = BS(page, 'html.parser')
    # Tìm dữ liệu trong mã HTML của trang web
    data_year = soup.find('div', id= 'finance_income').find('tr', class_ = 'tr_header').find_all('td')
    listYear = []
    for i in range(1,len(data_year)):
        # Thêm dữ liệu vào list year tạo ban đầu
        listYear.append(data_year[i].get_text())
    listYear.reverse()

    # Tìm dữ liệu trong mã HTML của trang web
    DoanhThuBanHang = soup.find('div', id= 'finance_income').find('table', class_ = 'table_finance').find_all('tr')[1].find_all('td')
    DoanhThu = []
    for i in range(1,len(DoanhThuBanHang)):
        # Thêm dữ liệu vào list Doanh thu tạo ban đầu và ép về kiểu Float
        DoanhThu.append(float(replaceNumber(DoanhThuBanHang[i].get_text())))
    DoanhThu.reverse()

    LoiNhuanSauThue = soup.find('div', id= 'finance_income').find('table', class_ = 'table_finance').find_all('tr')[7].find_all('td')
    LoiNhuan = []
    for i in range(1,len(LoiNhuanSauThue)):
        # Thêm dữ liệu vào list Lợi nhuận tạo ban đầu và ép về kiểu Float
        LoiNhuan.append(float(replaceNumber(LoiNhuanSauThue[i].get_text())))
    LoiNhuan.reverse()

    return listYear, DoanhThu, LoiNhuan

# Thay đổi ','
def replaceNumber(i):
    return i.replace(',', '')

# Vẽ biểu đồ
def DrawDiagram(code_stock):
    # Gọi lại dữ liệu từ hàm downData với các index[0] tương ứng là listYear,[1]Doanhthu và [2]LoiNhuan
    year=downData(code_stock)[0]
    DoanhThu=downData(code_stock)[1]
    LoiNhuan=downData(code_stock)[2]
    
    plt.title('KẾT QUẢ KINH DOANH QUA CÁC NĂM')
    plt.ylabel('Tổng doanh thu')
    plt.bar(year,DoanhThu,color='g', width=0.3)
    plt.twinx()
    plt.ylabel('Lợi Nhuận sau thuế')
    plt.plot(year,LoiNhuan, 'y', marker='o')
    plt.legend(['LoiNhuan'])
    plt.show()

print(downData('VCB'))
DrawDiagram('VCB')




