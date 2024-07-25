from django.shortcuts import render
from django.db.models import Sum, F, Count
from .models import Product, Order
from datetime import date, timedelta


def report_view(request):
    # Bugungi kun va so'nggi 10 kun
    today = date.today()
    ten_days_ago = today - timedelta(days=10)

    # Har bir mahsulotdan qancha sotilgan (umumiy miqdor)
    products_quantity = Product.objects.annotate(total_quantity_sold=Sum('order__quantity'))

    # Har bir mahsulotdan umumiy tushgan pul (price * quantity)
    products_revenue = Product.objects.annotate(total_revenue=Sum(F('order__quantity') * F('price')))

    # Har bir mijozning umumiy buyurtma soni
    customers_orders = Order.objects.values('customer').annotate(total_orders=Count('id'))

    # Har bir mijozning umumiy xarajatlari
    customers_spent = Order.objects.values('customer').annotate(total_spent=Sum(F('quantity') * F('product__price')))

    # Eng ko'p sotilgan mahsulot
    top_selling_product = Product.objects.annotate(total_quantity_sold=Sum('order__quantity')).order_by(
        '-total_quantity_sold').first()

    # Umumiy tushgan pul
    total_revenue = Order.objects.aggregate(total_revenue=Sum(F('quantity') * F('product__price')))

    # Bir kunlik hisobot
    one_day_report = Order.objects.filter(sold_date=today).values('product__name').annotate(
        total_quantity_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
    )

    # 10 kunlik hisobot
    ten_day_report = Order.objects.filter(sold_date__gte=ten_days_ago, sold_date__lte=today).values(
        'product__name').annotate(
        total_quantity_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
    )

    context = {
        'today': today,
        'ten_days_ago': ten_days_ago,
        'products_quantity': products_quantity,
        'products_revenue': products_revenue,
        'customers_orders': customers_orders,
        'customers_spent': customers_spent,
        'top_selling_product': top_selling_product,
        'total_revenue': total_revenue,
        'one_day_report': one_day_report,
        'ten_day_report': ten_day_report,
    }

    return render(request, 'report.html', context)