from bs4 import BeautifulSoup
import requests
import sys

def print_title(title):
    general_details = ("{}\n"
                       "{} | {} | {}\n"
                       "{}\n"
                       "Protagonistas: {}\n"
                       "Creadores: {}\n")

    specific_details = ("Descarga: {}\n"
                    "Géneros: {}\n"
                    "Moods: {}\n"
                    "Elenco: {}\n")

    season_details = ("Temporada {} | {}\n"
                      "{}\n"
                      "Episodios\n")

    episode_details = ("{}. {}\n"
                       "{}\n")

    print(general_details.format(title['title'], title['year'], title['maturity'], title['genre'], title['synopsis'], ", ".join(title['starring']), ", ".join(title['creators'])))
    print("=" * 30)

    print(specific_details.format(title['details']['download'], ", ".join(title['details']['genres']), ", ".join(title['details']['moods']), ", ".join(title['details']['cast'])))
    print("=" * 30)

    for n in range(0, len(title['seasons'])):
        season = title['seasons'][n]
        print(season_details.format(n+1, season['year'], season['synopsis']))
        
        for e in range(0, len(season['episodes'])):
            episode = season['episodes'][e]
            print(episode_details.format(e+1, episode['title'], episode['synopsis']))
        print("=" * 20)


def scrape(target_url):
    # TO-DO: Handle exceptions: connection
    http_response = requests.get(target_url)
    html_soup = BeautifulSoup(http_response.content, 'html.parser')

    details = html_soup.find(class_ = 'details-container')

    #
    # General
    #
    title = {}
    title['title'] = details.find(attrs = {'data-uia': 'title-info-title'}).string
    title['synopsis'] = details.find(attrs = {'data-uia': 'title-info-synopsis'}).string
    title['year'] = details.find(attrs = {'data-uia': 'item-year'}).string
    title['maturity'] = details.find(attrs = {'data-uia': 'item-maturity'}).string
    title['genre'] = details.find(attrs = {'data-uia': 'item-genre'}).string
    title['starring'] = details.find(attrs = {'data-uia': 'info-starring'}).string.split(',')
    try:
        title['creators'] = details.find(attrs = {'data-uia': 'info-creators'}).string.split(',')
    except AttributeError as e:
        title['creators'] = []
    #
    # Seasons
    #
    seasons_soup = html_soup.find_all(class_ = 'season')
    seasons = []
    for s in seasons_soup:
        season = {}
        year_string = s.find(attrs = {'data-uia': 'season-release-year'}).string.split()
        season['year'] = year_string[-1]
        season['synopsis'] = s.find(attrs = {'data-uia': 'season-synopsis'}).string
        season['episodes'] = []
        #
        # Episodes
        #
        episodes_soup = s.find_all(attrs = {'data-uia': 'episode'})
        for e in episodes_soup:
            episode = {}
            title_string = e.find(attrs = {'data-uia': 'episode-title'}).string.split()
            episode['title'] = " ".join(title_string[1:])
            episode['synopsis'] = e.find(attrs = {'data-uia': 'episode-synopsis'}).string
            season['episodes'].append(episode)
        
        seasons.append(season)

    title['seasons'] = seasons

    #
    # Details
    #
    more_details = {}
    more_details_soup = html_soup.find(attrs = {'data-uia': 'section-more-details'})

    more_details['download'] = more_details_soup.find(attrs = {'data-uia': 'more-details-item-download'}).text

    genres_tags = more_details_soup.find_all(attrs = {'data-uia': 'more-details-item-genres'})
    genres = []
    for g in genres_tags:
        genre = g.text.strip(',')
        genres.append(genre)

    mood_tags = more_details_soup.find_all(attrs = {'data-uia': 'more-details-item-mood-tag'})
    moods = []
    for m in mood_tags:
        mood = m.text.strip(',')
        moods.append(mood)

    cast_tags = more_details_soup.find_all(attrs = {'data-uia': 'more-details-item-cast'})
    cast = []
    for m in cast_tags:
        cast_item = m.string
        cast.append(cast_item)

    more_details['genres'] = genres
    more_details['moods'] = moods
    more_details['cast'] = cast

    title['details'] = more_details
    return title

def main(argv):
    url = "https://www.netflix.com/ar/title/70143836"
    if len(argv) > 1:
        url = argv[1]
    title = scrape(url)
    print_title(title)

if __name__ == "__main__":
    main(sys.argv)