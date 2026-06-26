from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseForbidden
from asgiref.sync import sync_to_async  # Дозволяє безпечно виконувати синхронний код
from .models import Note, Category
from .forms import NoteForm


# --- СИНХРОННА ЛОГІКА ДЛЯ ГОЛОВНОЇ СТОРІНКИ ---
def get_notes_data(request):
    user = request.user
    if not user.is_authenticated:
        return None, None, None, None, None, None, None

    # Обробка форми
    form = NoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.user = user
        note.save()
        return True, None, None, None, None, None, None

    # Отримання та фільтрація даних
    notes_queryset = Note.objects.filter(user=user).select_related('category', 'user').order_by('-id')

    search_query = request.GET.get('search', '')
    if search_query:
        notes_queryset = notes_queryset.filter(title__icontains=search_query)

    category_id = request.GET.get('category', '')
    if category_id:
        notes_queryset = notes_queryset.filter(category_id=category_id)

    reminder_filter = request.GET.get('reminder_filter', '')
    now = timezone.now()
    if reminder_filter == 'upcoming':
        notes_queryset = notes_queryset.filter(reminder__gt=now)
    elif reminder_filter == 'past':
        notes_queryset = notes_queryset.filter(reminder__lt=now)
    elif reminder_filter == 'none':
        notes_queryset = notes_queryset.filter(reminder__isnull=True)

    # Примусово виконуємо запити (перетворюємо в списки) всередині синхронного контексту
    notes = list(notes_queryset)
    categories = list(Category.objects.all())

    return False, notes, form, categories, search_query, category_id, reminder_filter


# --- АСИНХРОННІ VIEWS (ЕНДПОІНТИ) ---
async def notes_home(request):
    # Безпечно викликаємо синхронну логіку в окремому потоці
    is_redirect, notes, form, categories, search_query, category_id, reminder_filter = await sync_to_async(
        get_notes_data, thread_sensitive=True)(request)

    if is_redirect is None:
        return redirect('login')
    if is_redirect:
        return redirect('notes_home')

    context = {
        'notes': notes,
        'form': form,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_reminder': reminder_filter,
    }

    # Рендеринг шаблону
    return await sync_to_async(render, thread_sensitive=True)(request, 'notes_list.html', context)


async def delete_note(request, note_id):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    # Виносимо пошук та видалення в окремий потік, щоб уникнути SynchronousOnlyOperation
    def sync_delete():
        try:
            note = Note.objects.get(id=note_id, user=user)
            note.delete()
            return True
        except Note.DoesNotExist:
            return False

    success = await sync_to_async(sync_delete, thread_sensitive=True)()
    if not success:
        return HttpResponseForbidden("Ви не можете видалити цю нотатку або її не існує.")

    return redirect('notes_home')
