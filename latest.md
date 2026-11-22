# PTCGP Reddit 百源选题雷达｜2026-11-22 立即执行（未达标）

**时间窗口**：2026-11-19T12:42:57+08:00 — 2026-11-22T12:42:57+08:00（北京时间）。
**报告生成时间**：2026-11-22T12:49:42+08:00。
**研究质量：未通过百源门槛**。Reddit 是本轮唯一社媒平台，没有搜索 X。

## 信源漏斗（真实回读）

- 直接打开、去重的 Reddit 原帖/评论 URL：**34**（10 个顶层帖 + 24 个评论永久链接）。
- 含具体构筑意图的已查看记录：**32**；相关独立作者账号（仅内容层观察、非精确72小时核证）：**29**。
- 严格核实“作者 + 创建时间精确落入72小时 + 构筑信息”的来源：**0 / 100**；网页只显示相对时间且可能为缓存，不能编造 created_utc。
- GitHub Actions 的 Reddit 公开 JSON 采集工作流确已成功运行，但三个 subreddit 的 new.json 全部 **HTTP 403 Blocked**；原始帖子/评论元数据回收数：**0**。失败原始日志：[Reddit 403 日志](./evidence/reddit-public-raw-2026-11-22T044528Z.json)。
- 同一顶层帖多位用户回复不能算多条互不关联的讨论。本轮仅检查了 10 个不同顶层讨论串（包含非构筑原帖），不代表全量社区覆盖。

## 5 个尚未进入物种目录的待验证 SEO 选题（非合格百源结论）

1. **Chandelure（水晶灯火灵）**：Oricorio 弃牌加速、Copycat/Hiking Trail、Meloetta 变体，支持卡位争论。独立构筑主帖 https://www.reddit.com/r/PTCGP/comments/1y22t44/new_chandelure_deck/ ；其他用户讨论在该帖评论中。建议比较快攻与Meloetta节奏型构筑。
2. **Aegislash（坚盾剑怪）**：Cursed Metal 的 Togedemaru、Dialga ex、Melmetal、Mega Skarmory 等搭档。求助与多名作者实质建议 https://www.reddit.com/r/PokemonPocket/comments/1y0sfrt/amy_good_builds_that_combo_with_this_card/ 。同一顶层帖，未证明跨帖升温。
3. **Blastoise（水箭龟）**：C1 普通版限定赛、Lorelei＋Lapras、Squirtle 麻痹进化时机。见 https://www.reddit.com/r/PTCGP/comments/1y1dwkw/we_never_knew_how_much_wed_miss_him_til_he_was/ 和 https://www.reddit.com/r/PTCGP/comments/1y0rm9r/unpopular_opinion_i_like_the_limited_battles/ 的不同玩家构筑回复。
4. **Paldean Clodsire（帕底亚土王）**：Rika 能量加速、Whiscash 搭档以及 Red Card 与 Stadium 替换。见 https://www.reddit.com/r/PokemonPocket/comments/1xzve1f/if_youre_struggling_with_the_limited_battles_this/ 以及 https://www.reddit.com/r/PTCGP/comments/1y1i9ao/what_cards_do_you_think_people_are_sleeping_on/ 。
5. **Zoroark（索罗亚克）**：C1 Foul Play，Pidgeot + Blue's Provocation 与 Clodsire 牌组替换版。见 https://www.reddit.com/r/PTCGP/comments/1y1dwkw/we_never_knew_how_much_wed_miss_him_til_he_was/ 以及 https://www.reddit.com/r/PTCGP/comments/1y1i9ao/what_cards_do_you_think_people_are_sleeping_on/ 。

注意：这些物种没有在当次确认的[物种目录 All/Name 两页](https://www.pokemontcgpocket.app/en/deck/pokemon?sort=name)中出现（第一页40个，第二页Vespiquen，总41个）。其中一些已经有独立 **Deck 详情页**，不等于拥有按物种聚合的物种目录页；生成新物种页时必须区别于现有详情页，避免重复SEO内容。

## 证据审计与下游 Agent 说明

- [evidence/2026-11-22-1242-web-audit.json](./evidence/2026-11-22-1242-web-audit.json)：本轮网页直读的 34 个真实链接、作者、物种归类、父帖子ID与 **时间未核实** 标志。
- [evidence/reddit-public-raw-2026-11-22T044528Z.json](./evidence/reddit-public-raw-2026-11-22T044528Z.json)：GitHub Actions Reddit API 403 拒绝日志。
- [latest.json](./latest.json)：主榜 candidates=[]，仅 watchlist=5，audit.coverage_met=false。其他 Agent **不得**据此自动发布5个物种SEO页面。
- [history/2026-11-22-1242.json](./history/2026-11-22-1242.json)：本次历史快照。

**阻碍不是“检索完成但恰好没有100篇”，而是可验证的 Reddit 原始元数据获取受限。** 要稳定达到100条有精确作者与发布时间的信源，需要合规的 Reddit API OAuth 访问或授权数据服务；不能尝试绕过403或把相对时间硬当绝对时间。