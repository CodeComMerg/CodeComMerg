from perceval.backend import uuid
from perceval.backends.git import (Git,
                                   GitCommand,
                                   GitParser,
                                   GitRepository)
import argparse
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import dateutil.tz
from dateutil.relativedelta import relativedelta
import datetime

from dbo import *
from optparse import OptionParser

usage = "usage: %prog [options] -r path-to-repo"
parser = OptionParser(usage=usage)
parser.add_option("-r", "--repo", metavar="REPO", help="Path to repo"),

(options, args) = parser.parse_args()

print('Extracting information for %s...' % options.repo)

try:
    with db.atomic():

        commit_count = 0

        git = Git(options.repo, 'repo')
        commits = git.fetch()

        for commit in commits:
            try:
                commit_count += 1

                uuid = commit['uuid']
                tag = commit['tag']

                data = commit['data']
                
                AuthorDate = data['AuthorDate']
                _commit = data['commit']
                CommitDate = data['CommitDate']
                Author = data['Author']

                message = data['message']
                Commit = data['Commit']
        
                commit_dbo = CommitDBO(
                    uuid=uuid,
                    _commit=_commit,
                    CommitDate=CommitDate,
                    AuthorDate=AuthorDate,
                    Author=Author,
                    message=message,
                    Commit=Commit,
                    tag=tag
                )
                commit_dbo.save()
                print(message)

                for f in data['files']:
                    try:
                        print('--' + f['file'])
                        file = f['file']
                        if 'action' in f: 
                            action = f['action'] 
                        else: 
                            action = 'X'

                        if 'removed' in f: 
                            removed = f['removed'] 
                        else: 
                            action = 'X'

                        if 'added' in f: 
                            added = f['added'] 
                        else: 
                            action = 'X'

                        commit_file_dbo = CommitFileDBO(
                            commit=commit_dbo,
                            commit_date=commit_dbo.CommitDate,
                            file=file,
                            action=action,
                            removed=removed,
                            added=added,
                            commit_author=commit_dbo.Author
                        )
                        commit_file_dbo.save()
                    except Exception as fex:
                        print('FILE ERROR')
                        print(fex)
            except Exception as cex:
                print('COMMIT ERROR')
                print(cex)
        print('SUCCESS: %s commits added to db.' % commit_count)
except Exception as e:
    print('ERROR')
    print(e)

