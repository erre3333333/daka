# 🎨 前端部署指南

## 方案 A: Railway 部署（推荐）

### 步骤 1: 创建前端项目

1. 打开 https://railway.app/new
2. 点击 **"Deploy from GitHub repo"**
3. 选择 **`erre3333333/daka`** 仓库

### 步骤 2: 配置构建

在项目 **Settings** 中设置：

| 配置项 | 值 |
|--------|-----|
| Build Command | `cd frontend && npm install && npm run build` |
| Output Directory | `frontend/dist` |
| Start Command | `npx serve -s dist -l $PORT` |

### 步骤 3: 设置环境变量

| 变量 | 值 |
|------|-----|
| `VITE_API_BASE` | `https://你的后端地址.up.railway.app/api` |

### 步骤 4: 自定义域名（可选）

1. Settings → Networking → Custom Domain
2. 添加你的域名

---

## 方案 B: Vercel 部署

### 步骤 1: 导入项目

1. 打开 https://vercel.com/new
2. 选择 **"Import Git Repository"**
3. 选择 **`erre3333333/daka`**

### 步骤 2: 配置构建

| 配置项 | 值 |
|--------|-----|
| Framework | Vite |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

### 步骤 3: 环境变量

| 变量 | 值 |
|------|-----|
| `VITE_API_BASE` | `https://你的后端地址.up.railway.app/api` |

### 步骤 4: 部署

点击 **"Deploy"** 完成部署

---

## 方案 C: Netlify 部署

### 步骤 1: 导入项目

1. 打开 https://app.netlify.com
2. 点击 **"Add new site"** → **"Import an existing project"**
3. 选择 GitHub → **`erre3333333/daka`**

### 步骤 2: 配置构建

| 配置项 | 值 |
|--------|-----|
| Base directory | `frontend` |
| Build command | `npm run build` |
| Publish directory | `dist` |

### 步骤 3: 环境变量

Site settings → Environment variables → 添加：

| 变量 | 值 |
|------|-----|
| `VITE_API_BASE` | `https://你的后端地址.up.railway.app/api` |

---

## 验证部署

部署完成后，访问前端地址，应该能看到：
- 页面正常加载
- 打卡功能正常
- 天气显示正常

## 常见问题

### Q: 页面空白？

A: 检查 `VITE_API_BASE` 环境变量是否正确设置

### Q: API 请求失败？

A: 确保后端已部署并正常运行

### Q: 样式丢失？

A: 检查 Google Fonts 是否可访问
