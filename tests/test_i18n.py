from __future__ import with_statement

from base import TestCase


class TestI18NCase(TestCase):
    def test_submitted_not_valid(self):
        self.app.config['CSRF_ENABLED'] = False

        response = self.client.post(
            "/",
            headers={'Accept-Language': 'zh-CN,zh;q=0.8'},
            data={}
        )
        assert '\u8be5\u5b57\u6bb5\u662f' in response.data
