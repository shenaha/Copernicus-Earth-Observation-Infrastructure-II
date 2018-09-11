from util import *

#variables for DMS connection and queues
DMS = "https://dms.eu-de.otc.t-systems.com/v1.0/"+PROJECTID+"/queues/%s/"
MESSAGES,CONSUMER = DMS+"messages", DMS+"groups/%s/"
QUEUE,ENDPOINT = {
  "SP-idavailable":("134db8ea-9314-4ba0-9a7c-effb9d1ef528","g-673c1c78-1821-4a2e-b92c-ba156917766f")# id of the queue, id of the user groud
  ,"SP-iddownloaded": ("77adfeab-5017-437c-a9ef-5fb2213f7d9c","g-3fee5dc6-d58a-41a2-aded-f3cd12735d6e")
}, dict()

for name,ids in QUEUE.iteritems():
  ENDPOINT[name] = (MESSAGES%ids[0], CONSUMER%ids)
  print(ENDPOINT[name])

import json
#function for sending message to queue
def send (name, body=""):
  authorized("post", ENDPOINT[name][0], json={"messages":[{"body":body}]})

#function for acknowledging messages and iterate through them
def next (name):
  body = None
  rsp = authorized("get", ENDPOINT[name][1]+"messages?max_msgs=1")
  messages = json.loads(rsp.text)
  if messages:
    msg = messages[0]
    rsp = authorized("post", ENDPOINT[name][1]+"ack", json={"message":[{"handler":msg["handler"], "status":"success"}]})
    if json.loads(rsp.text)["success"]!=1: raise ValueError("Message acknowledgment: %s "%rsp.text)
    body = msg["message"]["body"]
  return body

#for testing the queue
#send("SP-idavailable","hallo1")
#send("SP-idavailable","hallo2")
#send("SP-idavailable","hallo3")
