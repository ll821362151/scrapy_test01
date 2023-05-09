# from fake_useragent import UserAgent
#
# # fake-useragent 代理ip，暂时未用
# class RandomUserAgentMiddleware(object):
#     def __init__(self, crawler):
#         super(RandomUserAgentMiddleware, self).__init__()
#         self.ua = UserAgent()
#         self.ua_type = crawler.settings.get('USER_AGENT_TYPE', 'random')
#         self.ua_rotation_enabled = crawler.settings.get('USER_AGENT_ROTATION_ENABLED', False)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler)
#
#     def process_request(self, request, spider):
#         if self.ua_rotation_enabled:
#             if self.ua_type == 'random':
#                 ua = self.ua.random
#             else:
#                 ua = getattr(self.ua, self.ua_type)
#             request.headers.setdefault('User-Agent', ua)
#
#
# class RandomProxyMiddleware(object):
#     def __init__(self, settings):
#         super(RandomProxyMiddleware, self).__init__()
#         self.proxy_list = settings.getlist('PROXY_LIST')
#         self.proxy_auth = settings.get('PROXY_AUTH', None)
#         self.proxy_rotation_enabled = settings.get('PROXY_ROTATION_ENABLED', False)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings)
#
#     def process_request(self, request, spider):
#         if self.proxy_rotation_enabled and self.proxy_list:
#             request.meta['proxy'] = self.proxy_list.pop(0)
#             if self.proxy_auth:
#                 request.headers['Proxy-Authorization'] = self.proxy_auth
#             self.proxy_list.append(request.meta['proxy'])
