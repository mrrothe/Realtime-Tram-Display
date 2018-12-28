import mysql.connector
import json
from string import Template
import db_config # Import database configuration from file
html_template="""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Tram Time Display</title>
<meta name="viewport" content="width=device-width, user-scalable=no">
<style>
.searchresult{
    background-color: grey;
    margin: 20px;
    padding: 20px;
    display: block;
    font-family: Sans-Serif;
    font-size: 1.6em;
    }
    .searchresult:hover {
background-color: green;
    }
a {
    color: wheat;
    text-decoration: none;
}
.searchdetail {
    margin: 20px;
}
</style>
</head>
<body>
"""
searchspan=Template("""
<span class="searchresult">
<a href="/tramdisplay/tramTimes?stop=$code">
            <span class="searchdetail CommonName">$name</span>
            <span class="searchdetail Landmark">$landmark</span>
            <span class="searchdetail Street">$street</span>
            <span class="searchdetail Platform">$platform</span>
            <span class="searchdetail Locality">$locality</span>
            <span class="searchdetail Suburb">$suburb</span>
            </a>
            </span>
""")
def response(message, status_code):
    return {
        'statusCode': str(status_code),
        'body': message,
        'headers': {
            'Content-Type': 'text/html',
            },
        }

def lambda_handler(event, context):
    if "queryStringParameters" in event and "search" in event['queryStringParameters']:
        searchstring='%'+event['queryStringParameters']['search']+'%'
    else:
        return response("Please specify a search string ", 400)
    mydb = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password= password,
        database=database,
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM tramstops WHERE (CONCAT_WS(' ',CommonName,Landmark,Street,Platform,Locality,Suburb)) LIKE %s",(searchstring,))
    results=mycursor.fetchall()
    out=""
    for result in results:
        out+=(searchspan.substitute(name=result['CommonName'],landmark=result['Landmark'],street=result['Street'],platform=result['Platform'],locality=result['Locality'],suburb=result['Suburb'],code=result['ATCO']))
    return response(html_template+out+'</body></html>',200)

