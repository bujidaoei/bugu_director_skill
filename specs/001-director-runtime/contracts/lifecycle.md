# 生命周期与恢复合同

依据data-model，director事务是唯一状态写入口。

1. 模式receipt缺失→mode_required，任何生产请求拒绝。
2. Stage输入引用完整且依赖accepted才ready；业务生产能力需validated。管理员能力试验独立于Project/Stage，不绕过此门，按production.md的ValidationRun合同执行。
3. 提案保存正文及结构化依赖→owner校验→原件hash→提交revision。
4. Stage完成条件是实际产物+技术检查+语义质量+当前模式通过决策；进程exit0不足。
5. 半自动await_review持久等待，控制进程/问答中断不改变状态。
6. 修订计算依赖闭包，事务标invalidated并撤销受影响批准；无关通过成果保持hash。
7. worker lease/fencing epoch保护本地写入；外部request fence永久保留，lease回收不准重提。
8. 浏览器离线全自动继续；coordinator/worker崩溃后重建状态与输出对账，unknown不推进。
9. 暂停不杀上游任务、不清history；取消只针对当前所有权任务，晚到产物保留。
10. 三轮不同修复假设均无改善且仍硬失败→stalled，附实际对比和最佳候选；新增可用能力/需求可新run恢复。
11. 数据备份恢复完成关系/hash/版本及外部任务核实后才启调度；未知任务恢复后仍未知。
12. 模式切换记录当前revision、新mode receipt、task安全检查点；auto→semi撤销自动推进资格并切换受控身份。

必须实测：写产物后DB失败、DB成功outbox未发、submit已发响应丢失、worker抢占、并发CAS冲突、
重启history丢失、媒体外改、磁盘不足、审核中断、取消晚到及schema升级回滚。
故障注入只验证控制协议；实际GPU/媒体/镜像恢复另有真实工作负载证据。
