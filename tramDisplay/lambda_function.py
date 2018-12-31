import requests
import json
from string import Template
import re
html_template="""
<meta http-equiv="refresh" content="30">
<html lang="en">
<head>
<meta charset="utf-8">
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
body{
    background-color:darkslategrey;
    
}
#tramdisplay{
    width: 100%;
    padding: 30px;
    color: orange;
    font-size:  8vw;
    font-family: 'LCDDot TR';
    display: grid;
    grid-template-columns: 40% 25% 35%;
    grid-column-gap: 3vw;
    grid-row-gap: 2vw;
}
.destination {
  grid-column-start: 1;
  grid-column-end: 2 ;
}
.time {
  grid-column-start: 3;
  grid-column-end: 4;
}
.late {
    grid-column-start: 2;
    grid-column-end: 3;
    color: red;
}
.ontime {
    grid-column-start: 2;
    grid-column-end: 3;
    color: lime;
}
#realtime{
    color: #1E9CF1;
    font-size:  14vw;
    grid-column-start: 1;
    grid-column-end: 3;
}
</style>
</head>
<body>
<div id="tramdisplay">
"""
def response(message, status_code):
    return {
        'statusCode': str(status_code),
        'body': message,
        'headers': {
            'Content-Type': 'text/html',
            },
        }

def lambda_handler(event, context):
    out=""
    if "queryStringParameters" in event and "stop" in event['queryStringParameters']:
        stop=event['queryStringParameters']['stop']
    else:
        error="Please specify a stop"
        return response(error, 400)
    stop = re.sub('\W+','',stop)
    print(stop)
    tram_data = requests.get("https://robinhood.arcticapi.com/network/stops/"+stop+"/visits").json()
    visits = tram_data["_embedded"]["timetable:visit"]
    v=0
    for visit in visits:
        if visit['isRealTime'] and v<5:
            v+=1
            if visit['expectedArrivalTime'] == visit['aimedArrivalTime']:
                ontime = "On Time"
                ontimeclass="ontime"
            else:
                ontime = "Late"
                ontimeclass="late"
            tramspan=Template("""
            <span class="tramdetail destination">$dest</span>
            <span class="tramdetail $ontimeclass">$ontime</span>
            <span class="tramdetail time">$time</span>
            """)
            out+=(tramspan.substitute(dest=visit['destinationName'],ontimeclass=ontimeclass,ontime=ontime,time=visit['displayTime']))
    return response(html_template+out+'<div id="realtime"> </div><script>function updateClock() {var now = new Date();document.getElementById("realtime").innerHTML = ((now.getHours()<10?"0":"")+now.getHours() + ":" + (now.getMinutes()<10?"0":"")+now.getMinutes()+ ":" + (now.getSeconds()<10?"0":"")+now.getSeconds());setTimeout(updateClock, 1000);};updateClock();</script></body></html>', 200)