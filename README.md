## My orchestration tool
### You must have python3 installed and pip3 check it [here](https://docs.python-guide.org/starting/install3/linux/)
### How to install it (be sure you are on the project dir - root level)
```
python3 -m virtualenv env
. ./env/bin/activate 
pip3 install -r Pipfile.lock
```

## How to create a instruction:
[Yaml format](https://en.wikipedia.org/wiki/YAML)
```
version "1.0"
jobs:
  env_vars: # It will pass over every shell execution to the ssh session
    - FOO=bar
    - BAR=foor
  # First execution
  before_install: # will be the first block to execute
     - shell: # One line instruction to execute
       metadata: # dict with aditional instruction
         sudo: true |false # Execute as sudo 

  # Second block execution
  install: # will be executed after before_install
     - package: # string containing list of packages ex: "apache culr vil"
       metadata: # dict with aditional instruction
         sudo: true |false # Execute as sudo
         notify: "job:name" # Execute any shell block after this package has been instaled
  # Third block execution
  dirs:
     - destination: # path where you want to create on remote server
       metadata: # dict with aditional instruction
         sudo: true |false # Execute as sudo
         owner: "root" # owner of the path (chown -R)
         group: "root" # group of the path (chown -R)
         chmod: "755" # mode of the path (chmod )
         notify: "job:other_name" # Execute any shell block after this path has been created instaled

  # Fiveth block execution
  templates: # Instructions to create a file or update 
     - destination: # Path and file to be created to the remote server
       metadata: # dict with aditional instruction
         sudo: true |false # Execute as sudo
         owner: "root" # owner of the path (chown -R)
         group: "root" # group of the path (chown -R)
         chmod: "755" # mode of the path (chmod )
         notify: "job:other_name" # Execute any shell block after this path has been created instaled

  # Last block execution
  execute: # Final execution
    - name: # Name of the step
      metadata:
        sudo: true |false # Execute as sudo
        shell: "service x restart" # shell one line execution
```

After the yaml ready, fire:
```
python3 slk.py --servers 192.168.1.2:2222 192.168.1.4 192.168.1.5:2222  --user=my_user --password=my_pass -c ./tasks.yml
```
or
```
python3 slk.py --servers 192.168.1.2:2222 192.168.1.4 192.168.1.5:2222  --user=my_user --ssh-key=./path/to/my/key -c ./tasks.yml
```
or 
```
python3 slk.py --servers 192.168.1.2:2222 192.168.1.4 192.168.1.5:2222  --user=my_user --ssh-key=./path/to/my/key --password=my_key_pass -c ./tasks.yml
```

## Script options
```
usage: slk.py [-h] [-c CONFIG] [-u USERNAME] [-s SERVERS [SERVERS ...]]
              [--ssh-key SSH_KEY] [--password PASSWORD]

Manage my default app

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
  -u USERNAME, --username USERNAME
  -s SERVERS [SERVERS ...], --servers SERVERS [SERVERS ...]
  --ssh-key SSH_KEY     Path ssh key to connect to the server
  --password PASSWORD   Password to connect

```
