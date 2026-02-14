## 电商智能客服与风控系统

一个面向电商场景的全栈 AI Agent 项目，完整打通了「意图识别 → RAG 检索 → 订单/退款业务逻辑 → 人机协同风控 → 实时通知」的闭环。

---

### 🎯 项目定位（适合放在简历里的那一行）

> 基于 FastAPI 与 LangChain/LangGraph 的电商智能客服与风控系统，支持订单查询、政策咨询、退款申请，并通过管理员后台实现高风险退款的人机协同审核。

---

### 🚀 核心功能
- **用户侧对话入口**：登录后发起订单查询、物流进度查询、政策咨询、退款申请等多轮对话。
- **RAG 政策问答**：从政策文档构建向量化知识库，基于 PgVector + HNSW 实现语义检索。
- **退款业务流程**：接入真实订单模型与退款规则，判断是否可退、退多少、走自动还是人工审核。
- **管理员工作台**：查看高风险退款审核任务，在线审批，决策结果实时推送给用户。
- **结构化消息卡片**：以订单卡片、退款进度卡片、审核卡片等形式展示关键业务信息。

---

### 🧩 技术亮点

- **RAG + PgVector**：使用 PgVector 存储 Embedding，结合 HNSW 索引实现低延迟语义检索。
- **LangGraph 工作流编排**：将意图识别、订单查询、退款处理、人工审核拆分为节点，使用状态机式工作流管理复杂对话流程。
- **人机协同风控闭环**：基于审计日志（AuditLog）和结构化消息（MessageCard），实现高风险退款从「自动识别 → 生成审核任务 → 管理员审批 → 恢复 Agent 流程 → 通知用户」的完整链路。
- **工程化落地**：引入 Alembic 管理数据库迁移，Celery 处理异步任务，Redis 作为缓存与队列，具备接近真实生产环境的架构。
- **实时通信**：使用 FastAPI WebSocket + 自定义 ConnectionManager 实现用户侧与管理员侧的状态变更实时推送。

---

### 🛠 技术栈概览

- **后端框架**：FastAPI、SQLModel、Alembic  
- **大模型与工作流**：LangChain、LangGraph、OpenAI/Qwen（可替换其他模型）  
- **存储与缓存**：PostgreSQL + PgVector、Redis  
- **异步任务**：Celery  
- **实时通信**：FastAPI WebSocket  
- **前端**：Gradio（用户界面 & 管理员工作台）  

---

### 📂 目录结构

- `app/`：主应用代码  
  - `api/v1/`：RESTful API 与 WebSocket 路由（登录、聊天、管理员审核等）  
  - `core/`：配置、数据库连接、认证模块  
  - `models/`：用户、订单、退款、审计日志、消息卡片、知识库等数据模型  
  - `graph/`：LangGraph 工作流、状态与节点定义  
  - `frontend/`：基于 Gradio 的用户端与管理端界面  
  - `tasks/`：Celery 异步任务（退款支付、短信/通知等）  
  - `websocket/`：WebSocket 连接管理（用户与管理员实时推送）  
- `migrations/`：数据库迁移脚本（Alembic）  
- `scripts/`：数据初始化、知识库构建、数据库校验脚本  
- `pyproject.toml`：依赖与项目配置  

---

### ⚙️ 本地运行

1. 安装依赖（Python 3.10+）：
   ```bash
   # 可根据个人习惯选择 pip / poetry，这里仅示意
   pip install -r requirements.txt
   ```
2. 配置环境变量（数据库、Redis、LLM Key 等），参考 `app/core/config.py`。  
3. 初始化数据库并执行迁移：
   ```bash
   alembic upgrade head
   ```
4. 初始化示例数据 & 知识库（可选）：
   ```bash
   python scripts/seed_data.py
   python scripts/etl_policy.py
   ```
5. 启动服务：
   ```bash
   uvicorn app.main:app --reload
   ```

---

  

