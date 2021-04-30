from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt

def index(request):
    
    return render(request, 'login.html')

def register(request):
    
    register_user = User.objects.filter(email = request.POST['email'])

    if len(register_user) != 0:
        messages.error(request, "User with that email already exists!")
        return redirect('/')

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')

    hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw,
    )

    request.session['user_id'] = new_user.id
    return redirect ('/')

def login(request):
    login_user = User.objects.filter(email = request.POST['email'])

    if len(login_user) == 0:
        messages.error(request, "Please check your email and password.")
        return redirect('/')

    user = login_user[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please check your email and password.")
        return redirect('/')

    request.session['user_id'] = user.id
    return redirect ('/books')

def books(request):
    
    context = {
        'allbooks' : Book.objects.all(),
        'addedby' : User.objects.filter(id=request.session['user_id']).first().books_uploaded.all(),
        'liked' : User.objects.filter(id=request.session['user_id']).first().liked_books.all()
    }
    return render (request, 'books.html', context)

def books_id(request, book_id):
    
    thisuser=Book.objects.get(id=book_id).user_who_like.all()
    thisbook=Book.objects.get(id=book_id)
    likedthisbook=Book.objects.get(id=book_id).user_who_like.filter(id=request.session['user_id'])
    context = {
        'thisuser' : thisuser,
        'thisbook' : thisbook,
        'likedthisbook': likedthisbook,
    }
    return render (request, 'books_id.html', context)

def books_ad(request):
    
    if request.method =='POST':
        errors = User.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else: 
            user_id=request.session['user_id']
            bookobject=Book.objects.create(title=request.POST['title'], description=request.POST['description'], uploaded_by=User.objects.get(id=user_id))
            this_user=User.objects.get(id=user_id)
            bookid=bookobject.id
            bookobject.user_who_like.add(this_user)
            return redirect ('/books')

def books_id_update(request, book_id):
   
    if request.method =='POST': 
        updates=Book.objects.get(id=book_id)
        updates.title=request.POST['title']
        updates.description=request.POST['description']
        updates.save()
        return redirect (f'/books/{updates.id}')
    else:
        return redirect ('/books')

def favorite(request, book_id):
    
    user_id=request.session['user_id']
    bookobject=Book.objects.get(id=book_id)
    this_user=User.objects.get(id=user_id)
    bookobject.user_who_like.add(this_user)
    return redirect ('/books')


def unfavorite(request, book_id):
    
    user_id=request.session['user_id']
    bookobject=Book.objects.get(id=book_id)
    this_user=User.objects.get(id=user_id)
    bookobject.user_who_like.remove(this_user)
    return redirect ('/books')

def eliminate(request, book_id):
    
    deleted=Book.objects.get(id=book_id)
    if deleted.uploaded_by.id == request.session["user_id"]:
        deleted.delete()
    return redirect ('/books')

