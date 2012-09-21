""" Books
"""
import logging
from random import randint
from DateTime import DateTime
import feedparser
import urllib
from Products.Five.browser import BrowserView

logger = logging.getLogger('allen.ploneconf2010.google')
FEED = 'http://books.google.com/books/feeds/volumes'

class Books(BrowserView):
    """ Grab books from books.google.com """

    @property
    def items(self):
        """ Get items
        """
        query = self.request.form.get('q', 'python')
        maxitems = self.request.form.get('m', 100) or 100
        maxitems = int(maxitems)

        for start in range(0, maxitems, 10):
            url = {
                'max-results': 10,
                'q': query
            }
            if start:
                url['start-index'] = start
            url = urllib.urlencode(url)
            data = feedparser.parse(FEED + '?' + url)

            for entry in data['entries']:
                entrydata = feedparser.parse(entry['id'])
                entries = entrydata.get('entries')
                if not entries:
                    continue
                yield entries[0]

    def add_book(self, form):
        """ Add a book from google feed entry
        """
        isbn = form.get('identifier').replace(':', '-')
        title = form.get('title')

        if isbn in self.context.objectIds():
            logger.warn('Skipping book %s as it is already imporder', title)
            return

        author = form.get('creator', '')
        rating = form.get('rating', 0) or randint(0, 5)

        updated = form.get('updated_parsed')
        updated = '%d/%d/%d %d:%d:%d' % tuple(updated[0:6])
        updated = DateTime(updated)

        query = {
            'creators': author and [author] or [],
            'isbn': isbn,
            'link': form.get('id', ''),
            'publisher': form.get('publisher', ''),
            'rating': rating,
            'subject_keywords': [x.strip() for
                                 x in form.get('subject', '').split('/')],
            'description': form.get('summary', ''),
            'title': title,
            'effective_date': updated
        }
        book_id = self.context.invokeFactory('Book', isbn, title=title)
        book = self.context[book_id]
        book.processForm(data=1, metadata=1, values=query)
        logger.info('Added book %s', title)

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        logger.info('Books import started: %s', kwargs)
        for item in self.items:
            self.add_book(item)
        logger.info('Books import done')
        return 'Done'
