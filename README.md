# wytorproxy
wyscan tor proxy lib &amp; help doc (需要更多的IP，防止屏蔽)

安装配置tor & privoxy
-----------------------------------
#### 安装tor
yum -y install libevent libevent-devel libpcap-devel openssl-devel
wget http://tor.hermetix.org/dist/tor-0.2.1.25.tar.gz
tar zvxf tor-0.2.1.25.tar.gz
cd tor-0.2.1.25
./configure & make & make install
/* 后台启动 */
nohup tor &

#### 安装 privoxy
yum -y install privoxy
/* 配置privoxy连接tor路由 */
echo 'forward-socks5 / 127.0.0.1:9050 .' >> /etc/privoxy/config
/* 启动privoxy服务 */
service privoxy start

127.0.0.1:8118 此时127.0.0.1的8118端口就介入tor的网络，享用匿名IP服务了

