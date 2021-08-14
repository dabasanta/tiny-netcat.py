# Tiny-netcat.py

![](https://raw.githubusercontent.com/dabasanta/tiny-netcat.py/main/examples/netcat-logo.jpg)

**tiny-netcat** is a python script that provide shell access for remote connections through sockets.

Is util in systems were socat, netcat or nc binary is missing and you need an intermediate way to gain initial access.

## Dependencies

- __Python3__ or __Python2__ installed in the host
- Use in **Linux** hosts

## Use cases

Ideal for __initial access__ phase were a blind *RCE* is commonly obtained. Feel you free to prescind of the parameters if you cannot execute the script with arguments; in this cases, you can replace the *argparse* parameters with a  static variable host/port to bind there.

## Usage
The script is very simple: Use *-h* or run it without parameters to obtain a help message.
```bash
./tiny-netcat.py <-h|--help>

usage: tiny-netcat.py [-h] [-i HOST] [-p PORT]

Simple NetCat alternative

optional arguments:
  -h, --help            show this help message and exit
  -i HOST, --host HOST  Host were listen for incoming connections
  -p PORT, --port PORT  Port were listen for incoming connections

Example:
    ./netcat.py -h 10.10.10.100 -p 5555

    You can connect to the socket by using netcat or nc in the attacker computer:
        netcat|nc 10.10.10.100 5555
        nc>
```
Use **-i** to set the IPv4 address where you want bind the shell.
Use **-p** to set the port where you wnat listen. Default port is 4444.

You can connect to the socket using netcat or nc.

![](https://raw.githubusercontent.com/dabasanta/tiny-netcat.py/main/examples/ConnectionExample.png)

## Limitations
This is a very limited shell, his purpose is not be a interactive shell, is provide a shell access when another tools went failed.


