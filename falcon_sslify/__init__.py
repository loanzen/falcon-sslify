# -*- coding: utf-8 -*-
import falcon

YEAR_IN_SECS = 365 * 24 * 60 * 60


class FalconSSLify(object):
    """
    Initialize the falcon sslify middleware passing in configuration options. All
    configuration options are optional.

    Args:
        age(int, optional): Specifies the maximum duration for
            HTST(HTTP Strict Transport Policy). Default is ``31536000`` (1 year)

        subdomains(bool, optional): Specify if you would like to include subdomain in
            HSTS policy. Default is ``True``

        permanent(bool, optional): Specifies whether redirect is issued with
            HTTP 302 response or a HTTP 301 one. Default is ``True`` which means
            permanent redirect aka HTTP 302 response code

        skips(list, optional): A list of paths to be excluded from being redirected

    """
    def __init__(self, age=YEAR_IN_SECS, subdomains=True,
                 permanent=True, skips=None):

        self.hsts_age = age
        self.hsts_subdomains = subdomains
        self.permanent = permanent
        self.skip_list = skips or []

    def skips(self, req):
        for skip in self.skip_list:
            if req.path.startswith('/{0}'.format(skip)):
                return True
        return False

    @property
    def hsts_header(self):
        """
        Returns the proper HSTS() policy.
        """
        hsts_policy = 'max-age={0}'.format(self.hsts_age)

        if self.hsts_subdomains:
            hsts_policy += '; includeSubDomains'

        return hsts_policy

    def is_secure(self, req):
        if req.protocol.lower() == 'https':
            return True

    def process_request(self, req, resp):
        if self.skips(req) or self.is_secure(req):
            return

        xfp = req.get_header('X-FORWARDED-PROTO')
        if xfp and xfp.lower() == 'https':
            return

        if req.url.startswith('http://'):
            url = req.url.replace('http://', 'https://', 1)
            if self.permanent:
                raise falcon.HTTPMovedPermanently(url)
            else:
                raise falcon.HTTPFound(url)

    def process_response(self, req, resp, _):
        if not self.skips(req) and self.is_secure(req):
            resp.set_header('Strict-Transport-Security', self.hsts_header)
