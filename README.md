# JLUZH Healthy card sentry - Serverless

吉珠健康卡自动打卡(云函数)

## 使用文档

### 设置环境变量

| 环境变量名        | 变量解释                          | 变量示例（默认值）                 | 是否必填 |
|-------------------|-----------------------------------|------------------------------------|----------|
| USERNAME          | 登录学号                          | 04180001                           | Y        |
| PASSWORD          | 登录密码                          | 123456                             | Y        |
| LOCATION_TYPE     | 地区编号  珠海1,在广东2,其他地区4 | 2                                  |          |
| PHONE             | 当前使用的电话号码                | 10086     (默认值是历史填报手机号) |          |
| LOCATION          | 假期期间去向                      | 广东省珠海市金湾区                 |          |
| LOCATION_DETAILED | 当前住址                          | 广东省珠海市金湾区吉林大学珠海学院 |          |
| SCKEY             | Server酱通知 API KEY              | 填写后执行完毕会发送状态给微信     |          |

## 开发文档

### 关于运行环境的一些问题

由于需要`BS4`来解析HTML（因为CAS认证里面有一个`<input name='execution'>`，为了提取这个参数，需要解析HTML），而且腾讯云函数默认运行容器内木有这个lib，所以上传代码时，需要将这些依赖手动打包进去

参考资料:

[腾讯云函数python默认lib列表](https://cloud.tencent.com/document/product/583/11061)  
[腾讯云函数python打包代码时附带lib方法](https://cloud.tencent.com/document/product/583/39780)  
