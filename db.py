# -*- coding: utf-8 -*-
import pymysql
import bcrypt
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.config = DB_CONFIG
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            print("数据库连接成功")
        except pymysql.Error as err:
            print("数据库连接失败: %s" % err)
            raise
    
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("数据库连接已关闭")
    
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.lastrowid
        except pymysql.Error as err:
            print("执行查询失败: %s" % err)
            self.connection.rollback()
            raise
    
    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except pymysql.Error as err:
            print("获取数据失败: %s" % err)
            raise
    
    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except pymysql.Error as err:
            print("获取单条数据失败: %s" % err)
            raise
    
    def initialize_database(self):
        """初始化数据库和表结构"""
        try:
            # 创建数据库（如果不存在）
            temp_config = self.config.copy()
            db_name = temp_config.pop('database')
            temp_conn = pymysql.connect(**temp_config)
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % db_name)
            temp_cursor.close()
            temp_conn.close()
            
            # 重新连接到具体数据库
            self.connect()
            
            # 创建文章表
            create_posts_table = """
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                date DATE NOT NULL,
                author VARCHAR(100) NOT NULL,
                category VARCHAR(100) NOT NULL,
                excerpt TEXT NOT NULL,
                image VARCHAR(255) NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            self.execute_query(create_posts_table)
            
            # 创建用户表
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                role ENUM('admin', 'editor') DEFAULT 'editor',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            self.execute_query(create_users_table)
            
            # 检查是否已有数据，没有则插入示例数据
            check_data = "SELECT COUNT(*) as count FROM posts"
            result = self.fetch_one(check_data)
            if result['count'] == 0:
                # 插入示例文章数据 - 从博客园提取
                sample_posts = [
                    ("我喜欢用vim来编辑，经常要按到esc", "2014-07-07", "symons1992", "技术", "我喜欢用vim来编辑，经常要按到esc，但是去按那个按键确实比较的远，而且CapsLock这个按键对我来说着实有些鸡肋，所以就想在win7上也能像ubuntu那样把capslock映射为esc，在网上寻找的过程中，找到了一个靠谱的做法。", "https://via.placeholder.com/600x400/667eea/ffffff?text=Vim"),
                    ("TCP三次握手并不神秘", "2018-05-23", "symons1992", "网络", "TCP三次握手并不神秘，只是tcp连接的建立过程。最重要的还是了解它的思想和模型，其实我们日常中已经解决了这种问题。", "https://via.placeholder.com/600x400/764ba2/ffffff?text=TCP"),
                    ("大话池概念", "2018-05-08", "symons1992", "技术", "池概念经常会被开发人员提起，进程池，线程池，连接池等等，但是这个池概念到底是个什么意思，我用一个比较现实中的例子来讲。", "https://via.placeholder.com/600x400/f093fb/ffffff?text=Pool"),
                    ("Presto插入partition数据的问题", "2020-12-25", "symons1992", "大数据", "我最近发现直接在presto里面插入partition数据，如果原来有数据则不会替换，会产生冗余数据。但是目前presto又不支持insert overwrite，所以我们现在的做法是在pipeline里面增加一个操作删除即将要写入的partition。", "https://via.placeholder.com/600x400/4facfe/ffffff?text=Presto"),
                    ("快速排序算法复习", "2021-03-27", "symons1992", "算法", "今天再刷题的时候遇见了一个需要用到快速选择的题目，所以需要写一个快排，但是我发现我竟然忘了。。。来复习下。", "https://via.placeholder.com/600x400/00f2fe/ffffff?text=QuickSort")
                ]
                
                insert_post = """
                INSERT INTO posts (title, date, author, category, excerpt, image)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                for post in sample_posts:
                    self.execute_query(insert_post, post)
                
                print("示例数据插入成功")
            
            # 检查是否已有用户，没有则创建admin用户
            check_users = "SELECT COUNT(*) as count FROM users"
            users_result = self.fetch_one(check_users)
            if users_result['count'] == 0:
                # 创建admin用户，密码使用bcrypt哈希
                admin_password = "admin123"
                hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
                
                insert_user = """
                INSERT INTO users (username, password, email, role)
                VALUES (%s, %s, %s, %s)
                """
                
                self.execute_query(insert_user, ("admin", hashed_password, "admin@example.com", "admin"))
                print("Admin用户创建成功，初始密码：admin123")
            
        except Exception as e:
            print("初始化数据库失败: %s" % e)
            raise
