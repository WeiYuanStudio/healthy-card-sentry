# JLUZH Healthy card sentry - Serverless

吉珠健康卡自动打卡(云函数)

## 开发文档

### 关于运行环境的一些问题

由于需要`BS4`来解析HTML（因为CAS认证里面有一个`<input name='execution'>`，为了提取这个参数，需要解析HTML），而且腾讯云函数默认运行容器内木有这个lib，所以上传代码时，需要将这些依赖手动打包进去

参考资料:

[腾讯云函数python默认lib列表](https://cloud.tencent.com/document/product/583/11061)  
[腾讯云函数python打包代码时附带lib方法](https://cloud.tencent.com/document/product/583/39780)  
