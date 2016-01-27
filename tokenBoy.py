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
            ret = tokens[name]

        self.write( json.dumps( ret ) )

application = tornado.web.Application([
    (r"/token", TokenHandler),
    (r"/", MainHandler),
])

def args_render( s ):

    if s.startswith('{{') and s.endswith("}}"):
        render_map  = {}
        render_map['results'] = tokens
        s = s.strip('{}')
        idxs = s.split('.')

        target = render_map
        for idx in idxs:
            target = target[idx]

        if type(target) != str:
            raise Exception("render %s error"%s)
        #print('render result:',target)
        return target
    else:
        return s 

def refresh_token(group):
    
    print('refresh group:',group)

    def handle(response):
        #print('async httpclient response: ',response)
        #print('async httpclient response body: ',response.body)
        if response.code == 200:
            ret_dict = json.loads( response.body.decode('utf8') )
            tokens[group] = ret_dict
            print('%s request ret:%s'%(group,tokens[group])) 
        else:
            print('request token %s error, will retry after 10s'%group)
            tornado.ioloop.IOLoop.instance().call_later(10, refresh_token, group)

    try:
        #render request args
        args = {}
        for (k,v) in config.token_sources[group]['args'].items():
            args[k] = args_render( v )

        url = tornado.httputil.url_concat( config.token_sources[group]['url'], args )
        async_http_client = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest( url, method=config.token_sources[group]['method']  )
        async_http_client.fetch( request, callback = handle )
    
    except Exception as e:
        print('Exception:',e)
        print('build request for %s failed, will retry after 10s'%group)
        tornado.ioloop.IOLoop.instance().call_later(10, refresh_token, group)



def refresh_all_token():
    print('begin refresh all token...')
    
    for group in config.token_sources.keys():    
        refresh_token(group)


if __name__ == "__main__":
    application.listen(config.bind_port,address=config.bind_ip)
    tornado.ioloop.IOLoop.instance().call_later(0, refresh_all_token)
    tornado.ioloop.PeriodicCallback(refresh_all_token,7000*1000).start()
    tornado.ioloop.IOLoop.instance().start()
