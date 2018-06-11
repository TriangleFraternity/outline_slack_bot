import unittest

from com.illinoistriangle.lib.urlmarker import find_urls


class FindUrlTest(unittest.TestCase):
  def test_empty_url(self):
    urls = find_urls('hello')
    self.assertTrue(len(urls) == 0)

  def test_one_url(self):
    urls = find_urls('hello https://google.com/123/abc')
    self.assertEqual([
      'https://google.com/123/abc'
    ], urls)

  def test_multiple_urls(self):
    urls = find_urls('hello https://google.com/123/abc https://wsj.com/paywall (some random comments) http://tl.dr')
    self.assertEqual([
      'https://google.com/123/abc',
      'https://wsj.com/paywall',
      'http://tl.dr'
    ], urls)
