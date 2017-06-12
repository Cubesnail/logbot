import requests, json, random, re
from pprint import pprint
from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Question, Answer, Person

PAGE_ACCESS_TOKEN = 'EAAWFFadPFaQBAGgGgJdQTlI9FO1il77J5hiSVeaDYBF5Bwln1ZCeEuqMjavAoYP0U9CMgwWKclLBRZAoCXFilZCMgG5S1JTBoaHrugXyGLKO1eQZAnVsAVxNZBMH6zUgOlI2PEs53nVhcjCD3qnHuHvX0vctKhZAxMsKo4gCXwvQZDZD'
dictionary = {
    'quiz':["""This is a quiz"""],
    'test':["""This is a test"""],
    'exam':["""This is an exam"""]
}

# Create your views here.
def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    reply = ''
    for token in tokens:
        if token in dictionary:
            reply = random.choice(dictionary[token])
            break
    if not reply:
        reply = "I didn't understand! Send 'test', 'exam', 'quiz'"
    answer_list = Question.objects
    print(tokens)
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json()
    pprint(user_details)
    #look for person via first_name
    try:
        person = Person.objects.get(fbid__startswith=fbid)
        reply = 'old person'
    except Person.DoesNotExist:
        # add person
        reply = 'new person'
        new_person = Person.objects.create(first_name=user_details['first_name'],last_name=user_details['last_name'],fbid = fbid)
        new_person.save()
    #if user_details['fbid'] not in 
    #if user_details['first_name'] == 'Dillon' and token in ['penis','shit','fuck']:
    #    reply = 'Send my bot a real message pls'
    #else:
    #    reply = 'hi '+user_details['first_name']+'! ' + reply
    #if user_details['first_name'] in ['Derrick', 'Dillon', 'Liz']:
    #    reply = "fbid is:" + fbid
    if token in ['info']:
        reply = '{0} {1} {2}'.format(person.first_name, person.last_name, person.fbid)
    
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":reply}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    #pprint(status.json())

class logbot_view(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '0123456789':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        pprint(incoming_message)
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message and not('is_echo' in message['message']):
                    # Print the message to the terminal
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
