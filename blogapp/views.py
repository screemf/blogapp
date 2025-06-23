from datetime import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.timezone import now
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound
from .forms import AuthorForm, ContactForm, CommentForm, ImageForm, PostForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Author, Like, Image
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden




# Create your views here.
# def index(request):
# return HttpResponse("Hello, world. You're at the polls index.")
def index(request):
    total_posts = Post.objects.count()
    total_users = User.objects.count()
    total_authors = Author.objects.filter(is_verified=True).count()
    total_pending_authors = Author.objects.filter(is_verified=False).count()

    # Получение поста с самым большим количеством лайков
    most_liked_post = Post.objects.order_by('-likes').first()

    # Получение комментария с самым большим количеством лайков
    most_liked_comment = Comment.objects.order_by('-likes').first()

    context = {
        'title': 'Домашняя Страница',
        'total_posts': total_posts,
        'total_users': total_users,
        'total_authors': total_authors,
        'total_pending_authors': total_pending_authors,
        'most_liked_post': most_liked_post,
        'most_liked_comment': most_liked_comment,
    }

    return render(request, 'blogapp/index.html', context)


def contacts(request):
    return HttpResponse("moskva")


# def author_create(request):
#   for i in range(10):
#      author = Author.objects.create (name=f'Author{i}',
#                                     age = 40+i,
#                                    email = f'{i}@mail.com',
#                                   bio = f'test {i}')
#  author.save()
# return HttpResponse("Create author")

def authors(request):
    authors = Author.objects.all().order_by('-is_verified', 'name')
    return render(request, 'blogapp/authors.html', context={'authors': authors})


def author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return HttpResponseNotFound('Author not found')
    return render(request, 'blogapp/author.html', context={'author': author})


def author_create_form(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect('authors')
    else:
        form = AuthorForm()
    return render(request, 'blogapp/author_form.html', context={'form': form})


'''Допилить можно только своих авторов апдейтить'''


def author_update_form(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('authors')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'blogapp/author_update_form.html', context={'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(f'Сообщение от {form.cleaned_data["name"]}:{form.cleaned_data["message"]}')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'blogapp/contact.html', context={'form': form})


# def post_list(request):
# posts = Post.objects.all()
# return render(request,'blogapp/post_list.html',context={'posts':posts} )

# def post_detail(request, post_id):
# post = get_object_or_404(Post,id=post_id)
# return render(request,'blogapp/post_detail.html',context={'post':post})

class PostListView(ListView):
    model = Post
    template_name = 'blogapp/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[('post_count')] = Post.objects.count()
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blogapp/post_list.html', {'posts': posts})


# def create_post(request):
#  if request.method == "POST":
#     title = request.POST.get('title')
#    content = request.POST.get('content')
#   new_post = Post.objects.create(title=title, content=content)
#
# Notify the WebSocket group
#       channel_layer = get_channel_layer()
#      async_to_sync(channel_layer.group_send)(
#         'posts',
#        {
#           'type': 'post_list_update',
#          'post': {
#             'title': new_post.title,
#            'content': new_post.content,
#       }
#  }
# )

#  return redirect('post_list')
# return render(request, 'blogapp/post_list.html')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blogapp/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blogapp/post_form.html'
    fields = ['title', 'content', 'category']
    success_url = reverse_lazy('posts')

    def get_author(self):
        try:
            return Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        image_form = ImageForm(self.request.POST, self.request.FILES)
        if form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        author = self.get_author()

        if not author or not author.is_verified:
            raise PermissionDenied("Автор не подтвержден")

        post = form.save(commit=False)
        post.author = author
        post.is_published = True
        post.published_date = now()
        post.save()

        image = image_form.save(commit=False)
        image.post = post
        image.save()

        # часть с вебсокетами
        post_data = {
            'title': post.title,
            'content': post.content,
            'id': post.id,
            'author_id': post.author.id,
        }

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            'post_group',
            {
                'type': 'post_created',
                'post': post_data,
            }
        )

        return super().form_valid(form)

    def form_invalid(self, form, image_form):
        return self.render_to_response(
            self.get_context_data(form=form, image_form=image_form)
        )

    def get_context_data(self, **kwargs):
        kwargs['image_form'] = kwargs.get('image_form', ImageForm())
        return super().get_context_data(**kwargs)


'''Обновление постов 
Доработки:
'''


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blogapp/post_form.html'
    fields = '__all__'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.published_date = timezone.now()
        return super().form_valid(form)


'''Удаление постов'''


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blogapp/post_confirm_delete.html'
    success_url = reverse_lazy('posts')


'''Тестирование создает пользователей'''


def create_user(request):
    user = User.objects.create_user(username='test', password='test', email='test@mail.com')
    return HttpResponse(f'Пользователь создан {user.username} ')


'''Функция для добавления комментариев к посту + коментариев к коментариям
Доработка: Прикрутить WS к комментам Сделанно  '''


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent__isnull=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent = Comment.objects.get(id=parent_id)
            new_comment.save()
            comment_data = {
                'comment': new_comment.text,
                'comment_id': new_comment.id,
                'post_id': post.id,
                'comment_author_id': new_comment.author.id,
                'parent_id': parent_id if parent_id else None
            }

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f'comment_group_{post.id}',
                {
                    'type': 'comment_created',
                    'comment': comment_data,
                }
            )
            return redirect('post', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


'''Удаление коментария - удаялет каскадно
Доработки:
1. Прикрутить WS
Реалзиованно через пост чтобы не парится с отрпавлением в хедарах токена'''


@login_required
@require_http_methods(["POST"])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return JsonResponse({'success': False, 'message': 'Вы не можете удалить этот комментарий.'})

    comment.delete()
    return JsonResponse({'success': True, 'massage': 'ваш коментарий был удален'})


'''Функция лайк для поста
 Доработки:
 1. Самолайк невозможен - если ты автор - Нужно перерабатывать модель возможно поздже 
 2.один лайк на одну запись от одного юзера - Сделанно
 3. Смапить авторов и пользователей - добавить бульен к пользователю если тру значит должен быть id автора сделано'''


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    existing_like = Like.objects.filter(post=post, user=request.user).first()

    if existing_like:
        existing_like.delete()
        post.likes -= 1
    else:
        Like.objects.create(post=post, user=request.user)
        post.likes += 1

    post.save()
    return JsonResponse({'likes': post.likes})


# def like_post(request, post_id):
# post = get_object_or_404(Post, id=post_id)
# post.likes += 1
# post.save()
# return JsonResponse({'likes': post.likes})

'''Функция лайк для коментария
 Доработки:
 1. Самолайк невозможен - Не будет Сделано - нужно перерабатывать модель
 2.один лайк на одну запись от одного юзера - СДЕЛАНО'''


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    existing_like = Like.objects.filter(comment=comment, user=request.user).first()

    if existing_like:
        existing_like.delete()
        comment.likes -= 1
    else:
        Like.objects.create(comment=comment, user=request.user)
        comment.likes += 1

    comment.save()
    return JsonResponse({'likes': comment.likes})


@staff_member_required
@require_POST
def toggle_verified(request, author_id):
    if not request.user.is_staff: return HttpResponseForbidden("Недостаточно прав")
    author = get_object_or_404(Author, id=author_id)
    author.is_verified = not author.is_verified
    author.save()
    return redirect('authors')


def attach_image_to_post(post_id, image_file):
    try:
        post = Post.objects.get(id=post_id)

        image = Image.objects.create(post=post, image=image_file)

        return image
    except ObjectDoesNotExist:
        print("Добавилось")
        return None


def upload_image_to_post(request, post_id):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image = attach_image_to_post(post_id, image_file)
        if image:
            return redirect('post_detail', pk=post_id)
        else:
            return HttpResponse("Post not found.", status=404)
    return HttpResponse("Invalid request.", status=400)
