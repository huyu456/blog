from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http.response import Http404, HttpResponse
from .models import Blog, BlogType, ReadNum


def blog_same_data(request, blogs_all_list):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blogs_all_list, 4)
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number

    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
        print(blog_count)

    context = {}
    # context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blogs_list'] = page_of_blogs.object_list
    context['blog_dates'] = blog_dates_dict
    context['blog_types'] = BlogType.objects.all()
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = blog_same_data(request, blogs_all_list)
    return render(request, 'blog.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)

    if not request.COOKIES.get('blog_%s_read' % blog_pk,):
        # 通过查询博客数量来判断是否存在
        if ReadNum.objects.filter(blog=blog).count():
            # 存在记录
            readnum = ReadNum.objects.get(blog=blog)# 查询出具体的某一条博客
            # readnum.read_num += 1
            # readnum.save()
        else:
            readnum = ReadNum(blog=blog)
            # readnum.read_num += 1
            # readnum.save()
        readnum.read_num += 1
        readnum.save()

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    response = render(request, 'blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_pk,'true',max_age=43200)
    return response


def blog_type_list(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)  # 查询出BlogType中的blog_type,查询条件为blog_type_p
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = blog_same_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog_type_list.html', context)


def blog_dates_list(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = blog_same_data(request, blogs_all_list)
    return render(request, 'blog_date.html', context)


def search(request):
    try:
        wd = request.GET.get('wd')
        if not wd:
            return HttpResponse('没有查询到结果!')

        blogs_all_list = Blog.objects.filter(title__contains=wd)
        context = blog_same_data(request, blogs_all_list)
        context['wd'] = wd
    except Exception:
        raise Http404
    return render(request, 'search.html', context)
