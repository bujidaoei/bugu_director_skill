# 阶段审核、质量与权限合同

半自动S01–S10全部暂停，每包包含通俗summary、设计理由、固定media manifest、实际预览链接、
检查结果/不确定项、文件位置、选择/修改影响及project/stage/revision/input_digest/artifact_digest。

Host工具handler读取冻结包，构造官方ctx.userQuestions.ask问答。问答固定选项是明确批准、提出修改、停止；
自由文本先记录修改/解释意图，模糊文本不能自动批准。问答超时、异常、中断保存await_review。
制作模型调用审核工具只能触发问答，不能传approved=true令其通过。
签发方直接使用官方Web answerer返回事件和scope，生成有认证且不可重放的receipt。
receipt包含actor=human、subject/project/stage/package、revision、两digest、decision、nonce、timestamp、issuer版本。
任何包变更、文件hash变化、跨项目、actor=AI、无真实问答或重复nonce拒绝。
签发凭据及审批端点只对隔离host角色开放，制作shell不拥有；同UID/root全权部署不满足此不变量。

全自动不触发每阶段用户问答，AI审查产生actor=auto_quality的decision，明确区分human批准。
质量profile从素材/目标推导，在S03首次冻结并带版本，变更有依据及影响记录。
每项QualityCheck指定实际媒体、时间区间/帧/台词、观察与证据、检查器版本和pass/fail/unknown。
硬失败逐项阻塞：换脸、错台词/说话人、漏剧情、关键空间/道具/动作错、网格残留、不能完整解码。
unknown不能抵消硬失败，软分仅用于可接受候选排序。
画风/光照/造型合法变体按资产状态检查，不仅用像素/embedding阈值判身份。
完整终审复核整集节奏、镜间连续性、声线、字幕、混音和音画；不得只汇总逐镜pass。
独立审查AI与创作者分上下文，读取实际产物；真实验收还有独立人工逐镜核验。
