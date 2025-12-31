# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import bcrypt
from db import Database

app = Flask(__name__)

# 手动添加CORS头
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

db = Database()

@app.route('/')
def index():
    return "个人博客API服务运行中"

# 模拟博客文章数据 - 从博客园提取
mock_posts = [
    {
        'id': 1,
        'title': "我喜欢用vim来编辑，经常要按到esc",
        'date': "2014-07-07",
        'author': "symons1992",
        'category': "技术",
        'excerpt': "我喜欢用vim来编辑，经常要按到esc，但是去按那个按键确实比较的远，而且CapsLock这个按键对我来说着实有些鸡肋，所以就想在win7上也能像ubuntu那样把capslock映射为esc，在网上寻找的过程中，找到了一个靠谱的做法。",
        'image': "https://via.placeholder.com/600x400/667eea/ffffff?text=Vim"
    },
    {
        'id': 2,
        'title': "TCP三次握手并不神秘",
        'date': "2018-05-23",
        'author': "symons1992",
        'category': "网络",
        'excerpt': "TCP三次握手并不神秘，只是tcp连接的建立过程。最重要的还是了解它的思想和模型，其实我们日常中已经解决了这种问题。",
        'image': "https://via.placeholder.com/600x400/764ba2/ffffff?text=TCP"
    },
    {
        'id': 3,
        'title': "大话池概念",
        'date': "2018-05-08",
        'author': "symons1992",
        'category': "技术",
        'excerpt': "池概念经常会被开发人员提起，进程池，线程池，连接池等等，但是这个池概念到底是个什么意思，我用一个比较现实中的例子来讲。",
        'image': "https://via.placeholder.com/600x400/f093fb/ffffff?text=Pool"
    },
    {
        'id': 4,
        'title': "Presto插入partition数据的问题",
        'date': "2020-12-25",
        'author': "symons1992",
        'category': "大数据",
        'excerpt': "我最近发现直接在presto里面插入partition数据，如果原来有数据则不会替换，会产生冗余数据。但是目前presto又不支持insert overwrite，所以我们现在的做法是在pipeline里面增加一个操作删除即将要写入的partition。",
        'image': "https://via.placeholder.com/600x400/4facfe/ffffff?text=Presto"
    },
    {
        'id': 5,
        'title': "快速排序算法复习",
        'date': "2021-03-27",
        'author': "symons1992",
        'category': "算法",
        'excerpt': "今天再刷题的时候遇见了一个需要用到快速选择的题目，所以需要写一个快排，但是我发现我竟然忘了。。。来复习下。",
        'image': "https://via.placeholder.com/600x400/00f2fe/ffffff?text=QuickSort"
    }
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """获取所有博客文章 - 支持数据库和模拟数据"""
    try:
        db.connect()
        query = "SELECT * FROM posts ORDER BY date DESC"
        posts = db.fetch_all(query)
        return jsonify({
            'success': True,
            'data': posts,
            'message': '获取文章成功'
        })
    except Exception as e:
        print("数据库获取失败，使用模拟数据: %s" % e)
        # 数据库连接失败时返回模拟数据
        return jsonify({
            'success': True,
            'data': mock_posts,
            'message': '使用模拟数据'
        })
    finally:
        db.disconnect()

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """获取单篇博客文章 - 支持数据库和模拟数据"""
    try:
        db.connect()
        query = "SELECT * FROM posts WHERE id = %s"
        post = db.fetch_one(query, (post_id,))
        if post:
            return jsonify({
                'success': True,
                'data': post,
                'message': '获取文章成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '文章不存在'
            }), 404
    except Exception as e:
        print("数据库获取失败，使用模拟数据: %s" % e)
        # 数据库连接失败时从模拟数据中查找
        post = next((p for p in mock_posts if p['id'] == post_id), None)
        if post:
            return jsonify({
                'success': True,
                'data': post,
                'message': '使用模拟数据'
            })
        else:
            return jsonify({
                'success': False,
                'message': '文章不存在'
            }), 404
    finally:
        db.disconnect()

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录验证"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': '缺少必要的登录信息'
            }), 400
        
        username = data['username']
        password = data['password']
        
        db.connect()
        query = "SELECT * FROM users WHERE username = %s"
        user = db.fetch_one(query, (username,))
        
        if not user:
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401
        
        # 验证密码
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # 登录成功，返回用户信息（不含密码）
            user_info = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
            
            return jsonify({
                'success': True,
                'data': user_info,
                'message': '登录成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '登录失败: %s' % str(e)
        }), 500
    finally:
        db.disconnect()

@app.route('/api/posts', methods=['POST'])
def create_post():
    """创建新的博客文章"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': '请求数据为空'
            }), 400
        
        # 验证必要字段
        required_fields = ['title', 'category', 'author', 'excerpt', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': '缺少必要字段: %s' % field
                }), 400
        
        # 获取可选字段
        image = data.get('image', 'https://via.placeholder.com/600x400/667eea/ffffff?text=Default')
        
        # 连接数据库并插入数据
        db.connect()
        insert_query = """
        INSERT INTO posts (title, date, author, category, excerpt, image, content)
        VALUES (%s, CURDATE(), %s, %s, %s, %s, %s)
        """
        
        # 执行插入
        post_id = db.execute_query(insert_query, (
            data['title'],
            data['author'],
            data['category'],
            data['excerpt'],
            image,
            data['content']
        ))
        
        # 获取插入的文章
        get_query = "SELECT * FROM posts WHERE id = %s"
        new_post = db.fetch_one(get_query, (post_id,))
        
        return jsonify({
            'success': True,
            'data': new_post,
            'message': '文章发布成功'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '创建文章失败: %s' % str(e)
        }), 500
    finally:
        db.disconnect()

if __name__ == '__main__':
    # 初始化数据库 - 优雅处理连接失败
    try:
        db.initialize_database()
        print("数据库初始化成功")
    except Exception as e:
        print("数据库初始化失败，将使用模拟数据: %s" % e)
    finally:
        db.disconnect()
    
    # 启动Flask应用 - 使用端口5001
    app.run(debug=True, host='0.0.0.0', port=5001)
