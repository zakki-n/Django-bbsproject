from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm   # ユーザー登録用のフォームクラスをインポート
from django.urls import reverse_lazy
from django.views import generic

# SignUpViewクラスを作成
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')     # サインアップ成功時、ログインページのURLにリダイレクト
    template_name = 'accounts/signup.html'

# Create your views here.
