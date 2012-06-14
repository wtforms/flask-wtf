from base import TestCase
from flask.ext.wtf import html5


class DummyField(object):
    def __init__(self, data, name='f', label='', id='', type='TextField'):
        self.data = data
        self.name = name
        self.label = label
        self.id = id
        self.type = type

    _value       = lambda x: x.data
    __unicode__  = lambda x: x.data
    __call__     = lambda x, **k: x.data
    __iter__     = lambda x: iter(x.data)
    iter_choices = lambda x: iter(x.data)


class HTML5Tests(TestCase):

    field = DummyField("name", id="name", name="name")

    def test_url_input(self):

        self.assertEqual(html5.URLInput()(self.field),
            '<input id="name" name="name" type="url" value="name">')

    def test_search_input(self):

        self.assertEqual(html5.SearchInput()(self.field),
            '<input id="name" name="name" type="search" value="name">')

    def test_date_input(self):

        self.assertEqual(html5.DateInput()(self.field),
            '<input id="name" name="name" type="date" value="name">')

    def test_email_input(self):

        self.assertEqual(html5.EmailInput()(self.field),
            '<input id="name" name="name" type="email" value="name">')

    def test_number_input(self):

        self.assertEqual(html5.NumberInput()(self.field, min=0, max=10),
            '<input id="name" max="10" min="0" name="name" type="number" value="name">')

    def test_range_input(self):

        self.assertEqual(html5.RangeInput()(self.field, min=0, max=10),
            '<input id="name" max="10" min="0" name="name" type="range" value="name">')

