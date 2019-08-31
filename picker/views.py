from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import tweepy
import random
from django.shortcuts import redirect


def init_api():
    CONSUMER_KEY = "z1rGUsDaJnddDkMIUrjn1LLeH"
    CONSUMER_SECRET = "PrUZQYmk2o47DfWYtJRtBARpMBBorbtYfoUHCy334fhJp33k8i"
    ACCESS_KEY = "1031914262896074759-dmVsehvCdK31Briwe1IRsRGJbUuux8"
    ACCESS_SECRET = "bci7y24cdz7tCl6wsbMfD6zTsh0HFN3mtGcuLLsh2sgQU"
    api = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(api)


def get_id(url):
    try:
        hehe = url.split("/")[5]
        if "?" in hehe:
            return str(hehe.replace(hehe[hehe.find("?"):(int(len(hehe)))], ''))
        else:
            return hehe
    except:
        print("Exception")
        return "undefined"


def index(request):
    template = loader.get_template("picker/index.html")
    return HttpResponse(template.render(context = None, request = request))


def howto(request):
    template = loader.get_template("picker/how.html")
    return HttpResponse(template.render(context = None, request = request))

def about(request):
    template = loader.get_template("picker/about.html")
    return HttpResponse(template.render(context=None, request=request))


def result(request):
    if request.method == 'POST':
        template = loader.get_template("picker/result.html")
        api = init_api()
        candidates = []
        variable = request.POST.get("tweet_url", "undefined")
        id = get_id(variable)
        if id == "undefined":
            context = {
                "title": "Whoops!",
                "data": "Wrong url"
            }
            return HttpResponse(template.render(context, request))
        else:
            h = api.retweets(id, 100)
            for status in h:
                print(status.user.id)
                candidates.append(status.user.id)

            print(candidates)
            if len(candidates) != 0:
                winner = random.choice(candidates)
                user = api.get_user(id = winner)
                context = {
                    "title" : "Congratulations!",
                    "data": "@"+user.screen_name
                }
                return HttpResponse(template.render(context, request))
            else:
                context = {
                    "title" : "Whoops!",
                    "data" : "No retweet found yet"
                }
                return HttpResponse(template.render(context, request))

    else:
        return redirect("index")


