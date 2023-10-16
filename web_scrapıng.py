import pandas as pd
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector
import time
from colorama import Fore, Style


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}


# Eğer bir siteye giriş yapamıyorsak user agent almalıyız.

url1 = "https://www.arabam.com/ilan/galeriden-satilik-land-rover-range-sport-3-0-sdv6-autobiography/2012-autobiography-3-0-sdv6-joystick-5bolge-kamera-buz-dolabi/23604878"
url2 = "https://www.arabam.com/ilan/galeriden-satilik-bmw-5-serisi-520i-premium/2015-bmw-5-20i-premium-hayalet-e-vakum-perde-elk-bagaj-k-isitma/23598960"


def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    #print(soup.prettify())
    return soup

soup = get_data(url1)

# find içine verdiğimiz özelliğin ilk bulduğunu alır döndürür
# finf all içine verdiğimiz tagten content içinde ne kadar var ise hepsini list döndürür

title = soup.find("div", class_="product-name-container").text.strip() #text.strip() text tagleri strip boşlukları siliyor 

#print(title)

price = soup.find("div",class_="product-price").text.strip().replace("TL",'') #dataya kayıt yapacağımız için TL ifadesini silelim 

#print(price)

#---- txt dosyası oluşturuyoruz ve url ve priceları içine ekliyoruz bu sayede daha esnek yapıya ulaşıyoruz.

# şimdiki zamanı alalım 
now = datetime.now()

formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

def read_urls(): 
    with open("/Users/ayhancagan/Desktop/txt/urls.txt") as f:
        urls =f.readlines()

    #print(urls)
    return urls

def connect_db():
    #veri tabanı bağlantısı kuruyoruz.
    mydb = mysql.connector.connect(
        host='localhost',
        user="root",
        password="",
        database="program_1"
    )
    return mydb 

def insert_value(mydb,data):
    mycursor = mydb.cursor()
# veri tabanına ekleme işlemi yapmak istiyoruz.
    for value in data:
        sql = "INSERT INTO products (title, price, date, site) VALUES (%s, %s, %s, %s)"
        val = (value["title"], value["price"], value["time"], "arabam.com")
        mycursor.execute(sql, val) #sql çalıştırıp value veriyoruz
    mydb.commit() # yaptığımız işlemleri veri tabanına kaydediyoruz


ur_list = read_urls() #artık txt dosyasına linkleri girdiğimizde fonksiyone olarak okuyabileceğiz.
                 
def parse(ur_list):# txt dosyası içindeki url listesi içinde döngüye giriyoruz ve price ve listeyı ayırıyoruz.
    product_list = [] # en dışarıda ürünlerin kayıtı için liste oluşturuyoruz.
    for ur in ur_list:
        parts = ur.split("price:")
        url = parts[0].strip()
        check_price = parts[1].strip().replace(".", "").replace(",", ".")  # Türkçe sayı biçimini düzeltiyoruz   
        soup = get_data(url)     
        title = soup.find("div", class_="product-name-container").text.strip() # daha önce yazdığımız kodları fonk içine ekliyoruz.
        price = (soup.find("div",class_="product-price").text.strip().replace("TL",'').replace(".", "").replace(",", ".") )

        
        print("Tittle:", title,'\n',"Price:",float(price),"\n","Check_price:",float(check_price))  

        # check_price ile fiyat kontrolu yapmak istiyoruz.
        if price is not None:
            if check_price>=price:
                print('Favori İlanınızın Fiyatı Düştü!!!')

        info = {'title':title,'price':price,'check_price':check_price,"time":formatted_time} # dictionary halinde veriyi çekmek istediğimiz için oluşturuyoruz.

        product_list.append(info)  

    return product_list # listeyi kullanabilmek için döndürüyoruz.



product_list = parse(ur_list) 

#print(product_list) # sözlük halinde içerikleri yazdırıyoruz.. 


mydb = connect_db()
insert_value(mydb, product_list)











   





