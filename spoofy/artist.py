from .object import Object
from .mixins import ImageMixin, ExternalURLMixin


class Artist(Object, ExternalURLMixin):
	'''
	Represents an Artist object.
	
	id: str
		Spotify ID of the artist.
	name: str
		Name of the artist.
	uri: str
		Spotify URI of the artist.
	link: str
		Spotify URL of the artist.
	external_urls: dict
		Dictionary that maps type to url.
	'''

	_type = 'artist'

	def __init__(self, client, data):
		super().__init__(client, data)

		self._fill_external_urls(data.pop('external_urls'))

	async def top_tracks(self, market='from_token'):
		'''
		Returns this artists top tracks.

		:param market: Market to find tracks for.
		:return: A list of maximum 10 :class:`FullTrack` instances.
		'''

		return await self._client.get_artist_top_tracks(self.id, market=market)

	async def related_artists(self):
		'''
		Get related artists.

		:return: A list of maximum 20 :class:`FullArtist` instances.
		'''

		return await self._client.get_artist_related_artists(self.id)


class SimpleArtist(Artist):
	'''Alias for :class:`Artist`'''
	pass


class FullArtist(Artist, ImageMixin):
	'''
	Represents a complete Artist object.
	
	This type has some additional attributes not existent in :class:`Artist` or :class:`SimpleArtist`.
	
	follow_count: int
		Follow count of the artist.
	genres: List[str]
		Genres associated with the artist.
	popularity: int
		An indicator of the popularity of the track, 0 being least popular and 100 being the most.
	images: List[:class:`Image`]
		List of associated images.
	'''

	def __init__(self, client, data):
		super().__init__(client, data)

		self.follower_count = data['followers']['total']
		self.genres = data.pop('genres')
		self.popularity = data.pop('popularity')

		self._fill_images(data.pop('images'))
