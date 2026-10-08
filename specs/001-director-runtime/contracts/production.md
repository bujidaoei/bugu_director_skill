# 生产适配、工作流与媒体合同

首版实现ComfyUI；其他供应商不创建空实现。厂商语法与业务事实隔离。

| 操作 | 约束 | 返回事实 |
| --- | --- | --- |
| probe_capabilities | 配置、固定节点/模型/工作流身份、硬件和真实验收 | validated/unverified/revoked目录，缺项阻塞 |
| compile_request | 完整输入snapshot、capability版本、参数binding schema | 规范API graph、request_hash、引用/上传计划 |
| prepare | 持久task/attempt/prompt UUID、原件hash | prepared manifest；未发外部请求 |
| submit | 唯一worker资格、已持久fence；POST不自动重试 | receipt或submission_unknown；不把HTTP200当产物通过 |
| reconcile | prompt_uuid、request_hash、queue/history及登记文件 | submitted/running/outputs或unknown；history空不等于未执行 |
| fetch_outputs | 精确filename/subfolder/type，根边界检查 | 临时文件→完整探测/解码/hash→不可变文件登记 |
| cancel | 精确queue任务身份；running任务的GPU独占证据 | confirmed/unconfirmed；不无条件global interrupt |

## 首次能力试验与签收

常规生产只允许validated版本；首次真实验收走独立`capability-trial`，不暂时改能力状态。
管理身份创建ValidationRun，冻结精确capability revision、UI/API图、binding、节点/模型hash、许可、
硬件、测试输入/期望及grant；grant绑定run/digest/允许操作/有效期，制作AI无自行签发资格。
尚未validated但来源、许可、固定版本与输入安全门合格的工作流可在此用途真实执行。

确定性编译器显式接收purpose=production/validation；production必须validated，
validation必须有效管理grant且snapshot匹配。两用途均做参数/引用/节点检查及持久prepare/fence/submit/reconcile，
禁止为试验开启POST重试或绕过未知提交。所有试验任务/媒体归属于ValidationRun，不进入业务资产或delivery选片。

Run状态为created→authorized→running→evidence_ready→assessing→passed/failed/unknown；
响应丢失仍需对账，unknown保持未签收。技术完整解码和独立内容观察覆盖该能力所需的全部测试场景，
保存原件、请求、实际媒体、检查及管理签收receipt。签收事务以CAS核对依赖版本和证据digests，
全部必需项pass且可信独立签收才令该版本validated；变更/缺证据/失败保持unverified或revoked。
成功样例可作为能力验收参考，业务生产须重新生成与正常质检，不能直接把试验媒体标为用户通过成果。

## 常规请求及媒体

ComfyUI固定版支持自定义prompt UUID，但服务端无重复UUID去重，队列/history在内存。
禁止宣称exactly-once；不确定时阻塞，显式replacement attempt保留旧风险。
任何请求记录workflow API graph、原UI源、binding schema、节点实现version/hash、模型revision/hash/license、
seed及实际参数、输入引用、硬件、原生规格、输出节点和真实任务/响应摘要。

输入路径真实解码和解析；URL下载每次重定向核验协议/地址，默认拒绝私网/回环/元数据端点，
限制大小/时长/下载时间并记录真实失败；用户显式配置授权内网源走独立allow配置，不是域名子串匹配。
ZIP/文档及文件名防路径穿越，FFmpeg采用参数列表、限定探测范围，不遍历未请求整条长视频。

Grid layout=2x2、四项唯一且有shot/keyframe/time映射；原单帧独立存储。
整四格直输必须单独validated；默认视频从已验收单帧/首尾/多参考能力编译。
声音包含voice身份、逐字台词、实测时长和ASR/发音检查；图视频包含实际解码及独立内容检查。
生成成功、技术有效、质量通过与批准字段互不代替；实际不存在媒体禁止登记generated。
