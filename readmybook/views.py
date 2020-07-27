from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout, login, authenticate
from .forms import UserForm, LoginForm, ProfilePostRegisterForm, ProfileEditForm, NewBookForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Institue, BooksDB, Book, requestBook
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your views here.

def landing(request):
    return render(request, 'readmybook/landing.html')


class UserFormView(View):
    template_name = 'readmybook/register.html'
    form_class = UserForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            profile = Profile.objects.create(user=user)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profile-post-register')

        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    template_name = 'readmybook/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    if user.profile.firstName == '':
                        return redirect('profile-post-register')

                    return redirect('profile', name=user.username)
            else:
                messages.warning(request, 'Please check your login credentials again')
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})


class ProfilePostRegisterView(LoginRequiredMixin, View):
    form_class = ProfilePostRegisterForm
    template_name = 'readmybook/profile_post_register.html'

    def get(self, request):
        form = self.form_class(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)

        return render(request, self.template_name, {'form': form})


def profile(request, name):
    try:
        user = User.objects.get(username=name)
        bookslist = BooksDB.objects.filter(owner=user)
        return render(request, 'readmybook/profile.html', {'userprofile': user, 'bookslist': bookslist})
    except:
        return redirect('landing')


class ProfileEditView(LoginRequiredMixin, View):
    form_class = ProfileEditForm
    template_name = 'readmybook/profile_edit.html'

    def get(self, request):
        form = self.form_class(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', name=request.user.username)

        return render(request, self.template_name, {'form': form})


def bookSearch(request):
    if request.is_ajax() and request.method == "GET":
        searchtext = request.GET.get('searchtext', None)
        book_owned = BooksDB.objects.filter(owner=request.user)
        blist = []
        for bowned in book_owned:
            blist.append(bowned.book.name)
        booklist = Book.objects.filter(name__icontains=searchtext.strip())
        form = NewBookForm()
        html = render_to_string('readmybook/book_search.html', {'bookslist': booklist, 'blist': blist, 'form': form})
        data_dict = {"search-result": html}
        return JsonResponse(data_dict)

    return JsonResponse({}, status=400)


def genSearch(request):
    if request.is_ajax() and request.method == "GET":
        searchtext = request.GET.get('searchtext', None)
        users = User.objects.filter(username__icontains=searchtext.strip())[:4]
        booklist = Book.objects.filter(name__icontains=searchtext.strip())[:4]
        html = render_to_string('readmybook/gen_search.html', {'users': users, 'booklist': booklist})
        data_dict = {"search-result": html}
        return JsonResponse(data_dict)

    return JsonResponse({}, status=400)


def addBook(request):  # Using AJAX as I might remove refreshing of page someday, also I needed practice with AJAX
    if request.is_ajax() and request.method == 'GET':
        bookpk = request.GET.get('bookpk', None)
        print('BOOK PK HERE,', bookpk)
        book = Book.objects.get(pk=bookpk)
        newbook = BooksDB(owner=request.user, book=book)
        newbook.save()

    return HttpResponse("success")


def addBookForm(request):
    if request.is_ajax() and request.method == 'POST':
        form = NewBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            bookadd = BooksDB(book=book, owner=request.user)
            bookadd.save()
        return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})


def removeBook(request):
    if request.is_ajax() and request.method == 'GET':
        bookid = request.GET.get('bookpk', None)
        BooksDB.objects.get(pk=bookid).delete()
        return JsonResponse({'success': True, 'message': 'Book was successfully removed'})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


def bookPage(request, bookid):
    book = Book.objects.get(pk=bookid)
    booksinDB = BooksDB.objects.filter(book=book)
    list = requestBook.objects.filter(request_by=request.user)
    list2 = []
    for i in list:
        if i.book.book == book and i.status != 'completed':
            list2.append(i.request_to.username)

    return render(request, 'readmybook/book-page.html', {'book': book, 'booksinDB': booksinDB, 'requestedlist': list2})


def bookRequested(request):
    if request.is_ajax() and request.method == 'GET':
        bookid = request.GET.get('bookid', None)
        to_name = request.GET.get('to_name', None)
        book = BooksDB.objects.get(pk=bookid)
        touser = User.objects.get(username=to_name)
        newrequest = requestBook(book=book, request_by=request.user, request_to=touser)
        newrequest.save()
        return JsonResponse({'message': 'Request was put up'})


def bookRequestPage(request):
    request_received = requestBook.objects.filter(request_to=request.user)
    request_sent = requestBook.objects.filter(request_by=request.user)
    return render(request, 'readmybook/book_requests.html', {'rreceived': request_received, 'rsent': request_sent})


def reqAccepted(request):
    if request.is_ajax() and request.method == 'GET':
        reqid = request.GET.get('reqid', None)
        req = requestBook.objects.get(pk=reqid)
        if req.book.status == 'available':
            req.status = 'received-pen'
            req.book.status = 'notavailable'
            req.book.save()
            req.save()
            return JsonResponse({'message': 'Request accepted'})


def reqReceive(request):
    if request.is_ajax() and request.method == 'GET':
        reqid = request.GET.get('reqid', None)
        req = requestBook.objects.get(pk=reqid)
        req.status = 'returned-pen'
        req.save()
        return JsonResponse({'message': 'Book handed over', 'status': 'received'})


def reqReceivedBack(request):
    if request.is_ajax() and request.method == 'GET':
        reqid = request.GET.get('reqid', None)
        req = requestBook.objects.get(pk=reqid)
        req.status = 'completed'
        req.to_status = 'done'
        req.by_status = 'done'
        req.save()
        req.book.status = 'available'
        req.book.save()
        return JsonResponse({'status': 'completed'})


def reqCancel(request):
    if request.is_ajax() and request.method == 'GET':
        reqid = request.GET.get('reqid', None)
        req = requestBook.objects.get(pk=reqid)
        if req.status == 'pending':
            req.delete()
        else:
            req.book.status = 'available'
            req.delete()
            req.save()

        return JsonResponse({'message': 'Request Cancelled'})
