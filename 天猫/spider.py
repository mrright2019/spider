import requests
from bs4 import BeautifulSoup


headers = {
#GET /search_product.htm?q=%E6%89%8B%E6%9C%BA&imgfile=&commend=all&ssid=s5-e&search_type=tmall&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306 HTTP/1.1
'Host': 'list.tmall.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://www.taobao.com/',
'Connection': 'keep-alive',
'Cookie': 'cna=X6tZFHMGsCUCAd9jxHpxbUf+; isg=BEVFtBTktfPcF5bEniGhucyEV4G_qtJf3A2vC0eqH3yL3mVQDlNiZI607MKNhRFM; hng=CN%7Czh-CN%7CCNY%7C156; t=38af3005015213b788a7554f054677e2; _tb_token_=a8e6e6e97ebe; cookie2=1e3eae460c269c5d10542251e4af65b5; tt=taobao-main; _med=dw:1536&dh:864&pw:1920&ph:1080&ist:0; res=scroll%3A1519*6762-client%3A1519*750-offset%3A1519*6761-screen%3A1536*864; l=aBtiU2KiyYDkVGbBkMa2BsmAa707a0fPZrkCEMam8TEhNT5Wg_OQkJno-Vw6p_hC5TUy_X-iI; cq=ccp%3D1; pnm_cku822=098%23E1hv5QvUvbpvj9CkvvvvvjiPR2ShsjlHRsLwtjivPmPhsj3RR2LWljtVPLMy1vhCvvOvChCvvvmtvpvIMMYvKNMMvPQvvhXVvvmvw9vvByOvvUhQvvCVB9vv9BQvvhXUvvmCUgyCvv4CvhE20nmivpvUvvCC8JvKERZEvpCW98jiTB0xdXuKHkx%2Fzj7J%2Bu0OjLVxfBkK5dUfbj7Q%2Bu0Od56OfwmKDf8rwATQD40Xdig0747BhC97%2B3%2BIaNoAdXkKfCT91E%2B7%2Bulsb9GCvvpvvPMMRphvCvvvphm5vpvhvvCCBv%3D%3D',
'Upgrade-Insecure-Requests': '1',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
}
url = 'https://list.tmall.com/search_product.htm?q=%E6%89%8B%E6%9C%BA&imgfile=&commend=all&ssid=s5-e&search_type=tmall&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'


def spider(url):
	res= requests.get(url,headers=headers)
	soup = BeautifulSoup(res.content.decode('gbk'),features="lxml")
	# print(soup)
	product_list = soup.find_all("div",attrs={"class":"product-iWrap"})
	for product in product_list:
		price = product.find("em").text
		print(price.replace(" ","").replace("\n",""))
		title = product.find("div",attrs={'class':"productTitle productTitle-spu"}).text.replace(" ","").replace("\n","")
		print(title.replace(" ","").replace("\n",""))
		shop = product.find("a",attrs={"class":"productShop-name"}).text
		print(shop.replace(" ","").replace("\n",""))
		productstatus = product.find("p",attrs={'class':'productStatus'})
		if productstatus:
			print("月销量:",productstatus.find("em").text.replace(" ","").replace("\n",""))


spider(url)