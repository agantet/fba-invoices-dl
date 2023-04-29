import argparse
import requests

############# Get a list of orderIDs which meet some "params" constraints (limit, orderStatus, sort, etc.)
def get_order_list(cookie, params, dl=False):
	url = "https://sellercentral.amazon.fr/orders-api/search?" + params
	#print(url)
	headers = {'cookie':cookie}
	response = requests.get(url, headers=headers)
	jsonres = response.json()
	errors = []
	orderlist = []
	for i in jsonres["orders"]:
		if (dl==True):
			print("------------- " + i["sellerOrderId"])
			res = download_pdf_from_orderid(i["sellerOrderId"], cookie)
			if (res != 0): #retry
				res = download_pdf_from_orderid(i["sellerOrderId"], cookie)

			if (res !=0):
				errors.append(i["sellerOrderId"])
			else:
				orderlist.append(i["sellerOrderId"])
		else:
			orderlist.append(i["sellerOrderId"])
	return orderlist, errors

############# Dowload PDF invoices
def download_pdf_from_orderid(orderid, cookie):

       host = "https://sellercentral.amazon.fr/"
       path = "taxdocument/api/get-entity?orderId=" + orderid
       headers = {'cookie':cookie}
       url = host + path
       #print(url)
       try:
              pdflocation = requests.get(url, headers=headers, timeout=10).json()["taxDocuments"][0]["location"]
              #print(pdflocation)
       except Exception as e:
              print("pdflocation failed. " + orderid + " invoice not downloaded")
              print(e)
              return -1
       
       url = host + pdflocation
       try:
              pdfurl = requests.get(url, headers=headers, timeout=10).url.replace("%2F", "/").replace("%3A", ":").split("=")[2].split("&openid.identity")[0]
              print(pdfurl)
       except Exception as e:
              print("pdfurl failed. " + orderid + " invoice not downloaded")
              print(e)
              return -1
       
       try:
              pdf =  requests.get(pdfurl, headers=headers, timeout=15)
       except Exception as e:
              print("pdf failed. " + orderid + " invoice not downloaded")
              print(e)
              return -1
       
       filename = "Invoice " + orderid + ".pdf"
       try:
              with open(filename, "wb") as f:
                     f.write(pdf.content) 
       except Exception as e:
              print("pdf write failed. " + orderid + " invoice not written on FS")
              print(e)
              return -1
       return 0

def main():
       parser = argparse.ArgumentParser(
             prog = 'FBAInvoicesHelper',
             description = 'Get FBA invoices',
             epilog = '')
       parser.add_argument('cookie', help='Session cookie')
       parser.add_argument('params', help='Search constraints (ex: limit=30&sort=order_date_desc)')
       parser.add_argument('-dl', '--download', action='store_true', help='Flag to enable download of invoices')
       args = parser.parse_args()

       if ("cookie" in args and "params"):
              print("\n")
              orders,errors = get_order_list(args.cookie, args.params, dl=True if (args.download) else False)
              print("\n\n------------- Summary: " + str(len(orders)-len(errors)) + "/" + str(len(orders)) + " invoices successfully found.\n") 
              print("\n- Successfully found invoices iDs:")
              print(orders)
              print("\n- Errors encoutered for invoices IDs:")
              print(errors)

if __name__ == '__main__':
       main()
