from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from .forms import SignupForm
from django.contrib.auth import login,logout
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm  
import csv
import pandas as pd
from django.http import HttpResponse
from django.db.models.functions import TruncMonth
# from django.contrib.auth.views import LoginView


def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")  
    
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after signup
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "tracker/register.html", {"form": form})

def custom_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")  # Redirect if already logged in

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # ✅ Log in the user
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "tracker/login.html", {"form": form})

@login_required
def dashboard(request):


    all_expenses = Expense.objects.filter(user=request.user)
    
    # Calculate total expenses across all categories (for header display)
    total_expenses = all_expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    # Get category-wise summary (for filter display)
    category_summary = all_expenses.values("category").annotate(total=Sum("amount"))
   

    return render(
        request,
        "tracker/dashboard.html",
        {
            "total_expenses": total_expenses,  # Always sum of all expenses
            "category_summary": category_summary,  
        },
    )



@login_required
def add_edit_expense(request, pk=None):
    if pk:  # If expense_id is provided, fetch the expense for editing
        expense = get_object_or_404(Expense, id=pk, user=request.user)
    else:  # Otherwise, create a new expense
        expense = None

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.user = request.user
            new_expense.save()
            return redirect("dashboard")
    else:
        form = ExpenseForm(instance=expense)

    return render(
        request,
        "tracker/add_expense.html",
        {"form": form, "expense": expense},
    )

@login_required
def delete_expense(request, pk):

    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect('expense-list')

@login_required
def filter_expenses(request):
    category = request.GET.get("category", "All")
    expenses = Expense.objects.filter(user=request.user)

    if category != "All":
        expenses = expenses.filter(category=category)

     # Group expenses by month
    monthly_expenses = (
        expenses.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    months = [item["month"].strftime("%b %Y") for item in monthly_expenses]  # Format: "Jan 2024"
    month_totals = [item["total"] for item in monthly_expenses]
    

    expenses_data = list(expenses.values("id", "title", "amount", "category", "date"))
    category_summary = expenses.values("category").annotate(total=Sum("amount"))
    categories = [item["category"] for item in category_summary]
    totals = [item["total"] for item in category_summary]

    return JsonResponse(
        {"expenses": expenses_data,
        "categories": categories,
        "totals": totals, "months": months,
        "month_totals": month_totals})




@login_required
def export_expenses(request):
    format_type = request.GET.get("format", "csv")
    selected_ids = request.GET.getlist("ids")  # Get selected expense IDs

    # Filter expenses based on selected IDs, or return all if none selected
    expenses = Expense.objects.filter(user=request.user)
    if selected_ids:
        expenses = expenses.filter(id__in=selected_ids)

    expenses = expenses.values("title", "amount", "category", "date")

    # Calculate total expenses
    total_expenses = sum(expense["amount"] for expense in expenses)

    if format_type == "xlsx":
        df = pd.DataFrame(expenses)
        df.loc[len(df)] = ["Total", total_expenses, "All Categories", ""]  # Add Total Row

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="expenses.xlsx"'

        with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Expenses")

        return response

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(["Title", "Amount", "Category", "Date"])
    for expense in expenses:
        writer.writerow([expense["title"], expense["amount"], expense["category"], expense["date"]])
    writer.writerow(["Total", total_expenses])  # Add Total Row
    return response



@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')



@login_required
def expense_list(request):
    selected_category = request.GET.get("category", "All")  
    expenses = Expense.objects.filter(user=request.user)  # Filter by logged-in user
    category_summary = expenses.values("category").annotate(total=Sum("amount"))
    return render(
        request, 
        "tracker/expense_list.html", 
        {
         "expenses": expenses, 
         "category_summary": category_summary,
         "selected_category": selected_category,
        }
    )