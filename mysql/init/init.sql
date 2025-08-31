-- MySQL 初始化脚本
-- 此脚本会在MySQL容器首次启动时自动执行

-- 创建示例表
USE localenv;

CREATE TABLE IF NOT EXISTS __users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS __posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES __users(id) ON DELETE CASCADE
);

-- 插入示例数据
INSERT INTO __users (username, email, password_hash) VALUES 
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx/L/jyW'),
('user1', 'user1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx/L/jyW');

INSERT INTO __posts (user_id, title, content, status) VALUES 
(1, '欢迎使用LocalEnv', '这是一个示例文章，展示MySQL数据库的基本功能。', 'published'),
(2, '我的第一篇文章', '用户创建的示例内容。', 'draft');

-- 创建索引
CREATE INDEX idx_posts_user_id ON __posts(user_id);
CREATE INDEX idx_posts_status ON __posts(status);
CREATE INDEX idx_posts_created_at ON __posts(created_at);

-- 显示创建的表
SHOW TABLES;