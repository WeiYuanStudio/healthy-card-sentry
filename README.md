# JLUZH Healthy Card Sentry - Serverless

健康卡自动打卡(云函数)

## 声明

该项目仅供技术学习使用，请遵守相关Law。

## 使用文档

### 1.注册所需要的云函数服务

注册腾讯云账号，并找到云函数服务。腾讯云的云函数服务每月有巨额的免费额度，基本上不可能用完。

对于个人用户来说只有外网流量费用需要自费，应该是套外1G流量0.8元的价格。1块钱应该都能用一学期了。

先用后月结的模式。账户欠费后会停止云服务。不会上征信XD，或者直接从你微信支付扣费，大可放心使用。

### 2.向云函数提交代码

创建一个云函数，按照上图设定。代码ZIP打包可在该仓库的Release找到

[1.0发布版本页面](https://gitee.com/WeiYuanStudio/healthy-card-sentry/releases/v1.0)

打包好的文件是`healthy-card-sentry.zip`

[![slGb60.png](https://s3.ax1x.com/2021/01/10/slGb60.png)](https://imgchr.com/i/slGb60)

### 3.完成个人设定

函数运行时会通过读取环境变量中的参数登录你的账号，并发送健康卡信息。所有的执行都在你的账号的云函数中，不存在信息泄露问题。只有腾讯云和你账号所有者——你，有权获取这些信息。

| 环境变量名        | 变量解释                          | 变量示例（默认值）                 | 是否必填 |
|-------------------|-----------------------------------|------------------------------------|----------|
| USERNAME          | 登录学号                          | 04180001                           | Y        |
| PASSWORD          | 登录密码                          | 123456                             | Y        |
| LOCATION_TYPE     | 地区编号  珠海1,在广东2,其他地区4 | 2                                  |          |
| PHONE             | 当前使用的电话号码                | 10086     (默认值是历史填报手机号) |          |
| LOCATION          | 假期期间去向                      | 广东省珠海市金湾区                 |          |
| LOCATION_DETAILED | 当前住址                          | 广东省珠海市金湾区吉林大学珠海学院 |          |
| SCKEY             | Server酱通知 API KEY              | 填写后执行完毕会发送状态给微信     |          |

[![slGHlq.png](https://s3.ax1x.com/2021/01/10/slGHlq.png)](https://imgchr.com/i/slGHlq)

### 4.设定定时触发器

按照图中的设定就是一小时填一次健康表

[![slG7pn.png](https://s3.ax1x.com/2021/01/10/slG7pn.png)](https://imgchr.com/i/slG7pn)


除此之外，当然你也可以进阶操作，自己编写cron表达式，腾讯云函数支持多个和多种触发器，你可以在创建后慢慢研究。

参考自定义cron表达式

```
0 4 * * *
```

该表达式为每天4点整点填写健康表。建议错峰填报，避免服务端负载过大，导致自动填报失败。

自定义表达式虽好，但提交前请务必检查表达式是否合理，误操作的表达式填写可能会造成极高频率的函数执行。导致健康卡服务器承受过大压力，同时你的server chan账号可能因为过高频率的调用被封禁。

## 查看函数执行情况

[![slGqXV.png](https://s3.ax1x.com/2021/01/10/slGqXV.png)](https://imgchr.com/i/slGqXV)

创建完函数后你可以在函数管理点击测试，启动一次自动填报，之后你可以在日志查询看到执行日志。若在环境变量中填写了server chan的`SCKEY`的同学，你的微信将收到填报执行结果的反馈推送。

[![sltYSs.jpg](https://s3.ax1x.com/2021/01/10/sltYSs.jpg)](https://imgchr.com/i/sltYSs)
[![sltGWj.jpg](https://s3.ax1x.com/2021/01/10/sltGWj.jpg)](https://imgchr.com/i/sltGWj)

## 开发文档

### 关于运行环境的一些问题

由于需要`BS4`来解析HTML（因为CAS认证里面有一个`<input name='execution'>`，为了提取这个参数，需要解析HTML），而且腾讯云函数默认运行容器内木有这个lib，所以上传代码时，需要将这些依赖手动打包进去

参考资料:

[腾讯云函数python默认lib列表](https://cloud.tencent.com/document/product/583/11061)  
[腾讯云函数python打包代码时附带lib方法](https://cloud.tencent.com/document/product/583/39780)  
