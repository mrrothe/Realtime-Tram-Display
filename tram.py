import colorama as col
import requests

def print_info(text):
    print(col.Fore.BLUE + "[-] " + text)
def print_good(text):
    print(col.Fore.GREEN + "[+] " + text)
def print_bad(text):
    print(col.Fore.RED + "[!] " + text)


tram_data=requests.get("https://robinhood.arcticapi.com/network/stops/9400ZZNOESK2/visits").json()
visits=tram_data["_embedded"]["timetable:visit"]
for visit in visits:
     if visit['isRealTime']:
             print_info('Destination: ' + visit['destinationName'])
             if visit['expectedArrivalTime']==visit['aimedArrivalTime']:
                    print_good("On Time")
             else:
                    print_bad("Late")
             print_info('Time to Tram: ' + visit['displayTime'])
             print("  ")