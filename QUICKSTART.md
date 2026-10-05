# 快速开始

本仓库是技能目录，技能代码位于独立包仓库。先选一个与你当前任务相关的技能即可。

## 1. 准备终端

安装 Node.js / npm，在目标项目目录打开终端。无需克隆本导航仓库。

## 2. 查看包内技能

```bash
npx skills add full-stack-skills/vue-skills --list
```

包名可在 [README 技能目录](README.md#技能目录) 中查找；技能名见 [技能索引](SKILLS_INDEX.md)。

## 3. 安装到项目

```bash
# 为当前项目的 Codex 安装 Vue 3 技能
npx skills add full-stack-skills/vue-skills --skill vue3 --agent codex

# Claude Code 用户可改用这个宿主名
npx skills add full-stack-skills/vue-skills --skill vue3 --agent claude-code
```

不指定 `--skill` 或 `--agent` 时，可按 CLI 提示选择。需要跨项目复用时再添加 `--global`，不要把项目安装与用户级安装混为一谈。

## 4. 确认并使用

```bash
npx skills list
```

在宿主中按其技能加载方式使用。例如向 Codex 提出“使用 $vue3 帮我检查这个 Vue 页面”。如果技能没有显示，检查 CLI 输出的宿主和安装位置，并重新加载宿主会话。

## 更新与排查

```bash
npx skills update
```

- 找不到包：复制目录中的完整 `full-stack-skills/<package>` 地址。
- 找不到技能：先用 `--list` 查询，不要用包名代替技能名。
- 网络或认证失败：先确认可以访问对应 GitHub 仓库，再检查终端的网络和 Git 认证配置。
- 需要宿主路径或手工安装：见 [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md)。

## 需要连接外部工具？

查看 [生态导航](README.md#生态导航)，选择相应插件市场并阅读其宿主安装说明。技能包与插件市场使用不同安装机制，可按任务单独选择。

本目录不再提供旧版 `adapters/`、`fskill` 或 Claude Code marketplace 清单。CLI 选项以 [Skills CLI 官方文档](https://github.com/vercel-labs/skills) 为准；本次核对安装说明未执行任何安装或更新命令。
