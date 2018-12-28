import requests
import json
from string import Template
import re
html_template="""
<!doctype html>
<html lang="en">
<meta http-equiv="refresh" content="30" />
<head>
    <meta charset="utxf-8" />
    <title>Tram Time Display</title>
    <meta name="viewport" content="width=device-width, user-scalable=no">
    <style>
        @font-face {
            font-family: 'LCDDot TR';
            src: url('https://s3.rothe.uk/LCDDot-TR.woff2') format('woff2'),
                url('https://s3.rothe.uk/LCDDot-TR.woff') format('woff');
            font-weight: normal;
            font-style: normal;
        }
        body {
            background-color: slategrey;
        }
        #tramdisplay {
            background-color: darkslategrey;
            width: 90%;
            padding: 30px;
            margin: auto;
            color: orange;
            font-size: 6em;
            font-family: 'LCDDot TR';
        }
        .tramvisit {
            display: block;
            width: 100%;
        }
        .tramdetail {
            margin-bottom: 30px;
            float: left;
            display: block;
            width: 33%;
        }
        .destination {
            text-align: left
        }
        .time {
            text-align: right
        }
        .late {
            color: red;
            text-align: center;
        }
        .ontime {
            color: lime;
            text-align: center;
        }
        #realtime {
            color: #1E9CF1;
            font-size: 2em;
            margin: 30px;
        }
    </style>
</head>
<body>
    <div id="tramdisplay">
"""
def response(message, status_code): #Formats response for API gateway
    return {
        'statusCode': str(status_code),
        'body': message,
        'headers': {'Content-Type': 'text/html',},
        }

def lambda_handler(event, context):
    out="" # Initialise return string
    if "queryStringParameters" in event and "stop" in event['queryStringParameters']: # If stop paremter is defined
        stop=event['queryStringParameters']['stop']
    else:
        error="Please specify a stop"
        return response(error, 400)
    stop = re.sub('\W+','',stop) # Strip non alphanumeric characters from search string
    tram_data = requests.get("https://robinhood.arcticapi.com/network/stops/"+stop+"/visits").json()
    visits = tram_data["_embedded"]["timetable:visit"]
    v=0 # Initialise counter
    for visit in visits:
        if visit['isRealTime'] and v<5: # limit maximum trams to display on screen - adjust to match screensize
            v+=1
            if visit['expectedArrivalTime'] == visit['aimedArrivalTime']: # If tram is running to expected time
                ontime = "On Time"
                ontimeclass="ontime"
            else:
                ontime = "Late"
                ontimeclass="late"
            tramspan=Template("""<span class="tramvisit" id="tv_1">
            <span class="tramdetail destination">$dest</span>
            <span class="tramdetail $ontimeclass">$ontime</span>
            <span class="tramdetail time">$time</span>
            </span>""")
            out+=(tramspan.substitute(dest=visit['destinationName'],ontimeclass=ontimeclass,ontime=ontime,time=visit['displayTime']))
    return response(html_template+out+'<div id="realtime"> </div><script>function updateClock() {var now = new Date();document.getElementById("realtime").innerHTML = ((now.getHours()<10?"0":"")+now.getHours() + ":" + (now.getMinutes()<10?"0":"")+now.getMinutes()+ ":" + (now.getSeconds()<10?"0":"")+now.getSeconds());setTimeout(updateClock, 1000);};updateClock();</script></body></html>', 200)
    