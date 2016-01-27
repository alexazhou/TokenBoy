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

* 支持自定义请求参数
* 支持同时添加多组配置  
* 参数中支持引用获取到的结果

下面的例子是一组配置，中包含了监听本地8888端口，配置获取微信access_token以及微信jssdk ticket，其中获取jssdk时，使用了之前获取到的access_token作为请求参数。


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
    
    #A example config for weixin JSSDK ticket
	token_sources['weixin_jsticket'] = {
    	'url':'https://api.weixin.qq.com/cgi-bin/ticket/getticket',
    	'method':'GET',
    	'args':{
    	    'type':'jsapi',
    	    'access_token':'{{results.weixin.access_token}}' #这里使用了微信access_token作为请求参数"
    	},
	}

###模版引用：
"{{}}"中的内容即表示模版引用，上面的例子中weixin在这里是组别，access_token为要选用的键

# 运行

编辑 config.py，设置需要监听的ip地址和端口，以及获取Token的接口，然后执行

<b>python3 tokenBoy.py </b>

访问 http://127.0.0.1:8888/token?name=weixin
返回如下：

    {"access_token": "lQ0ztuo3HJuiflq28rtnEVpgSCpcWjUfQW7ROtNavNA09w-B3Z0y_WWbFsWr3GPPKumx-dnMfg325qk0ZzzGsQQyYCjAVNbolESaDFsdLGUFVLhAGATJZ", "expires_in": 7200}
    
其他需要使用Token的代码可以通过以上的方式从tokenBoy获取当前有效的token

也就是tokenBoy从微信服务器获取token，其他程序从tokenBoy获取token →_→

###注意事项
TokenBoy是一个简单专注的程序，所以并不包含身份认证相关的功能。为了避免token泄露，最好将TokenBoy放置在内网，或者配置为只监听127.0.0.1地址。

# 依赖

* python3
* tornado
