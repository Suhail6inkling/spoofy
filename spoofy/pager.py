from .http import Request

from pprint import pprint

import logging

log = logging.getLogger(__name__)


class Pager:
	def __init__(self, http, obj, max=None):
		self.http = http
		self.max = max
		self.current = -1
		self.set_next(obj)

	def set_next(self, obj):
		self.total = obj['total']
		self.next = obj['next']
		self.items = obj['items']
		self.limit = obj['limit']
		self.offset = obj['offset']

	async def get_next(self):
		req = Request('GET')
		req.url = self.next
		obj = await self.http.request(req)
		self.set_next(obj)

	def __aiter__(self):
		return self

	async def __anext__(self):
		self.current += 1
		current = self.current % self.limit
		if self.current >= self.total:
			raise StopAsyncIteration
		if self.max is not None:
			if self.current >= self.max:
				raise StopAsyncIteration
		if current == 0 and self.current > 0:
			if self.next is None:
				raise StopAsyncIteration
			await self.get_next()
		return self.items[current]


class SearchPager(Pager):
	def __init__(self, http, obj, type, max=None):
		self.type = type
		super().__init__(http, obj, max)

	def set_next(self, obj):
		obj = obj[self.type]
		super().set_next(obj)


class CursorBasedPaging(SearchPager):

	def set_next(self, obj):
		obj[self.type]['offset'] = None
		self.cursors = obj[self.type]['cursors']
		super().set_next(obj)
