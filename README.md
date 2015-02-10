# wytorproxy
wyscan tor proxy lib &amp; help doc <br />
(当你需要更多的IP，防止服务被屏蔽，写一个tor的控制脚本，就能每分钟刷新一下tor洋葱池的IP)

BUG反馈
-----------------------------------
> 微博：http://weibo.com/ringzero<br />
> 邮箱：ringzero@0x557.org<br />

#### 使用实例
> [root@10-8-11-221 wytorproxy]# python wytorproxy.py <br />
> {"code":0,"data":{"country":"美国","country_id":"US","area":"","area_id":"","region":"","region_id":"","city":"","city_id":"","county":"","county_id":"","isp":"","isp_id":"","ip":"96.47.226.20"}}
    
安装配置tor & privoxy
-----------------------------------
### 安装tor
    yum -y install libevent libevent-devel libpcap-devel openssl-devel
    wget http://tor.hermetix.org/dist/tor-0.2.1.25.tar.gz
    tar zvxf tor-0.2.1.25.tar.gz
    cd tor-0.2.1.25
    ./configure & make & make install
    /* 后台启动 */
    nohup tor &

### 安装 privoxy 并配置与tor连接
    yum -y install privoxy
    /* 配置privoxy连接tor路由 */
    echo 'forward-socks5 / 127.0.0.1:9050 .' >> /etc/privoxy/config
    /* 启动privoxy服务 */
    service privoxy start

使用TOR代理
-----------------------------------
> 127.0.0.1:8118
> 此时127.0.0.1的8118端口就接入tor的网络，享用匿名IP服务了

### 使用iptables做NAT转换，映射到外网IP上供更多的服务器使用
(如果你想在外网使用的话，下面是实现方法)

    sed -i '/net.ipv4.ip_forward/ s/\(.*= \).*/\11/' /etc/sysctl.conf
    sysctl -p
    iptables -t nat -A PREROUTING -p tcp -i eth0 --dport 8778 -j DNAT --to 127.0.0.1:8118
    iptables -t nat -A POSTROUTING -j MASQUERADE
    service iptables save
    service iptables restart
