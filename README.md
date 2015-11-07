# TokenBoy
一个自动刷新微信Token的服务（A service base on tornado use to auto refresh weixin token）

TokenBoy是一个自动定时刷新Token的服务，可以每隔一段时间自动获取token，保存在内存中，再通过一个web接口提供token给本地其他程序。

# 作用
从微信服务器获取的access_token，有效期只有一段时间(目前为7200秒)。access_token过期后就无法使用，需要重新获取。而每次获取新的access_token之后，老的access_token自动失效。

这种情况下如果在web应用的各个逻辑点对token进行刷新，很容易出现冲突。所以最好在一个单独的服务里面处理定时刷新token的工作。

TokenBoy就是为了解决这个问题而存在。

# 配置

TokenBoy可以只需要简单的配置即可使用。除了可以用于微信，还可以用于其他有类似接口的地方。

编辑 config.py，设置需要监听的ip地址和端口，以及获取Token的接口。

    bind_ip = '0.0.0.0'
    bind_port = 8888

    token_sources['weixin'] = {
        'url':'https://api.weixin.qq.com/cgi-bin/token',
        'method':'GET',
        'args':{
            'grant_type':'client_credential',
            'appid':'*********************',
            'secret':'*********************'
        }
    }
    
# 运行

<b>python3 tokenBoy.py </b>


# 依赖

* python3
* tornado
