## 插件说明

对数据库进行增删改查

## 插件配置

将 `plugins/hello` 目录下的 `config.json.template` 配置模板复制为最终生效的 `config.json`。 (如果未配置则会默认使用`config.json.template`模板中配置)。

以下是插件配置项说明：

```bash
{
    "host":"localhost", #地址
    "user":"root",      #用户名
    "password":"1234",  #密码
    "database":"chat"   #数据库名
}
```


注意：

 - 目前仅支持MySql
 - 记得安装依赖pip3 install -r requirements.txt


