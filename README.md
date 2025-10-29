# keepass4crack
python keepass4 cracker

``` 
usage: main.py [-h] -d DATABASE -w WORDLIST [-k KEYFILE] [-t THREADS]

simple multi-process brute-force tool for KeePass (.kdbx) files. Works with password-only or password+keyfile
setups.

options:
  -h, --help            show this help message and exit
  -d, --database DATABASE
                        Path to the KeePass .kdbx file
  -w, --wordlist WORDLIST
                        Text file with passwords to try, one per line
  -k, --keyfile KEYFILE
                        Optional keyfile to use if the database requires it
  -t, --threads THREADS
                        Number of parallel processes to use (default: all CPU cores)

``` 


```
uv run main.py -d target.kdbx -w /usr/share/wordlists/rockyou.txt -t 20
Database file : target.kdbx
Wordlist      : /usr/share/wordlists/rockyou.txt
Threads used  : 20

Loaded 14344306 passwords to test
Testing passwords :D:   0%|                                            | 45/14344306 [00:04<393:40:45 , 9.4 pwd/sec]
``` 



