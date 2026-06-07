# Prompt Management System (FastAPI + SQLite)

一个轻量级 Prompt 管理系统，支持 Prompt 创建、版本管理、模板渲染与基础结构化设计。基于 FastAPI + SQLite 实现，采用分层架构设计，便于扩展为 Prompt Engineering 平台或 LLM 应用后端。

---

## 📌 系统目标

该项目用于解决 Prompt 的以下问题：

- Prompt 无版本管理问题
- Prompt 修改不可追溯
- Prompt 模板复用困难
- Prompt 与 LLM 调用耦合严重

目标是构建一个可扩展的 Prompt 管理后端系统。

---

## 🧱 系统架构设计（分层架构）

整体采用经典三层结构：

```
Client (HTTP Request)
        ↓
FastAPI Router Layer (API Layer)
        ↓
Service Layer (Business Logic)
        ↓
Database Layer (SQLite + SQL)
        ↓
SQLite File Storage
```

---

## 📦 各层职责

### 1. API 层（FastAPI）

目录：`routes/`

职责：

- 接收 HTTP 请求
- 参数校验（Pydantic）
- 调用 Service / Database
- 返回 JSON Response

接口示例：

- `POST /prompts`
- `GET /prompts`
- `GET /prompts/{prompt_id}`
- `POST /prompts/{prompt_id}/versions`

---

### 2. Service 层（业务逻辑）

目录：`services/`

职责：

- Prompt 模板渲染
- 版本选择逻辑（latest / specific version）
- 变量注入处理（format）
- 业务规则封装（不涉及 HTTP / SQL）

核心函数：

- `render_version(prompt_id, version, variables)`
- `render_latest_prompt(prompt_id, variables)`
- `render_content(content, variables)`

---

### 3. Database 层（SQLite）

目录：`database/`

文件：`database.py`

职责：

- 直接操作 SQLite
- CRUD Prompt
- CRUD Prompt Version
- 返回 dict / row 数据结构

核心函数：

#### Prompt
- `create_prompt(name)`
- `get_prompt(prompt_id)`
- `get_all_prompts()`

#### Version
- `create_version(prompt_id, content, tags)`
- `get_version(prompt_id, version)`
- `get_latest_version(prompt_id)`
- `get_all_versions(prompt_id)`

---

### 4. Schema 层（Pydantic）

目录：`schemas/`

职责：

- 请求数据结构定义
- 响应数据结构定义
- API 数据约束

示例：

- `PromptCreate`
- `PromptResponse`
- `VersionCreate`
- `VersionResponse`

---

## 🗄 数据库设计（SQLite）

### prompts 表

```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

### prompt_versions 表

```sql
CREATE TABLE prompt_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(prompt_id) REFERENCES prompts(id),
    UNIQUE(prompt_id, version)
);
```

---

## ⚙️ 已实现功能

### Prompt 管理

- 创建 Prompt
- 查询单个 Prompt
- 查询全部 Prompt

---

### Version 管理（已完成验证 ✔）

- 创建 Prompt Version
- 自动版本递增（latest version + 1）
- 查询指定版本
- 查询最新版本
- 查询所有版本

---

### Prompt 渲染能力

- 支持模板变量替换

示例：

```
"Translate {text} to Chinese"
```

输入：

```json
{
  "text": "hello"
}
```

输出：

```
Translate hello to Chinese
```

---

## 🧪 当前已验证功能

✔ Prompt 创建成功  
✔ Prompt 查询成功  
✔ Version 创建成功（核心功能已验证）  
✔ SQLite CRUD 正常运行  
✔ FastAPI 路由可用  
✔ 数据结构稳定  

---

## 🧩 技术栈

- FastAPI
- SQLite
- Pydantic
- Python 3.10+
- Uvicorn

---

## 🚧 后续计划

- 接入 LLM（DeepSeek / OpenAI）
- Prompt Generate API
- Prompt Version History UI
- Prompt Diff 对比
- Prompt A/B Testing
- Redis Cache（可选）
- 用户系统（多租户支持）

---

## 📁 项目结构（当前）

```
project/
│
├── database/
│   └── database.py
│
├── schemas/
│   └── prompt.py
│
├── services/
│   └── prompt_service.py
│
├── routes/
│   └── prompt_api.py
│
├── main.py
└── init_db.py
```

---

## 🚀 启动方式

```bash
python main.py
```

访问：

```
http://127.0.0.1:8000/docs
```

---

## 📌 说明

该项目为学习型 + 工程原型项目，用于理解：

- Web 后端分层设计
- Prompt Engineering 系统结构
- SQLite 在轻量后端中的应用
- FastAPI 架构模式
```