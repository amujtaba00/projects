from bs4 import BeautifulSoup
import mechanize
import urllib
import re
import requests
import geocoder
from geopy.geocoders import Nominatim
import geopy
import urllib.request
import json
from geopy.distance import geodesic

address = 'L9E+1G5+Milton,+ON'




def smt():
    return("yes")




def liner(address):
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.geocode(address)
    #(1,location)
    return (location.latitude, location.longitude)
    
def letgoLiner(address):
    address = address.replace(' ','+')

    endpoint =f'https://maps.googleapis.com/maps/api/geocode/json?address={address}=&key=uthough'
    request = endpoint
    response = urllib.request.urlopen(request).read()
    latlong = json.loads(response)
    keysone  = latlong.keys()
    results = latlong['results']
    try:
        geometry = results[0]['geometry']
    except IndexError:
        return('Check Posting')

    location = geometry['location']
    lat = location['lat']
    lng = location['lng']
    return(lat,lng)




def kijijiUrlMaker(address,radius,minprice,maxprice,search):
    accsearch = search.replace(" ","+")
    new = address.replace(" ","+")
    base = f"https://www.kijiji.ca/b-search.html?formSubmit=true&address={new}&adIdRemoved=&adPriceType=&brand=&carproofOnly=false&categoryName=&cpoOnly=false&gpTopAd=false&highlightOnly=false&ll=&locationId=&minPrice={minprice}&maxPrice={maxprice}&origin=&pageNumber=1&radius={radius}&searchView=LIST&sortByName=dateDesc&userId=&urgentOnly=false&keywords={accsearch}&categoryId=0&dc=true"
    return(base)


def postalcode(address):
    geolocator = geopy.Nominatim(user_agent='myapp')
    #('yes')
    zipcode = geolocator.reverse(liner(address))
    return(zipcode.raw['address']['postcode']).replace(' ','')


def craigslistUrlMaker(address,radius,minprice,maxprice,search):
    accsearch = search.replace(" ","+")
    new = postalcode(address)
    base = f'https://toronto.craigslist.org/search/sss?query={accsearch}&sort=rel&search_distance={radius}&postal={new}&min_price={minprice}&max_price={maxprice}'
    #(base)
    return(base)


def numberfinder(num):
    try:
        return(re.findall(r'\d+',num)[0])
    except:
        return(0.0)

#(numberfinder(' ,50km    ')[0])



def sorter(myList,n):
    myList.sort(key = lambda x: x[n])
    for item in myList:
        if item[n] == 0.0:
            item[n] = 'Please Contact'
        else:
            item[n] = str(item[n])
        
    return(myList)

def priceSorter(myList):
    for item in myList:
        if item[2] == 0.0:
            item[2] = 'Please Contact'
        elif item[2] != 'Please Contact':
            item[2] = str(item[2]) + '$'

def distSorter(myList):
    for item in myList:
        if item[4] == 0.0:
            item[4] = 'Please Contact'
        elif item[4] != 'Please Contact':
            item[4] =  str(item[4]) + 'km'




def letgoUrlMaker(address, radius, minprice, maxprice,search,finalpostings):
    lat = liner(address)[0]
    lon = liner(address)[1]
    location = (lat,lon)
    search = search.replace(' ','%20')
    url = f'https://www.letgo.com/en-ca?distance={radius}&latitude={lat}&longitude={lon}&price%5Bmax%5D={maxprice}&price%5Bmin%5D={minprice}&searchTerm={search}'
    ##(url)
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, features='lxml')
    ##(soup.find('body'))
    listings = soup.find_all('div',class_='sc-fzqNJr fZQQCV')
    i = 0
    numberOfResults = numberfinder((soup.find('div',class_='sc-fzqARJ jzDIJt').text)[:7])
    ##('Number of Results: ', (numberOfResults))
    for post in listings:
    
        ##('Title: ',post.find(class_="sc-fzqMAW lxfBG").text)
        post_title = post.find(class_="sc-fzqMAW lxfBG").text
        ##('Location: ',post.find(class_="sc-fzqMAW ewUxzL").text)
        post_location = post.find(class_="sc-fzqMAW ewUxzL").text
        ##('Link: ',post.find(class_="sc-fzqMAW lxfBG").a['href'])
        post_url = post.find(class_="sc-fzqMAW lxfBG").a['href']
        ##('Coordinates: ',letgoLiner(post.find(class_="sc-fzqMAW ewUxzL").text))
        destination = letgoLiner(post.find(class_="sc-fzqMAW ewUxzL").text)
        urltwo = post.find(class_="sc-fzqMAW lxfBG").a['href']
        ##('second url', urltwo)
        responsetwo = requests.get(urltwo)
        datatwo = responsetwo.text
        souptwo = BeautifulSoup(datatwo,features='html5lib')
        ##(souptwo)
        try:
            link = souptwo.find(class_="wrapper").find(class_="sc-fzoyAV givzfL").find('img')['src']
        except AttributeError:
            link = 'bleh'
        post_image_url = link
        try:
            price = (souptwo.find(class_="wrapper").find(class_="sc-fzoyAV givzfL").find(class_='price').text)[3:]
        except AttributeError:
            price = None
        post_price = price

        # #.find(class_="sc-pHIBf hDBhPd")
        ##('Image Link: ',link)
        ##('Price: ',price)
        #link = str(link)
        ##''('link: ',link)
        ##('https://img'+link.split('img')[2]+'img_600')
        ##(souptwo)
        try:
            distance = str(round(geodesic(location,destination).km))
        except ValueError:
            distance = 'N/A'
        ##('Distance: ',distance)
        post_distance = distance
        ##('ID: ',(i))
        i +=1
        if i == int(numberOfResults):
            break
        finalpostings.append([post_title,post_url,post_price,post_image_url,post_distance,post_location])
    return(finalpostings)


letgoUrlMaker('1367 Chretien Street',10,10,2010,'Assassins Creed',[])

##(letgoLiner('Milton, L9T 0P4'))
#https://www.letgo.com/en-ca?distance=10&latitude=43.4819335&longitude=-79.8491818&price%5Bmax%5D=10&price%5Bmin%5D=20008&searchTerm=PS4
#https://www.letgo.com/en-ca?distance=10&latitude=43.4850031&longitude=-79.8545778&price%5Bmax%5D=2000&price%5Bmin%5D=10&searchTerm=ps4
#



