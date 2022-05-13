# ZCST(JLUZH) Healthy Card Sentry - Serverless

健康卡自动打卡(云函数)

## 声明

该项目仅供技术学习使用，请遵守相关 Law。

## 使用文档

**文档待更新，现已改用青龙面板触发执行**

简单说明：
1. 自行安装青龙面板到服务器
2. 使用`ql repo https://gitee.com/WeiYuanStudio/healthy-card-sentry.git`命令拉取该脚本
3. 在面板内的依赖管理安装Python依赖`bs4`，若遇到失败也可以自行在容器内或者服务器内安装python的`bs4`依赖
4. 复制`user_data.csv.template`，并重命名为`user_data.csv`，自行补全该文件内打卡信息，一个人一行
5. 拉取完毕后，删除面板自动导入的那几个该项目的任务。
6. 自行添加任务，任务命令为`task WeiYuanStudio_healthy-card-sentry/index.py`，定时规则推荐`0 * * * *`（一小时一次打卡）

关于user_data.csv
|描述|csv 头|
|-------------|------------|
| 登录学号        | login_id   |
| 登录密码        | login_pwd  |
| 常住地址        | xjzdz      |
| 假期去向        | jqqx       |
| 现人员位置广东非珠海2 | xrywz      |
| 省码          | pcode      |
| 市码          | ccode      |
| 区码          | dcode      |
| 具体地址        | jtdz       |
| 最后接种时间      | hsjcsj     |
| 省名          | pname      |
| 市名          | cname      |
| 区名          | dname      |