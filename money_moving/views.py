from django.shortcuts import render, redirect
from .forms import TransactionForm

# Create your views here.
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_transaction')
    else:
        form = TransactionForm()

    return render(request, 'money_moving/add_transaction', {'form': form})