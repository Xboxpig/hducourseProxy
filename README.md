# HDU-CourseProxy

**HDU-CourseProxy** 是一个专为 HDUCourse 设计的直播课程桥接工具。它通过自动化鉴权技术，将原本封闭的 SSO 登录与课程 API 转化为结构化数据，旨在最终实现直播流地址的自动提取与分发。

> **当前项目状态：[WIP] 开发中** > 🟢 已完成：自动化 SSO 鉴权、Token 状态监测、课程列表抓取、本地配置管理。
> 
> 🟡 待完成：直播流地址（playUrl）解析、自动推流至播放端。

---

## 📂 文件结构

项目采用代码与配置分离的结构，确保核心逻辑的整洁与安全：

Plaintext

```
HDU-CourseProxy/
├── config.json          # 个人配置文件（需手动创建，存账号密码）
├── session.json         # 自动生成的本地缓存文件（存储 JWT Token）
├── .gitignore           # Git 忽略名单（保护隐私）
└── src/                 # 核心源代码目录
    ├── main.py          # 项目调度中心，负责整体流程控制
    ├── hdu_auth.py      # 鉴权模块，处理 Selenium 自动化登录
    ├── hdu_api.py       # 数据处理模块，负责课程 API 请求与清洗
    └── tokenchecker.py  # 二分判断模块，实时监测 Token 有效性
```

---

## 🚀 快速开始

### 1. 克隆项目

Bash

```
git clone https://github.com/你的用户名/HDU-CourseProxy.git
cd HDU-CourseProxy
```

### 2. 环境配置

确保已安装 Chrome 浏览器及对应的 WebDriver，并安装依赖：

Bash

```
pip install requests selenium urllib3
```

### 3. 创建配置文件

在项目根目录下新建 `config.json`，并填入你的凭据：

JSON

```
{
    "username": "你的学号",
    "password": "你的密码",
    "max_retries": 3,
    "days_offset": 7
}
```

### 4. 运行

Bash

```
python src/main.py
```

---

## 🛠 当前功能实现

- **智能鉴权系统**：基于 Selenium 自动化技术，自动处理学校 SSO 登录，并精准拦截 `jwt-token`。
    
- **Token 保活机制**：程序启动时优先读取 `session.json`。若 Token 失效（捕获到 10013 错误），将自动唤起浏览器进行补登，无需人工干预。
    
- **高容错调度**：针对 SSO 页面加载不稳定的痛点，内置了超时重载与重试机制。
    
- **结构化输出**：自动获取未来 N 天的课程表，包括课程 ID、名称、时间及地点。
    

---

## 📅 路线图 (Roadmap)

- [x] 模块化重构与路径自适应
    
- [x] 基于 10013 错误码的二分判断逻辑
    
- [ ] **[下一阶段]** 解析 `vod_live` 详情，提取 `playUrl` 直播地址
    
- [ ] **[计划中]** 集成 FFmpeg，实现直播流一键推送到播放端 (MediaMTX)
    

---

## ⚠️ 免责声明

本项目仅供学习和个人便利使用，请勿用于任何违反校规或法律法规的行为。用户需自行承担因使用本项目而产生的相关风险。
