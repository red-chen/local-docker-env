# 项目介绍

# LocalEnv

LocalEnv 是一个本地Docker环境搭建工具，用于快速部署中间件，比如MySQL、PostgreSQL、Redis。

## 功能特性

- 🚀 一键部署MySQL、PostgreSQL、Redis服务
- 🔄 支持服务的启动、停止、重启操作
- 🗑️ 支持完全删除服务和数据
- 📊 实时查看服务状态和日志
- ⚙️ 预配置的服务参数，开箱即用
- 🔧 支持自定义配置文件

## 快速开始

### 前置要求

- Docker 和 Docker Compose
- Python 3.6+

### 安装使用

1. 克隆或下载项目文件
2. 确保Docker服务正在运行
3. 使用Python脚本管理服务：

```bash
# 部署所有服务
python localenv.py deploy

# 只部署特定服务
python localenv.py deploy mysql redis

# 查看服务状态
python localenv.py status

# 重启服务
python localenv.py restart

# 停止服务
python localenv.py stop

# 删除服务（保留数据）
python localenv.py remove

# 删除服务和数据
python localenv.py remove --volumes

# 查看日志
python localenv.py logs

# 实时查看特定服务日志
python localenv.py logs mysql -f
```

## 服务信息

### MySQL
- **端口**: 3306
- **用户名**: localenv
- **密码**: localenv123
- **数据库**: localenv
- **Root密码**: root123

### PostgreSQL
- **端口**: 5432
- **用户名**: localenv
- **密码**: localenv123
- **数据库**: localenv

### Redis
- **端口**: 6379
- **密码**: redis123

## 目录结构

```
local-env/
├── docker-compose.yml      # Docker Compose配置文件
├── localenv.py             # Python管理脚本
├── .env.example            # 环境变量示例
├── mysql/
│   ├── conf/               # MySQL配置文件目录
│   └── init/               # MySQL初始化脚本
│       └── init.sql
├── postgres/
│   └── init/               # PostgreSQL初始化脚本
│       └── init.sql
└── redis/
    └── conf/               # Redis配置文件
        └── redis.conf
```

## 自定义配置

1. 复制 `.env.example` 为 `.env`
2. 修改环境变量以自定义端口、密码等配置
3. 修改对应的配置文件以调整服务参数

## 数据持久化

所有服务的数据都通过Docker卷进行持久化存储：
- `mysql_data`: MySQL数据
- `postgres_data`: PostgreSQL数据  
- `redis_data`: Redis数据

## 故障排除

### 端口冲突
如果遇到端口冲突，可以修改 `docker-compose.yml` 中的端口映射。

### 权限问题
确保当前用户有权限访问Docker。

### 服务启动失败
使用 `python localenv.py logs <service>` 查看具体错误信息。

## 许可证

MIT License

