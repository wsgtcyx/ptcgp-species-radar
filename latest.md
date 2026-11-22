# PTCG Pocket 缺页物种 Deck 雷达｜Iteration 2/5

**采集截止** 2026-11-22T15:42:16+08:00（北京时间），固定72h：2026-11-19T15:42:16+08:00 至 2026-11-22T15:42:16+08:00；报告生成 2026-11-22T15:48:51+08:00。

**严格合格信源 3/100，实际直读且取得正文的原始记录 20，独立有效讨论 3，可核平台作者账号 2，正式候选 0/5，待核 4。** 100源缺97，正式候选缺5。quality_gate=failed；source_diversity_insufficient=true。没有同口径历史基线，不宣称上涨。

## 本轮严格合格原创来源（逐条）

1. **PocketMads / badgerbreath — Malamar（乌贼王）＋Meowstic＋Mega Mewtwo X ex**：发于北京时间 **2026-11-21 05:41:23.978794**，HTML 原始 `time datetime=2026-11-20T21:41:23.978794+00:00`，作者独立策略说明及20张牌表可读。通过干扰、退场与低能耗 Malamar 攻击，再转 Mega Mewtwo X ex，意图 C（完整牌表+策略）。[玩家原帖](https://app.pocketmads.com/feed/c0575dfc-71e3-41bb-89f4-14eefdc0bc7e)。
2. **Bluesky / fictionlife06 — Alolan Exeggutor（阿罗拉椰蛋树）＋Mega Venusaur**：北京时间 **2026-11-22 03:20:46.184**，官方 first-party `getAuthorFeed` 记录 `createdAt=2026-11-21T19:20:46.184Z`。玩家把另一位创作者的清单稍作修改，实际打了42局（18胜24败），说明前置能量加速、Mega Venusaur 必要性及 Umbreon 的克制。原创是玩家修改及实际比赛解释，非宣称原始牌表原创；意图 C。[原始帖子](https://bsky.app/profile/fictionlife06.bsky.social/post/3n2tt2z6glc2f)。
3. **Bluesky / fictionlife06 — Lycanroc＋Paldean Clodsire（帕底亚土王）**：北京时间 **2026-11-22 03:15:44.231**，官方 first-party `getAuthorFeed` 记录 `createdAt=2026-11-21T19:15:44.231Z`。作者复制视频构筑但亲自打17场（9胜8败），列出对局双方的牌组及胜负，原创部分为实际实战经验；意图 C。[原始帖子](https://bsky.app/profile/fictionlife06.bsky.social/post/3n2tsrz7jms2f)。

分平台严格合格：**Bluesky 2、PocketMads 1、Reddit 0、YouTube 0、X 0**。时间分布0–24h为2、24–48h为1、48–72h为0。两个Bluesky帖子来自同一作者，**不是2个独立作者**。

## 新建观察对象（非合格开发候选）

- **Malamar / 乌贼王 / カラマネロ**：一位作者、一张完整20卡牌表、一条讨论；目录42物种未收录。适合进一步核验混乱控制与单能耗输出是否能提供超越Mewtwo页的独立内容。A/B档资格不足。
- **Alolan Exeggutor / 阿罗拉椰蛋树 / アローラナッシー**：一位作者、一条42战体验；目录缺页，但配套 Mega Venusaur 已在站内，缺独立主轴和卡号证据。
- **Paldean Clodsire / 帕底亚土王 / ドオー**：一位作者、一条17战测试；与 Lycanroc 共轴，不能将同一条体验拆成两个成熟建页机会，主轴归属及具体卡号均待核。
- **Chandelure / 水晶灯火灵 / シャンデラ**：本轮直接读取一篇 Reddit 帖及两条分别有永久链接的构筑评论，涉及 Oricorio、Meloetta、Leaf、Red 等变体。页面只显示“11h/10h/9h ago”，来源标为“Crawled today”，无精确抓取时刻，因此按严格规则 **0条计入百源**。原帖 [Chandelure](https://www.reddit.com/r/PTCGP/comments/1y22t44/new_chandelure_deck/)；评论 [mnk907](https://www.reddit.com/r/PTCGP/comments/1y22t44/comment/19szfoqorwqhx/)、[myrtlebitch](https://www.reddit.com/r/PTCGP/comments/1y22t44/comment/19szgu601axi8/)。

## YouTube（日语路线）审计

从 [日语公开视频目录](https://etc64.com/pokepoke/pokepoke-movielist/) 发现近期不同创作者的视频线索。GitHub Actions 第一方获取八条视频 watch 地址均得到 HTTP 200，**实际仅返回标题“ - YouTube”的通用页面**，无可核原发作者、上传日期、描述、字幕或具体视频内容，**8条全不计数**。官方频道 RSS 获取 HTTP 200，但只有视频 ID、发布日期，不构成实质牌组内容验证。未用第三方目录标题冒充视频原文。

Bluesky 官方作者 Feed 四个账号均 HTTP 200，共读回**15条**在固定窗口内的原发帖记录，2条满足实质构筑，其他包含非 Pocket 游戏、无牌表的 Colorless Deck 或普通对局感想，不能凑数。PocketMads 公开 Feed 可读、日期准确，但本轮窗口内只有上述1条独立有效发布。Reddit 另有帖可能落在边界，时间无法严格判定，不计。X 无可用原创来源。

## 站内排除

站内 [All + Name 物种目录](https://pokemontcgpocket.app/en/deck/pokemon?sort=name) 已从 GitHub Actions 正常读取两页（第一页40、第二页2，末页明确Page 2 of 2），默认排序也是两页；**共42基础物种**。按名称排除 Mega/ex 不另算物种，已收录 Venusaur/Mewtwo 等基础物种排除，并额外排除 Rayquaza。观察4种不在本轮目录中；公开 sitemap 与单一Deck页是否重复仍需补检。

## 质量门槛与发布

`latest.json.candidates=[]`；`watchlist` 共4条观察，不可自动建页。缺少100条跨平台真实玩家原文和至少10个不同讨论簇，必须标记不合格。全量逐条证据 [evidence/2026-11-22-154216-iteration2.json](./evidence/2026-11-22-154216-iteration2.json)；本轮第一方访问底稿 [evidence/2026-11-22-154216-iteration2-live-probe.json](./evidence/2026-11-22-154216-iteration2-live-probe.json)；版本历史 [history/2026-11-22-154216-iteration2.json](./history/2026-11-22-154216-iteration2.json)。

公开报告 https://wsgtcyx.github.io/ptcgp-species-radar/ ，机器 JSON https://wsgtcyx.github.io/ptcgp-species-radar/latest.json 。是否部署和公网HTTP同步，见本轮实际 Actions 与回读验证，报告自身不会预先声明成功。
