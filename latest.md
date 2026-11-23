# PTCG Pocket 新物种 Deck SEO 选题雷达 · 2026-11-23

**合格信源 1/100｜实际打开 9｜独立讨论 1｜合格候选 0/5。**

- 冻结北京时间：2026-11-20T09:59:17+08:00 至 2026-11-23T09:59:17+08:00（72小时）。
- **quality_gate=failed / coverage_met=false / shortfall=99。** 正式建页缺口 5。独立父帖只有 1，source_diversity_insufficient=true；不能推断热门物种、增长率或全面热度。
- 严格合格平台：note.com 1；Bluesky 0；YouTube 0；PocketMads 0；Reddit 0；X 0。0–24h / 24–48h / 48–72h = **0 / 0 / 1**。合格作者 1，父讨论簇 1；发现索引不计入100。
- 共尝试逐条核验14条不同原帖/原视频URL；9条可直接打开原始页面，严格通过1条。发现总量未按独立原文可靠去重，填null，不拿搜索结果数冒充有效数。

## 本轮唯一严格合格原文

[ゆーまっくす，2026-11-20 23:51 北京时间](https://note.com/bambee_san/n/n6e5b19644fb8)：玩家原发自述 Rabbit Jump/玛力露丽实战，并复盘雷伊布（Jolteon）＋雷电兽（Manectric）构筑：妨碍与换位灵活，但雷电兽打点不够、雷伊布易被击倒，因此减少使用；另提仙子伊布抽牌辅助。未实际测试的皮卡丘及阿罗拉雷丘ex搭配**没有计为实战**。原页显示 2026-11-21 00:51 JST，精确到分钟；对应北京时间 2026-11-20 23:51，分钟区间全部处于本轮窗口内。本文属上轮链接**本轮重读复核**，非本轮新发现。

## 两个观察对象；都不是可执行建页推荐

1. **雷伊布 Jolteon / サンダース：B档有限证据。** 1作者/1父帖/0构筑评论，48–72小时1条；与雷电兽组合主要是实战优缺点反馈，未确认准确卡号或其为构筑主轴。本站名称目录未列出雷伊布但雷电兽已经有物种页；独立hub路径与sitemap不能核实，**只判待核**。最需要第二位作者、第二个父帖的当期实战牌表，核实卡形态、既有详情与独立SEO价值。
2. **乌贼王 Malamar / カラマネロ：C档时间待核。** [badgerbreath 的PocketMads原牌表](https://app.pocketmads.com/feed/c0575dfc-71e3-41bb-89f4-14eefdc0bc7e)可直读 Meowstic／Mega Mewtwo X 搭配与20张卡，但仅显示 Nov20 的发布日期及编辑标记，不能确定首发时刻是否落在本轮冻结时间窗内，**不计100**。本站已经有 [Malamar B3＋Mega Sableye ex策略归档](https://www.pokemontcgpocket.app/en/deck/malamar-b3-mega-sableye-ex-b3b)；应先验证时间、确切卡号、第二作者及变体价值，不能把已有归档当成hub。

## 跨平台原文取证与失效路径

- **note.com：** 4篇第一方原创直读，3篇时间落窗，其中上文1篇可计；另外一篇[全画卡组日记](https://note.com/bambee_san/n/n4fca267747db)只有美术收藏叙述，一篇[假想旧卡包分析](https://note.com/4_4_6/n/na30efb0e4f5c)是AI辅助理论构思，均不计；[阿罗拉椰蛋树／叶伊布原帖](https://note.com/azarashoshi/n/nc4a781011bfd)首发时间早于窗口2小时48分，排除。
- **Bluesky：** 尝试3条原帖及官方公开getPostThread路线，本轮原文无法读回，0合格；不复用昨日6条。
- **YouTube：** 2个视频watch及官方频道RSS路线失败，0合格；目录与仅标题不计。
- **PocketMads：** 公开feed扫描20项，直读1页，有牌表但只有日级首发日期，0合格。
- **Reddit：** 检查3个社区new及4条原帖，页面只给出旧缓存/16–17天前原帖；搜索受限，0合格。
- **X：** 公开搜索页面受限，未能直读原帖，0合格。不突破403/429/登录墙。

## 本站42物种完整分页审计

成功遍历 [Popular/All P1](https://www.pokemontcgpocket.app/en/deck/pokemon)、[P2末页](https://www.pokemontcgpocket.app/en/deck/pokemon?page=2)、[Name P1](https://www.pokemontcgpocket.app/en/deck/pokemon?sort=name)、[P2末页](https://www.pokemontcgpocket.app/en/deck/pokemon?page=2&sort=name)。每排序2页，共42个基础物种目录入口，失败页0；已有玛力露丽、雷电兽、皮卡丘等物种入口直接排除。独立hub路径和sitemap不可读，任何未列目录的物种均不能标“确认缺页”。另外现有 [帕底亚土王策略](https://www.pokemontcgpocket.app/en/deck/paldean-clodsire-c1) 和 [阿罗拉椰蛋树ex＋叶伊布ex](https://www.pokemontcgpocket.app/en/deck/alolan-exeggutor-ex-c1-leafeon-ex-a2a) 属于防止重复建页的站内旁证，不能算新社媒信源。

## 审计与发布

四份独立平台manifest及结构化合并证据保存到 `evidence/`；本地运行仓库 `pipeline/merge_evidence.py` 对冻结窗、平台域、原文ID、去重汇总，结果 **accepted=1/rejected=0**。新一轮不是上轮累计；全部计数从唯一严格合格明细生成，其他13条逐条保留排除原因。

- [本轮证据](https://github.com/wsgtcyx/ptcgp-species-radar/blob/main/evidence/2026-11-23-095917-daily.json) · [同轮历史](https://github.com/wsgtcyx/ptcgp-species-radar/blob/main/history/2026-11-23-095917-daily.json) · [latest.json](https://github.com/wsgtcyx/ptcgp-species-radar/blob/main/latest.json)
- [GitHub Pages 最新JSON](https://wsgtcyx.github.io/ptcgp-species-radar/latest.json) · [首页](https://wsgtcyx.github.io/ptcgp-species-radar/)。提交时 publication=**pending_deploy_verification**；仓库回读、Actions部署与独立公网HTTP检验结果以本轮聊天执行记录为准，不能把仅提交说成公网可用。
