from django.shortcuts import render, redirect

from .models import User, Quote
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    users = User.objects.all()
    for user in users:
        print user.email
    if 'messages' in request.session:
        context={
        'messages': request.session['messages']
        }
        del request.session['messages']
    else:
        context = {
        'messages': [],
        'users': users
        }
    return render(request, 'quotes/index.html', context)


def register(request):
    #print request.POST
    if request.method == 'POST':
        messages = User.objects.register(request.POST)
        #Above line might be postData
    if not messages:
        print "No messages! Success!"
        # fetch user id and name via email
        user_list = User.objects.all().filter(email=request.POST['email'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].name
        return redirect('/quotes')
    else:
        request.session['messages'] = messages
        print messages
    return redirect('/')

def login(request):
    users = User.objects.all()
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password'],
    }
    if request.method == 'POST':
        messages = User.objects.login(request.POST)
    if not messages:
        print "No messages! Success!"
        user_list = User.objects.all().filter(email=request.POST['email'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].name
        return redirect('/quotes')
    else:
        request.session['messages'] = messages
        return redirect('/')

def quotes(request):
    # users = User.objects.get(id=id)
    quotes = Quote.objects.all().order_by('-id')[:5]
    # favorites = User.objects.filter(user_favorite=user_favorite)
    context ={
        'quotes': quotes
    }
    print "Request:", request.POST
    print "Quotes:", Quote.objects.all()
    # print "Users:", users.name
    # print "Favorites:", favorites
    return render(request, 'quotes/quotes.html', context)

def users(request, id):
    name = User.objects.get(id=id)
    quote = Quote.objects.get(id=id)
    user = User.objects.get(id=id)
    quote_poster = User.objects.filter(quote_poster__id=id)
    user_quote = user.quote_poster.add(quote)
    context = {
        'user': user
    }
    print user_quote
    return render(request, 'quotes/quotes.html', context)

def add_quote(request):
    if request.method == 'POST':
        quote = request.POST['quote']
        # poster = request.POST['poster']
        # print "Quote: ", quote, "Poster: ", poster
        result = Quote.objects.validate(request.POST)
        if result[0]:
            messages.info(request, result[1])
            return redirect('/quotes')
        messages.error(request, result[1])
        return redirect('/quotes')

def remove_quote(request):
    if request.method == 'POST':
        return redirect('/quotes')

def add_fave(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        return redirect('/quotes')
