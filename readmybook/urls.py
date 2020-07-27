from django.urls import path
from . import views

urlpatterns=[
    path('', views.landing, name='landing'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(),name='login'),
    path('profilesetup/', views.ProfilePostRegisterView.as_view(),name='profile-post-register'),
    path('user/<slug:name>/', views.profile, name='profile'),
    path('editprofile/', views.ProfileEditView.as_view(),name='profile-edit'),
    path('ajax/booksearch/', views.bookSearch, name='book-search'),
    path('ajax/gensearch/', views.genSearch, name='gen-search'),
    path('ajax/addbook/', views.addBook, name='add-book'),
    path('ajax/addnewbook/',views.addBookForm, name='add-new-book'),
    path('ajax/removebook/',views.removeBook, name='remove-book'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
    path('book/bookid=<int:bookid>',views.bookPage,name='book-page'),
    path('bookrequests/',views.bookRequestPage,name='bookrequests'),
    path('ajax/bookrequested',views.bookRequested, name='bookrequested'),
    path('ajax/reqaccepted/',views.reqAccepted, name='req-accepted'),
    path('ajax/reqbookreceive/',views.reqReceive, name='req-receive'),
    path('ajax/reqbookreceivedback/',views.reqReceivedBack, name='req-rec-back'),
    path('ajax/reqcancel/',views.reqCancel, name='cancel-request'),

]