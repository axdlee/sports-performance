# -*- coding: utf-8 -*-
"""
自定义按钮组件 - 解决macOS下tkinter按钮背景色显示问题
"""

import tkinter as tk


class CustomButton(tk.Frame):
    """
    自定义按钮类
    使用Frame和Label组合来模拟按钮，完美支持自定义背景色
    """
    
    def __init__(self, parent, text="", command=None, 
                 bg="#3498db", fg="white", 
                 font=("Microsoft YaHei", 11, "bold"),
                 width=20, height=2,
                 activebackground=None, activeforeground=None,
                 disabledbackground="#bdc3c7", disabledforeground="#7f8c8d",
                 state=tk.NORMAL, cursor="hand2", **kwargs):
        """
        初始化自定义按钮
        
        Args:
            parent: 父容器
            text: 按钮文本
            command: 点击回调函数
            bg: 正常状态背景色
            fg: 正常状态前景色
            font: 字体
            width: 宽度（字符数）
            height: 高度（行数）
            activebackground: 悬停时背景色
            activeforeground: 悬停时前景色
            disabledbackground: 禁用状态背景色
            disabledforeground: 禁用状态前景色
            state: 按钮状态 (tk.NORMAL 或 tk.DISABLED)
            cursor: 鼠标光标样式
        """
        # 初始化Frame
        super().__init__(parent, bg=bg, cursor=cursor, **kwargs)
        
        # 保存参数
        self.command = command
        self.normal_bg = bg
        self.normal_fg = fg
        self.active_bg = activebackground or self._darken_color(bg)
        self.active_fg = activeforeground or fg
        self.disabled_bg = disabledbackground
        self.disabled_fg = disabledforeground
        self._state = state
        self._cursor = cursor
        self.font = font
        
        # 创建Label作为按钮内容
        self.label = tk.Label(
            self,
            text=text,
            bg=bg,
            fg=fg,
            font=font,
            cursor=cursor,
            padx=width*6,  # 转换字符宽度为像素
            pady=height*8  # 转换行高为像素
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # 强制更新，确保控件已创建
        self.update_idletasks()
        
        # 绑定事件
        if state == tk.NORMAL:
            self._bind_events()
        
        # 应用初始状态
        if state == tk.DISABLED:
            self.config_state(tk.DISABLED)
    
    def _darken_color(self, color):
        """
        将颜色变暗（用于悬停效果）
        """
        if color.startswith('#'):
            # 解析十六进制颜色
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # 降低亮度
            r = max(0, int(r * 0.8))
            g = max(0, int(g * 0.8))
            b = max(0, int(b * 0.8))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def _bind_events(self):
        """绑定鼠标事件"""
        # 悬停事件
        self.bind("<Enter>", self._on_enter)
        self.label.bind("<Enter>", self._on_enter)
        
        self.bind("<Leave>", self._on_leave)
        self.label.bind("<Leave>", self._on_leave)
        
        # 按下和释放事件（用于视觉反馈）
        self.bind("<ButtonPress-1>", self._on_press)
        self.label.bind("<ButtonPress-1>", self._on_press)
        
        # 使用 ButtonRelease 来触发命令（更可靠）
        self.bind("<ButtonRelease-1>", self._on_release_click)
        self.label.bind("<ButtonRelease-1>", self._on_release_click)
    
    def _unbind_events(self):
        """解绑鼠标事件"""
        self.unbind("<Enter>")
        self.label.unbind("<Enter>")
        self.unbind("<Leave>")
        self.label.unbind("<Leave>")
        self.unbind("<ButtonPress-1>")
        self.label.unbind("<ButtonPress-1>")
        self.unbind("<ButtonRelease-1>")
        self.label.unbind("<ButtonRelease-1>")
    
    def _on_enter(self, event):
        """鼠标进入事件"""
        if self._state == tk.NORMAL:
            self.configure(bg=self.active_bg)
            self.label.configure(bg=self.active_bg, fg=self.active_fg)
    
    def _on_leave(self, event):
        """鼠标离开事件"""
        if self._state == tk.NORMAL:
            self.configure(bg=self.normal_bg)
            self.label.configure(bg=self.normal_bg, fg=self.normal_fg)
    
    def _on_press(self, event):
        """鼠标按下事件"""
        if self._state == tk.NORMAL:
            # 按下时稍微变暗
            darker_bg = self._darken_color(self.active_bg)
            self.configure(bg=darker_bg)
            self.label.configure(bg=darker_bg)
    
    def _on_release_click(self, event):
        """鼠标释放事件 - 触发点击"""
        if self._state == tk.NORMAL:
            # 检查鼠标是否还在按钮内
            x, y = event.x, event.y
            widget_width = self.winfo_width()
            widget_height = self.winfo_height()
            
            # 恢复悬停颜色
            if 0 <= x <= widget_width and 0 <= y <= widget_height:
                self.configure(bg=self.active_bg)
                self.label.configure(bg=self.active_bg)
                
                # 触发命令
                if self.command:
                    self.command()
            else:
                self.configure(bg=self.normal_bg)
                self.label.configure(bg=self.normal_bg)
    
    def config_state(self, state):
        """
        配置按钮状态
        
        Args:
            state: tk.NORMAL 或 tk.DISABLED
        """
        self._state = state
        
        if state == tk.DISABLED:
            # 禁用状态
            self.configure(bg=self.disabled_bg, cursor="")
            self.label.configure(bg=self.disabled_bg, fg=self.disabled_fg, cursor="")
            self._unbind_events()
        else:
            # 正常状态
            self.configure(bg=self.normal_bg, cursor=self._cursor)
            self.label.configure(bg=self.normal_bg, fg=self.normal_fg, cursor=self._cursor)
            self._bind_events()
    
    def config(self, **kwargs):
        """
        配置按钮属性
        
        支持的参数:
            state: 按钮状态
            bg: 背景色
            fg: 前景色
            text: 文本
            command: 回调函数
            cursor: 光标样式
        """
        if 'state' in kwargs:
            self.config_state(kwargs.pop('state'))
        
        if 'bg' in kwargs:
            self.normal_bg = kwargs['bg']
            if self._state == tk.NORMAL:
                super().config(bg=kwargs['bg'])
                self.label.config(bg=kwargs['bg'])
        
        if 'fg' in kwargs:
            self.normal_fg = kwargs['fg']
            if self._state == tk.NORMAL:
                self.label.config(fg=kwargs['fg'])
        
        if 'text' in kwargs:
            self.label.config(text=kwargs['text'])
        
        if 'command' in kwargs:
            self.command = kwargs['command']
        
        if 'cursor' in kwargs:
            self._cursor = kwargs['cursor']
            if self._state == tk.NORMAL:
                super().config(cursor=kwargs['cursor'])
                self.label.config(cursor=kwargs['cursor'])
        
        # 处理其他Frame参数
        frame_kwargs = {k: v for k, v in kwargs.items() 
                       if k not in ['state', 'bg', 'fg', 'text', 'command', 'cursor']}
        if frame_kwargs:
            super().config(**frame_kwargs)
    
    def cget(self, key):
        """获取配置值"""
        if key == 'state':
            return 'disabled' if self._state == tk.DISABLED else 'normal'
        elif key == 'bg':
            return self.normal_bg
        elif key == 'fg':
            return self.normal_fg
        elif key == 'text':
            return self.label.cget('text')
        else:
            return super().cget(key)
