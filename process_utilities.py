import os
import logging
import psutil
from datetime import datetime
import time
#from azure.communication.email import EmailClient, EmailContent, EmailAddress, EmailMessage, EmailRecipients

##------------------------------------ kill_process notes ------------------------------------
##  kill_process takes 3 arguments:
##    1. process name -> string, required
##    2. kill -> boolean, required
##    3. time limit (minutes) -> integer, optional (default: 60)
##
##  Syntax examples:
##    process_utilities.kill_process('chromedriver', True)
##      - kills active 'chromedriver' processes with uptime > 60 minutes (default is 60 minutes)
##    process_utilities.kill_process('chromedriver', True, 15)
##      - kills active 'chromedriver' processes with uptime > 15 minutes
##    process_utilities.kill_process('chromedriver', False)
##      - produces logging statements to give info on 'chromedriver' proceses
##      - returns a python dictionary of processes
##---------------------------------------------------------------------------------------------
def kill_process(PROCNAME, kill, time_limit=60):
    end = datetime.now()
    end_ts = time.mktime(end.timetuple())
    pid_dict = {}

    #print(f'Checking for {PROCNAME} processes...')
    for proc in psutil.process_iter(): # check for process name matches
        if proc.name() == PROCNAME:
            pid_dict.update({proc.pid:{
                'process name':proc.name(),
                'epoch_ts':proc.create_time(),
                'started':datetime.utcfromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
            }})
            start_ts = pid_dict[proc.pid]['epoch_ts']
            elapsed = round((end_ts - start_ts) / 60, 2)
            pid_dict[proc.pid]['minutes active'] = elapsed

    print(f'{len(pid_dict)} {PROCNAME} processes found.')
    for pid in list(pid_dict.keys()):
        print(f"pid: {pid}\t Runtime: {pid_dict[pid]['minutes active']} minutes")

    if kill==True:
        for pid in list(pid_dict.keys()):
            if pid_dict[pid]['minutes active'] > time_limit:
                psutil.Process(pid).kill()
                print(f' - pid {pid} terminated successfully.')
        time.sleep(0.5)
    return pid_dict
##------------------------------------- end kill_process -------------------------------------

##------------------------------------ email_error notes -------------------------------------
## PLACEHOLDER FOR USE NOTES
##--------------------------------------------------------------------------------------------
#def email_error(func_name, ex):
#    start = time.time()
#    print(f'Calling [email_error] from process_utilities')

#    try:
#        connection_string = os.environ['email_connection_id'] # ACS connection string
#        client = EmailClient.from_connection_string(connection_string)
#        sender = os.environ['email_sender_id']
#        #content = EmailContent(
#        #    subject="Test email from Python",
#        #    plain_text="This is plaintext body of test email.",
#        #    html= "<html><h1>This is the html body of test email.</h1></html>",
#        #)
#        content = EmailContent(
#            subject=f'Error occurred in {func_name}',
#            plain_text=ex,
#            html= f"<html><h1>{ex}</h1></html>",
#        )
#        # email_recipient_name is the display name of the email recipient
#        recipient = EmailAddress(email=os.environ['email_recipient_id'], display_name=os.environ["email_recipient_name"])
#        message = EmailMessage(
#            sender=sender,
#            content=content,
#            recipients=EmailRecipients(to=[recipient])
#        )

#        response = client.send(message)
#        if (not response or response.message_id=='undefined' or response.message_id==''):
#            print("Message Id not found.")
#        else:
#            print("Send email succeeded for message_id :"+ response.message_id)
#            message_id = response.message_id
#            counter = 0
#            while True:
#                counter+=1
#                send_status = client.get_send_status(message_id)
#                if (send_status):
#                    print(f"Email status for message_id {message_id} is {send_status.status}.")
#                if (send_status.status.lower() == "queued" and counter < 12):
#                    time.sleep(10)  # wait for 10 seconds before checking next time.
#                    counter +=1
#                else:
#                    if(send_status.status.lower() == "outfordelivery"):
#                        current_date_time = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
#                        print(f"Email delivered for message_id {message_id} at {current_date_time}")
#                        break
#                    else:
#                        print("Looks like we timed out for checking email send status.")
#                        break

#    except Exception as ex:
#        logging.error(ex)
#        raise

#    finally:
#        end = time.time()
#        print(f'[email_error] execution time: {end - start:0.3f} seconds')

###------------------------------------ end email_error --------------------------------------
##email_error()