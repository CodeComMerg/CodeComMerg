# CodeComMerg

# Description

Code Communication Merge is designed to extract history of commit data of projects hosted on GitHub. The tool reuses code from another open source tool from https://github.com/grimoirelab/perceval. The main obejective of CodeComMerg is to link commit data with various communication channels such as mailing list, IRC and others. This tool will be used for the current ongoing Ph.D research in the area of Free Libre/ Open Source Software (FLOSS).

# Download

git clone https://github.com/CodeComMerg/CodeComMerg.git
    
    
# Installations

1- cd CodeCommMerg (Goto the the directory of the project)

2- run: pip install -r requirements.txt in your shell. (To install (all) the dependencies of our script like preceval or peewe. Activate your virtualenv first, if you want to use one.)

# Usage

python git_to_db.py [options] -r path-to-repo -n repo-name -d database-name

Options:

  -h, --help            show this help message and exit
  
  -r REPO, --repo=REPO  Path to repo
  
  -n NAME, --name=NAME  Name of repo
  
  -d DB, --database=DB  Name of the database
  
  
# License

Licensed under GNU General Public License (GPL), version 3 or later.




