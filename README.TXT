系统名称：用户权限校验系统
运行环境：编码环境 Windows
用户权限和功能：
    普通用户：
        登录注册；
        可以查看自己和所有人未删除的文章；
        可以上传，更新，删除自己的文章；
    管理员：
        可以查看自己和所有人未删除的文章；
        可以上传，更新自己的文章；
        可以删除所有人的文章（这些文章必须是未删除状态）

项目大致技术介绍：
    使用flask+redis+mysql，使用Blueprint，把系统按照用户角色和功能分为admin(管理员蓝图),public(公共功能蓝图),user(普通用户蓝图)
    admin:管理员新增文章接口，管理员更新文章接口
    public:登录接口，注册接口，所有用户获取文章接口，所以用户删除文章接口
    user:普通用户新增文章接口，普通用户更新文章接口

启动（部署）服务方式：
    1.mysql文件位置：在项目根目录的
    2.在ups.config.py 文件中 修改MYSQL_PASSWORD变量（输入你的数据库密码）
    3.（请多担待，因为开发是使用的windows系统，如果您的是非windows系统，此方式也很方便）通过 Pycharm 工具打开此项目，使用此项目内置的虚拟环境，然后通过通过Pycharm终端 输入 python manage.py 命令运行脚本从而启动服务。

测试：
    我把postman接口测试的所有接口导出到了项目根目录的postman.json文件中，您直接导入到postman中即可测试。

接口文档：

###########public################

/public/account POST
所有用户注册接口
	参数：
	password str 必传
	mobile str 必传
	role_type int 必传

/public/account GET
所有用户登录接口
	参数：
	password str 必传
	mobile str 必传

/public/acticle GET
所有用户获取未删除文章（自己的文章或作全部用户的文章）
	参数：
	only_self int 必传(1:只看自己的文章 2：全部)
	page_size int 必传
	page_index int 必传

/public/acticle DELETE
所有用户删除文章（管理员可以删除所有用户的未被删除的文章，普通用户只能删除自己的未被删除的文章）
	参数：
	acticle_id int 必传

###########admin################

/admin/acticle POST
管理员新增文章
	参数：
	content str 必传 文章内容

/admin/acticle PUT
管理员更新文章
    参数：
    content str 必传 文章内容
    acticle_id int 必传 文章id

###########user################

/user/acticle POST
普通用户新增文章
	参数：
	content str 必传 文章内容

/user/acticle PUT
普通用户更新文章
    参数：
    content str 必传 文章内容
    acticle_id int 必传 文章id


