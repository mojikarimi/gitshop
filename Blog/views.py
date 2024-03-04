# Create your views here.
from __future__ import unicode_literals
from statistics import mean
from django.shortcuts import render, redirect
from .models import Category, SubCategory, Post, Comments, OpinionComment
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from jdatetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
def blog(request):
    posts = Post.objects.using('blog').order_by('-date')
    cats = Category.objects.using('blog').all()
    sub_cats = SubCategory.objects.using('blog').all()
    visit_posts = Post.objects.using('blog').order_by('view')[:5]
    post_tags = ''
    for post in posts:
        post_tags += f'{post.tags},'
    post_tags = list(set(post_tags.split(',')))[:20]
    if '' in post_tags:
        post_tags.remove('')
    context = {
        'posts': posts,
        'cats': cats,
        'sub_cats': sub_cats,
        'post_tags': post_tags,
        'visit_posts': visit_posts,
    }
    return render(request, 'front/Blog/blog.html', context=context)


def post(request, title):
    my_post = Post.objects.using('blog').get(title=title)
    comments = Comments.objects.using('blog').filter(post_id=my_post.pk, status=True).order_by('-date')
    comments_score = comments.values('score')
    comments_score_list = []
    for comment_score in comments_score:
        comments_score_list.append(comment_score['score'])
    sub_cats = SubCategory.objects.using('blog').filter(category=my_post.category)
    related_posts = Post.objects.using('blog').filter(category=my_post.category)[:5]
    if comments:
        score = round(mean(comments_score_list))
    else:
        score = 0
    my_post.score = score
    post_tags = list(set(my_post.tags.split(',')))[:20]
    my_post.view += 1
    my_post.save(using='blog')
    context = {
        'my_post': my_post,
        'sub_cats': sub_cats,
        'post_tags': post_tags,
        'related_posts': related_posts,
        'comments': comments,
        'counts': len(comments),
        'score': str(score),
        'number_score': len(comments_score_list)
    }
    return render(request, 'front/Blog/post.html', context=context)


def comment_post(request, pk):
    if request.method == 'POST':
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        if len(str(month)) == 1:
            month = '0' + str(month)
        if len(str(day)) == 1:
            day = '0' + str(day)
        star = request.POST.get('star')
        if star == None:
            star = 0
        title = request.POST.get('title')
        text = request.POST.get('text')
        comment = Comments(title=title, score=star, comment=text, date=f'{year}/{month}/{day}',
                           user=request.user.username, user_id=request.user.pk, post_id=pk)
        comment.save(using='blog')
        post_title = Post.objects.using('blog').get(pk=pk)
        post_title = post_title.title
        return redirect('post', title=post_title)


# Panel views
@login_required
@permission_required(perm='Blog.add_post')
def panel_add_post(request):
    if not request.user.is_staff:
        return redirect('index')

    cats = Category.objects.using('blog').order_by('title')
    sub_cats = SubCategory.objects.using('blog').order_by('category', 'title')
    context = {
        'cats': cats,
        'sub_cats': sub_cats,
    }
    if request.method == 'POST':
        tags = request.POST.getlist('tags')[0]
        title = request.POST.get('title')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        full_text = request.POST.get('full_text')
        cat_id = Category.objects.using('blog').get(title=category).pk
        sub_cat_id = SubCategory.objects.using('blog').filter(title=sub_category, category=category)
        if len(sub_cat_id) == 0 or len(sub_cat_id) >= 2:
            messages.error(request, 'Category and subcategory do not match')
            return redirect('panel_add_post')
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        if len(str(month)) == 1:
            month = '0' + str(month)
        if len(str(day)) == 1:
            day = '0' + str(day)

        try:
            img = request.FILES['image']
            fs = FileSystemStorage(location='Media/PanelBlog/')
            filename = fs.save(img.name, img)
            imgurl = fs.url('PanelBlog/' + filename)
            if str(img.content_type).startswith('image'):
                if img.size <= 5242880:
                    post = Post(title=title, image_url=imgurl, image=img,
                                author=f"{request.user.first_name} {request.user.last_name}",
                                date=f'{year}/{month}/{day}', category=category,
                                category_id=cat_id, subcategory_id=sub_cat_id[0].pk, subcategory=sub_category,
                                full_text=full_text, tags=tags, usrer_id=request.user.pk)
                    post.save(using='blog')
                else:
                    fs.delete(filename)
            else:
                fs.delete(filename)
        except:
            pass
    return render(request, 'back/PanelBlog/add_post.html', context=context)


@login_required
@permission_required(perm='Blog.delete_post')
def panel_delete_post(request, pk):
    if not request.user.is_staff:
        return redirect('index')
    # Function to delete category with PK
    post = Post.objects.using('blog').get(pk=pk)
    post.delete()
    return redirect('panel_post_lists')


@login_required
@permission_required(perm='Blog.change_post')
def panel_edit_post(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    post = Post.objects.using('blog').get(pk=pk)
    cats = Category.objects.using('blog').order_by('title')
    sub_cats = SubCategory.objects.using('blog').order_by('category', 'title')
    context = {'post': post, 'cats': cats,
               'sub_cats': sub_cats}
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        tags = request.POST.getlist('tags')[0]
        title = request.POST.get('title')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        full_text = request.POST.get('full_text')
        cat_id = Category.objects.using('blog').get(title=category).pk
        sub_cat_id = SubCategory.objects.using('blog').filter(title=sub_category, category=category)
        if len(sub_cat_id) == 0 or len(sub_cat_id) >= 2:
            messages.error(request, 'Category and subcategory do not match')
            return redirect('panel_add_post')
        try:
            img = request.FILES['image']
            fs = FileSystemStorage(location='Media/PanelBlog/')
            filename = fs.save(img.name, img)
            imgurl = fs.url('/PanelBlog/' + filename)
            if str(img.content_type).startswith('image'):
                if img.size <= 5242880:
                    post.image = img
                    post.image_url = imgurl
                    post.save(using='blog')
                else:
                    fs = FileSystemStorage(location='Media/PanelBlog/')
                    fs.delete(filename)
            else:
                fs = FileSystemStorage(location='Media/PanelBlog/')
                fs.delete(filename)

        finally:
            post.title = title
            post.category = category
            post.subcategory = sub_category
            post.category_id = cat_id
            post.subcategory_id = sub_cat_id[0].pk
            post.full_text = full_text
            post.tags = tags
            post.save(using='blog')
            return redirect('panel_post_lists')

    return render(request, 'back/PanelBlog/edit_post.html', context=context)


@login_required
@permission_required(perm='Blog.view_post')
def panel_post_lists(request):
    if not request.user.is_staff:
        return redirect('index')

    posts = Post.objects.using('blog').order_by('-date')
    cats = Category.objects.using('blog').order_by('title')
    sub_cats = SubCategory.objects.using('blog').order_by('category', 'title')
    context = {'posts': posts, 'cats': cats,
               'sub_cats': sub_cats, }

    return render(request, 'back/PanelBlog/post_lists.html', context=context)


@login_required
@permission_required(perm='Blog.add_category')
def panel_add_category(request):
    # Function to add new category
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        category = request.POST.get('category')
        if len(Category.objects.using('blog').filter(
                title=category)) >= 1:  # Calculation of the number of categories with this title
            messages.error(request, 'There is a category with this title')
            return redirect('panel_add_category')
        category = Category(title=category)
        category.save(using='blog')
        messages.success(request, f'{category} category was created')

        return redirect('panel_add_category')
    cats = Category.objects.all()
    context = {
        'cats': cats,
    }
    return render(request, 'back/PanelBlog/add_category.html', context=context)


@login_required
@permission_required(perm='Blog.delete_category')
def panel_delete_category(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    # Function to delete category with PK
    cat = Category.objects.using('blog').get(pk=pk)
    cat.delete(using='blog')
    return redirect('panel_add_category')


@login_required
@permission_required(perm='Blog.change_category')
def panel_edit_category(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    # Function to edit category with PK
    if request.method == 'POST':
        new_cat = request.POST.get('new_cat')
        if len(Category.objects.using('blog').filter(
                title=new_cat)) >= 1:  # Calculation of the number of categories with this title
            messages.error(request, 'No change was made (It already exists)')
            return redirect('panel_add_category')
        cat = Category.objects.using('blog').get(pk=pk)
        cat.title = new_cat
        cat.save(using='blog')
        return redirect('panel_add_category')


@login_required
@permission_required(perm='Blog.add_subcategory')
def panel_add_sub_category(request):
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        category_title = request.POST.get('category_title')
        sub_category = request.POST.get('sub_category')
        if len(SubCategory.objects.using('blog').filter(title=sub_category, category=category_title)) >= 1:
            # Calculation of the number of sub categories with this title
            messages.error(request, 'There is a sub category with this title')
            return redirect('panel_add_sub_category')
        cat_id = Category.objects.using('blog').get(title=category_title).pk
        sub_cat = SubCategory(title=sub_category, category_id=cat_id, category=category_title)
        sub_cat.save(using='blog')
        messages.success(request, f'{sub_category} sub category was created')
        return redirect('panel_add_sub_category')
    cats = Category.objects.using('blog').all()
    sub_cats = SubCategory.objects.using('blog').all()
    context = {
        'cats': cats,
        'sub_cats': sub_cats,
    }
    return render(request, 'back/PanelBlog/add_sub_category.html', context=context)


@login_required
@permission_required(perm='Blog.delete_subcategory')
def panel_delete_sub_category(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    # Function to delete sub category with PK
    sub_cat = SubCategory.objects.using('blog').get(pk=pk)
    sub_cat.delete(using='blog')
    messages.warning(request, 'Removed successfully')
    return redirect('panel_add_sub_category')


@login_required
@permission_required(perm='Blog.change_subcategory')
def panel_edit_sub_category(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    # Function to edit sub category with PK
    if request.method == 'POST':
        new_cat = request.POST.get('new_cat')
        new_sub_cat = request.POST.get('new_sub_cat')
        if len(SubCategory.objects.using('blog').filter(title=new_sub_cat, category=new_cat)) >= 1:
            # Calculation of the number of sub categories with this title
            messages.error(request, 'No change was made (It already exists)')
            return redirect('panel_add_sub_category')
        cat = SubCategory.objects.using('blog').get(pk=pk)
        cat.title = new_sub_cat
        cat.category = new_cat
        cat.save(using='blog')
        return redirect('panel_add_sub_category')


@login_required
@permission_required(perm='Blog.view_comments')
def panel_comments(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    comments = Comments.objects.using('blog').filter(post_id=pk).order_by('-date')
    context = {
        'comments': comments,
    }
    return render(request, 'back/PanelBlog/comments.html', context=context)


@login_required
@permission_required(perm='Blog.change_comments')
def panel_comments_edit(request, pk):
    if not request.user.is_staff:
        return redirect('index')
    if request.method == 'POST':
        comments = Comments.objects.using('blog').get(pk=pk)
        status = request.POST.get('status')
        if status == 'on':
            comments.status = True
        else:
            comments.status = False
        comments.save(using='blog')
        return redirect(request.META['HTTP_REFERER'])


@login_required
@permission_required(perm='Blog.delete_comments')
def panel_comments_delete(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    comment = Comments.objects.using('blog').get(pk=pk)
    comment.delete(using='blog')
    return redirect(request.META['HTTP_REFERER'])


# The first Ajax code is very busy and complicated #

def like_system(request):
    if request.method == 'POST':
        type_comment = request.POST.get('comment_id')
        if 'true' in type_comment:
            if len(OpinionComment.objects.using('blog').filter(opinion=1, user_id=request.user.pk,
                                                               comment_id=int(type_comment[5:]),
                                                               user=request.user)) >= 1:
                comment = Comments.objects.using('blog').get(pk=int(type_comment[5:]))
                data = {'number_like': comment.like, 'number_dis_like': comment.dis_like,
                        'comment_id': int(type_comment[5:])}
                return JsonResponse(data)
            elif len(OpinionComment.objects.using('blog').filter(opinion=0, user_id=request.user.pk,
                                                                 comment_id=int(type_comment[5:]),
                                                                 user=request.user)) >= 1:
                opinioncomment = OpinionComment.objects.using('blog').get(opinion=0, user_id=request.user.pk,
                                                                          comment_id=int(type_comment[5:]),
                                                                          user=request.user)
                opinioncomment.opinion = 1
                opinioncomment.save()
                comment = Comments.objects.using('blog').get(pk=int(type_comment[5:]))
                comment.like += 1
                comment.dis_like -= 1
                comment.save(using='blog')

                data = {'number_like': comment.like, 'number_dis_like': comment.dis_like,
                        'comment_id': int(type_comment[5:])}
                return JsonResponse(data)
            else:

                opinioncomment = OpinionComment(opinion=1, user_id=request.user.pk, comment_id=int(type_comment[5:]),
                                                user=request.user)
                opinioncomment.save(using='blog')
                comment = Comments.objects.using('blog').get(pk=int(type_comment[5:]))
                comment.like += 1
                comment.save(using='blog')
                data = {'number_like': comment.like, 'number_dis_like': comment.dis_like,
                        'comment_id': int(type_comment[5:])}
                return JsonResponse(data)
        elif 'false' in type_comment:
            if len(OpinionComment.objects.using('blog').filter(opinion=0, user_id=request.user.pk,
                                                               comment_id=int(type_comment[6:]),
                                                               user=request.user)) >= 1:
                comment = Comments.objects.using('blog').get(pk=int(type_comment[6:]))
                data = {'number_like': comment.like, 'number_dis_like': comment.dis_like,
                        'comment_id': int(type_comment[6:])}
                return JsonResponse(data)
            elif len(OpinionComment.objects.using('blog').filter(opinion=1, user_id=request.user.pk,
                                                                 comment_id=int(type_comment[6:]),
                                                                 user=request.user)) >= 1:
                opinioncomment = OpinionComment.objects.using('blog').get(opinion=1, user_id=request.user.pk,
                                                                          comment_id=int(type_comment[6:]),
                                                                          user=request.user)
                opinioncomment.opinion = 0
                opinioncomment.save(using='blog')
                comment = Comments.objects.get(pk=int(type_comment[6:]))
                comment.like -= 1
                comment.dis_like += 1
                comment.save(using='blog')
                data = {'number_like': comment.like, 'number_dis_like': comment.dis_like,
                        'comment_id': int(type_comment[6:])}
                return JsonResponse(data)
        else:
            opinioncomment = OpinionComment(opinion=0, user_id=request.user.pk, comment_id=int(type_comment[6:]),
                                            user=request.user)
            opinioncomment.save(using='blog')
            comment = Comments.objects.using('blog').get(pk=int(type_comment[6:]))
            comment.dis_like += 1
            comment.save(using='blog')
            data = {'number_like': comment.like, 'number_dis_like': comment.dis_like,
                    'comment_id': int(type_comment[6:])}
            return JsonResponse(data)
