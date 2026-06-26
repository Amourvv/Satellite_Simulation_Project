# Satellite Resource Platform

面向多层 LEO / GEO / 地面网络共存场景的资源管理仿真与可视化平台。

这个项目从一个最小可行版本开始：先搭建可视化与仿真骨架，再逐步加入频谱、链路预算、路由、计算卸载和联合资源管理算法。

## 项目目标

- 使用 Cesium + Vue 3 可视化卫星、轨道、地面站和可见链路。
- 使用 FastAPI 提供仿真状态、场景配置和算法结果接口。
- 支持从简单 Walker LEO 星座开始，逐步扩展到 LEO / GEO / 地面网络共存。
- 为论文实验保留可复现实验配置、指标导出和算法对比能力。

## 当前骨架

```text
.
├── backend/        FastAPI 仿真服务
├── frontend/       Vue 3 + Cesium 前端入口
├── docs/           架构、模型和路线文档
└── experiments/    实验场景配置
```

## 第一阶段 MVP

1. 后端生成一个简化 LEO 星座与地面站。
2. 前端显示地球、卫星、轨道近似轨迹和可见链路。
3. 后端返回距离、仰角、自由空间路径损耗、理论容量等基础链路指标。
4. 支持仿真时间播放，为后续频谱、网络和计算资源管理接入状态流。

## 本地启动

后端：

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

前端：

```bash
cd frontend
npm install
npm run dev
```

前端默认读取 `http://localhost:8000` 的后端接口。

