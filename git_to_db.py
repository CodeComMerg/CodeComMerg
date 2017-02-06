from perceval.backend import uuid
from perceval.backends.core.git import (Git,
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
from datetime import datetime, date
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
import datetime
from playhouse.sqlite_ext import SqliteExtDatabase

from dbo import *
from optparse import OptionParser

usage = "Usage: %prog [options] -r path-to-repo -n repo-name -d database-name"
option_parser = OptionParser(usage=usage)
option_parser.add_option("-r", "--repo", metavar="REPO", help="Path to repo"),
option_parser.add_option("-n", "--name", metavar="NAME", help="Name of repo"),
option_parser.add_option("-d", "--database", metavar="DB", help="Name of the database"),

(options, args) = option_parser.parse_args()

if not options.repo or not options.name or not options.database:
    print (usage)
    sys.exit()

database = SqliteExtDatabase('%s.db' % options.database)
database_proxy.initialize(database)
database.connect()
database.create_tables([CommitDBO, CommitFileDBO, FileHistoryDBO], safe=True)

print('Extracting information for %s to %s...' % (options.repo, options.database))

try:
    with database.atomic():

        commit_count = 0

        git = Git(options.repo, options.name)
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

                message = (data['message'])
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
                            commit_date=date_parser.parse(commit_dbo.CommitDate),
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

        # process files in-activities
        try:
            files = CommitFileDBO.select((fn.Distinct(CommitFileDBO.file)))

            for f in files:
                print('File:' + f.file)
                
                commits = CommitFileDBO.select().where(CommitFileDBO.file==f.file).order_by(-CommitFileDBO.commit_date)
                
                if commits.count() > 0:
                    last = commits[0]
                    last_commit_on = date_parser.parse(last.commit_date)
                    last_commit_on = last_commit_on.replace(tzinfo=None)
                    datetime_on = datetime.now()
                    inactive_since_obj = datetime_on - last_commit_on
                    inactive_since = inactive_since_obj.days
                    print('--- --- days since last activity %s days' % inactive_since)

                if commits.count() > 1:
                    slast = commits[1]           
                    last_activity_after_obj = date_parser.parse(last.commit_date) - date_parser.parse(slast.commit_date)
                    last_activity_after = last_activity_after_obj.days
                    print('--- --- last activity was after %s days' % last_activity_after)
                else:
                    last_activity_after = -1

                file_history = FileHistoryDBO(
                    file=f.file,
                    number_of_activities=commits.count(),
                    last_activity_after=last_activity_after,
                    inactive_since=inactive_since
                )
                file_history.save()
            print('SUCCESS: %s files history added to db.' % files.count())                
        except Exception as e:
            print('Error processing file activities.')
            print(e)
except Exception as e:
    print('ERROR')
    print(e)


