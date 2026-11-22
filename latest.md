# PTCGP Reddit 百源新物种 Deck SEO 选题雷达｜2026-11-22 15:04 运行（未通过门槛）

**本轮 run_id**：`2026-11-22-150407-BJT`。采集开始 / cutoff：**2026-11-22T15:04:07+08:00**。严格窗口：**2026-11-19T15:04:07+08:00 — 2026-11-22T15:04:07+08:00**。报告生成于 2026-11-22T15:06:48+08:00。

## 最重要结论

- **严格合格 Reddit 构筑来源：0/100，差额 100。** 源数据不存在完整的作者、原发时间和直读正文核验，因此失败不等于 Reddit 没有相关讨论。
- 直接读取原帖/评论尝试 4 条（2 原帖、2 独立评论），**原始记录成功 0**，全部返回 `Cache miss`，HTTP状态未暴露。Reddit 新帖列表只返回3个月前的旧缓存，JSON访问也失败。
- **合格建页候选：0/5，缺5；待核观察：1。** 站内全分页直接验收失败，不能宣称任何物种确定缺页。
- 父讨论串严格已核 0，独立作者严格已核 0；这不是两版区讨论数的真实零值，而是本轮严格核验结果。

## 观察线索（不是合格选题）

1. **Chandelure（水晶灯火灵 / シャンデラ）**，具体卡号与版本**未核**。搜索结果显示 2026-11-21 的 [New Chandelure deck](https://www.reddit.com/r/PTCGP/comments/1y22t44/new_chandelure_deck/)，作者在帖子正文摘要中介绍 Chandelure＋Oricorio、弃牌增伤、Copycat＋Hiking Trail 轮转。这是值得继续追查的**索引线索**，不是可计数的原始 Reddit 记录。原帖直读失败，作者和独立原发时间未核；本站也未完整排除，不能推荐自动建页。
2. [Peak deck build](https://www.reddit.com/r/PTCGPocketTrading/comments/1y1jdnd/peak_deck_build/) 为 2026-11-21 搜索索引线索，讨论存在实际卡槽和对局建议，但具体主轴物种无法从正文索引确认，且提到引用创作者构筑，因此**不进入任何物种候选**。

## 时间戳可用性小测

| 测试 | 对象 | 结果 | HTTP 状态 |
|---|---|---|---|
| 原帖1 | https://www.reddit.com/r/PTCGP/comments/1y22t44/new_chandelure_deck/ | Cache miss，无法核原帖作者和精确时间 | 未提供 |
| 原帖2 | https://www.reddit.com/r/PokemonPocket/comments/1y0sfrt/amy_good_builds_that_combo_with_this_card/ | Cache miss，无法核原帖作者和精确时间 | 未提供 |
| 评论1 | https://www.reddit.com/r/PTCGP/comments/1y22t44/comment/19szfoqorwqhx/ | Cache miss，无法独立核评论ID、作者、时间 | 未提供 |
| 评论2 | https://www.reddit.com/r/PokemonPocket/comments/1y0sfrt/comment/19swgf541jupx/ | Cache miss，无法独立核评论ID、作者、时间 | 未提供 |

查阅 [r/PTCGP/new](https://www.reddit.com/r/PTCGP/new/) 时仅取得三个月前的缓存页；[公开JSON](https://www.reddit.com/r/PTCGP/new.json?limit=5) 无法获取。使用本地标准 HTTP GET 的试探也仅获得网络连接异常（无 HTTP 状态），没有绕过授权或限制。

## 站内排除审核

[物种目录](https://pokemontcgpocket.app/en/deck/pokemon) 及 `?sort=name`、`?page=2` 的直接打开均无法完整回读。公开搜索索引虽显示 `Page 2 of 2`，并在该页列出 Bewear ex，但并不等价于已按 All+Name 实时逐页抓完。**直读完成页数：0；实际末页：NA；完整物种数量：NA；已确认缺页：0。** 额外排除 Rayquaza；但因未完整遍历，不给任何新物种明确的未收录断言。

## 本轮检索覆盖与失败

Reddit 社区目标：r/PTCGP、r/PokemonPocket、r/PokemonTCGP；补查 r/PTCGPocketTrading。覆盖的搜索语言：英文、日语、西语、葡语。英文示例：`site:reddit.com/r/PTCGP/comments/ deck 2026 Nov 21 Pokémon Pocket`、`site:reddit.com/r/PokemonPocket/comments/ deck 2026 Nov 20 21 22`；日语：`site:reddit.com "ポケポケ" "構築" "11月21日" 2026`；西语：`site:reddit.com "PTCG Pocket" "mazo" "noviembre" 2026`；葡语：`site:reddit.com "PTCGP" "baralho" "novembro" 2026`。完整代表性查询见 JSON 证据文件；不假装完成所有 new/rising/hot 分页。本轮本地收集的独立索引 Reddit 原帖 URL 5 条，其中 1 条于11月18日，超出窗口；1 条为实体 TCG Live；1 条为机器汇总；所有记录均因无法同时核原始时间/作者等而不计入严格100源。

无可信前72小时同口径基线，未计算增长率（NA）。任何来源都没有因为被搜索到就计入“100源”。

## 可审计文件与机器读取

- 本轮证据：[evidence/2026-11-22-150407.json](./evidence/2026-11-22-150407.json)
- 同日独立历史快照：[history/2026-11-22-150407.json](./history/2026-11-22-150407.json)
- 最新机器数据：[latest.json](./latest.json)
- 质量门禁：`audit.quality_gate=failed`，`reporting.strict_eligible_count=0`，`reporting.qualified_count=0`，`candidates=[]`。
- GitHub Pages 入口：https://wsgtcyx.github.io/ptcgp-species-radar/；JSON：https://wsgtcyx.github.io/ptcgp-species-radar/latest.json 。实际部署及公网回读要单独核查，不由报告文本自证。
