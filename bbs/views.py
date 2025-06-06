from django.shortcuts import render
from django.views import generic    # 汎用ビューのインポート
from .models import Article     # models.pyのArticleクラスをインポート
from django.urls import reverse_lazy    # reverse_lazy関数をインポート
from .forms import SearchForm   # forms.pyからsearchFormクラスをインポート
from django.contrib.auth.mixins import LoginRequiredMixin   # LoginRequiredMixinをインポート
from django.core.exceptions import PermissionDenied    # PermissionDeniedをインポート

# IndexViewクラスを作成
class IndexView(generic.ListView):
    model = Article     # Articleモデルを使用 
    template_name = 'bbs/index.html'    # 使用するテンプレート名を指定（Articleも自動で渡す）
    
# DetailViewクラスを作成
class DetailView(generic.DetailView):
    model = Article
    template_name = 'bbs/detail.html'
    
# CreateViewクラスを作成
# 新規投稿はログインしているユーザーのみ
class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    template_name = 'bbs/create.html'
    fields = ['content']
    
    # 格納する値をチェック
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

# UpdateViewクラスを作成
# 投稿編集はログインしているユーザーのみ
class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    template_name = 'bbs/create.html'
    fields = ['content']    # 項目をcontentのみに変更
    
    # dispatchメソッドで権限チェックを追加
    def dispatch(self, request, *args, **kwargs):
        # 編集対象の投稿オブジェクトを取得
        obj = self.get_object()
        # 投稿者と現在のユーザーが一致しない場合は403エラーを発生
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません。')
        # 親クラスのdispatchを呼び出して通常の処理を継続
        return super(UpdateView, self).dispatch(request, *args, **kwargs)
    
# DeleteViewクラスを作成
# 投稿削除はログインしているユーザーのみ
class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    template_name = 'bbs/delete.html'
    success_url = reverse_lazy('bbs:index')
    
    def dispatch(self, request, *args, **kwargs):
        # 削除対象の投稿オブジェクトを取得
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('削除権限がありません。')
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

# 検索機能のビュー
def search(request):
  articles = None # 検索結果を格納する変数を初期化
  searchform = SearchForm(request.GET) # GETリクエストで送信したデータが格納される（詳細は解説にて）
    
  # Formに正常なデータがあれば
  if searchform.is_valid():
      query = searchform.cleaned_data['words']   # queryにフォームが持っているデータを代入
      articles = Article.objects.filter(content__icontains=query)    # クエリを含むレコードをfilterメソッドで取り出し、articles変数に代入
      return render(request, 'bbs/results.html', {'articles':articles,'searchform':searchform})
  
# カスタム403のビュー(アクセス権限が無い場合)
def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {'error_message': str(exception)}, status=403)