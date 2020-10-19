from bs4 import BeautifulSoup
import requests
import sys

class Title():
    
    def __init__(self, name, synopsis, year, maturity, genre, starring, creators):
        self.name = name
        self.synopsis = synopsis
        self.year = year
        self.maturity = maturity
        self.genre = genre
        self.starring = starring
        self.creators = creators
        self.seasons = []

    def add_season(self, season):
        self.seasons.append(season)

    def set_details(self, download, genres, moods, cast):
        self.download = download
        self.genres = genres
        self.moods = moods
        self.cast = cast

    def print(self):
        general_details = ("{}\n"
                           "{} | {} | {}\n"
                           "{}\n"
                           "Protagonistas: {}\n"
                           "Creadores: {}\n")
        
        specific_details = ("Descarga: {}\n"
                            "Géneros: {}\n"
                            "Moods: {}\n"
                            "Elenco: {}\n")

        print(general_details.format(self.name, self.year, self.maturity, self.genre, self.synopsis, ", ".join(self.starring), ", ".join(self.creators)))
        print("=" * 30)
        print(specific_details.format(self.download, ", ".join(self.genres), ", ".join(self.moods), ", ".join(self.cast)))
        print("=" * 30)

        for s in range(0, len(self.seasons)):
            self.seasons[s].print(s+1)

class Season():
    
    def __init__(self, year, synopsis):
        self.year = year
        self.synopsis = synopsis
        self.episodes = []

    def add_episode(self, episode):
        self.episodes.append(episode)

    def print(self, seasonNumber):
        season_details = ("Temporada {} | {}\n"
                          "{}\n"
                          "Episodios\n")
        print(season_details.format(seasonNumber, self.year, self.synopsis))
        for e in range(0, len(self.episodes)):
            self.episodes[e].print(e+1)

class Episode():
    
    def __init__(self, name, synopsis):
        self.name = name
        self.synopsis = synopsis

    def print(self, episodeNumber):
            episode_details = ("{}. {}\n"
                               "{}\n")
            print(episode_details.format(episodeNumber, self.name, self.synopsis))

class NetflixScrapper():

    @staticmethod
    def scrape_title(target_url):
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

        netflixTitle = Title(title['title'], title['synopsis'], title['year'], title['maturity'], title['genre'], title['starring'], title['creators'],)

        #
        # Seasons 
        #
        seasons_soup = html_soup.find_all(class_ = 'season')
        for s in seasons_soup:
            season = {}
            year_string = s.find(attrs = {'data-uia': 'season-release-year'}).string.split()
            season['year'] = year_string[-1]
            season['synopsis'] = s.find(attrs = {'data-uia': 'season-synopsis'}).string
            season['episodes'] = []
            
            netflixSeason = Season(season['year'], season['synopsis'])
            
            #
            # Episodes
            #
            episodes_soup = s.find_all(attrs = {'data-uia': 'episode'})
            for e in episodes_soup:
                episode = {}
                title_string = e.find(attrs = {'data-uia': 'episode-title'}).string.split()
                episode['title'] = " ".join(title_string[1:])
                episode['synopsis'] = e.find(attrs = {'data-uia': 'episode-synopsis'}).string
                netflixSeason.add_episode(Episode(episode['title'], episode['synopsis']))
            
            netflixTitle.add_season(netflixSeason)

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
        netflixTitle.set_details(more_details['download'], more_details['genres'], more_details['moods'], more_details['cast'])
        return netflixTitle


def main(argv):
    url = "https://www.netflix.com/ar/title/70143836"
    if len(argv) > 1:
        url = argv[1]
    title = NetflixScrapper.scrape_title(url)
    title.print()

if __name__ == "__main__":
    main(sys.argv)