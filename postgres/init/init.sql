-- PostgreSQL 初始化脚本
-- 此脚本会在PostgreSQL容器首次启动时自动执行

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 创建示例表
CREATE TABLE IF NOT EXISTS __categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS __products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INTEGER REFERENCES __categories(id),
    stock_quantity INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS __orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_email VARCHAR(100) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    order_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器
CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON __products 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- 插入示例数据
INSERT INTO __categories (name, description) VALUES 
('电子产品', '各类电子设备和配件'),
('图书', '各类书籍和出版物'),
('服装', '男女服装和配饰');

INSERT INTO __products (name, description, price, category_id, stock_quantity, metadata) VALUES 
('iPhone 15', '最新款苹果手机', 7999.00, 1, 50, '{"color": "black", "storage": "128GB"}'),
('MacBook Pro', '专业级笔记本电脑', 12999.00, 1, 20, '{"screen": "14inch", "chip": "M3"}'),
('Python编程指南', '学习Python的最佳教材', 89.00, 2, 100, '{"author": "张三", "pages": 500}'),
('休闲T恤', '舒适的纯棉T恤', 99.00, 3, 200, '{"size": "M", "material": "cotton"}');

INSERT INTO __orders (order_number, customer_email, total_amount, status, order_data) VALUES 
('ORD-2024-001', 'customer1@example.com', 8088.00, 'completed', '{"items": [{"product_id": "iPhone 15", "quantity": 1}]}'),
('ORD-2024-002', 'customer2@example.com', 188.00, 'pending', '{"items": [{"product_id": "Python编程指南", "quantity": 2}]}');

-- 创建索引
CREATE INDEX idx_products_category_id ON __products(category_id);
CREATE INDEX idx_products_price ON __products(price);
CREATE INDEX idx_products_name_gin ON __products USING gin(name gin_trgm_ops);
CREATE INDEX idx_products_metadata_gin ON __products USING gin(metadata);
CREATE INDEX idx_orders_status ON __orders(status);
CREATE INDEX idx_orders_customer_email ON __orders(customer_email);

-- 创建视图
CREATE VIEW product_summary AS
SELECT 
    p.id,
    p.name,
    p.price,
    c.name as category_name,
    p.stock_quantity,
    p.is_active
FROM __products p
LEFT JOIN __categories c ON p.category_id = c.id;

-- 显示创建的表
\dt