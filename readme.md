# Serverless Tram Time Display
## Realtime Tram Times for Nottingham

tram.py
-------

Shows tram data on the command line

**Prerequisites**: colorama and requests - Install with pip

**Usage**: $python3 tram.py *ATCOCode*

You can find the atco code for your stop in [ntm.csv](tramSearch/ntm.csv)

**Example**:

![Example Output](https://s3.eu-west-2.amazonaws.com/s3.rothe.uk/tram.py.example.png "Example Output")

tramDisplay
-----------

Needs to be deployed to AWS Lambda (or equivilent serverless infrastructure)

Prerequisites: requests module needs to be packaged along with the script. 

tramSearch
----------

Needs to be deployed to AWS Lambda (or equivilent serverless infrastructure)

Prerequisites: requests and mysql modules need to be packaged along with the script. 

Configuration for database containing ATCO stop information needs to be provided in db_config.py

You can find further information about the development and deployment of these scripts at
https://blog.rothe.uk/serverless-tram-time-display/

