'''
pip 安装助手
版本:1.0
作者：星星宇
日期:2024年1月1日
这是一个本地命令行程序，用于在通过pip安装程序时，自动在命令后添加国内的镜像网站，以加快安装速度。
以下列出几个常用的国内镜像网站：
1. 阿里云：https://mirrors.aliyun.com/pypi/simple/
2. 清华大学：https://pypi.tuna.tsinghua.edu.cn/simple/
3. 中国科技大学：https://pypi.mirrors.ustc.edu.cn/simple/
4. 华中理工大学：https://pypi.hustunique.com/
5. 山东理工大学：https://pypi.sdutlinux.org/
6. 北京理工大学：https://pypi.bit.edu.cn/simple/
功能：
1. 打开后显示当前pip版本和默认镜像网站，显示当前pip版本通过pip --version实现
2.当用户输入"1 numpy"时，调用pip安装numpy，并在后面加上默认的镜像网站，安装命令为pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
3.当用户输入"2"时，列出所有的镜像网站，用户可通过键入数字的方式选自其中之一，将其设置为默认的镜像网站。
4.当安装失败的时候，比如没在指定的镜像网站中搜索到相应的软件，则显示"安装失败"。和相应的错误信息
5.当用户输入"3 numpy"时，使用默认镜像网站更新numpy，更新命令为pip install --upgrade numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
6.当用户输入"4"时，调用pip list命令输出当前安装的库列表
numpy只是一个示例，用户可以根据需要安装其他的软件包。
'''

import subprocess
import sys
import os

class PipInstallHelper:
    def __init__(self):
        self.mirrors = {
            "1": "https://mirrors.aliyun.com/pypi/simple/",
            "2": "https://pypi.tuna.tsinghua.edu.cn/simple/",
            "3": "https://pypi.mirrors.ustc.edu.cn/simple/",
            "4": "https://pypi.hustunique.com/",
            "5": "https://pypi.sdutlinux.org/",
            "6": "https://pypi.bit.edu.cn/simple/"
        }
        self.default_mirror = "2"  # 默认使用清华大学镜像
        self.mirror_names = {
            "1": "阿里云",
            "2": "清华大学",
            "3": "中国科技大学",
            "4": "华中理工大学",
            "5": "山东理工大学",
            "6": "北京理工大学"
        }
    
    def get_pip_version(self):
        """获取pip版本信息"""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "无法获取pip版本信息"
        except Exception as e:
            return f"获取pip版本时出错: {str(e)}"
    
    def install_package(self, package_name):
        """安装指定的包"""
        mirror_url = self.mirrors[self.default_mirror]
        command = [sys.executable, "-m", "pip", "install", package_name, "-i", mirror_url]
        
        try:
            print(f"正在安装 {package_name}，使用镜像: {self.mirror_names[self.default_mirror]}")
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print(f"{package_name} 安装成功！")
                if result.stdout:
                    print("安装输出:")
                    print(result.stdout)
            else:
                print(f"安装失败")
                if result.stderr:
                    print("错误信息:")
                    print(result.stderr)
                if result.stdout:
                    print("输出信息:")
                    print(result.stdout)
        except Exception as e:
            print(f"安装过程中出错: {str(e)}")
    
    def upgrade_package(self, package_name):
        """更新指定的包"""
        mirror_url = self.mirrors[self.default_mirror]
        command = [sys.executable, "-m", "pip", "install", "--upgrade", package_name, "-i", mirror_url]
        
        try:
            print(f"正在更新 {package_name}，使用镜像: {self.mirror_names[self.default_mirror]}")
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print(f"{package_name} 更新成功！")
                if result.stdout:
                    print("更新输出:")
                    print(result.stdout)
            else:
                print(f"更新失败")
                if result.stderr:
                    print("错误信息:")
                    print(result.stderr)
                if result.stdout:
                    print("输出信息:")
                    print(result.stdout)
        except Exception as e:
            print(f"更新过程中出错: {str(e)}")
    
    def list_installed_packages(self):
        """列出当前安装的所有包"""
        try:
            print("正在获取已安装的包列表...")
            result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                                  capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print("\n当前安装的包列表:")
                print("=" * 60)
                print(result.stdout)
                print("=" * 60)
            else:
                print("获取包列表失败")
                if result.stderr:
                    print("错误信息:")
                    print(result.stderr)
        except Exception as e:
            print(f"获取包列表时出错: {str(e)}")
    
    def show_mirrors(self):
        """显示所有可用的镜像网站"""
        print("\n可用的镜像网站:")
        for key, name in self.mirror_names.items():
            print(f"{key}. {name}: {self.mirrors[key]}")
        print(f"\n当前默认镜像: {self.mirror_names[self.default_mirror]}")
    
    def set_default_mirror(self, mirror_number):
        """设置默认镜像"""
        if mirror_number in self.mirrors:
            self.default_mirror = mirror_number
            print(f"默认镜像已设置为: {self.mirror_names[mirror_number]}")
        else:
            print("无效的镜像编号")
    
    def show_welcome_info(self):
        """显示欢迎信息和当前状态"""
        print("=" * 50)
        print("pip 安装助手 v1.0")
        print("=" * 50)
        #打印当前python版本
        print(f"当前python版本: {sys.version}")
        print(f"当前pip版本: {self.get_pip_version()}")
        print(f"当前默认镜像: {self.mirror_names[self.default_mirror]} - {self.mirrors[self.default_mirror]}")
        print("=" * 50)
        print("使用说明:")
        print("1 包名     - 安装指定的包")
        print("2          - 查看并选择默认镜像")
        print("3 包名     - 更新指定的包")
        print("4          - 查看当前安装的包列表")
        #打印“5 包名      - 卸载指定的包”
        print("5 包名      - 卸载指定的包")

        print("q 或 quit  - 退出程序")
        print("=" * 50)
    
    def uninstall_package(self, package_name):
        """卸载指定的包"""
        command = [sys.executable, "-m", "pip", "uninstall", package_name, "-y"]
        
        try:
            print(f"正在卸载 {package_name}")
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print(f"{package_name} 卸载成功！")
                if result.stdout:
                    print("卸载输出:")
                    print(result.stdout)
            else:
                print(f"卸载失败")
                if result.stderr:
                    print("错误信息:")
                    print(result.stderr)
                if result.stdout:
                    print("输出信息:")
                    print(result.stdout)
        except Exception as e:
            print(f"卸载过程中出错: {str(e)}")
    
    def uninstall_all_packages(self):
        """卸载所有包"""
        command = [sys.executable, "-m", "pip", "uninstall", "-y"]
        
        try:
            print("正在卸载所有包")
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print("所有包卸载成功！")
                if result.stdout:
                    print("卸载输出:")
                    print(result.stdout)
            else:
                print("卸载失败")
                if result.stderr:
                    print("错误信息:")
                    print(result.stderr)
                if result.stdout:
                    print("输出信息:")
                    print(result.stdout)
        except Exception as e:
            print(f"卸载过程中出错: {str(e)}")

    def run(self):
        """运行主程序"""
        self.show_welcome_info()
        
        while True:
            try:
                user_input = input("\n请输入命令: ").strip()
                
                if user_input.lower() in ['q', 'quit']:
                    print("感谢使用pip安装助手，再见！")
                    break
                
                if user_input == "2":
                    self.show_mirrors()
                    choice = input("请选择镜像编号 (1-6): ").strip()
                    self.set_default_mirror(choice)
                elif user_input.startswith("1 "):
                    package_name = user_input[2:].strip()
                    if package_name:
                        self.install_package(package_name)
                    else:
                        print("请输入要安装的包名")
                elif user_input.startswith("3 "):
                    package_name = user_input[2:].strip()
                    if package_name:
                        self.upgrade_package(package_name)
                    else:
                        print("请输入要更新的包名")
                elif user_input == "4":
                    self.list_installed_packages()
                #如果输入all，卸载所有包
                elif user_input.startswith("5 "):
                    package_name = user_input[2:].strip()
                    if package_name == "all":
                        self.uninstall_all_packages()
                    else:
                        self.uninstall_package(package_name)
                else:
                    print("无效的命令，请重新输入")
                    
            except KeyboardInterrupt:
                print("\n程序被用户中断")
                break
            except Exception as e:
                print(f"程序运行出错: {str(e)}")

if __name__ == "__main__":
    helper = PipInstallHelper()
    helper.run()