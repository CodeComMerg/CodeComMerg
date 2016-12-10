import sqlite3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime
from datetime import datetime, date
from dateutil import parser

database_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        if __name__ == '__main__':
            database = SqliteExtDatabase('output.db')
        else:
            database = database_proxy

class CommitDBO(BaseModel):
    uuid = TextField(unique=False)
    _commit = TextField()
    CommitDate = DateTimeField()
    AuthorDate = DateTimeField()    
    Author = TextField()
    message = TextField()
    Commit = TextField()
    tag = TextField()


class CommitFileDBO(BaseModel):
    commit = ForeignKeyField(CommitDBO, related_name='files')
    file = TextField()
    action = TextField()
    removed = TextField()
    added = TextField()
    commit_date = DateTimeField()
    commit_author = TextField()


class Messages(BaseModel):
    message_id = CharField(primary_key=True)
    mailing_list_url = CharField()
    mailing_list = CharField()
    first_date = DateTimeField()
    first_date_tz = IntegerField()
    arrival_date = DateTimeField()
    arrival_date_tz = IntegerField()
    subject = CharField()
    message_body = TextField()
    is_response_of = CharField()
    mail_path = TextField()


class FileHistoryDBO(BaseModel):
    file = TextField()
    inactive_since = IntegerField()
    last_activity_after = IntegerField()
