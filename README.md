# bugu_director_skill

面向DSH镜像的AI漫剧制作系统设计：自然语言接入文字、图片和视频，选择全自动或半自动，
完成剧本、风格、角色/声音、场景、四宫格、视频、返修、剪辑和规范交付。

**当前状态：调研与Spec Kit设计基线；运行库和生产技能包尚未实现，真实成片/镜像验收尚未完成。
当前固定DSH为预发布，正式发布受阻。** 本仓不是已安装可自动出片的产品。

## 阅读入口

- [企业方案](docs/enterprise-plan.md)：产品流程、关键设计、交付与里程碑。
- [需求规格](specs/001-director-runtime/spec.md)：6用户故事、40需求及14验收结果。
- [技术计划](specs/001-director-runtime/plan.md)：服务/权限/状态/生产/声音/镜像边界。
- [实施任务](specs/001-director-runtime/tasks.md)：依赖顺序、并行工作及真实验收任务。
- [独立设计复查](specs/001-director-runtime/evidence/planning-analysis.json)：已修订问题、覆盖及验证范围。
- [研究决策](specs/001-director-runtime/research.md)、[数据模型](specs/001-director-runtime/data-model.md)、
  [合同](specs/001-director-runtime/contracts/cli.md)、[验收指南](specs/001-director-runtime/quickstart.md)。
- [来源会话与范围](specs/001-director-runtime/research/source-context.md)、
  [核心套件](specs/001-director-runtime/research/core-suite.md)、
  [其余8套件](specs/001-director-runtime/research/supporting-suites.md)、
  [DSH/ComfyUI集成](specs/001-director-runtime/research/upstream-integration.md)。

## 已完成研究及边界

当前参考快照9套件、871文件、31技能入口；所有入口逐个研究，关键实现/合同/附属规则深入检查。
核心89+5项离线测试通过，但原整包验收失败，记录14项缺口/风险；其他套件21项缺陷隔离复现。
完整目录hash及测试/许可证据位于[研究证据](specs/001-director-runtime/evidence/reference-inventory.json)。
这些是参考研究结果，不能算本项目真实媒体或生产验收。

DSH技能ID规划为`bugu-director-skill`，产品和仓库保持`bugu_director_skill`。
首版单主机单GPU、ComfyUI优先、有声单集，随后验证跨集同脸同声及局部返修。
全自动无默认预算/次数额度；半自动每阶段需真实用户批准当前版本。

## 开发与分发

遵循[AGENTS.md](AGENTS.md)及[宪章](.specify/memory/constitution.md)，使用Spec Kit全过程管理。
参考复用逐文件核实许可；受限制创作文本不进入商业分发，已授权代码保留署名/许可及修改记录。
本轮没有借入Acheng生产代码或创作正文。现有Spec Kit工具保留[第三方通知](THIRD_PARTY_NOTICES.md)。
原创项目的发行许可在正式制品阶段单独确定，本轮没有替用户授予新开源许可。
目标远端：[bujidaoei/bugu_director_skill](https://github.com/bujidaoei/bugu_director_skill)。
设计基线的main同步与后续生产制品发布分别记录，推送不解除正式发布门禁。
