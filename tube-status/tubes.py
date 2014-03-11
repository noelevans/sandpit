from urllib import urlopen

statusURL = "http://www.tfl.gov.uk/tfl/livetravelnews/realtime/tube/default.html"
startTag = '<dl id="lines">'
endTag = "<h2>Tube stations</h2>"
statusPage = urlopen(statusURL).read()

start = statusPage.find(startTag)
end = statusPage.find(endTag)

stati = statusPage[start+len(startTag):end]
stati = stati.replace("\n", "")

def tubeLines(input):
    lines = 




re.findall('<dt class=".*">(.*)</dt>'	, samp)

