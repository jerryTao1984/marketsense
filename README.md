# 🦆 识盘鸭

> 像 Duolingo 一样学炒股 — A 股知识闯关学习应用

## 功能特性

- **手机号登录** — 输入 11 位手机号即可登录，无需验证码/密码
- **四大学习模块** — 基础概念、交易法则、K线实盘、K线预测，共 15 关 500+ 题目
- **关卡解锁** — 逐关通关解锁下一关
- **真实 A 股数据** — 接入 StockPillar API，展示真实 K 线图表、资金流、基本面数据
- **答题记录** — 记录每道题的对错、正确率统计
- **错题本** — 自动收集错题，支持针对单关卡重新复习
- **做题记录** — 查看所有答题历史，按关卡分组
- **已答题自动跳过** — 答对的题不再出现，专注错题和新题
- **体力系统** — 5 颗心，答错扣心，通关回 1 颗
- **连胜天数** — 连续打卡天数统计

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | Vue 3 + Vite + TypeScript + Vant 4 + Pinia |
| 后端 | FastAPI + Uvicorn + SQLite |
| 部署 | Docker + Docker Compose |
| 数据源 | StockPillar API（真实 A 股行情） |

## 项目结构

```
marketsense/
├── backend/
│   ├── main.py              # FastAPI 后端（含所有 API 接口）
│   ├── init_db.py           # 数据库初始化 + 题目数据
│   ├── requirements.txt     # Python 依赖
│   └── *.py                 # 题目生成脚本
├── src/
│   ├── api/index.ts         # 前端 API 封装
│   ├── stores/user.ts       # Pinia 用户状态管理
│   ├── router/index.ts      # Vue Router 路由配置
│   └── views/               # 页面组件
│       ├── LoginView.vue        # 手机号登录
│       ├── HomeView.vue         # 首页（模块入口）
│       ├── CategoryView.vue     # 关卡列表
│       ├── QuizView.vue         # 答题页
│       ├── ProfileView.vue      # 个人中心（正确率统计）
│       ├── WrongAnswersView.vue # 错题本
│       ├── ReviewQuizView.vue   # 错题重做
│       └── HistoryView.vue      # 做题记录
├── Dockerfile               # 多阶段构建（前端 + 后端）
├── docker-compose.yml       # 一键部署配置
├── deploy.sh                # 一键部署脚本
└── update.sh                # 更新服务脚本
```

## 本地开发

### 后端

```bash
cd backend
pip install -r requirements.txt
python3 main.py
# 运行在 http://localhost:8000
```

### 前端

```bash
npm install
npx vite
# 运行在 http://localhost:5173，自动代理 API 到 8000
```

## Docker 部署（推荐）

只需要一个端口 5000，前后端合并运行。

```bash
# 克隆代码
git clone https://github.com/jerryTao1984/marketsense.git
cd marketsense

# 一键部署
chmod +x deploy.sh
./deploy.sh

# 访问 http://服务器IP:5000
```

### 更新服务

```bash
./update.sh
# 自动 git pull → 重建镜像 → 重启服务
```

### 手动部署

```bash
docker compose build
docker compose up -d

# 查看日志
docker compose logs -f

# 停止
docker compose down
```

### 数据持久化

数据库文件存储在 `./data/shipanya.db`，通过 Docker volume 映射到宿主机，容器重建数据不会丢失。

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/phone-login` | 手机号登录 |
| GET | `/api/v1/categories` | 获取所有分区和关卡 |
| GET | `/api/v1/questions/{level_id}` | 获取关卡题目 |
| POST | `/api/v1/questions/check` | 提交答案判定 |
| POST | `/api/v1/progress/complete` | 关卡结算 |
| GET | `/api/v1/user/profile` | 用户资料 + 正确率统计 |
| GET | `/api/v1/user/wrong-answers` | 获取错题列表 |
| GET | `/api/v1/user/done-questions` | 获取已答对的题目 |
| GET | `/api/v1/user/history` | 获取做题记录 |
| POST | `/api/v1/user/deduct-heart` | 扣除体力 |
| POST | `/api/v1/user/refill-hearts` | 恢复体力 |

## 关卡一览

| 分区 | 关卡 | 内容 |
|------|------|------|
| 📖 基础概念 | L1~L4 | 市场基础、财务报表、技术指标、投资策略 |
| 🐢 交易法则 | T1~T4 | 海豚交易法、海龟交易法、深度估值、波动率反转 |
| 📊 K线实盘 | K1~K4 | 单根K线、K线组合、趋势形态、量价分析 |
| 🔮 K线预测 | P1~P3 | 下周涨跌预测、趋势转折预测、支撑压力预测 |
