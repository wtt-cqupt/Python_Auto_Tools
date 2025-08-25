'''
python环境管理器
版本:1.0
作者：星星宇
日期:2024年1月1日
这是一个本地命令行程序，用于管理python环境，主要通过pip和python命令来实现。
功能：
1. 检查python版本--通过python -V 命令来实现
2. 检查pip版本--通过pip -V 命令来实现
3. 升级pip--通过pip install --upgrade pip 命令来实现
4. 安装python包--通过pip install 包名 命令来实现
5. 卸载python包--通过pip uninstall 包名 命令来实现
6. 查看已安装的python包--通过pip list 命令来实现
7. 查看python包的详细信息--通过pip show 包名 命令来实现
8. 执行任意系统命令--通过python -c "import os; os.system('命令')" 命令来实现
9. 退出程序--通过exit 命令来实现

'''

import subprocess
import sys
import os

class PythonEnvManager:
    def __init__(self):
        self.python_cmd = sys.executable
    
    def run_command(self, command):
        """执行系统命令并返回结果"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "命令执行超时"
        except Exception as e:
            return -1, "", f"执行命令时发生错误: {e}"
    
    def check_python_version(self):
        """检查python版本--功能1"""
        print("=== 检查Python版本 ===")
        returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -V')
        if returncode == 0:
            print(f"Python版本: {stdout.strip()}")
        else:
            print(f"获取Python版本失败: {stderr}")
        print()
    
    def check_pip_version(self):
        """检查pip版本--功能2"""
        print("=== 检查pip版本 ===")
        returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -m pip -V')
        if returncode == 0:
            print(f"pip版本: {stdout.strip()}")
        else:
            print(f"获取pip版本失败: {stderr}")
        print()
    
    def upgrade_pip(self):
        """升级pip--功能3"""
        print("=== 升级pip ===")
        print("正在升级pip，请稍候...")
        returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -m pip install --upgrade pip')
        if returncode == 0:
            print("pip升级成功！")
            print(stdout)
        else:
            print(f"pip升级失败: {stderr}")
        print()
    
    def install_package(self, package_name):
        """安装python包--功能4"""
        print(f"=== 安装Python包: {package_name} ===")
        returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -m pip install {package_name}')
        if returncode == 0:
            print(f"包 {package_name} 安装成功！")
            print(stdout)
        else:
            print(f"包 {package_name} 安装失败: {stderr}")
        print()
    
    def uninstall_package(self, package_name):
        """卸载python包--功能5"""
        if package_name.lower() == 'all':
            self.uninstall_all_packages()
            return
            
        print(f"=== 卸载Python包: {package_name} ===")
        confirm = input(f"确定要卸载包 {package_name} 吗？(y/n): ").strip().lower()
        if confirm == 'y':
            returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -m pip uninstall -y {package_name}')
            if returncode == 0:
                print(f"包 {package_name} 卸载成功！")
                print(stdout)
            else:
                print(f"包 {package_name} 卸载失败: {stderr}")
        else:
            print("取消卸载操作")
        print()
    
    def uninstall_all_packages(self):
        """卸载所有python包"""
        print("=== 卸载所有Python包 ===")
        
        # 获取已安装包列表
        returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -m pip list --format=freeze')
        if returncode != 0:
            print(f"获取包列表失败: {stderr}")
            return
        
        # 解析包列表，排除pip和setuptools
        packages = []
        for line in stdout.strip().split('\n'):
            if line and not line.startswith('#'):
                package_name = line.split('==')[0].lower()
                # 保留pip和setuptools，避免破坏Python环境
                if package_name not in ['pip', 'setuptools']:
                    packages.append(package_name)
        
        if not packages:
            print("没有找到可卸载的包")
            return
        
        print(f"找到 {len(packages)} 个可卸载的包:")
        for i, pkg in enumerate(packages, 1):
            print(f"  {i}. {pkg}")
        
        confirm = input("确定要卸载所有这些包吗？此操作不可恢复！(y/n): ").strip().lower()
        if confirm != 'y':
            print("取消卸载操作")
            return
        
        print("开始卸载所有包...")
        success_count = 0
        fail_count = 0
        
        for package in packages:
            print(f"正在卸载 {package}...")
            returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -m pip uninstall -y {package}')
            if returncode == 0:
                print(f"✓ {package} 卸载成功")
                success_count += 1
            else:
                print(f"✗ {package} 卸载失败: {stderr}")
                fail_count += 1
        
        print(f"\n卸载完成！成功: {success_count}, 失败: {fail_count}")
        print()
    
    def list_packages(self):
        """查看已安装的python包--功能6"""
        print("=== 已安装的Python包 ===")
        returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -m pip list')
        if returncode == 0:
            print(stdout)
        else:
            print(f"获取包列表失败: {stderr}")
        print()
    
    def show_package_info(self, package_name):
        """查看python包的详细信息--功能7"""
        print(f"=== 包 {package_name} 的详细信息 ===")
        returncode, stdout, stderr = self.run_command(f'"{self.python_cmd}" -m pip show {package_name}')
        if returncode == 0:
            print(stdout)
        else:
            print(f"获取包 {package_name} 信息失败: {stderr}")
        print()
    
    def execute_system_command(self, command):
        """执行任意系统命令--功能8"""
        print(f"=== 执行系统命令: {command} ===")
        returncode, stdout, stderr = self.run_command(command)
        if returncode == 0:
            print("命令执行成功！")
            if stdout:
                print("输出:")
                print(stdout)
        else:
            print(f"命令执行失败: {stderr}")
        print()
    
    def show_help(self):
        """显示帮助信息"""
        print("=== Python环境管理器 - 帮助信息 ===")
        print("可用命令:")
        print("  1 或 python    - 检查Python版本")
        print("  2 或 pip       - 检查pip版本")
        print("  3 或 upgrade    - 升级pip")
        print("  4 或 install    - 安装Python包 (用法: install 包名)")
        print("  5 或 uninstall  - 卸载Python包 (用法: uninstall 包名 或 uninstall all)")
        print("  6 或 list       - 查看已安装的Python包")
        print("  7 或 show       - 查看包详细信息 (用法: show 包名)")
        print("  8 或 exec       - 执行系统命令 (用法: exec 命令)")
        print("  9 或 exit       - 退出程序")
        print("  help           - 显示此帮助信息")
        print()
    
    def run_interactive(self):
        """运行交互式命令行界面"""
        print("=== Python环境管理器 ===")
        print("输入 'help' 查看帮助信息，输入 'exit' 退出程序")
        print()
        
        while True:
            try:
                user_input = input("PythonEnv> ").strip()
                
                if not user_input:
                    continue
                
                # 解析用户输入
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                # 处理退出命令--功能9
                if command in ['9', 'exit', 'quit']:
                    print("退出程序")
                    break
                
                # 处理帮助命令
                elif command == 'help':
                    self.show_help()
                
                # 处理功能1: 检查python版本
                elif command in ['1', 'python']:
                    self.check_python_version()
                
                # 处理功能2: 检查pip版本
                elif command in ['2', 'pip']:
                    self.check_pip_version()
                
                # 处理功能3: 升级pip
                elif command in ['3', 'upgrade']:
                    self.upgrade_pip()
                
                # 处理功能4: 安装包
                elif command in ['4', 'install']:
                    if args:
                        package_name = ' '.join(args)
                        self.install_package(package_name)
                    else:
                        print("错误: 请指定要安装的包名")
                        print("用法: install 包名")
                        print()
                
                # 处理功能5: 卸载包
                elif command in ['5', 'uninstall']:
                    if args:
                        package_name = ' '.join(args)
                        self.uninstall_package(package_name)
                    else:
                        print("错误: 请指定要卸载的包名")
                        print("用法: uninstall 包名")
                        print()
                
                # 处理功能6: 列出包
                elif command in ['6', 'list']:
                    self.list_packages()
                
                # 处理功能7: 显示包信息
                elif command in ['7', 'show']:
                    if args:
                        package_name = ' '.join(args)
                        self.show_package_info(package_name)
                    else:
                        print("错误: 请指定要查看的包名")
                        print("用法: show 包名")
                        print()
                
                # 处理功能8: 执行系统命令
                elif command in ['8', 'exec']:
                    if args:
                        system_command = ' '.join(args)
                        self.execute_system_command(system_command)
                    else:
                        print("错误: 请指定要执行的命令")
                        print("用法: exec 命令")
                        print()
                
                else:
                    print(f"未知命令: {command}")
                    print("输入 'help' 查看可用命令")
                    print()
                
            except KeyboardInterrupt:
                print("\n程序被用户中断")
                break
            except EOFError:
                print("\n退出程序")
                break
            except Exception as e:
                print(f"发生错误: {e}")
                print()

def main():
    """主函数"""
    manager = PythonEnvManager()
    manager.run_interactive()

if __name__ == "__main__":
    main()