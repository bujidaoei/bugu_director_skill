# CLI与本机控制服务合同

目标命令为`bugu-director`，本轮未实现。所有生产操作走持久服务，不启动无追踪长shell。

| 命令 | 输入及授权 | 结果 |
| --- | --- | --- |
| init | 标题、来源、owner；模式可为空 | project_id及mode_required/ready；不开始生产 |
| mode | project_id、auto/semi、真实用户模式receipt、expected_revision | 新授权版本；切换时暂停并核实安全检查点 |
| start | project_id、expected_revision、command_id | queued/running或实际阻塞 |
| status | project_id、可选episode/task | 阶段、revision、待审、能力缺口、任务/产物和真实进度 |
| review | project_id、stage/revision | 冻结审核包、digests、媒体位置、问题、待决策 |
| approve | package_id、expected_revision、trusted receipt | 只有可信host/人工入口可发；AI身份拒绝 |
| revise | package_id、用户修改、expected_revision | 变更提案、影响闭包及新待制作版本 |
| pause/resume | project_id、expected_revision | 持久暂停/对账后继续，不删除请求身份 |
| cancel | project/task、expected_revision | cancel_requested；未确认则明确cancel_unconfirmed |
| export | delivery/timeline版本、固定profile | export_pending或通过交付引用 |
| capabilities | 类型/版本 | 真实注册能力及验收状态，未验证条目不能业务生产 |
| capability-trial | create/run/status/accept/reject、管理身份、固定能力版本、trial grant、expected_revision | 隔离ValidationRun及真实证据；accept须独立签收，不接受AI自报pass |
| backup/restore | 管理身份、明确目标 | 一致性备份/校验恢复记录；不覆盖目标已有项目 |
| daemon/worker | 显式配置路径、服务角色 | 监督进程；健康分别报告controller/coordinator/worker/backend |

每个写命令携带command_id（UUID）及expected_revision；同command_id同payload返回原结果，异payload为conflict。
stdout只有JSON结果（--human为通俗呈现），stderr结构化诊断；日志不得包含凭据/登录token。
结果schema包含schema_version、command_id、ok、project_id、revision、state、data、errors、evidence_refs。
ok表示命令成功受理，不代表媒体/阶段通过。exit0为命令成功，2为输入不合法，3为版本/批准冲突，
4为缺能力/待处理，5为后端不可用/未知提交，6为本地持久化失败，7为权限拒绝。

控制连接使用本机Unix socket或仅loopback受认证端点，部署统一配置；
读、制作提案、生产、管理、human-approval各身份分开。AI CLI不持有审批签发凭据。
未经认证连接、跨project访问、路径越界、重放receipt均拒绝并记录安全事件。
