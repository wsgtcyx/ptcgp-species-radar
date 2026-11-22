# PTCGP Pocket 缺页物种 Deck 雷达｜2026-11-22 15:17 跨平台运行

**run_id：** `2026-11-22-151703-BJT-multiplatform`。北京时间 **cutoff=2026-11-22T15:17:03+08:00**；严格窗口 **2026-11-19T15:17:03+08:00 — 2026-11-22T15:17:03+08:00**。报告生成于 **2026-11-22T15:21:56+08:00**。

## 核心结论：11/100，未达标

- **严格合格原文 11/100，缺 89**，质量门 `failed`、`coverage_met=false`；**已打开并列入逐 URL 审计的原帖/评论 16 条**，实际严核跨平台原创资料为 Reddit 帖子1、独立评论10。
- **有效顶层讨论簇 2，可核独立作者 11**。一条是 Chandelure 具体组牌帖，另一条是主帖以活动吐槽为主但包含 8 条有实质构筑内容的独立评论；**讨论簇集中，source_diversity_insufficient=true**。
- 分平台严格合格数：Reddit **11**；X **0**，YouTube **0**，Bluesky **0**。其余平台为无法核验原始元数据，不代表没有讨论。只有 Reddit 原文直读链路局部可用；另外三平台本轮未获得可用于计数的原文。
- **合格可建页候选 0/5，差 5；待核观察物种 5**。100 源没过门禁，本轮 `candidates=[]`，不能向下游 Agent 触发建页。
- 时间精度：Reddit 仅见 `11h/10h/9h/1d ago` 与原页面本日爬取标签。逐条保留保守的发帖时间上下界，全部两端都落在固定窗口；**没有伪造 created_utc、卡号或精确发布时间**。1d 记录不能强行划入唯一 24h 段；原时间窗分布记录在证据 JSON。
- 独立证据资产：[evidence/2026-11-22-151703-multiplatform.json](./evidence/2026-11-22-151703-multiplatform.json)，历史快照：[history/2026-11-22-151703-multiplatform.json](./history/2026-11-22-151703-multiplatform.json)。

## 待核观察名单（不能当成五个通过百源门的候选）

1. **Chandelure（水晶灯火灵/シャンデラ）**：3 条严格有效、3 作者、1 讨论簇。Oricorio 弃牌增伤、Meloetta 变体、Copycat/Hiking Trail、Cape/Leaf vs X Speed。主轴潜力清晰，但缺少第二个独立讨论簇和其他平台可核作者。原帖 https://www.reddit.com/r/PTCGP/comments/1y22t44/new_chandelure_deck/ （本页显示 11h ago；官方绝对原发时间未获取）；评论 https://www.reddit.com/r/PTCGP/comments/1y22t44/comment/19szfoqorwqhx/ 与 https://www.reddit.com/r/PTCGP/comments/1y22t44/comment/19szgu601axi8/ 。
2. **Pidgeot（大比鸟/ピジョット）**：2 条有效、2 作者、1 讨论簇。与 Zoroark、Umbreon 配 Blue's Provocation 的切换/复制攻击路线。评论 https://www.reddit.com/r/PTCGP/comments/1y1dwkw/comment/19sxtl6ij8g0x/ 和 https://www.reddit.com/r/PTCGP/comments/1y1dwkw/comment/19sxtx3fltb1e/ 。已有不同搭档，但仍集中单帖、卡号未核。
3. **Blastoise（水箭龟/カメックス）**：2 条有效、2 作者、1 讨论簇。Squirtle 麻痹的进化时机、Blue's Provocation / Lapras 的牌组协作。 https://www.reddit.com/r/PTCGP/comments/1y1dwkw/comment/19sxtn25u8o4g/ 和 https://www.reddit.com/r/PTCGP/comments/1y1dwkw/comment/19sxwei7qrm04/ 。
4. **Zoroark（索罗亚克/ゾロアーク）**：1 条有效、1 作者、1 讨论簇。与 Pidgeot 同源共轴，Foul Play 复制对手攻击用途，有页间重叠风险。 https://www.reddit.com/r/PTCGP/comments/1y1dwkw/comment/19sxtl6ij8g0x/ 。
5. **Aegislash（坚盾剑怪/ギルガルド）**：当前严格有效 0；旧讨论原帖与6条独立评论在本轮打开，显示 `2d ago`，无法将每条记录的保守时间范围完整限制在本窗口，**严守时效不能计数**。原帖 https://www.reddit.com/r/PokemonPocket/comments/1y0sfrt/amy_good_builds_that_combo_with_this_card/ 。作为下一轮重新获取可靠时间的观察线索。

上述 5 个基础物种都不在本轮完整遍历的目录 41 种之列；但仍应在开发前检查现有单 Deck 详情/内容重叠。**不能宣称“正在升温”**，因为缺同口径可比历史基线。

## 站内排除与采集边界

网站 https://pokemontcgpocket.app/en/deck/pokemon 的 **All + Name** 直接检查 Page 1 of 2（40 个）和 Page 2 of 2（Vespiquen 1 个），共 **41 个基础物种**；其他排序检查过列表顺序但未做全量重新遍历。Mega/ex/普通形态归为基础物种；Rayquaza 额外排除。已有目录物种（包括 Venusaur、Vespiquen、Fuecoco、Charizard、Umbreon、Pikachu、Dragonite、Mew 等）全部不能列入新建主榜。

发现流程查询涵盖英语、日语、西语、葡语，范围为 Reddit r/PTCGP / r/PokemonPocket / r/PokemonTCGP 及附属社区、X、YouTube、Bluesky 公开搜索。先不带历史物种名进行新发现，再反查 Chandelure / Pidgeot / Zoroark 等。访问障碍：Reddit `/new` 与公开 JSON 缓存不稳定；X 原帖无法独立核作者与时间；YouTube 2 条视频无法查看内容/字幕；Bluesky 公共作者 feed 未成功直读。索引和简介不计源，不制造增长率。

**可核验原始来源清单及逐条排除/时间区间：** [evidence/2026-11-22-151703-multiplatform.json](./evidence/2026-11-22-151703-multiplatform.json)，含每条真实原始 Reddit permalink、作者、内容要点、时间界限、父帖及平台分布。已确认有效评论涉及 1 条一般活动讨论父帖；不将该父帖冒充一篇原创牌表主帖。

## GitHub 发布状态

提交文件时 `publication.status=pending`，不在文件内自证最终部署状态。GitHub 源码回读、Pages 目标提交部署与 Pages JSON/首页实时 HTTP 可达性将在提交之后独立核查。仓库 https://github.com/wsgtcyx/ptcgp-species-radar ，网页 https://wsgtcyx.github.io/ptcgp-species-radar/ ，JSON https://wsgtcyx.github.io/ptcgp-species-radar/latest.json ，Raw https://raw.githubusercontent.com/wsgtcyx/ptcgp-species-radar/main/latest.json 。
