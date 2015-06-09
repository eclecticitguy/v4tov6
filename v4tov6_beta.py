__author__ = 'wblack'

## Author: Will Black
## Project: IPv4 to IPv6 Address Conversion

from netaddr import *
from netaddr import IPAddress
from netaddr import valid_ipv4


facing = None
y = None
z = None

def join_ip(facing, net_type, first, second, third):
    return "2607:F380:000" + facing + ":0:" + "0:01" + net_type + first + ":" + second + ":" + third + "1"

def combine_ip(ip_input, cidr_len):
    return ip_input + "/" + cidr_len

## Convert user CIDR length into CENIC-standard IPv6 CIDR length
def cenic_cidr_std(cidr_input):
    return str(92 + cidr_input)

def v4_to_hex(v4_in):
    return str(IPAddress(v4_in).__hex__().lstrip("0x"))

## Start conversion and run until user stops by pressing N ##

user_input = True

while user_input is True:

    # # Enter IPv4 address from user

    ip_input = raw_input('Enter IPv4 Address: ')

    ## Confirm entered IPv4 address is valid, otherwise re-enter address until correct

    while valid_ipv4(ip_input, INET_PTON) is not True:
        ip_input = raw_input('IPv4 Address invalid. \nPlease enter a valid IPv4 Address: ')

    ## Convert confirmed IPv4 address into hexadecimal format using
    ## the netaddr.ip.IPAddress hex method and strip off the leading 0x

    hex_addr = v4_to_hex(ip_input)

    fst_grp = hex_addr[0]
    snd_grp = hex_addr[1:5]
    thd_grp = hex_addr[5:]


    print('The IPv4 address you entered was: ' + ip_input + '\n')

    while True:
        try:
            facing = int(raw_input('Enter 0 for "internal-facing" or 1 for "external-facing": '))
            if facing < 0 or facing > 1:
                facing = int(raw_input('Please choose either 0 or 1: '))
            break
        except ValueError:
            print "Please enter an integer"

    while True:
        try:
            y = int(raw_input('Enter Subnet mask length in CIDR notation (eg. 31 for /31): '))
            if y < 1 or y > 32:
                y = int(raw_input('Invalid input.  Please enter a number between 1 and 32'))
            break
        except ValueError:
            print "Please enter an integer"

    while True:
        try:
            z = int(raw_input('Enter Network Type ( HPR=0, DC=1, ISP=2, PeerNet=3 ): '))
            if z < 0 or z > 3:
                z = int(raw_input('Invalid input.  Please enter 0, 1, 2, or 3'))
            break
        except ValueError:
            print "Please enter an integer"


    ## Convert responses into strings for concatenation into CENIC IPv6 format

    facing = str(facing)
    z = str(z)

    ## Convert standard IPv6 address into string, so we can concatenate CIDR length into final formatted output
    ## Use netaddr.ip.IPAddress class to provide clean IPv6 formatting

    final_ip = str(IPAddress(join_ip(facing, z, fst_grp, snd_grp, thd_grp), 6))

    ## Print converted IPv4 to IPv6 address

    print ('\nThe converted IPv4 to IPv6 address is: ' + combine_ip(final_ip, cenic_cidr_std(y)))

    ## Ask whether to convert another.  If answer doesn't match Y or N, repeat question.

    user_response = None
    while user_response != "Y" and user_response != "N":
        user_response = str(raw_input('Do you want to convert another (Y or N)?  ')).upper()

    if user_response == "Y":
        user_input = True
    elif user_response == "N":
        user_input = False
    else:
        print "Something is wrong"