token_sources = {}
bind_ip = '0.0.0.0'
bind_port = 8888

#A example config for weixin token
token_sources['weixin'] = {
    'url':'https://api.weixin.qq.com/cgi-bin/token',
    'method':'GET',
    'args':{
        'grant_type':'client_credential',
        'appid':'*****************',
        'secret':'**************************'
    },
}

#A example config for weixin JSSDK token
token_sources['weixin_jsticket'] = {
    'url':'https://api.weixin.qq.com/cgi-bin/ticket/getticket',
    'method':'GET',
    'args':{
        'type':'jsapi',
        'access_token':'{{results.weixin.access_token}}' #this means the args is the access_token or weixin group
    },
}




