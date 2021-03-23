from django.shortcuts import render

import csv, io
from django.shortcuts import render
from django.contrib import messages

from api.models import Category

def category_upload(request):
    template = 'category_upload.html'

    if request.method == 'GET':
        return render(request,  template)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        if csv_file.name == 'category.csv':
            _, created = Category.objects.update_or_create(
                id=column[0],
                name=column[1],
                slug=column[2]
            )
        elif csv_file.name == 'comments':
            _, created = Category.objects.update_or_create(
                id=column[0],
                review_id=column[1],
                text=column[2],
                author=column[3],
                pub_date=column[4]
            )
        elif csv_file.name == 'genre.csv':
            _, created = Category.objects.update_or_create(
                id=column[0],
                name=column[1],
                slug=column[2],
            )
    context= {}
    return render(request, template, context)