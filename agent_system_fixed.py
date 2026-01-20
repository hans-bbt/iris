#!/usr/bin/env python3
import os
import json
import subprocess
import sys
from typing import Tuple, Optional
from openai import OpenAI

class AgentSystem:
    def __init__(self, api_config_path: str = None):
        self.client = None
        self.conversation_history = []
        
        # 尝试从不同位置加载API配置
        possible_paths = [
            api_config_path,
            os.path.expanduser("~/agent/api.txt"),
            os.path.expanduser("~/agent1/api.txt"),
            "/home/hbt/agent1/api.txt",
            "/etc/agent/api.txt",
            "api.txt"
        ]
        
        api_key = None
        base_url = None
        
        for path in possible_paths:
            if path and self.load_api_config(path):
                api_key = self.api_key
                base_url = self.api_url
                print(f"API配置从 {path} 加载成功")
                break
        
        if not api_key:
            print("警告: 未找到API配置文件，请手动输入API信息")
            api_key = input("请输入API Key: ").strip()
            base_url = "https://api.deepseek.com"
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    
    def load_api_config(self, path: str) -> bool:
        """从文件加载API配置"""
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        self.api_url = lines[0].strip()
                        self.api_key = lines[1].strip()
                        return True
        except Exception as e:
            print(f"加载API配置失败: {e}")
        return False
    
    def execute_command(self, command: str) -> Tuple[str, int]:
        """执行系统命令并返回输出"""
        try:
            print(f"执行命令: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            output = result.stdout
            if result.stderr:
                output += f"\n错误输出:\n{result.stderr}"
            return output, result.returncode
        except subprocess.TimeoutExpired:
            return "命令执行超时（5分钟）", -1
        except Exception as e:
            return f"命令执行失败: {e}", -1
    
    def call_deepseek_api(self, prompt: str) -> Optional[str]:
        """调用DeepSeek API"""
        if not self.client:
            return "API客户端未初始化，无法调用大模型"
        
        try:
            # 构建完整的历史记录
            messages = self.conversation_history.copy()
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                stream=False
            )
            
            reply = response.choices[0].message.content
            
            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            # 限制历史记录长度
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return reply
            
        except Exception as e:
            return f"API调用失败: {e}"
    
    def parse_command_from_response(self, response: str) -> str:
        """从大模型响应中提取命令"""
        # 简单实现：寻找代码块或命令标记
        lines = response.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('```bash') or line.strip().startswith('```sh'):
                # 提取代码块中的命令
                command_lines = []
                for next_line in lines[i+1:]:
                    if next_line.strip().startswith('```'):
                        break
                    command_lines.append(next_line)
                return '\n'.join(command_lines).strip()
            elif line.strip().lower().startswith('命令:'):
                return line.split(':', 1)[1].strip()
        
        # 如果没有明显标记，返回整个响应
        return response.strip()
    
    def run(self, initial_task: str = None):
        """主运行循环"""
        print("=== Agent系统启动 ===")
        print(f"Python版本: {sys.version}")
        print(f"当前目录: {os.getcwd()}")
        print("=" * 50)
        
        # 如果有初始任务，直接使用
        if initial_task:
            task = initial_task
        else:
            task = input("请输入任务描述: ").strip()
        
        if not task:
            print("任务不能为空")
            return
        
        iteration = 0
        max_iterations = 20  # 减少最大迭代次数
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n=== 第 {iteration} 轮迭代 ===")
            
            # 调用大模型获取命令
            print(f"发送给大模型的任务: {task}")
            response = self.call_deepseek_api(task)
            
            if not response:
                print("大模型返回空响应")
                break
            
            print(f"\n大模型响应:\n{response}")
            
            # 解析命令
            command = self.parse_command_from_response(response)
            print(f"\n解析出的命令:\n{command}")
            
            # 检查是否退出
            if command.lower() in ['exit', 'quit', '结束']:
                print("接收到退出命令，结束运行")
                break
            
            # 检查是否是错误信息
            if 'API调用失败:' in command or '失败:' in command:
                print(f"检测到错误信息，不执行命令: {command}")
                task = "上一轮出现了错误，请重新考虑正确的命令"
                continue
            
            # 执行命令
            output, returncode = self.execute_command(command)
            print(f"\n命令执行结果 (返回码: {returncode}):\n{output[:1500]}")  # 限制输出长度
            
            # 准备下一轮的任务
            task = f"上一条命令执行结果:\n{output[:3000]}\n\n请根据以上结果决定下一步操作，输出下一个命令（或exit结束）"
        
        if iteration >= max_iterations:
            print(f"达到最大迭代次数 ({max_iterations})，自动结束")

if __name__ == "__main__":
    import sys
    initial_task = None
    if len(sys.argv) > 1:
        initial_task = ' '.join(sys.argv[1:])
    
    agent = AgentSystem()
    agent.run(initial_task)
