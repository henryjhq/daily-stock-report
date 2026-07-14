# 安装 daily-stock-report

支持三个 AI 编程助手：Claude Code、Codex、Codebuddy。

## 我该做什么

把下面「发给 AI 助手」那段话完整复制，贴给你的 AI 编程助手，回车。30 秒装好。

---

## 发给 AI 助手

> 请帮我安装 daily-stock-report skill。
>
> 仓库地址：https://github.com/<user>/daily-stock-report.git
>
> 1. 判断你自己是什么 agent：
>    - Claude Code → 克隆到 ~/.claude/skills/daily-stock-report/
>    - Codex → 克隆到 ~/.codex/skills/daily-stock-report/
>    - Codebuddy → 克隆到 ~/.codebuddy/skills-marketplace/skills/daily-stock-report/
> 2. git clone 到对应目录
> 3. cd 进入目录，运行 chmod +x setup.sh && ./setup.sh
> 4. 装好后告诉我，跑 /daily-stock-report 测试一下

---

## 装好之后

- `/daily-stock-report` — 弹菜单选市场，然后生成 PDF 报告
- `/daily-stock-report 美股` — 跳过菜单，直接出美股报告
- `/daily-stock-report 港股` — 跳过菜单，直接出港股报告

---

## 更新

以后有新版本时，进入安装目录跑：

```bash
./setup.sh --update
```

---

## 卸载

```bash
rm -rf ~/.claude/skills/daily-stock-report
```

如果也装了其他 agent，同样删除对应目录即可。
