# 实施与验收运行指南

本轮只存在研究/设计和只读盘点工具；下述bugu-director命令是待实现合同的验收调用，现阶段不可运行。
只有实际命令及证据生成后才能勾选对应实施任务。不要安装不存在的发行包或把示例命令当结果。

## 当前可运行的研究/Spec Kit检查

在仓库根PowerShell执行：

```powershell
.\.specify\scripts\powershell\check-prerequisites.ps1 -Json -RequireSpec -RequireTasks -IncludeTasks
.\.venv\Scripts\python.exe tools\research_inventory.py 'D:\bugu_data\ai漫剧\skills\Acheng 影视牛马skill（全自动全资产生成skill）\Acheng 影视牛马skill（全自动全资产生成skill）\acheng-director-suite-v4.3.9\skills' "$env:TEMP\bugu-reference-inventory.json"
```

输出应能找到当前feature全部设计文档；清单应有31入口，文件hash与研究快照一致才可复用其结论。
如果参考目录变化，建立新的证据/研究变更，不能覆盖旧快照冒充同一来源。

## 实施前置环境

- 固定Python/依赖锁/FFmpeg、ComfyUI正式release，director服务及可信Host bridge已实现并安装。
  多连接WAL还须核验实际SQLite为官方已修复稳定引擎（3.51.3+或官方3.50.7/3.44.6回移），
  当前开发Python3.12.13的SQLite3.50.4不作为合格生产数据库基线。
- 配置项目根、ComfyUI输入/输出根、数据本地FS、模型/provider及专属DSH profile，秘密运行时注入。
- 真实视觉调用验证；需要的image/video/TTS/ASR/sfx/music工作流逐个validated，权重/节点/图hash及许可齐全。
- 单GPU资源互斥、磁盘容量、服务鉴权和备份路径有效；不能把现有H3成功推广到所有能力。
- 当前DSH alpha仅预览试验；正式发布须等待独立稳定版迁移门通过。

首次能力验收先用管理身份创建`capability-trial`，按production合同冻结ValidationRun/Grant与实际测试范围。
run/status保存真实请求/媒体/技术和独立内容检查，accept只由可信独立签收人提交；
未验证图不能走业务start，试验样例不进入用户选片或交付，unknown不能签收。
此入口同样为待实现合同；本轮没有启动GPU生成或冒认样例通过。

## 主样片

用自有授权原创素材制作60–90秒、8–12镜头、2角色、2场景、至少2四宫格的竖屏样片，
有中文对话、道具交接、跨景、音效、整集配乐和字幕。先冻结创作标准和逐镜期望事件。
验收采用1080×1920/24fps、48kHz stereo，−16 LUFS±1、TP≤−1dBTP，音画/口型误差≤100ms。
原生生成与缩放分别记录；任一hard fail或必需质量unknown不能通过。

## 用户故事验收矩阵

| 范围 | 操作 | 必须实际观察/保存 |
| --- | --- | --- |
| US1输入 | 五路径真实成功+损坏/不可获取/缺视觉拒绝 | 原件/hash/来源、模型路由、抽帧/转写、解释及blocked |
| US2半自动 | 每个S01–S10等待；明确拒绝→修改→批准；模糊/空/超时/断连 | frozen review、官方回应、可信receipt、受影响批准失效；未批准推进次数0 |
| US2防伪 | AI发approved参数/调用shell、重放/跨项目/stale、媒体外改 | 权限拒绝与状态未推进；signer隔离；自有问答中断重启重新展示同hash |
| US3全自动 | 首选auto后断开浏览器，自主生产/审核/返修 | 不逐步询问，无默认额度；真实产物/QC/停滞或blocked原因 |
| US4复用 | 约30秒续集，合法换装或道具状态；返修一镜 | 同脸同声/场景实际观察，无关通过产物hash不变 |
| US5交付 | 导出全部版本/分轨/字幕/清单，并按timeline重建 | 完整解码/听检、镜序/台词无漏、播放/Range/下载/重启有效 |
| US6镜像 | 空卷、旧卷、重启、备份恢复、升级/回滚 | 同一image digest、skill发现/正文hash/overlay来源、无数据覆盖、无秘密 |
| 正式发布 | 故意使用alpha及真正稳定基线分别判门 | alpha必须formal=false；稳定且所有业务门通过才formal=true |

## 故障验收

1. 实际提交后丢响应：fence先已持久，只读对账，POST不得重复。
2. worker被终止、lease过期：接管本地状态，但prepared与已发网络请求分别处理。
3. ComfyUI重启导致queue/history为空：任务保持未知，不猜失败/未运行。
4. 输出已写DB失败：重启manifest对账恢复，不因文件存在而永久失败。
5. 审核问答中断：director保存await_review，Host重展同digest；新revision拒绝旧receipt。
6. 磁盘不足、取消晚到、资源冲突：有真实错误/取消状态，晚到产物不进final，不interrupt他人。
7. 故障协议桩与真实GPU/镜像故障结果分开；不能将mock输出算作生产成功。

## 工程/进度与性能检查

执行已实现的测试、lint/类型、依赖/hash/license检查及独立Spec Kit analyze/converge。
T087测量前在`evidence/acceptance/control-scale-profile.json`冻结实际CPU/内存/OS、磁盘/FS/挂载、
SQLite/runtime/image身份、20项目×1000资产控制记录、授权真实媒体清单、去重与逻辑/物理字节数。
控制记录可重复引用授权媒体；合成索引明确标benchmark，不声称20,000项独立真实生成。
数据清单与备份必须包含该profile全部真实媒体，metadata-only恢复另报，不能通过完整恢复门。
冻结后再计时，不能根据结果缩小数据集；报告通过范围及实际总字节，不外推任意TB级恢复。

查询使用20个并发客户端按项目轮询status/review，分别记录cold首轮，预热60秒后持续采样10分钟，
保存全部请求/失败/原始时长；两类查询各自p95≤2秒，失败不能删除后再算通过。
可对账恢复从监督服务启动到所有可对账任务重新呈现为≤60秒，未知任务列出并继续unknown。
完整恢复从空目标目录受理restore到全部DB关系、媒体hash核对完成且服务可用为≤10分钟，
包括实际复制/读取/解码所需校验；冻结源、目标磁盘及备份总字节和原始计时。
项目事实完成前不勾产品任务，新增失败归入变更及实际未完成tasks。

## 证据与发行

每个验收记录execution_host/date、source/image/dependency版本、workflow/model/skill hashes、
输入、真实操作、输出、媒体完整探测/解码、逐镜观察、审批/修复/恢复事件和结论。
发行时交付同一已验收镜像，不重建同标签；许可证/SBOM/锁及项目数据排除检查通过。
最后正常推送工作分支及main，用远端查询证明一致。凭据不入命令、源码或日志。
