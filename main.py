import requests
import os
from bs4 import BeautifulSoup
import smtplib

# create some parameters for the headers """ i got the headers using "myhttpheader.com"
PARAMETERS = {
        "Accept-Language":"en-US,en;q=0.9",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"

        }
""" import your Amazon URL"""
AMAZON_URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
my_email = "pythondanielpython@gmail.com"
passwords = os.environ["gmail_password"]
response = requests.get(url=AMAZON_URL, headers=PARAMETERS)
data = response.text


"""Cook your soup using beautifulsoup"""
soup = BeautifulSoup(data, "html.parser") # you can use either "lxml" or "html.parser". either one worked for me
# print(soup.prettify())
# we need to find the price of what we want to buy


price_list = soup.find(class_="a-offscreen")


"""STEP 3: get the price of what you want to buy"""
item_price = [price.getText().strip("' ' ") for price in price_list]
cleaned_item = [value.strip("' $") for value in item_price if value.strip("' ' ")][0]
PRICE = float(cleaned_item)
title = soup.find(name="span", id="productTitle", class_="a-size-large product-title-word-break").getText()
REVIEW = soup.find(name="span", class_="a-icon-alt").getText()
LINK_NAME = soup.find(name="a", id="bylineInfo", class_="a-link-normal").getText()
LINK = soup.find(name="a", id="bylineInfo", class_="a-link-normal").get(key="href")

"""Make comparism"""
THRESHHOLD = float(90)

"""Send the message to my email"""

if PRICE <= THRESHHOLD:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=passwords)
        connection.sendmail(
            from_addr="pythondanielpython@gmail.com",
            to_addrs="arcdaniel20@gmail.com",

            msg=f"Subject: PRICE JUST DROPPED🥰.\n\nThe price of\n\n{title}"
                f" \njust dropped to 👉 ${PRICE}.\n Review is: {REVIEW}\n\nSounds Good? purchase {LINK_NAME} "
                f"by clicking this link: {LINK}".encode("utf-8"))
        print("done!")



