from flask import Flask, render_template ,request
# import pymongo
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ",'')

        try:
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            # html_content = r.content
            soup = bs(flipkartPage, 'html.parser')
            # print(soup)
            bigboxes = soup.findAll("div", {"class": "_1AtVbE col-12-12"})
            # print(bigboxes )
            del bigboxes[:3]
            # print(bigboxes[0])
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            r = requests.get(productLink)
            next_content = r.content
            next_page_soup = bs(next_content, "html.parser")
            content_box = next_page_soup.find_all("div", {"class": "_1YokD2 _3Mn1Gg col-8-12"})
            commentboxes = next_page_soup.find_all('div', {'class': "_16PBlm"})
            try:
                title = content_box[0].find_all('span', {'class': 'B_NuCI'})[0].text

                # print("Title :", title)
            except:
                title = "No Title"
                # print(title)

            # Price
            try:
                price_data = content_box[0].find_all('div', {'class': '_25b18c'})
                price = price_data[0].div.text

            except:
                Price = "Not Available"

            #   Actual Price
            try:
                actual_price = price_data[0].find_all('div', {'class': '_3I9_wc _2p6lqe'})[0].text

            except:
                actual_price =  "Not Available"

            #   Discounts
            try:
                discount = price_data[0].span.text

            except:
                discount =  "Not Available"

            # finding the Ratings and review

            try:
                ratings_review = content_box[0].find_all('div', {'class': '_3_L3jD'})
                ratings = ratings_review[0].find_all('div', {'class': '_3LWZlK'})[0].text

            except:
                ratings =  "Not Available"

            # ratings_no = ratings_data[0].span.span.text

            try:
                ratings_review = content_box[0].find_all('div', {'class': '_3_L3jD'})
                ratings_data = ratings_review[0].find_all('span', {'class': '_2_R_DZ'})
                ratings_no = ratings_data[0].span.text
                ratings_no = ratings_no.split('&')[0].split(' ')[0]

            except:
                ratings_no = "Not Available"

            try:
                review_no = ratings_data[0].span.text
                reviews_no = review_no.split('&')[1].split(' ')[0]

            except:
                reviews_no = "Not Available"

            # Hightlights ......
            try:
                highlight_data = content_box[0].find_all('div', {'class': '_2418kt'})
                highlight =  highlight_data[0].find_all('ul')[0].text

            except:
                highlight =  "Not Available"

            # Image link

            try:
                img_content_box = next_page_soup.find_all("div", {"class": "CXW8mj _3nMexc"})
                img_link = img_content_box[0].img['src']

            except:
                img_link = "Not Available"

            try:
                buy_link =  productLink
            except:
                buy_link =  "Buy link is not available"

            product_data = {
                "title": title,
                "price": price,
                "actual_price": actual_price,
                "discount": discount,
                "ratings": ratings,
                "ratings_no": ratings_no,
                "reviews_no": reviews_no,
                "highlight": highlight,
                "img_link": img_link,
                "productLink": buy_link,

            }



            reviews = []
            for commentbox in commentboxes:
                try:
                    # name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = 'No Name'

                try:
                    # rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    # commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    # custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
            reviews.append(product_data)
            return render_template('result.html', reviews=reviews)

        except:
            return render_template('not_found.html')
    else:
        return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)