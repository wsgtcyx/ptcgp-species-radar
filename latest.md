# PTCG Pocket 新物种 Deck 雷达：2026-11-22 深度复核（未达百源门槛）

**研究时间**：2026-11-19T10:21:07+08:00 — 2026-11-22T10:21:07+08:00（北京时间，过去72小时）。GitHub Pages 链接：https://wsgtcyx.github.io/ptcgp-species-radar/

## 结论与质量门禁

**百源质量门禁未通过。** 本轮实际复核了 31 条独立可打开的 Reddit 原帖/评论 permalink（其中独立顶层讨论只有 3 条、评论链接 28 条），明确来自不同讨论的多作者证据不足。已核实 X 原帖 **0 条**，但不能据此认为 X 没有相关讨论。Reddit 评论的精确发帖时分也未能获取：`exact_datetime_verified_72h_sources=0`。因此这份报告是**探索性初筛，不是100条高质量72h证据覆盖的完整研究**。

不能用 31 个评论／帖 URL 冒充 31 个独立讨论串：父讨论只有 3 条，且混有未形成独立物种主轴的讨论。更不能将热度上升当作已核实。

## 暂定研究目标（5个，不等于5个已证实升温的页面）

1. **Aegislash（坚盾剑怪）** — Cursed Metal 的 +30增益，Togedemaru、Mega Skarmory、Dialga ex、Melmetal、Gholdengo ex。不同作者提供多个具体搭档/卡槽建议，但集中于同一讨论串：[Reddit Aegislash 求搭档](https://www.reddit.com/r/PokemonPocket/comments/1y0sfrt/amy_good_builds_that_combo_with_this_card/)；建议优先研究其独立物种页的不同构筑路线，暂不能推断搜索热度上涨。
2. **Blastoise（水箭龟）** — C1普通版 Aqua Charge。多名作者分享限定赛 Blastoise 牌组、Squirtle 麻痹进化时机，有另一条讨论建议搭配 Lorelei 与 Lapras：[Reddit 事件讨论](https://www.reddit.com/r/PTCGP/comments/1y1dwkw/we_never_knew_how_much_wed_miss_him_til_he_was/) 和 [限定赛策略帖](https://www.reddit.com/r/PTCGP/comments/1y0rm9r/unpopular_opinion_i_like_the_limited_battles/)。不同主贴中有实质讨论，但未验证重复作者的同口径趋势。
3. **Pidgeot（大比鸟）** — C1普通版与 Zoroark 或 Umbreon 组合、Blue's Provocation 调换前排：[Reddit 讨论](https://www.reddit.com/r/PTCGP/comments/1y1dwkw/we_never_knew_how_much_wed_miss_him_til_he_was/)；同一父讨论中两个独立作者，不能表述成多帖扩散。
4. **Dialga ex（帝牙卢卡）** — A2-119 Metallic Turbo，与 Aegislash 的 Cursed Metal、Dawn 能量支援共同成套：[Reddit 配合讨论](https://www.reddit.com/r/PokemonPocket/comments/1y0sfrt/amy_good_builds_that_combo_with_this_card/)；与Aegislash共用同一父帖，且主轴归属有争议，须单独验证搜索意图与页面区分度。
5. **Zoroark（索罗亚克）** — C1普通版 Foul Play，与 Pidgeot／Blue's Provocation 搭档。当前只有单一独立作者可核，[相关 Reddit 讨论](https://www.reddit.com/r/PTCGP/comments/1y1dwkw/we_never_knew_how_much_wed_miss_him_til_he_was/)；低信心研究线索，不宜自动生成独立 SEO 页。

**合格的“多源交叉验证正在升温”物种数：0/5。** 上述五项为未通过总体百源覆盖门槛的研究备选；其他 Agent 不得把 `candidates` 的这五项当作已经验证可直接开发的任务。

## 站内排除与信源覆盖

访问 https://www.pokemontcgpocket.app/en/deck/pokemon?sort=name ，逐页核查 name/all：**第一页40个，第二页只有 Vespiquen，合计41个物种**，还检查其他排序视图。以上5种均未在可见物种目录中，但可能有已存在的独立牌组详情页，应避免 SEO 内容互相重复。

不同原帖数量远低于100的主要原因是 Reddit 搜索索引更新不稳定、多语种检索中旧帖混入，以及 X 原站访问受限。已排除过期帖子、实体纸牌、机器人与无构筑意图的纯提及；对于评论时间只见相对“1d/2d”时，不捏造精确日期时分。

### 可审计证据清单

- [evidence/2026-11-22-deep-audit.json](./evidence/2026-11-22-deep-audit.json) — 每条真实查看过的 permalink、作者、父帖子、是否有构筑意图及时间精度。
- [latest.json](./latest.json) — Agent 稳定入口；明确 `audit.coverage_met=false`、三条父帖子以及五个暂定研究目标。
- [history/2026-11-22-deep-audit.json](./history/2026-11-22-deep-audit.json) — 本次不可混同的历史快照。

**发布校验**：以 GitHub 实际提交与 Pages 最新 Actions 为准；不能访问公共网站时仅能声明 GitHub 仓库回读成功或 Pages Actions 成功，不能声称已验证公开HTTP实时返回。

**下一步**：如希望真正稳定执行100源/次，需接入可访问完整发帖时间的 Reddit 数据采集、可靠的X公共搜索或授权数据源；如果证据不足，应保持低信心，不为凑五个创建薄内容页。