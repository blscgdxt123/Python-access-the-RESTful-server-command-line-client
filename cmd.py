import argparse
import requests
import json

# Creating an output dictionary
def creatDict(info_split, infoDict):
    href = info_split['href']
    temp = info_split['data']
    data = '\nname:' + temp[0]['value'] + '\nstudent id: ' + temp[1]['value'] + '\nemail: ' + temp[2]['value'] + \
    '\ntelephone number: ' + temp[3]['value'] + '\nhobby ' + temp[4]['value'] + '\nSerial number ' + href[26:]
    infoDict[temp[5]['value']] = data
    return infoDict

# Adding Information
def add(args):
    url = "http://localhost:1337/api/"
    try:
        payload = "{\r\n\"template\" : {\r\n\"data\": [\r\n{\r\n\"name\": \"name\",\r\n\"value\":\"" \
        + args.n \
        + "\",\r\n\"prompt\": \"name\"\r\n},\r\n{\r\n\"name\": \"studentid\",\r\n\"value\": \"" \
        + args.s \
        + "\",\r\n\"prompt\": \"student id\"\r\n},\r\n{\r\n\"name\": \"email\",\r\n\"value\": \"" \
        + args.e \
        + "\",\r\n\"prompt\": \"email\"\r\n},\r\n{\r\n\"name\": \"phone\",\r\n\"value\": \"" \
        + args.p \
        + "\",\r\n\"prompt\": \"telephone number\"\r\n},\r\n{\r\n\"name\": \"hobby\",\r\n\"value\": \"" \
        + args.b \
        + "\",\r\n\"prompt\": \"hobby\"\r\n}\r\n]\r\n}\r\n}"
        headers = {
        'Content-Type': 'text/html'
        }
        response = requests.request("POST", url, headers=headers, data=payload.encode())
        print("Adding succeeded")
    except:
        print("Failed to add information, please enter 'python cmd.py a -h' to view Help")
# Get Information
def get_list(args):
    url = "http://localhost:1337/api/"
    headers = {
    'Content-Type': 'text/html'
    }
    try:
        response = requests.request("GET", url, headers=headers)

        info = response.text
        #The valid fragment of info is captured
        info = info[269:-972]
        info = info.split("]\n    },")
        length = 0
        for item in info:
            length += 1
        infoDict = {}
        for i in range(length):
            if i == length -1:
                info_split = json.loads(info[i])
                infoDict = creatDict(info_split, infoDict)
            else:
                info_split = json.loads(info[i] + "]\n    }")
                infoDict = creatDict(info_split, infoDict)
        if args.m == 'ascend':
            judge_reverse = False
        if args.m == 'descend':
            judge_reverse = True
        sortedDict = sorted(infoDict, reverse=judge_reverse)
        print("Achieve success")
        for key in sortedDict:
            print(f'\n{key}:{infoDict[key]}')
    except:
        print("Failed to obtain information, please enter 'python cmd.py l -h' to view Help")
# Deleting Information
def delete_info(args):
    url = "http://localhost:1337/api/"
    url = url + args.o
    payload={}
    headers = {}
    try:
        response = requests.request("DELETE", url, headers=headers, data=payload)
        print("Successfully deleted")
    except:
        print("Failed to delete information, please enter 'python cmd.py d -h' to view Help")
# Update Information
def update_info(args):
    url = "http://localhost:1337/api/"
    url = url + args.o
    try:
        payload = "{\r\n\"template\" : {\r\n\"data\": [\r\n{\r\n\"name\": \"name\",\r\n\"value\":\"" \
        + args.n \
        + "\",\r\n\"prompt\": \"name\"\r\n},\r\n{\r\n\"name\": \"studentid\",\r\n\"value\": \"" \
        + args.s \
        + "\",\r\n\"prompt\": \"student id\"\r\n},\r\n{\r\n\"name\": \"email\",\r\n\"value\": \"" \
        + args.e \
        + "\",\r\n\"prompt\": \"email\"\r\n},\r\n{\r\n\"name\": \"phone\",\r\n\"value\": \"" \
        + args.p \
        + "\",\r\n\"prompt\": \"telephone number\"\r\n},\r\n{\r\n\"name\": \"hobby\",\r\n\"value\": \"" \
        + args.b \
        + "\",\r\n\"prompt\": \"hobby\"\r\n}\r\n]\r\n}\r\n}"
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload.encode())
        print("Updated successfully")
    except:
        print("Failed to update information, please enter 'python cmd.py u -h' to view Help")

parser = argparse.ArgumentParser(prog='PROG')
subparsers = parser.add_subparsers(help='sub-command help')
#Adding a subcommand add
parser_a = subparsers.add_parser("a", help='Adding Information')
parser_a.add_argument('-n', type=str, help='name')
parser_a.add_argument('-s', type=str, help='student id')
parser_a.add_argument('-e', type=str, help='email')
parser_a.add_argument('-p', type=str, help='telephone Number')
parser_a.add_argument('-b', type=str, help='hobby')
#Setting the Default Function
parser_a.set_defaults(func=add)

#Adding a subcommand list
parser_l = subparsers.add_parser('l', help='Get the list of information')
parser_l.add_argument('-m', type=str, help='ascend or descend')
#Setting the Default Function
parser_l.set_defaults(func=get_list)

#Adding a subcommand list
parser_d = subparsers.add_parser('d', help='Deleting Specified Information')
parser_d.add_argument('-o', type=str, help='Serial number')
#Setting the Default Function
parser_d.set_defaults(func=delete_info)

#Adding a subcommand update
parser_u = subparsers.add_parser("u", help='Modifying Information')
parser_u.add_argument('-o', type=str, help='Serial number')
parser_u.add_argument('-n', type=str, help='name')
parser_u.add_argument('-s', type=str, help='student id')
parser_u.add_argument('-e', type=str, help='email')
parser_u.add_argument('-p', type=str, help='telephone number')
parser_u.add_argument('-b', type=str, help='hobby')
#Setting the Default Function
parser_u.set_defaults(func=update_info)

args = parser.parse_args()

#Execute function function
if args.func == add:
    add(args)  
elif args.func ==  get_list:
    get_list(args)
elif args.func ==  delete_info:
    delete_info(args)
elif args.func == update_info:
    update_info(args)