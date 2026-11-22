# PTCGP Reddit 百源选题雷达｜2026-11-22 14:51 手动重跑

**窗口（北京时间）：** 2026-11-19T14:51:51+08:00 — 2026-11-22T14:51:51+08:00。生成时间 2026-11-22T14:55:56+08:00。

## 核心验收：百源未达标

- 最新检索索引里明确显示日期且有构筑内容的 Reddit 顶层帖：**2条**（11月20日、11月21日）。
- 本轮重新直接打开并同时核实作者、原始创建时间和正文的 Reddit 原帖/评论：**0条**。
- 严格合格信源：**0/100**；**quality_gate=failed**，差额 **100**。这不是 Reddit 实际讨论量为 0，而是当前工具无法完成严格证据验证。
- 之前 12:42 运行记录的 34 条网页 URL 来自**历史快照**，未在本轮重新完成时间核验，不得复用成今天的新证据。可查看 [之前的证据文件](./evidence/2026-11-22-1242-web-audit.json)。
- 直接打开近期 Reddit 帖子失败（Cache miss）；reddit.com/r/PTCGP/new/ 的可读取网页是几个月前缓存，Reddit公开 JSON 也未能读取。GitHub Actions 先前的采集试验见 [原始403日志](./evidence/reddit-public-raw-2026-11-22T044528Z.json)，**本轮未假称该API已恢复**。

## 本轮新增日期核对（Reddit 之外没有计入任何社交平台）

1. [New Chandelure deck](https://www.reddit.com/r/PTCGP/comments/1y22t44/new_chandelure_deck/) — Reddit 搜索显示 **2026-11-21**。牌组核心为 Chandelure＋Oricorio，依靠弃牌提高伤害，配 Copycat / Hiking Trail 加快轮转。当前搜索能取得时间日历日期及内容，**原帖无法重新直读，作者身份仅在上一轮档案中保存**，不能计入本轮100条严格合格来源。
2. [Unpopular opinion, I like the limited battles](https://www.reddit.com/r/PTCGP/comments/1y0rm9r/unpopular_opinion_i_like_the_limited_battles/) — Reddit 搜索显示 **2026-11-20**。讨论 Pikachu ex 在限定赛的打法以及兔子牌组的一致性问题。Pikachu 已有物种页，不构成新建目标；本轮原帖仍无法重新直读，因此也不计入严格100条。

## 物种页排除核查状态

[物种目录](https://www.pokemontcgpocket.app/en/deck/pokemon) 的最新搜索索引显示 **Page 1 of 2** 和 **Page 2 of 2**；第二页出现 Bewear ex。由于当前直接访问失败，**未能重新确认所有40+条目及过滤组合完整性**，不能以此宣布任何物种100%未收录。旧快照中的目录条目数量不能冒充本轮的完整核验结果。

## SEO观察名单：延续上一轮，非本轮5个新发现

Chandelure（水晶灯火灵）、Aegislash（坚盾剑怪）、Blastoise（水箭龟）、Paldean Clodsire（帕底亚土王）、Zoroark（索罗亚克）。除 Chandelure 本轮找到可核日期的原帖索引外，其余方向仍沿用上一轮研究线索，全部属于**待核观察，不可自动开页**。每项历史证据及状态在 `latest.json.watchlist` 中标注。

## 对下游Agent的约束

仅在 `audit.coverage_met=true` 且站内缺页已完整核验时，才允许将结果当作“百源完整调研”。本轮 `candidates=[]`、`watchlist=5`。请勿把上一轮34条URL和本轮2条搜索命中直接相加成36条合格信源，也不要捏造发帖时间、作者、增长率。

证据文件：[evidence/2026-11-22-1451-reexecution.json](./evidence/2026-11-22-1451-reexecution.json)。历史快照：[history/2026-11-22-1451-reexecution.json](./history/2026-11-22-1451-reexecution.json)。

GitHub和Pages是否同步以最新仓库提交与Pages部署检查为准；JSON不自我证明已发布。
