from django.shortcuts import render, get_object_or_404, redirect
from django_comments.views.moderation import perform_delete
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, UserProfile, M_UserArticle, UserLikePost
from .forms import PostAdminForm, UserProfileRegistrationForm
from django.http import JsonResponse
from django_comments.models import Comment
from django.contrib import auth
import datetime
import django.http as http

# Create your views here.
def home_page(request):
    post_ls = Post.objects.all().order_by('-last_mod')
    page = request.GET.get('page', 1)
    paginator = Paginator(post_ls, 6)
    recommend = []

    if not request.user.is_anonymous and M_UserArticle.objects.filter(pk=request.user):
        rec_ls = get_recommend(request.user)
        for r in rec_ls:
            recommend.append(r[0])

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'index.html', { 'post_ls':posts, 'recommend':recommend })

def post_article(request, pk):
    post = Post.objects.get(pk=pk)
    author = UserProfile.objects.get(pk=post.author)
    likers = UserLikePost.objects.filter(post=post)
    likers_cnt = likers.count()

    if not request.user.is_anonymous:
        reader = UserProfile.objects.get(pk=request.user)
        stat = ""
        add_user_read_article(request.user, post)

        if author.user in reader.subs.all():
            stat = 'Unfollow'
        else:
            stat = 'Follow'

        if likers.filter(user=request.user):
            alreadyLike = True
        else:
            alreadyLike = False

        return render(request, 'single.html', {
            'post':post, 'author':author, 'reader':reader, 
            'sub_stat': stat, 'likes':likers_cnt, 'ald_like':alreadyLike,
        })
    else:
        return render(request, 'single.html', {
            'post':post, 'author':author, 'reader':'', 
            'sub_stat': 'disable', 'likes':likers_cnt, 'ald_like':False,
        })

def post_new_article(request):
    if request.method == "POST":
        form = PostAdminForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_mod = datetime.datetime.now()
            post.save()
            return redirect('post_article', pk=post.pk)
    else:
        form = PostAdminForm(request.GET)
    return render(request, 'post_edit.html', {'form': form, 'type':'NEW'})

def post_edit_article(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostAdminForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_mod = datetime.datetime.now()
            post.save()
            return redirect('post_article', pk=post.pk)
    else:
        form = PostAdminForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'type':'EDIT', 'pk':pk})

def profile(request):
    profile = UserProfile.objects.get(pk=request.user)
    stat = False
    if request.method == "POST":
        firstname = request.POST['firstname_field']
        lastname = request.POST['lastname_field']
        intro = request.POST['intro']
        url = request.POST['url']
        location = request.POST['location']
        profile.firstname_field = firstname
        profile.lastname_field = lastname
        profile.intro = intro
        profile.photo_url = url
        profile.location = location
        profile.save()
        stat = True

    return render(request, 'profile.html', { 'profile': profile, 'stat': stat })

def status(request, pk):
    post_cnt = 0
    post_pct = 0
    like_cnt = 0
    like_avg = 0
    fol_cnt = 0
    sub_cnt = 0
    total_posts = Post.objects.count() 
    totlal_likes = UserLikePost.objects.count()
    profile = UserProfile.objects.get(pk=pk) # user's profile
    fol_cnt = profile.subers.count()
    sub_cnt = profile.subs.count()
    user_posts = Post.objects.filter(author=pk) # user's post
    post_cnt = user_posts.count()

    if total_posts != 0:
        post_pct = post_cnt * 100 / total_posts
        post_pct = round(post_pct, 2)

    for p in user_posts.all():
        like_cnt += UserLikePost.objects.filter(post=p.pk).count()
    
    if totlal_likes != 0:
        like_avg = like_cnt * 100 / totlal_likes
        like_avg = round(like_avg, 2)

    return render(request, 'status.html', {
        'profile':profile, 'post_cnt':post_cnt, 'like_cnt':like_cnt,
        'post_pct':post_pct, 'fol_cnt':fol_cnt, 'sub_cnt':sub_cnt,
        'like_avg':like_avg })

def search(request):
    keyword = request.POST.get('search')
    posts = Post.objects.filter(title__icontains=keyword)
    return render(request, 'search.html', {'posts':posts, 'key':keyword})

def delete_own_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.user.id != request.user.id:
        raise Http404
    perform_delete(request, comment)
    pk = comment.object_pk
    return redirect('post_article', pk=pk)

def delete_own_article(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('index')

def ajax_follow(request, pk):
    author = UserProfile.objects.get(pk=pk)
    reader = UserProfile.objects.get(pk=request.user)

    if author.user in reader.subs.all():
        # print("pk is in ")
        # print(reader.subs.all())
        reader.subs.remove(author.user)
        author.subers.remove(reader.user)
        return JsonResponse('Unfollow', safe=False)
    else:
        reader.subs.add(author.user)
        author.subers.add(reader.user)
        return JsonResponse('Follow', safe=False)

def ajax_like(request, pk):
    post = Post.objects.get(pk=pk)
    reader = UserProfile.objects.get(pk=request.user)
    posts = UserLikePost.objects.filter(user=reader.user)
    
    if posts.filter(post=post): # already like, so reclick means take like back.
        print('dislikes it')
        posts.filter(post=post).delete()
        return JsonResponse('Unlike', safe=False)
    else: # haven't like
        print('likes it')
        new_like = UserLikePost(user=reader.user, post=post)
        new_like.save()
        return JsonResponse('Like', safe=False)

def add_user_read_article(reader, article):
    if M_UserArticle.objects.filter(pk=reader).exists():
        data = M_UserArticle.objects.get(pk=reader)
        data.readed_article.add(article)
    else:
        new_data = M_UserArticle()
        new_data.user = reader
        new_data.save()
        new_data.readed_article.add(article)

    print("Reader " + str(reader) + " has read " + str(article.title))

def get_recommend(reader):
    posts = Post.objects.all()
    post_num = Post.objects.count()
    matrix = []
    labels = []
    target_label_index = []
    rec_ls = [0] * post_num
    for p in posts:
        ls = []
        for q in posts:
            readers = M_UserArticle.objects.all()
            count = 0
            if p != q:
                for r in readers:
                    if q in r.readed_article.all() and p in r.readed_article.all():
                        count += 1
            ls.append(count)
        matrix.append(ls)
        labels.append(p)

    target = M_UserArticle.objects.get(pk=reader)
    for t in target.readed_article.all():
        index = labels.index(t)
        target_label_index.append(index)
        for i in range(post_num):
            rec_ls[i] += matrix[index][i]
            

    print("Recommend:")
    print(rec_ls)
    print("Readed")
    print(target.readed_article.all())
    for l in target_label_index:
        rec_ls[l] = 0

    rec_pk = []
    for i in range(post_num):
        if rec_ls[i] != 0:
            rec_pk.append((posts[i], rec_ls[i]))

    rec_pk = sorted(rec_pk, key=lambda x: x[1], reverse=True)
    rec_pk = rec_pk[0:5]

    return rec_pk