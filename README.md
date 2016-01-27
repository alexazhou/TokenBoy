# TokenBoy
一个自动刷新微信Token的服务（A service base on tornado use to auto refresh weixin token）

TokenBoy是一个自动定时刷新Token的服务，可以每隔一段时间自动获取token，保存在内存中，再通过一个web接口提供token给本地其他程序。

# 作用
从微信服务器获取的access_token，有效期只有一段时间(目前为7200秒)。access_token过期后就无法使用，需要重新获取。而每次获取新的access_token之后，老的access_token自动失效。

这种情况下如果在web应用的各个逻辑点对token进行刷新，很容易出现冲突。所以最好在一个单独的服务里面处理定时刷新token的工作。

TokenBoy就是为了解决这个问题而存在。

# 配置

TokenBoy可以只需要简单的配置即可使用。除了可以用于微信，还可以用于其他有类似接口的地方。

###特性：

* 支持同时添加多组配置  
* 参数中支持引用获取到的结果

编辑 config.py，设置需要监听的ip地址和端口，以及获取Token的接口。

    bind_ip = '0.0.0.0'
    bind_port = 8888

    //weixin example
    token_sources['weixin'] = {
        'url':'https://api.weixin.qq.com/cgi-bin/token',
        'method':'GET',
        'args':{
            'grant_type':'client_credential',
            'appid':'*********************',
            'secret':'*********************'
        }
    }
    
    ps：这里可以用不同的名字(key)添加多组信息，tokenBoy都会进行刷新。后面获取的时候使用对应的名字获取即可
    #A example config for weixin JSSDK token
	token_sources['weixin_jsticket'] = {
    	'url':'https://api.weixin.qq.com/cgi-bin/ticket/getticket',
    	'method':'GET',
    	'args':{
    	    'type':'jsapi',
    	    'access_token':'{{results.weixin.access_token}}' #this means the args is the access_token or weixin group
    	},
	}
	
	#这里的获取微信jssdk ticket时引用了微信token作为参数

    
# 运行

<b>python3 tokenBoy.py </b>

访问 http://127.0.0.1:8888/token?name=weixin
返回如下：

    {"access_token": "lQ0ztuo3HJuiflq28rtnEVpgSCpcWjUfQW7ROtNavNA09w-B3Z0y_WWbFsWr3GPPKumx-dnMfg325qk0ZzzGsQQyYCjAVNbolESaDFsdLGUFVLhAGATJZ", "expires_in": 7200}
    
其他需要使用Token的代码可以通过以上的方式从tokenBoy获取当前有效的token

也就是tokenBoy从微信服务器获取token，其他程序从tokenBoy获取token →_→

# 依赖

* python3
* tornado
