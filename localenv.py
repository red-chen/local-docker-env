#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LocalEnv - 本地Docker环境管理工具
用于快速部署、重启、删除中间件服务（MySQL、PostgreSQL、Redis）
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

class LocalEnv:
    def __init__(self):
        self.compose_file = "docker-compose.yml"
        self.project_name = "localenv"
        
    def run_command(self, command, check=True):
        """执行shell命令"""
        print(f"执行命令: {' '.join(command)}")
        try:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            if e.stderr:
                print(f"错误信息: {e.stderr}")
            if check:
                sys.exit(1)
            return e
    
    def check_docker(self):
        """检查Docker是否安装并运行"""
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("错误: Docker未安装或无法访问")
                sys.exit(1)
            
            result = subprocess.run(["docker", "info"], capture_output=True, text=True)
            if result.returncode != 0:
                print("错误: Docker服务未运行，请启动Docker")
                sys.exit(1)
                
        except FileNotFoundError:
            print("错误: Docker未安装")
            sys.exit(1)
    
    def check_compose_file(self):
        """检查docker-compose.yml文件是否存在"""
        if not Path(self.compose_file).exists():
            print(f"错误: {self.compose_file} 文件不存在")
            sys.exit(1)
    
    def deploy(self, services=None):
        """部署服务"""
        print("🚀 开始部署LocalEnv服务...")
        self.check_docker()
        self.check_compose_file()
        
        # 创建必要的目录
        dirs = ["mysql/conf", "mysql/init", "postgres/init", "redis/conf"]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # 构建docker-compose命令
        cmd = ["docker-compose", "-f", self.compose_file, "-p", self.project_name, "up", "-d"]
        
        if services:
            cmd.extend(services)
        
        self.run_command(cmd)
        
        print("\n⏳ 等待服务启动...")
        time.sleep(5)
        
        # 检查服务状态
        self.status()
        
        print("\n✅ 部署完成！")
        self.show_connection_info()
    
    def restart(self, services=None):
        """重启服务"""
        print("🔄 重启LocalEnv服务...")
        self.check_docker()
        self.check_compose_file()
        
        cmd = ["docker-compose", "-f", self.compose_file, "-p", self.project_name, "restart"]
        
        if services:
            cmd.extend(services)
        
        self.run_command(cmd)
        
        print("\n⏳ 等待服务重启...")
        time.sleep(3)
        
        self.status()
        print("\n✅ 重启完成！")
    
    def stop(self, services=None):
        """停止服务"""
        print("⏹️  停止LocalEnv服务...")
        self.check_docker()
        
        cmd = ["docker-compose", "-f", self.compose_file, "-p", self.project_name, "stop"]
        
        if services:
            cmd.extend(services)
        
        self.run_command(cmd)
        print("\n✅ 服务已停止！")
    
    def remove(self, volumes=False):
        """删除服务和容器"""
        print("🗑️  删除LocalEnv服务...")
        self.check_docker()
        
        # 停止并删除容器
        cmd = ["docker-compose", "-f", self.compose_file, "-p", self.project_name, "down"]
        
        if volumes:
            cmd.append("-v")
            print("⚠️  将同时删除数据卷（数据将丢失）")
        
        self.run_command(cmd)
        print("\n✅ 删除完成！")
    
    def status(self):
        """查看服务状态"""
        print("📊 LocalEnv服务状态:")
        cmd = ["docker-compose", "-f", self.compose_file, "-p", self.project_name, "ps"]
        self.run_command(cmd, check=False)
    
    def logs(self, service=None, follow=False):
        """查看日志"""
        cmd = ["docker-compose", "-f", self.compose_file, "-p", self.project_name, "logs"]
        
        if follow:
            cmd.append("-f")
        
        if service:
            cmd.append(service)
        
        self.run_command(cmd, check=False)
    
    def show_connection_info(self):
        """显示连接信息"""
        print("\n📋 服务连接信息:")
        print("="*50)
        print("MySQL:")
        print("  主机: localhost")
        print("  端口: 3306")
        print("  用户名: localenv")
        print("  密码: localenv123")
        print("  数据库: localenv")
        print("  Root密码: root123")
        print()
        print("PostgreSQL:")
        print("  主机: localhost")
        print("  端口: 5432")
        print("  用户名: localenv")
        print("  密码: localenv123")
        print("  数据库: localenv")
        print()
        print("Redis:")
        print("  主机: localhost")
        print("  端口: 6379")
        print("  密码: redis123")
        print("="*50)

def main():
    parser = argparse.ArgumentParser(
        description="LocalEnv - 本地Docker环境管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python localenv.py deploy              # 部署所有服务
  python localenv.py deploy mysql redis # 只部署MySQL和Redis
  python localenv.py restart            # 重启所有服务
  python localenv.py restart postgres   # 只重启PostgreSQL
  python localenv.py stop               # 停止所有服务
  python localenv.py remove             # 删除所有服务
  python localenv.py remove --volumes   # 删除服务和数据卷
  python localenv.py status             # 查看服务状态
  python localenv.py logs               # 查看所有日志
  python localenv.py logs mysql -f      # 实时查看MySQL日志
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # deploy命令
    deploy_parser = subparsers.add_parser("deploy", help="部署服务")
    deploy_parser.add_argument("services", nargs="*", help="指定要部署的服务 (mysql, postgres, redis)")
    
    # restart命令
    restart_parser = subparsers.add_parser("restart", help="重启服务")
    restart_parser.add_argument("services", nargs="*", help="指定要重启的服务")
    
    # stop命令
    stop_parser = subparsers.add_parser("stop", help="停止服务")
    stop_parser.add_argument("services", nargs="*", help="指定要停止的服务")
    
    # remove命令
    remove_parser = subparsers.add_parser("remove", help="删除服务")
    remove_parser.add_argument("--volumes", "-v", action="store_true", help="同时删除数据卷")
    
    # status命令
    subparsers.add_parser("status", help="查看服务状态")
    
    # logs命令
    logs_parser = subparsers.add_parser("logs", help="查看日志")
    logs_parser.add_argument("service", nargs="?", help="指定服务名称")
    logs_parser.add_argument("-f", "--follow", action="store_true", help="实时跟踪日志")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    localenv = LocalEnv()
    
    try:
        if args.command == "deploy":
            localenv.deploy(args.services if args.services else None)
        elif args.command == "restart":
            localenv.restart(args.services if args.services else None)
        elif args.command == "stop":
            localenv.stop(args.services if args.services else None)
        elif args.command == "remove":
            localenv.remove(args.volumes)
        elif args.command == "status":
            localenv.status()
        elif args.command == "logs":
            localenv.logs(args.service, args.follow)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()