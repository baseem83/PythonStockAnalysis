import urllib
import json

class Stock(object):
    Stocks = []
    def __init__(self, symbol = None, sname = None, price = None, volume = None, avgVolume = None):
        self.Symbol = symbol
        self.Sname = sname
        self.Price = price
        self.Volume = volume
        self.AvgVolume = avgVolume
        self.VolumeRatio = self.CalcVolumeRatio()
        Stock.Stocks.append(self)
        
    def __lt__(self, other):
        # For the purposes of this application, stocks are compared by VolumeRatio
        # Stocks are sorted by VolumeRatio to determine daily activity

        try:
            return self.VolumeRatio < other.VolumeRatio
        except AttributeError:
            print 'Stocks can only be compared to other Stock instances'
        
    def CalcVolumeRatio(self):
        ''' Calculates the current volume to the average daily volume 
        '''
        return float(self.Volume) / float(self.AvgVolume)

try:
    # The list of stocks in which we are interested is stored in the below file.
    file = open('tickers.txt', 'r')
except IOError:
    print 'Error opening file. Aborting ...'
    exit()
    
# Below creates the path to the Yahoo query engine    
tickers = ",".join(['"' + line.strip() + '"' for line in file]).replace(' ', '%20')
path = "https://query.yahooapis.com/v1/public/yql?q="
qry = "select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20("
extension = "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
webaddress = path + qry + tickers + ")" + extension

try:
    website = urllib.urlopen(webaddress)
except IOError:
    print 'Website inaccessible. Aboring ... '
    exit()
   
#Parse the data that is returned into a JSON object
json_data = json.loads(website.read())

#Below can be commented out. The JSON is dumped into a txt file for inspection
#This is helpful with new JSON to determine syntax and to plan reading data
with open('jsoninfo.txt', 'w') as writeFile:
    writeFile.write("JSON Data\n")
    writeFile.write("===================================\n")
    json.dump(json_data, writeFile)
 
for stck in json_data["query"]["results"]["quote"]:
    try:
        Stock(stck['symbol'], stck['Name'], float(stck['Ask']), float(stck['Volume']), float(stck['AverageDailyVolume']))
    except TypeError: #used to handle situations wherein details for the stock are null for the day. Different business logic can be added if needed.
        continue
    
Stock.Stocks.sort()

for st in Stock.Stocks:
    print st.Symbol, ':', st.VolumeRatio