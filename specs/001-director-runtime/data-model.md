# 数据模型与不变量

2026-10-09；目标设计，表/迁移尚未实现。对应FR-001–FR-040及contracts。
数据库是控制状态唯一真值，创作正文与媒体使用不可变文件版本。业务对象以project_id隔离；
能力试验以ValidationRun隔离，不进入业务阶段与交付引用。

## 统一约束

- ID为运行库生成的规范UUID；用户标题不参与目录构造。
- revision为从1开始的正整数；写操作必须携带expected_revision并以CAS提交。
- digest为最终字节/规范结构的64位小写SHA-256；结构摘要使用UTF-8、键排序、无多余空白，序列顺序不变。
- 时间为带时区的UTC；用户界面按配置时区呈现。
- 相对路径resolve后必须仍在配置根内；禁止父级、绝对路径和符号链接/重解析点越界。
- 每个引用必须指定对象ID、版本及digest，禁止仅用“latest”。
- nullable费用代表unknown，0只代表明确测得0；未观察的质量不能标pass。
- 删除默认为版本退役，候选/失败/通过产物不自动物理删除；清理由独立授权策略处理。

## 实体

| 实体 | 关键字段 | 关系与规则 |
| --- | --- | --- |
| Project | id、title、owner、mode、mode_receipt、status、revision、quality_profile_ref | mode初始null；无模式receipt不得生产；每次切模式暂停/完成当前安全检查点，再绑定新授权 |
| Episode | id、project_id、sequence、stage_cursor、revision、brief_ref、script_ref | 同一项目sequence唯一；复用series资产必须显式绑定版本 |
| Source | id、original_name、kind、location、hash、bytes、origin、usage、rights_statement | 原件只读；usage为story/identity/style/action等；download URL不含日志凭据 |
| Observation | source_ref、tool/model/version、time_ranges、evidence_refs、findings、status | findings区分observed/inferred/unknown；真实图像/声音证据，缺能力为blocked |
| CreativeDocument | kind、version、file_ref、source_map、owner_module、dependency_refs | brief/script/style/spatial/storyboard等；owner限定写域；原著章节/原文对应不丢 |
| AssetIdentity | id、kind、identity_contract_ref、base_reference_refs、voice_ref | character/scene/prop；身份与合法状态变化分开 |
| AssetVersion | identity_id、version、variant_kind、state、media_refs、dependencies | base/outfit/lighting/injury/view/prop_state；approved版本不可覆盖 |
| VoiceIdentity | id、provider、model_ref、preset_voice_id、sample_ref、pronunciation_ref | 同角色默认固定声音；新声音必须新版本/重新验收 |
| Dialogue | id、speaker_ref、text、pronunciation、emotion、wav_ref、duration_ms、alignment_ref | 原文不静默改；实测时长>0才供镜头排期；转写核对结果单独保存 |
| Shot | id、order、purpose、duration、events、camera、performance、state_in/out、dialogue_refs | 镜头职责与合法状态；时长受实测台词/工作流范围约束 |
| Keyframe | id、shot_ref、temporal_position、media_ref、dependency_refs | 单帧原图独立保存，不能仅存拼图 |
| Grid | id、layout、organization、panels、image_ref | layout=2x2；panels恰好4项，索引1..4唯一；organization=four_shots/four_phases；每格shot/keyframe/time引用明确 |
| Capability | id、version、type、workflow_ref、binding_schema、node/model_refs、hardware、license、acceptance_ref、status | status=unverified/validated/revoked；只有validated可业务生产；任何依赖变更撤销验收 |
| ValidationRun/TrialGrant | run_id、capability_snapshot、purpose、test_cases、inputs/expected_refs、grant_digest、actor、expiry、status、evidence/acceptance_refs | 管理签发隔离试验；状态created/authorized/running/evidence_ready/assessing/passed/failed/unknown；真实独立签收才CAS启用能力，不借用业务阶段批准 |
| ProductionTask | id、purpose、owner_ref、project/episode/stage_refs、logical_key、capability_ref、input_digest、status、revision | purpose为production/validation；owner分别绑定Project或ValidationRun，两者互斥；同logical_key只有一个当前有效请求fence；被替代任务保留，不复用身份 |
| Attempt | id、task_id、number、prompt_uuid、request_hash、request_file、fence_epoch、submit_state、provider_status、artifact_refs | 请求先持久化；unknown不自动重发；新attempt须记录创建原因与旧风险 |
| Artifact | id、kind、file_ref、hash、bytes、probe、generation_state、technical_state、quality_state、approval_refs | generated/decoded/quality_pass/human_approved/delivered是独立字段；不存在实际文件不得generated |
| StageRun | id、stage、revision、input_digest、artifact_digest、dependency_snapshot、status、decision_ref | input/产物任何变化revision增加；旧通过/审核不可传递给新revision |
| ReviewPackage | id、stage_ref、summary_ref、manifest_ref、input_digest、artifact_digest、issues、status | 详细通俗报告、可播放媒体和文件定位；hash绑定的是整个规范manifest |
| Approval | id、project/stage/package_refs、revision、digests、actor、decision、receipt、created_at、invalidated_at | actor=human/auto_quality；半自动必须human且签发方可信；decision=approve/revise/stop；不可重放/跨项目 |
| QualityCheck | id、artifact_ref、profile_ref、check_kind、tool/model_ref、observations、hard_failures、soft_scores、evidence_refs、verdict | verdict=pass/fail/unknown/not_applicable；unknown不能满足必需门；软分不能抵消硬失败 |
| Repair | id、failure_refs、hypothesis、preserve_refs、change_scope、affected_closure、before/after_refs、comparison_ref | 三轮distinct hypothesis无改善+硬失败→stalled；不是全局次数上限 |
| Timeline | id、version、tracks、clips、in/out、dialogue/sfx/music/subtitle_refs、export_profile | 时间基用有理数/整数ticks，禁止浮点累计漂移；所有clip引用固定媒体版本 |
| Delivery | id、version、timeline_ref、outputs、selected_refs、candidate_index、quality/approval_refs、release_manifest | 全部候选有状态/hash；有/无字幕、分轨/字幕、重建材料齐全才可delivered |
| Command/Event/Outbox | command_id、actor、expected_revision、payload_hash；event sequence；outbox state | 同command_id同payload返回原结果，异payload冲突；事务同时写状态/事件/outbox |
| Lease | worker_id、resource、epoch、expiry、heartbeat | 过期可收回本地工作；不会解除已经持久化的外部请求fence |
| ReleaseBaseline | version、source_commit、skill/wheel hashes、dependency_lock、SBOM、status、acceptance_refs | stable_dependencies且真实全部门通过才正式；当前preview/release_blocked |

## 状态转换

Project：mode_required→ready→running；可转await_review/paused/blocked/stalled/cancelling；
cancelled终止当前run；delivered表示特定交付版本通过，用户修订创建新run而非覆盖历史。

Stage：not_ready→ready→running→artifact_ready→checking；
检查通过后auto模式为auto_accepted，semi模式为await_review→human_accepted；
失败→repairing→新revision；任何依赖改变→invalidated；unknown/能力缺失→blocked。
S10先通过最终检查及模式审批，再执行原子交付登记，失败保持export_pending可恢复。

Task：queued→claimed→prepared→submitting→submitted→running→outputs_pending→checking→complete；
submitting响应丢失→submission_unknown→reconciling；明确已提交可接submitted/running，
无法判定→blocked_unknown，不能转queued；明确未发出才能安全重试。
业务失败→failed；取消→cancel_requested→cancelled或cancel_unconfirmed，晚到文件为cancelled候选。

## 依赖图及变更

source→brief/script→style→identity/voice/scene→dialogue/shots→keyframes/grid→video→QC→timeline→delivery。
实际依赖以显式边为准，允许复用已通过支路；拒绝循环及跨项目隐式引用。
变更计算受影响闭包，事务登记invalidated；通过文件保持原字节。
批准绑定stage revision+input digest+artifact manifest digest，在该事务同时失效。
角色换装不重建身份基准，但引用该造型的关键帧/视频需重建；对白变化影响声音/时长/对应镜头及剪辑。

## 事务、文件及备份

SQLite本地FS、外键、FULL同步、短事务和busy处理；schema版本及升级独立迁移。
多连接WAL须官方稳定已修复WAL-reset的SQLite（3.51.3+或官方3.50.7/3.44.6修复分支），
启动不满足则拒绝进入生产；不能只凭Python版本推定SQLite安全。
DB提交与文件rename不是跨资源原子事务，采用attempt manifest/outbox和恢复扫描；
孤儿文件按task/request hash重接或登记unclaimed，不猜测完成状态。
一致性备份保存数据库快照、不可变引用文件、版本/配置非秘密摘要及核验清单；
恢复先校验hash/关系/未知任务，再启动调度，恢复不能清除未知外部请求fence。
