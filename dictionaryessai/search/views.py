from django.shortcuts import render,redirect
import bs4
import requests
from translate import Translator
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from translate import Translator






# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
   if request.method == 'POST':
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      password2 = request.POST['password2']
      if password == password2:
         if User.objects.filter(email=email).exists():
            messages.info(request, 'email already used')
            return redirect(register)
         elif User.objects.filter(username=username).exists():
            messages.info(request, 'username already used')
            return redirect(register)
         else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
      else:
         messages.info(request, 'password not the same')
         return redirect(register)
   else:   
    return render(request, 'register.html') 
 
 
def login(request):
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      user = auth.authenticate(username=username, password=password)
      if user is not None:
         auth.login(request, user)
         return redirect('/')
      else:
         messages.info(request, 'credentials invalid')
         return redirect('login')
   else:
           
      return render(request, 'login.html')
   
def logout(request):
   auth.logout(request)
   return redirect('/') 




def search(request):
    

    word = request.GET['word']

    res = requests.get('https://www.dictionary.com/browse/'+word)
    res2 = requests.get('https://www.thesaurus.com/browse/'+word)
    

    if res:
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        meaning = soup.find_all('div', {'value': '1'})
        meaning1 = meaning[0].getText()
    else:
        word = 'Sorry, '+ word + ' Is Not Found In Our Database'
        meaning = ''
        meaning1 = ''
        
        
        

    if res2:
        soup2 = bs4.BeautifulSoup(res2.text, 'lxml')

        synonyms = soup2.find_all('a', {'class': 'css-r5sw71-ItemAnchor etbu2a31'})
        ss = []
        for b in synonyms[0:]:
            re = b.text.strip()
            ss.append(re)
        se = ss
        

        

        antonyms = soup2.find_all('a', {'class': 'css-lqr09m-ItemAnchor etbu2a31'})
        aa = []
        for c in antonyms[0:]:
            r = c.text.strip()
            aa.append(r)
        ae = aa
    else:
        se = ''
        ae = ''


    results = {
        'word' : word,
        'meaning' : meaning1,
    }


    return render(request, 'search.html', {'se': se, 'ae': ae, 'results': results})

def translatef(request):
    if request.method == 'POST':
        english_text = request.POST['english_text']
        translator = Translator(to_lang="fr")
        french_text = translator.translate(english_text)
        return render(request, 'translatef.html', {'french_text': french_text})
    else:
        return render(request, 'translatef.html')
    
def translate1(request):
    if request.method == 'POST':
        english_text = request.POST['english_text']
        if english_text:
         translator = Translator(to_lang="en", from_lang='fr')
         french_text = translator.translate(english_text)
        return render(request, 'translate1.html', {'french_text': french_text})
    
    return render(request, 'translate1.html')    
    
