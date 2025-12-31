# 奥特曼博客

一个基于Flask和MySQL的个人博客系统，支持文章发布、管理和浏览功能。

## 技术栈

### 后端
- Python 2.7
- Flask 1.1.4
- MySQL

### 前端
- HTML5
- CSS3
- JavaScript (ES6+)

## 项目结构

```
├── app.py                  # Flask应用入口
├── config.py               # 配置文件
├── db.py                   # 数据库操作类
├── requirements.txt         # Python依赖库
├── index.html              # 博客首页
├── admin.html              # 后台管理页面
├── post.html               # 文章详情页
├── css/
│   └── style.css           # 样式文件
├── js/
│   └── script.js          # 前端脚本
└── blog_articles/          # 博客文章本地存储
```

## 安装和运行

### 1. 安装后端依赖

#### 使用requirements.txt

```bash
# 安装虚拟环境（推荐）
pip install virtualenv

# 创建虚拟环境
virtualenv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 前端依赖

本项目前端使用原生HTML/CSS/JavaScript，无需额外安装依赖。

### 3. 配置数据库

1. 安装MySQL服务器
2. 创建数据库和用户
3. 修改`config.py`文件，更新数据库连接信息

### 4. 启动服务

#### 启动后端API服务

```bash
# 激活虚拟环境（如果尚未激活）
source venv/bin/activate

# 启动Flask应用
python app.py

# 或使用gunicorn（生产环境推荐）
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

后端服务将运行在 http://localhost:5001

#### 启动前端静态服务器

```bash
# 使用Python 3内置HTTP服务器
python3 -m http.server 8000

# 或使用Python 2内置HTTP服务器
python -m SimpleHTTPServer 8000
```

前端服务将运行在 http://localhost:8000

## 访问博客

- 博客首页：http://localhost:8000
- 后台管理：http://localhost:8000/admin.html
- API文档：http://localhost:5001/api/posts

## 功能说明

### 1. 博客功能
- 查看最新文章
- 阅读文章详情
- 按分类浏览文章

### 2. 后台管理
- 登录认证
- 发布新文章
- 管理已发布的文章

## 注意事项

1. 确保MySQL服务已启动
2. 首次运行时，Flask应用会自动创建数据库表
3. 默认管理员账户：admin/admin123
4. 生产环境建议使用HTTPS和更安全的认证方式

## 部署建议

### 开发环境
- 使用Python内置HTTP服务器提供静态文件
- 使用Flask开发服务器运行后端

### 生产环境
- 使用Nginx或Apache提供静态文件
- 使用Gunicorn或uWSGI运行Flask应用
- 配置Supervisor管理进程
- 配置HTTPS

## 许可证

MIT License
