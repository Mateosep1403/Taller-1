from django.shortcuts import render
from django.http import HttpResponse

from.models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

def home (request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render('request', 'home.html', {'searchTerm':searchTerm, 'movies':movies})
def about (request):
    return render('request', 'about.html', {'name': 'Mateo Sepúlveda'})


def signup (request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})



def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()


    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}


    # Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1


    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))


    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')


    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)


    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)


    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()


    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')


    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})


def genre_statistics_view(request):
    matplotlib.use('Agg')

    # 1. Obtener todas las películas
    all_movies = Movie.objects.all()

    # 2. Crear un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_genre = {}

    # 3. Filtrar las películas y contar
    for movie in all_movies:
        # Considerar solo el primer género y limpiar espacios
        if movie.genre:
            genre = movie.genre.split(',')[0].strip()
            if genre in movie_counts_by_genre:
                movie_counts_by_genre[genre] += 1
            else:
                movie_counts_by_genre[genre] = 1

    # 4. Preparar datos para la gráfica
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_genre))

    # 5. Crear la gráfica de barras (¡con los datos de género!)
    plt.figure(figsize=(10, 6))  # Aumentar tamaño para que quepan los nombres
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')

    # 6. Personalizar la gráfica con nuevos títulos
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=45,
               ha="right")  # Rotar etiquetas para mejor lectura

    # 7. Ajustar el espaciado
    plt.subplots_adjust(bottom=0.25)

    # 8. Guardar la gráfica en un objeto BytesIO (esto no cambia)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 9. Convertir la gráfica a base64 (esto no cambia)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()  # Cerrar la figura para liberar memoria
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # 10. Renderizar la nueva plantilla 'genre_statistics.html' con la gráfica
    return render(request, 'genre_statistics.html', {'graphic': graphic})