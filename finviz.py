import requests, re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


class FinViz:

    def __init__(self):

        # make the request
        request = requests.get('http://finviz.com/')
        # maxe the soup
        soup = BeautifulSoup(request.text, 'html5lib')
        # soup has been brewed
        self._html = soup
        # self._html = BeautifulSoup(requests.get('http://finviz.com/').text,'html5lib')
        self._data = list()

    def refresh(self):
        self.__reinitalize__()

    def _reinitialize(self):
        r = requests.get('http://finviz.com')
        self._html = BeautifulSoup(r.text)

    def _parseColumnData(self, data):
        ret_data = data.findChild()
        ret_data = list(ret_data.children)
        result = list()
        for idx in ret_data:
            try:
                # parse the given data, into
                result.append(self._parseText(idx.getText()))
            except:
                # None Type, scrapping None Object, skip.
                pass
        return result

    def _parseText(self, text):
        # use regex for faster parsing of text, searching
        # for numbers and words, better and faster.

        # define regEx pattern
        # "find all alpha upper and lower words
        # + one and unlimited timees
        # match words who may or may not have spcaes betweent hem and
        # are mixed caes zero to unliited times
        regExText = '[A-Z a-z]+'
        # match a number with at least 1 to unlimited length
        ##the number must have a period and 1 through 2 numbers after it
        # match fully if there is a '+' OR '-' ZERO or 1 times
        regExDigit = '(\+|-?\d+.\d{1,2})'
        # regExDigit = '(\d+.\d{1,2})'
        listText = re.findall(regExText, text)
        listDigit = re.findall(regExDigit, text)
        resultSet = {
            'index': listText[0],
            'price': listDigit[0],
            'change': listDigit[1],
            'volume': listDigit[2],
            'signal': listText[1]
        }
        # return the resulting dictionary
        return resultSet

    def getLeftColumn(self):
        data = self._getMainColumnData(0)
        a = self._parseColumnData(data)
        return a

    def getRightColumn(self):
        data = self._getMainColumnData(1)
        a = self._parseColumnData(data)
        return a

    def _getMainColumnData(self, column):
        # scrape the specific elements
        searchResult = self._html.findAll('table', {'class': 't-home-table'})

        # we just want the first or second matches
        return searchResult[column]

    def getTrends(self):
        left_col = self.getLeftColumn()
        right_col = self.getRightColumn()

        combined_dict = list()

        for i in left_col:
            combined_dict.append(i)
        for i in right_col:
            combined_dict.append(i)
        return combined_dict


def fetch():
    # Summarising data
    testObject = FinViz()
    data = testObject.getTrends()
    prices = []
    names = []
    for i in data:
        print('Company: {0}, Price: {1}, Change: {2} , Volume: {3}'.format(i["index"], i["price"], i["change"],
                                                                           i["volume"]))
        prices.append(i["price"])
        names.append(i["index"])
    summarise(prices, names)
    getportfolio(data)


def summarise(prices, names):
    fig, ax = plt.subplots()
    ax.set_xlabel('Company')
    ax.set_ylabel('Price')
    ax.set_title('Graph of Company vs Price')
    width = 1 / 1.5
    plt.xticks(rotation='vertical')
    plt.bar(names, prices, width, color="blue")
    plt.show()


def getportfolio(data):
    for i in data:
        url = "https://finviz.com/quote.ashx?t={0}".format(i["index"])
        print(url)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        print(len(soup.find_all('td')))


if __name__ == "__main__":
    fetch()
