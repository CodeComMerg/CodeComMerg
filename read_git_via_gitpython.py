from git import *
import datetime

try:
    repo = Git('/home/mrx/src/gitmail/src/repo/perceval')
    fromdate = datetime.datetime(2016, 1, 1, 0, 0)

    commits = list(repo.iter_commits())
    _files = []

    print(len(commits))

    for commit in commits:
        email = commit.author.email
        name = commit.author.name
        message = commit.message

        print(name)        
        print(email) 
        print(message) 

        for _file in commit.stats.files:
            if(_files.count(_file) == 0):
                _files.append(_file)
                from_file = repo.from_file(_file)
                print(from_file)
                to_file = repo.to_file(_file)
                print(to_file)
    print(len(_files))
except Exception as e:
    print(e)