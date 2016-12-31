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
    number_of_activities = IntegerField()
    last_activity_after = IntegerField()
    inactive_since = IntegerField()


class EmailDBO(BaseModel):
    email_from = TextField(null=True)
    email_to = TextField(null=True)
    email_date = TextField(null=True)
    precedence = TextField(null=True)
    received_spf = TextField(null=True)
    return_path = TextField(null=True)
    delivered_to = TextField(null=True)
    subject = TextField(null=True)
    unixfrom = TextField(null=True)
    reply_to = TextField(null=True)
    list_unsubscribe = TextField(null=True)
    x_asf_spam_status = TextField(null=True)
    in_reply_to = TextField(null=True)
    received = TextField(null=True)
    x_spam_check_by = TextField(null=True)
    references = TextField(null=True)
    list_help = TextField(null=True)
    content_transfer_encoding = TextField(null=True)
    x_original_to = TextField(null=True)
    user_agent = TextField(null=True)
    list_post = TextField(null=True)
    message_id = TextField(null=True)
    mailing_list = TextField(null=True)
    mime_version = TextField(null=True)  
    content_type = TextField(null=True)
    list_id = TextField(null=True)
    body_plain = TextField(null=True)
