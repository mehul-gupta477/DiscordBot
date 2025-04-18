import feedparser


# parses the RSS feed and makes a list of all event dictionaries

# each event contains: Type, Title, Description, whenDate, pubDate, Location, and link

def getEvents(url):
    
    data = feedparser.parse(url)
    events = []
    
    for entry in data['entries']:
        descrip = entry.get("description", "")
        when = ""
        location = ""
        
        # gets the whenDate and the Location by string manipulation
        # if unable to find, then keeps it empty
        if "When:" in descrip: 
            try:
                when = descrip.split("When:")[1].split("\n")[0].strip()
            except IndexError:
                when = ""

        if "Location:" in descrip:
            try:
                location = descrip.split("Location:")[1].split("\n")[0].strip()
            except IndexError:
                location = ""

        event = {
            "Type" : "Event",
            "Title" : entry.get("title", ""),
            "Description" : descrip,
            "whenDate" : when,
            "pubDate" : entry.get("published", ""),
            "Location" : location,
            "link" : entry.get("link", "")
        }

        events.append(event) # list of each event which is stored in a dictionary
    
    return events
    


