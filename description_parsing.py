import urllib2
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup

page= "http://news.google.com/news?ned=us&topic=n&output=rss"

def getURL():
    page = urllib2.urlopen("http://news.google.com/news?ned=uk&topic=n&output=rss")
    return(page)

def printFunc(x):
    print(x)

def getDescription():
    soup = BeautifulStoneSoup(getURL(), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    xml =  soup.rss.channel.item.description
    next_xml = soup.rss.channel.item.description.next
    description_contents = BeautifulSoup( next_xml )
    return description_contents

def processDescriptionWithSoup(article_description, article_subposition):
    description_contents = BeautifulSoup( article_description )
    sub_positions = []
    sub_position = article_subposition

    for anchor in description_contents.findAll('a'):
      href_from_description = str(anchor['href'])
      href_contents = anchor.contents[0]
      string_contents = str(href_contents)
      if 'img' in string_contents:
          contents = href_from_description.split("&url=")[1]
          contents = contents.split("?newsfeed")[0]
      else:
          contents = string_contents
      if 'guardian' in href_from_description:
        sub_positions.append( [sub_position, href_from_description, contents] )
      sub_position += 1

    return sub_positions
  