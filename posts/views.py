import self
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .forms import PostCreationForm, PostUpdateForm, CreateCommentForm
from .models import Post, Category, Tag


# Create your views here.


class IndexView(ListView):
    template_name = 'posts/index.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['slider_posts'] =Post.objects.all().filter(slider_post=True)
        return context

class PostDetail(DetailView,FormMixin):
    template_name = 'posts/detail.html'
    model = Post
    context_object_name = 'single'
    form_class = CreateCommentForm

    def get(self,request,*args,**kwargs):
        self.hit = Post.objects.filter(id=self.kwargs['pk']).update(hit=F('hit')+1)
        return super(PostDetail, self).get(request,*args,**kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['previous']=Post.objects.filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
        context['next']=Post.objects.filter(id__gt=self.kwargs['pk']).order_by('pk').first()
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.post = self.object
            form.save()
            return super(PostDetail, self).form_valid(form)
        else:
            return super(PostDetail, self).form_invalid(form)

    def post(self,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('detail',kwargs={"pk":self.object.pk,"slug":self.object.slug})



class CategoryDetail(ListView):
    model = template_name = 'categories/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        self.category = get_object_or_404(Category,pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        self.category = get_object_or_404(Category,pk=self.kwargs['pk'])
        context['category']=self.category
        return context


class TagDetail(ListView):
    model = Post
    template_name = 'tags/tag_detail.html'
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        self.tag = get_object_or_404(Tag,slug=self.kwargs['slug'])
        return Post.objects.filter(tag=self.tag).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag,slug=self.kwargs['slug'])
        context['tag']=self.tag
        return context

@method_decorator(login_required(login_url='/users/login'),name="dispatch")
class CreatePostView(CreateView):
    template_name = 'posts/create-post.html'
    form_class = PostCreationForm
    model = Post


    def get_success_url(self):
        return reverse('detail',kwargs={"pk":self.object.pk,"slug":self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        tags=self.request.POST.get("tag").split(",")

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count()<1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                exist_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(exist_tag)
        return super(CreatePostView, self).form_valid(form)


@method_decorator(login_required(login_url='/users/login'), name="dispatch")
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('detail', kwargs={"pk": self.object.pk, "slug": self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tag.clear()
        tags = self.request.POST.get("tag").split(",")

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                exist_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(exist_tag)

        return super(UpdatePostView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UpdatePostView, self).get(request, *args, **kwargs)


@method_decorator(login_required(login_url='/users/login'), name="dispatch")
class DeletePostView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'posts/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(DeletePostView, self).get(request, *args, **kwargs)


class SearchView(ListView):
    model = Post
    template_name = 'posts/search.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query:
            return Post.objects.filter(Q(title__icontains=query)|
                                       Q(content__icontains=query)|
                                       Q(tag__title__icontains=query)
                                      ).order_by('id').distinct()
        return Post.objects.all().order_by('id')
