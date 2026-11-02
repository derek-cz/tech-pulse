# 技术雷达 (Tech Radar) 工具手册

> **目录位置**: `E:\AI\claude\工具\tech-radar\`  
> **定位**: 定时采集前沿技术资讯、提炼关键研报、多通道自动推送并沉淀至助手知识库的自动化管线。  
> **创建日期**: 2026-10-29  

---

## 一、系统架构与能力大纲

整个技术雷达分为 **信息采集 (Gather)**、**数据沉淀 (Archive)** 与 **多端推送 (Notify)** 三层：

```text
┌────────────────────────────────────────────────────────┐
│                   信息源采集 (fetcher.py)               │
│  ├─ 1. AI 动态: Hacker News 官方 API (高赞/高热度讨论)   │
│  ├─ 2. 本体/知识图谱: arXiv cs.AI/cs.LO 最新论文检索    │
│  └─ 3. GitHub 增长工具: GitHub 官方 API 爆发项目过滤     │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                   调度与组装 (main.py)                 │
├───────────────────────────┬────────────────────────────┤
│                           │                            │
│  [通道 A: 知识沉淀]        │   [通道 B: 飞书推送]        │
│  写入 Markdown 日报归档    │   组装富文本交互卡片        │
│  E:\AI\05-助手\03-外部知识\ │   飞书自建应用鉴权          │
│  技术雷达\简报归档\         │   直接下发个人单聊          │
└───────────────────────────┴────────────────────────────┘
```

### 核心能力特性

1. **三维雷达覆盖**：
   - **AI 前沿**：聚焦 AI/LLM 行业讨论与新产品发布，过滤低质噪音；
   - **本体论演进**：追踪语义网、知识表示与推理（cs.AI / cs.LO / cs.DB）底层学术论文与规范；
   - **开源新星**：抓取近 72 小时内全球 Star 增长最快的新生工具。
2. **飞书自建应用直推**：
   - 基于飞书开放平台内部应用（App ID: `cli_xxxxxxxxxxxxxxxx`）；
   - 支持免手动查 ID：通过 `tenant_access_token` 自动从租户中解析接收人标识；
   - 交互卡片排版：包含热度徽标、作者/发布时间、摘要及外链直达。
3. **双区知识管理规范契合**：
   - 执行脚本保留在执行区 `E:\AI\claude\工具\tech-radar\`；
   - 产出简报自动归档入 `E:\AI\05-助手\03-外部知识\技术雷达\简报归档\`，符合个人留档与对外知识分流规范。

---

## 二、代码工程结构

```text
E:\AI\claude\工具\tech-radar/
├── README.md               # 本技术手册与运维文档
├── fetcher.py              # 数据采集模块（集成 HN / arXiv / GitHub 检索逻辑）
├── main.py                 # 主执行调度入口（采集、归档、飞书推送）
└── config.json             # 运行时配置（飞书应用凭证与接收用户标识，可选）
```

---

## 三、配置与运行指南

### 1. 运行配置优先级
`main.py` 支持**环境变量优先**，缺省时自动读取同目录 `config.json`：

| 配置项 | 环境变量名 | 说明 |
| :--- | :--- | :--- |
| **App ID** | `FEISHU_APP_ID` | 飞书自建应用 ID（如 `cli_xxxxxxxxxxxxxxxx`） |
| **App Secret** | `FEISHU_APP_SECRET` | 飞书应用密钥（在飞书开放平台后台获取） |
| **Open ID** | `FEISHU_OPEN_ID` | 接收消息的个人用户唯一标识 |

### 2. 手动单次触发

打开终端执行以下命令即可：

```powershell
python "E:\AI\claude\工具\tech-radar\main.py"
```

---

## 四、定时调度部署方案

### 方案 A：Windows 本地计划任务（开机静默定时）

适合希望在工作电脑上每天固定时间触发（例如工作日早晨 09:00）：

1. 打开 PowerShell（管理员身份运行），执行以下命令注册定时任务：
   ```powershell
   $Action = New-ScheduledTaskAction -Execute "python.exe" -Argument '"E:\AI\claude\工具\tech-radar\main.py"' -WorkingDirectory "E:\AI\claude\工具\tech-radar"
   $Trigger = New-ScheduledTaskTrigger -Daily -At "09:00AM"
   Register-ScheduledTask -TaskName "TechRadarDailyDigest" -Action $Action -Trigger $Trigger -Description "每日技术雷达抓取与飞书推送"
   ```
2. 任务将在每天早晨 9:00 自动被 Windows 任务计划程序静默唤醒执行。

### 方案 B：GitHub Actions 云端全托管（免开机、全天候）

适合完全脱离本地电脑限制，代码推送到 GitHub 仓库后：
1. 仓库内添加 `.github/workflows/daily_digest.yml`；
2. 在 GitHub 仓库设置 `Settings` -> `Secrets and variables` -> `Actions` 配置 `FEISHU_APP_SECRET`；
3. Actions 每日根据 Cron 表达式定时启动 Ubuntu 容器运行采集和推送。

---

## 五、知识库归档与保鲜台账

每次任务执行完毕后，简报均会自动沉淀在：
- **简报目录**: `E:\AI\05-助手\03-外部知识\技术雷达\简报归档\YYYY-MM-DD.md`
- **生命周期索引**: 已在 `E:\AI\05-助手\文件清单.md` 中注册，状态为 🟢 正常更新。
