__author__ = 'wblack'

## Author: Will Black
## Project: IPv4 to IPv6 Address Conversion

from netaddr import *

t = None
y = None
z = None

user_input = True

while user_input is True:

    # # Enter IPv4 address from user

    ip_input = raw_input('Enter IPv4 Address: ')

    ## Confirm entered IPv4 address is valid, otherwise re-enter address until correct

    while valid_ipv4(ip_input, INET_PTON) is not True:
        ip_input = raw_input('IPv4 Address invalid. \nPlease enter a valid IPv4 Address: ')

    ## Convert confirmed IPv4 address into hexadecimal format using
    ## the netaddr.ip.IPAddress hex method and strip off the leading 0x

    v4_hex = (IPAddress(ip_input).__hex__()).lstrip("0x")

    ## Parse converted hex IPv4 address into three groups that will be later used in final IPv6 address

    fst_grp = v4_hex[0]
    snd_grp = v4_hex[1:5]
    thd_grp = v4_hex[5:len(v4_hex)]

    print('The IPv4 address you entered was: ' + ip_input + '\n')

    while True:
        try:
            t = int(raw_input('Enter 0 for "internal-facing" or 1 for "external-facing": '))
            if t < 0 or t > 1:
                t = int(raw_input('Please choose either 0 or 1: '))
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

    ## Convert user CIDR length into CENIC-standard IPv6 CIDR length

    cidr_len = (str(92 + y))

    ## Convert responses into strings for concatenation into CENIC IPv6 format

    t = str(t)
    y = str(y)
    z = str(z)

    ## Combine parsed hex values and user input values into standard IPv6 address

    joined_ip = (
        "2607:F380:000" + t + ":0:" + "0:01" + z + fst_grp + ":" + snd_grp + ":" + thd_grp + "1")

    ## Convert standard IPv6 address into string, so we can concatenate CIDR length into final formatted output
    ## Use netaddr.ip.IPAddress class to provide clean IPv6 formatting

    final_ip = str(IPAddress(joined_ip, 6))

    ## Concatenate converted IPv6 address with CIDR length

    final_net = final_ip + "/" + cidr_len

    ## Print converted IPv4 to IPv6 address

    print ('\nThe converted IPv4 to IPv6 address is: ' + final_net)
    print ('IPv6 Network address for input IPv4 address: ' + (str(IPNetwork(final_net).network)))
    print ('IPv6 Broadcast address for input IPv4 address: ' + (str(IPNetwork(final_net).broadcast)) + '\n')

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