from __future__ import annotations
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, ShowForm
from .models import Show, Subscription, Episode, UserProfile


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data['phone_number']
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone_number = phone_number
            profile.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    subscriptions = (
        Subscription.objects.filter(user=request.user)
        .select_related('show', 'last_notified_episode')
        .prefetch_related(
            Prefetch(
                'show__episodes',
                queryset=Episode.objects.order_by('-published_at', '-created_at'),
            )
        )
    )
    return render(request, 'tracker/dashboard.html', {'subscriptions': subscriptions})


@login_required
def add_show(request):
    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            show = form.save(commit=False)
            show.owner = request.user
            show.save()
            Subscription.objects.get_or_create(user=request.user, show=show)
            return redirect('show_detail', pk=show.pk)
    else:
        form = ShowForm()
    return render(request, 'tracker/show_form.html', {'form': form})


@login_required
def show_list(request):
    shows = Show.objects.filter(owner=request.user).annotate(episode_count=Count('episodes'))
    return render(request, 'tracker/show_list.html', {'shows': shows})


@login_required
def show_detail(request, pk):
    show = get_object_or_404(Show, pk=pk)
    if show.owner != request.user and not Subscription.objects.filter(user=request.user, show=show).exists():
        return redirect('dashboard')
    episodes = show.episodes.order_by('-published_at', '-created_at')
    return render(request, 'tracker/show_detail.html', {'show': show, 'episodes': episodes})
