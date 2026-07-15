# 🌸 宝宝生活小助手 v2.0

为女朋友打造的健康生活打卡助手，采用 Vue 3 + FastAPI + SQLite 架构。

## 功能特性

- ✅ **今日打卡** - 作息项目打卡，支持完成/跳过/重置
- 📊 **统计分析** - 本周/本月打卡统计，完成率图表
- 🌤️ **天气查询** - 西安/哈尔滨实时天气
- ⚙️ **设置管理** - 自定义作息项目，添加/删除/编辑
- 🤖 **AI 分析** - 智能分析打卡数据，给出建议
- 🎤 **语音输入** - 语音指令打卡

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Vant 4 + Pinia |
| 后端 | FastAPI + aiosqlite |
| 数据库 | SQLite |
| 部署 | Railway 免费层 |
| 天气 | Open-Meteo API |

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 部署

### Railway 部署

1. 推送代码到 GitHub
2. 在 Railway 创建项目
3. 连接 GitHub 仓库
4. 添加 Volume 挂载 `/data`
5. 设置环境变量 `DATA_DIR=/data`

## 项目结构

```
life-helper-v2/
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── database.py          # SQLite 数据库
│   ├── routers/             # API 路由
│   └── models/              # Pydantic 模型
├── frontend/
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── stores/          # Pinia 状态管理
│   │   └── api/             # API 封装
│   └── package.json
├── railway.json
└── README.md
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/schedules | 获取作息列表 |
| POST | /api/schedules | 添加作息 |
| PUT | /api/schedules/{id} | 更新作息 |
| DELETE | /api/schedules/{id} | 删除作息 |
| GET | /api/checkins | 获取打卡记录 |
| POST | /api/checkins | 打卡 |
| DELETE | /api/checkins | 取消打卡 |
| GET | /api/stats | 获取统计 |
| GET | /api/weather | 获取天气 |
| POST | /api/ai/analyze | AI 分析 |

## 环境变量

| 变量 | 说明 |
|------|------|
| DATA_DIR | 数据库目录 |
| AGNES_API_KEY | AI 服务密钥（可选） |

## License

ISC
