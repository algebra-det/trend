from django.shortcuts import render, redirect, get_object_or_404
from .models import MagicBox, Trophy
from .forms import MagicBoxForm, TrophyForm

from trend.decorators import admin_only

from django.contrib import messages

@admin_only
def trophies(request):
    trophies = Trophy.objects.all()
    context = {
        'trophies': trophies
    }
    return render(request, 'reward/trophies.html', context)

@admin_only
def trophy_detail(request, id):
    trophy = get_object_or_404(Trophy, pk=id)
    context = {
        'trophy': trophy
    }
    return render(request, 'reward/trophy_detail.html', context)


@admin_only
def create_trophy(request):
    if request.method == 'POST':
        form = TrophyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"nuovo trofeo creato con successo!")
            return redirect('reward:trophies')
    else:
        form = TrophyForm()

    context = {
        'form': form
    }

    return render(request, 'reward/create_trophy.html', context)


@admin_only
def update_trophy(request, id):
    trophy = get_object_or_404(Trophy, pk=int(id))
    if request.method == 'POST':
        form = TrophyForm(request.POST, request.FILES, instance=trophy)
        if form.is_valid():
            form.save()
            messages.success(request, f"trofeo aggiornato con successo!")
            return redirect('reward:trophy_detail', id=trophy.id)
    else:
        form = TrophyForm(instance=trophy)

    context = {
        'form': form,
        'trophy': trophy
    }

    return render(request, 'reward/update_trophy.html', context)


@admin_only
def delete_trophy(request, id):
    trophy = get_object_or_404(Trophy, pk=int(id))
    if request.method == 'POST':
        trophy.delete()
        messages.success(request, f"trofeo eliminato con successo!")
        return redirect('reward:trophies')
    context = {
        'trophy': trophy
    }
    return render(request, 'reward/delete_trophy.html', context)


# Magic Box
@admin_only
def magic_boxes(request):
    magic_boxes = MagicBox.objects.all()
    context = {
        'magic_boxes': magic_boxes
    }
    return render(request, 'reward/magic_boxes.html', context)


@admin_only
def magic_box_detail(request, id):
    magic_box = get_object_or_404(MagicBox, pk=id)
    context = {
        'magic_box': magic_box
    }
    return render(request, 'reward/magic_box_detail.html', context)

@admin_only
def create_magic_boxes(request):
    if request.method == 'POST':
        form = MagicBoxForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"scatola magica creata con successo!")
            return redirect('reward:magic_boxes')
    else:
        form = MagicBoxForm()

    context = {
        'form': form
    }

    return render(request, 'reward/create_magic_box.html', context)


@admin_only
def update_magic_boxes(request, id):
    magic_box = get_object_or_404(MagicBox, pk=int(id))
    if request.method == 'POST':
        form = MagicBoxForm(request.POST, request.FILES, instance=magic_box)
        if form.is_valid():
            form.save()
            messages.success(request, f"scatola magica aggiornata con successo!")
            return redirect('reward:magic_box_detail', id=magic_box.id)
    else:
        form = MagicBoxForm(instance=magic_box)

    context = {
        'form': form,
        'magic_box': magic_box
    }

    return render(request, 'reward/update_magic_box.html', context)


@admin_only
def delete_magic_boxes(request, id):
    magic_box = get_object_or_404(MagicBox, pk=int(id))
    if request.method == 'POST':
        magic_box.delete()
        messages.success(request, f"scatola magica eliminata con successo!")
        return redirect('reward:magic_boxes')
    context = {
        'magic_box': magic_box
    }
    return render(request, 'reward/delete_magic_box.html', context)
