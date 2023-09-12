from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.postgres.search import TrigramSimilarity
from .models import *
from django.contrib.postgres.search import SearchVector
from .forms import *
from django.contrib import messages
from . forms import *
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

class HomePage(ListView):
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        category_home_list = News_Category.objects.get(title='Trending News')
        return Post.objects.filter(category=category_home_list, published=True).order_by('-publish')[:5]
    
def post_cultures(request):
    post_culture_category = News_Category.objects.get(title='Culture')
    post_culture = Post.objects.filter(category=post_culture_category).order_by('-publish')[:1]
    return {'post_culture': post_culture}
      
def post_lists(request):
    post_Lists = Post.objects.filter(published=True).order_by('-publish')[:9]
    return {'post_Lists': post_Lists}    

def trending_posts(request):
    category_list = News_Category.objects.get(title='Trending News')
    post_trending = Post.objects.filter(category=category_list).order_by('-publish')[:9]
    return {'post_trending': post_trending, 'category_list': category_list}

def one_trending_news(request):
    category_trend = News_Category.objects.get(title='Trending News')
    one_news = Post.objects.filter(category=category_trend, published=True).order_by('-publish')[:1]
    return {'one_news': one_news, 'category_trend': category_trend}
    
    

def trending_news(request):
    category_list = News_Category.objects.get(title='Trending News')
    post_news = Post.objects.filter(category=category_list).order_by('-publish')[:5]
    return {'post_news': post_news}

def one_buisness_news(request):
    category_News = News_Category.objects.get(title='Buisness')
    buisness_news = Post.objects.filter(category=category_News).order_by('-publish')[:1]
    return {'buisness_news': buisness_news, 'category_News': category_News}

def buisness_news(request):
    category = News_Category.objects.get(title='Buisness')
    buisness_new = Post.objects.filter(category=category).order_by('-publish')[:6]
    return {'buisness_new': buisness_new, 'category': category }

def one_sports_news(request):
    category_sports = News_Category.objects.get(title='Sports')
    sports_news = Post.objects.filter(category=category_sports).order_by('-publish')[:1]
    return {'sports_news': sports_news, 'category_sports': category_sports}

def sports_news(request):
    category = News_Category.objects.get(title='Sports')
    sport_new = Post.objects.filter(category=category).order_by('-publish')[:6]
    return {'sport_new': sport_new}


def one_foreign_news(request):
    category_foreign = News_Category.objects.get(title='Foreign News')
    foreig_new = Post.objects.filter(category=category_foreign).order_by('-publish')[:1]
    return {'foreig_new': foreig_new, 'category_foreign': category_foreign }


def foreign_news(request):
    category_news = News_Category.objects.get(title='Foreign News')
    foreigns_new = Post.objects.filter(category=category_news).order_by('-publish')[:6]
    return {'foreigns_new': foreigns_new}





def sports_news(request):
    category = News_Category.objects.get(title='Sports')
    sport_new = Post.objects.filter(category=category).order_by('-publish')[:6]
    return {'sport_new': sport_new}



def sports_news(request):
    category = News_Category.objects.get(title='Sports')
    sport_new = Post.objects.filter(category=category).order_by('-publish')[:6]
    return {'sport_new': sport_new}


def one_health(request):
    category = News_Category.objects.get(title='Healthly Life')
    health_news = Post.objects.filter(category=category).order_by('-publish')[:1]
    return {'health_news': health_news, 'category': category }

def health_news(request):
    category = News_Category.objects.get(title='Healthly Life')
    health = Post.objects.filter(category=category).order_by('-publish')[:6]
    return {'health': health}

def feature_post(request):
    category_featured = News_Category.objects.filter(title='Featured Post')
    featured = Post.objects.filter(category=category_featured).order_by('-publish')[:1]
    return {'featured': featured, 'category_featured': category_featured}

def all_categories(request):
    all_category = News_Category.objects.all()
    return {'all_category': all_category}
def recent_post(request):
    recent = Post.objects.filter(published=True).order_by('-publish')[:8]
    return {'recent': recent}





class Category_list(ListView):
    model = Post
    context_object_name = 'categories'
    template_name = 'post/category.html'
    paginate_by = 5
    
    def get_queryset(self):
        category = get_object_or_404(News_Category, slug=self.kwargs['slug'])
        post_category = Post.objects.filter(category=category, published=True).order_by('-publish')
        return post_category
    
    
def post_details(request, id, slug, year, month, day):
    similiar_posts = None
    post_det = get_object_or_404(Post, id=id, slug=slug, publish__year=year, publish__month=month, publish__day=day)
    comment = None
    comments = post_det.comments.filter(active=True)
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post_det
            comment.save()
            messages.success(request, 'COMMENT SUBMITTED SUCESFULLY')
        else:
            messages.error(request, 'ERROR WHILE SUBMITTING THE FORM')
    else:
        form = CommentForm()
        post_tags_ids = post_det.tags.values_list('id', flat=True)
        similiar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post_det.id)
        similiar_posts = similiar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]        
    return render(request, 'post/single-post.html', {'post_det': post_det, 'form': form, 'comment': comment, 'comments': comments, 'similiar_posts': similiar_posts})

class Post_authors(ListView):
    model = Post
    context_object_name = 'authors'
    template_name = 'post/author.html'
    paginate_by = 5
    
    
    
    def get_queryset(self):
        self.authors = get_object_or_404(Author, user__username=self.kwargs['username'])
        post_authors = Post.objects.filter(author=self.authors, published=True).order_by('-publish')
        return post_authors 
    
  
    
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            
            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = f"Read {post.title}  at {post_url}\n\n"\
                f"{cd['name']}\'s  comments: {cd['comments']}"
            send_mail(subject, message, 'zenblog@gmail.com', [cd['to']])
            sent = True    
            messages.success(request, 'EMAIL SENT SUCCEFULLY')
        else:
            messages.error(request, 'ERROR WHILE SENDING EMAILS')    
            
        
    else:
        form = EmailPostForm()
    return render(request, 'post/share.html', {'form': form, 'post': post}) 








def post_search(request):
    form = SearchForms()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForms(request.GET)
        if form.is_valid():
            
            query = form.cleaned_data['query']
            results = Post.objects.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
            
    return render(request, 'post/search-result.html', {'form': form, 'query': query, 'results': results})   




def contact_us(request):
    if request.method == 'POST':
        form = Message_us(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'MESSAGE SENT SUCCESFULLY')
        else:
            messages.error(request, 'CORRECT THE ERROR BELOW')
    else:
        form = Message_us()
    return render(request, 'post/contact.html', {'form': form})                
    
    
def about_us(request):
    return render(request, 'post/about.html')    