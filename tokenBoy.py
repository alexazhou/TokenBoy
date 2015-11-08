import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.httputil
import urllib.parse
import time
import json
import config


tokens = {}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, tokenBoy~")

class TokenHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name','UnKnown')
        ret = {}
        if name not in tokens:
            ret['error'] = 'not found'
        else:
            ret['token'] = tokens[name]

        self.write( json.dumps( ret ) )

application = tornado.web.Application([
    (r"/token", TokenHandler),
    (r"/", MainHandler),
])


def token_refresher():
    print('token refresh...')
    
    for key in config.token_sources.keys():    
        def handle_factory( key):
            def handle(response):
                #print('async httpclient response: ',response)
                print('async httpclient response body: ',response.body)
                ret_dict = json.loads( response.body.decode('utf8') )
                tokens[key] = ret_dict['access_token']               
                print('%s token:%s'%(key,tokens[key])) 
            return handle            

        #body = urllib.parse.urlencode(config.token_sources[key]['args'])
        url = tornado.httputil.url_concat( config.token_sources[key]['url'], config.token_sources[key]['args'] )
        async_http_client = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest( url, method=config.token_sources[key]['method']  )
        async_http_client.fetch( request, callback=handle_factory(key) )





if __name__ == "__main__":
    application.listen(config.bind_port,address=config.bind_ip)
    tornado.ioloop.IOLoop.instance().call_later(0, token_refresher)
    tornado.ioloop.PeriodicCallback(token_refresher,7000*1000).start()
    tornado.ioloop.IOLoop.instance().start()
