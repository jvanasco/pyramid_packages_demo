from . import TestViews , headers_util

class TestViewsSimple(TestViews):

    def _urls_200(self,urls,is_preview=False,is_https=False):
        good= []
        bad= []
        for url in urls:
            headers= headers_util( is_preview=is_preview, is_https=is_https )
            res = self.app.get(url,headers=headers,extra_environ=headers)
            if res.status_int == 200 :
                good.append( url )
            else:
                bad.append( url )
        if len(bad) :
            self.fail("""The following urls did not HTTP-200 : %s""" % bad )

    def _urls_302(self,urls,is_preview=False,is_https=False):
        headers= headers_util( is_preview=is_preview, is_https=is_https)
        good= []
        bad= []
        for url in urls:
            res = self.app.get(url,headers=headers)
            if res.status_int == 302 :
                good.append( url )
            else:
                bad.append( url )
        if len(bad) :
            self.fail("""The following urls did not HTTP-302 : %s""" % bad )



    def test_some_urls(self):
        urls= [
            '/',
            '/account/sign-up',
            '/account/login',
        ]
        self._urls_200(urls)

