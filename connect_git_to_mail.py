from perceval.backends.pipermail import Pipermail
from perceval.backends.mbox import MBox, MBoxArchive
from playhouse.sqlite_ext import SqliteExtDatabase
from dbo import *
import re
from datetime import datetime, timedelta
from dateutil import parser as date_parser

try:
    # database = SqliteExtDatabase('%s.db' % options.database)
    database = SqliteExtDatabase('httpd-dev.db')
    database_proxy.initialize(database)
    database.connect()
    database.create_tables([CommitToEmailDBO], safe=True)

    NUMBER_OF_DAYS = 1000

    commits_from_unique_authors = CommitDBO.select(CommitDBO.Author).distinct()
    list_of_unique_authors = [re.search('<(.*)>', a.Author).group(1) for a in commits_from_unique_authors]

    emails_from_unique_users = EmailDBO.select(EmailDBO.email_from).distinct()

    list_of_unique_mailers = []
    for e in emails_from_unique_users:
        try:
            email = re.search('<(.*)>', e.email_from).group(1)
        except Exception as eX:
            email = e.email_from
        list_of_unique_mailers.append(email)

    common_users_of_git_and_emails = set(list_of_unique_authors) & set(list_of_unique_mailers)

    print('[%s] Common users in git and emails.' % (str(datetime.now())))
    for u in common_users_of_git_and_emails:
        print(u)

    if len(common_users_of_git_and_emails) > 0:
        total_connections_made = 0
        try:
            with database.atomic():
                all_the_commits = CommitDBO.select()
                for commit in all_the_commits:
                    author_of_this_commit = re.search('<(.*)>', commit.Author).group(1)
                    if any(author_of_this_commit in s for s in common_users_of_git_and_emails):
                   
                        commit_date = date_parser.parse(commit.CommitDate)
                        commit_from_date = commit_date - timedelta(days=NUMBER_OF_DAYS)
                        commit_from_date = commit_from_date.strftime("%Y-%m-%d")

                        commit_to_date = commit_date + timedelta(days=NUMBER_OF_DAYS)
                        commit_to_date = commit_to_date.strftime("%Y-%m-%d")

                        emails_of_this_author = EmailDBO.select().where(EmailDBO.email_from.contains(author_of_this_commit), EmailDBO.email_date.between(commit_from_date, commit_to_date))
                        print('[%s] Finding communication for commit # %s - %s by %s.' % (str(datetime.now()), commit.uuid, commit.message, commit.Author))
                        for email in emails_of_this_author:
                            total_connections_made+=1
                            print('[%s] - [%s] connection found.' % (str(datetime.now()), str(total_connections_made)))
                            commit_to_email = CommitToEmailDBO(commit=commit, email=email)
                            commit_to_email.save()
        except Exception as ex:
            print('Error : %s.' % ex)
            raise
            
    print('Program completed successfully. %s Total connections are made.' % total_connections_made)
except Exception as ex:
    print('Program exited with an error. %s' % ex)