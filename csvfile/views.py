import csv
import io
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render

from api.models import Category, Genre, Review, Title
from authentication.models import User


def category_upload(request):
    template = 'category_upload.html'

    if request.method == 'GET':
        return render(request, template)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        if csv_file.name == 'category.csv':
            _, created = Category.objects.update_or_create(
                id=column[0],
                name=column[1],
                slug=column[2]
            )
        elif csv_file.name == 'genre.csv':
            _, created = Genre.objects.update_or_create(
                id=column[0],
                name=column[1],
                slug=column[2]
            )
        elif csv_file.name == 'titles.csv':
            _, created = Title.objects.update_or_create(
                id=column[0],
                name=column[1],
                year=datetime.strptime(column[2], '%Y'),
                category=Category.objects.get(id=int(column[3]))
            )
        elif csv_file.name == 'users.csv':
            _, create = User.objects.update_or_create(
                id=column[0],
                username=column[1],
                email=column[2],
                role=column[3],
            )
        elif csv_file.name == 'review.csv':
            _, created = Review.objects.update_or_create(
                id=column[0],
                title_id=column[1],
                text=column[2],
                author=User.objects.get(id=column[3]),
                score=column[4],
                pub_date=datetime.strptime(column[5][0:10], '%Y-%m-%d')
            )
    context = {}
    return render(request, template, context)
