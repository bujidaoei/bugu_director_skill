# 研究决策与取舍

2026-10-09；完整研究见 [来源/会话](research/source-context.md)、[核心套件](research/core-suite.md)、
[其余8套件](research/supporting-suites.md)、[上游集成](research/upstream-integration.md)。
全文件SHA清单与离线探针位于evidence；本文件只总结决策，不冒充生产验收。

## R01：从提示词系统发展为真实制作系统

**Decision**：技能入口+创作规则+持久运行库+DSH Host控制四层，首版实现ComfyUI，不建空供应商。
**Rationale**：主参考明确不自动生图，execute未实现；用户需要声音/剪辑/最终成片及无人值守恢复。
**Alternatives considered**：整包改名无法新增能力；单个长SKILL不能承担耐久队列；大型分布式平台不符合首版单GPU规模。

## R02：借鉴架构，代码逐项准入

**Decision**：保留事实/状态分离、owner边界、引用图、独立编译、版本归档和局部影响思路；关键运行链路自研。
**Rationale**：参考89+5测试通过，但整包验收失败，另复现路径越界、hash错误、并发/崩溃恢复缺口和时长合同冲突。
**Alternatives considered**：照搬原调度器会带入不可恢复与阶段门缺失；把字数门作为质量标准没有生产证据。

## R03：商业复用按文件

**Decision**：原创创作表达独立编写；Apache/MIT纯实现可候选复用，保留来源/许可/修改，混入文本先分离；许可未知不分发。
**Rationale**：LICENSE-SCOPE区分工具代码与CC BY-NC-ND创作文本；后者不能据用户“照搬”获得权利。
**Alternatives considered**：只看根LICENSE/扩展名会漏嵌入提示词与案例；近义改写受限正文仍不是独立规则实现。
官方说明见[CC条款](https://creativecommons.org/licenses/by-nc-nd/4.0/)。

## R04：十阶段及两种授权

**Decision**：扩展用户六步为十阶段，补上接入、视觉基准、声音、剪辑、终审/交付；semi全部阶段待审。
**Rationale**：原六步缺声音与成片，也没有风格基准/实际素材理解。附件既定范围保留。
**Alternatives considered**：只在视频提示词后暂停不满足用户；全自动每次生产再询问违背已选择模式。

## R05：可信批准而非模型字符串

**Decision**：Host handler经官方ctx.userQuestions.ask取得明确回应，隔离角色签发绑定hash/revision/nonce的receipt。
**Rationale**：制作AI可写“approved=true”不构成人类同意；同UID完整shell无法靠0600保护审批密钥。
**Alternatives considered**：shell approve自由参数、解释模糊聊天为通过、超时自动继续均不满足需求。
问答投影恢复不是任意自有工具的自动能力，director自己持久pending review，重启重新显示固定包。

## R06：全自动官方配置与真实边界

**Decision**：专属项目profile使用danger-full-access；无需每阶段用户问答，质量审查独立任务。无默认额度。
**Rationale**：用户选择自主制作；官方approval=never仍拒绝需要额外审批的工具，缺能力不是“自动批准”能解决。
**Alternatives considered**：不存在approve(all)；全系统/root权限与半自动批准强防伪不能同时无条件承诺。
费用可知部分如实记录，user可选预算；三轮不同假设无改善且硬失败检测停滞，不是全局返修额度。

## R07：SQLite事务、不可变文件与恢复账本

**Decision**：本地FS SQLite/CAS/outbox/lease/request fence，媒体独立hash存储，备份用一致性API。
**Rationale**：参考JSON原子覆盖仍会丢索引；DB+文件不能跨资源原子，manifest与恢复扫描处理孤儿。
**Alternatives considered**：纯聊天/内存jobs不耐重启；SQLite放网络盘不支持WAL约束；多机服务数据库暂超范围。
依据[SQLite WAL](https://www.sqlite.org/wal.html)、[Python SQLite事务/backup](https://docs.python.org/3.12/library/sqlite3.html)。
本轮实际开发环境为Python3.12.13/SQLite3.50.4；官方WAL文档记录WAL-reset并发损坏缺陷，
修复于3.51.3+、官方回移3.50.7/3.44.6。当前开发引擎不能据此放行生产多连接WAL。
实施T006固定官方已修复稳定引擎身份/校验，T009启动验证，镜像独立依赖迁移及并发/备份恢复验收。
不修改本机或现有ai_drama来冒充已完成升级。

## R08：提交未知不重发

**Decision**：先持久请求UUID/hash/fence，POST只发一次，不确定先对账；历史空不代表未执行。
**Rationale**：ComfyUI支持client UUID但每次POST仍入队，queue/history只在内存。不能宣称exactly-once。
**Alternatives considered**：HTTP通用自动重试可能重复耗GPU/费用；仅靠lease回收会重复提交；以文件名判断归属不充分。

## R09：四格是规划与输入策略

**Decision**：独立帧→2×2合成；AI选four_shots/four_phases，保存映射，视频按能力编译。
**Rationale**：模型输入约束不同，拼图可能留下网格或打乱镜序；主参考16格不是用户4格合同。
**Alternatives considered**：直接整四格通用生产无验收；只存拼图失去独立首/尾/参考帧，难局部返修。

## R10：声音先实测，质检看实际媒体

**Decision**：voice身份/发音→逐句TTS/ASR→实测时长→分镜；技术检查+语义证据+独立终审，hard fail阻塞。
**Rationale**：同脸还需要同声；对白长度不能猜；帧/音轨解码不代表剧情、口型与连续性合格。
**Alternatives considered**：仅embedding或总分无法处理合法变体；首帧检查不能代表全镜头；生成原音轨不能保证指定声线。

## R11：独立镜像集成与媒体展示

**Decision**：ai_drama独立feature/worktree，固定skill/wheel/bridge release，显式seed/profile迁移和自有toolview。
**Rationale**：当前clean profile不启用旧production插件；社区插件只为自身工具名渲染媒体。
**Alternatives considered**：隐藏复活旧插件/直接COPY并覆盖已有卷违背当前合同；Markdown链接不是播放验收。
媒体来自受保护filename/subfolder/type入口，验收鉴权、Range、下载及重启；不依赖volatile history。

## R12：预览开发与正式稳定迁移分开

**Decision**：当前研究兼容DSH0.2.1-alpha.1，正式发布受阻；稳定上游迁移独立任务，整个验收重新绑定制品。
**Rationale**：截至研究日npm全部30版本及GitHub发布页无正式稳定DSH；ComfyUI0.39.0为正式release。
**Alternatives considered**：latest dist-tag不是稳定证明，兼容豁免也不是稳定/认证；不追踪main或补丁伪装稳定。
依赖/模型/节点精确锁、许可和真正能力试验在实施完成，不能在研究稿生成虚构lock。

## R13：交付与本轮边界

**Decision**：完整有声成片、无字幕版本、字幕/声音分轨、候选索引、可重建时间线及规范目录为最终目标。
本轮只交研究设计，正常推送GitHub设计基线，后续生产/镜像/正式发行未完成。
**Rationale**：原会话实现多次中断，当前只有模板；附件不能替代实际代码/成片。
**Alternatives considered**：把提示词或规划任务勾完冒称可安装生产技能违反用户AGENTS。

## Capability experiments before production

必须先验证：实际视觉路由、角色参考/局部编辑、首帧/首尾/多参考/整四格分别支持程度、中文TTS/ASR、
声音身份、音效/配乐、口型、真实QC、ComfyUI未知提交恢复、Host问答/自有toolview及非覆盖卷迁移。
每个试验有固定工作流/模型/hash/许可/硬件/实际输出与pass/fail/unknown。
首次试验通过管理员授权的独立ValidationRun/Grant运行unverified快照，共用编译校验/持久fence和真实检查；
媒体只归试验，可信独立签收后才CAS启用能力。禁止先标validated再试或把试验输出当业务成果。
当前这些生产能力均未被本项目验收；缺项有blocked路径，不需要用假实现填满通用接口。
