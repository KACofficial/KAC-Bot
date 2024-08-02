import tmdbsimple as tmdb


def init(api_key):
    tmdb.API_KEY = api_key


def search_movie(title, max_results=10):
    search = tmdb.Search()
    response = search.movie(query=title)
    results = response.get('results', [])
    return {"results": results[:max_results], "count": len(results)}


def search_movie_id(id):
    movie = tmdb.Movies(id)
    return movie.info()
    # return {
    #     "title": resp.get('title', 'Unknown Title'),
    #     "description": resp.get('overview', 'No description available')
    # }


def get_movie_poster(movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    backdrop_path = response.get('poster_path')

    if backdrop_path:
        base_url = 'https://image.tmdb.org/t/p/original'
        banner_url = f"{base_url}{backdrop_path}"
        return banner_url
    else:
        return None


def get_movie_banner(movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    backdrop_path = response.get('backdrop_path')

    if backdrop_path:
        base_url = 'https://image.tmdb.org/t/p/original'  # You can change 'original' to another size, e.g., 'w500'
        banner_url = f"{base_url}{backdrop_path}"
        return banner_url
    else:
        return None