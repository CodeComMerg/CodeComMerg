from perceval.backends.core.pipermail import Pipermail
from perceval.backends.core.mbox import MBox, MBoxArchive
from playhouse.sqlite_ext import SqliteExtDatabase
from dbo import *
from optparse import OptionParser
import sys, traceback
import json 
from dateutil import parser as date_parser
import re

try:
    # python mail_to_db.py -u 'http://mail-archives.apache.org/mod_mbox/httpd-dev/' -n 'httpd-dev' -d 'httpd-dev' -b mbox
    usage = "Usage: %prog [options] -u uri-to-email-archieve -n folder-name -d database-name -b pipermail or mbox"
    option_parser = OptionParser(usage=usage)
    option_parser.add_option("-u", "--uri", metavar="URI", help="URI to archieve"),
    option_parser.add_option("-n", "--name", metavar="NAME", help="Name of the folder"),
    option_parser.add_option("-d", "--database", metavar="DB", help="Name of the database"),
    option_parser.add_option("-b", "--backend", metavar="BACKEND", help="Name of the backend"),

    (options, args) = option_parser.parse_args()

    # options.uri = 'http://mail-archives.apache.org/mod_mbox/httpd-dev/'
    # options.name = 'httpd-dev-pm'
    # options.database = 'httpd-dev-pm'
    # options.backend = 'pipermail'


    if not options.uri or not options.name or not options.database or not options.backend:
        print (usage)
        sys.exit()

    database = SqliteExtDatabase('%s.db' % options.database)
    database_proxy.initialize(database)
    database.connect()
    database.create_tables([EmailDBO], safe=True)

    print('Extracting information from %s to %s.db...' % (options.uri, options.database))

    if options.backend == 'pipermail':
        pipermail = Pipermail(options.uri, options.name)
        messages = pipermail.fetch()
    elif options.backend == 'mbox':
        mbox = MBox(uri=options.uri, dirpath=options.name)
        messages = mbox.fetch()

    print('Reading information from %s to insert into %s.db...' % (options.name, options.database))

    try:
        with database.atomic():
            success_messages_count = 0
            error_messages_count = 0
            for message in messages:
                try:

                    success_messages_count += 1
                    data = message['data']

                    email_from = data['From']

                    if 'To' in data:
                        email_to = data['To']
                    else:
                        email_to = 'NA'

                    if 'Date' in data:
                        email_date = data['Date']
                        email_date_modified = date_parser.parse(data['Date']).strftime("%Y-%m-%d")
                    else:
                        email_date = '1970-01-01'

                    if 'Precedence' in data:
                        precedence = data['Precedence']
                    else:
                        precedence = 'NA'                       

                    if 'Received-SPF' in data:
                        received_spf = data['Received-SPF']
                    else:
                        received_spf = 'NA'
                        
                    if 'Return-Path' in data:
                        return_path = data['Return-Path']
                    else:
                        return_path = 'NA'

                    if 'Delivered-To' in data:
                        delivered_to = data['Delivered-To']
                    else:
                        delivered_to = 'NA'

                    if 'Subject' in data:
                        subject = data['Subject']
                    else:
                        subject = 'NA'

                    if 'unixfrom' in data:
                        unixfrom = data['unixfrom']
                    else:
                        unixfrom = 'NA'

                    if 'Reply-To' in data:
                        reply_to = data['Reply-To']
                    else:
                        reply_to = 'NA'

                    if 'list-unsubscribe' in data:
                        list_unsubscribe = data['list-unsubscribe']
                    else:
                        list_unsubscribe = 'NA'                       

                    if 'X-ASF-Spam-Status' in data:
                        x_asf_spam_status = data['X-ASF-Spam-Status']
                    else:
                        x_asf_spam_status = 'NA'
                    
                    if 'In-Reply-To' in data:
                        in_reply_to = data['In-Reply-To']
                    else:
                        in_reply_to = 'NA'

                    if 'Received' in data:
                        received = data['Received']
                    else:
                        received = 'NA'    

                    if 'X-Spam-Check-By' in data:
                        x_spam_check_by = data['X-Spam-Check-By']
                    else:
                        x_spam_check_by = 'NA'

                    if 'References' in data:
                        references = data['References']
                    else:
                        references = 'NA'

                    if 'list-help' in data:
                        list_help = data['list-help']
                    else:
                        list_help = 'NA'    

                    if 'Content-Transfer-Encoding' in data:
                        content_transfer_encoding = data['Content-Transfer-Encoding']
                    else:
                        content_transfer_encoding = 'NA'
                    
                    if 'X-Original-To' in data:
                        x_original_to = data['X-Original-To']
                    else:
                        x_original_to = 'NA'

                    if 'User-Agent' in data:
                        user_agent = data['User-Agent']
                    else:
                        user_agent = 'NA'

                    if 'List-Post' in data:
                        list_post = data['List-Post']
                    else:
                        list_post = 'NA'

                    if 'Message-ID' in data:
                        message_id = data['Message-ID']
                    else:
                        message_id = 'NA'

                    if 'Mailing-List' in data:
                        mailing_list = data['Mailing-List']
                    else:
                        mailing_list = 'NA'

                    if 'MIME-Version' in data:
                        mime_version = data['MIME-Version']
                    else:
                        mime_version = 'NA'

                    if 'Content-Type' in data:
                        content_type = data['Content-Type']
                    else:
                        content_type = 'NA'

                    if 'List-Id' in data:
                        list_id = data['List-Id']
                    else:
                        list_id = 'NA'

                    if 'body' in data:
                        if 'plain' in data['body']:                        
                            body_plain = data['body']['plain']
                        elif 'html' in data['body']: 
                            body_plain = data['body']['html']
                    else:
                        body_plain = 'NA'
        
                    email_to = email_to.replace("\r","\t")
                    # email_date = email_date.replace("\r","\t")
                    precedence = precedence.replace("\r","\t")
                    received_spf = received_spf.replace("\r","\t")
                    return_path = return_path.replace("\r","\t")
                    delivered_to = delivered_to.replace("\r","\t")
                    subject = subject.replace("\r","\t")
                    unixfrom = unixfrom.replace("\r","\t")
                    reply_to = reply_to.replace("\r","\t")
                    list_unsubscribe = list_unsubscribe.replace("\r","\t")
                    x_asf_spam_status = x_asf_spam_status.replace("\r","\t")
                    in_reply_to = in_reply_to.replace("\r","\t")
                    received = received.replace("\r","\t")
                    x_spam_check_by = x_spam_check_by.replace("\r","\t")
                    references = references.replace("\r","\t")
                    list_help = list_help.replace("\r","\t")
                    content_transfer_encoding = content_transfer_encoding.replace("\r","\t")
                    x_original_to = x_original_to.replace("\r","\t")
                    user_agent = user_agent.replace("\r","\t")
                    list_post = list_post.replace("\r","\t")
                    message_id = message_id.replace("\r","\t")
                    mailing_list = mailing_list.replace("\r","\t")
                    mime_version = mime_version.replace("\r","\t") 
                    content_type = content_type.replace("\r","\t")
                    list_id = list_id.replace("\r","\t")


                    email_to = email_to.replace(",","\,")
                    # email_date = email_date.replace(",","\,")
                    precedence = precedence.replace(",","\,")
                    received_spf = received_spf.replace(",","\,")
                    return_path = return_path.replace(",","\,")
                    delivered_to = delivered_to.replace(",","\,")
                    subject = subject.replace(",","\,")
                    unixfrom = unixfrom.replace(",","\,")
                    reply_to = reply_to.replace(",","\,")
                    list_unsubscribe = list_unsubscribe.replace(",","\,")
                    x_asf_spam_status = x_asf_spam_status.replace(",","\,")
                    in_reply_to = in_reply_to.replace(",","\,")
                    received = received.replace(",","\,")
                    x_spam_check_by = x_spam_check_by.replace(",","\,")
                    references = references.replace(",","\,")
                    list_help = list_help.replace(",","\,")
                    content_transfer_encoding = content_transfer_encoding.replace(",","\,")
                    x_original_to = x_original_to.replace(",","\,")
                    user_agent = user_agent.replace(",","\,")
                    list_post = list_post.replace(",","\,")
                    message_id = message_id.replace(",","\,")
                    mailing_list = mailing_list.replace(",","\,")
                    mime_version = mime_version.replace(",","\,") 
                    content_type = content_type.replace(",","\,")
                    list_id = list_id.replace(",","\,")


                    body_plain = re.escape(body_plain)
                    try:
                        email_dbo = EmailDBO(
                                        email_from = email_from,
                                        email_to = email_to,
                                        email_date = email_date,
                                        email_date_modified = email_date_modified,
                                        precedence = precedence,
                                        received_spf = received_spf,
                                        return_path = return_path,
                                        delivered_to = delivered_to,
                                        subject = subject,
                                        unixfrom = unixfrom,
                                        reply_to = reply_to,
                                        list_unsubscribe = list_unsubscribe,
                                        x_asf_spam_status = x_asf_spam_status,
                                        in_reply_to = in_reply_to,
                                        received = received,
                                        x_spam_check_by = x_spam_check_by,
                                        references = references,
                                        list_help = list_help,
                                        content_transfer_encoding = content_transfer_encoding,
                                        x_original_to = x_original_to,
                                        user_agent = user_agent,
                                        list_post = list_post,
                                        message_id = message_id,
                                        mailing_list = mailing_list,
                                        mime_version = mime_version, 
                                        content_type = content_type,
                                        list_id = list_id,
                                        body_plain = body_plain,
                        )
                        email_dbo.save()
                    except ValueError as ve:
                        print(ve)
                        raise
                    print('Saving email from %s to %s on %s...' % (email_from, email_to, email_date))

                except Exception as mex:
                    success_messages_count -= 1
                    error_messages_count += 1
                    print('ERROR READING AN EMAIL')
                    print(mex)
            print('SUCCESS: %s emails saved to db.' % success_messages_count)                
            print('ERROR: Unable to save %s emails.' % error_messages_count)                
    except Exception as tex:
        traceback.print_exc()
        print('ERROR DATABASE TRANSACTION')        
        print(tex)

except Exception as e:
        print(e)