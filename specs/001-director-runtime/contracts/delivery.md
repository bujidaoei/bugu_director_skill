# 时间线、交付、镜像与发布合同

Timeline固定版本包含镜序、媒体ID/hash、入出点ticks/timebase、画幅/帧率、转场、声音轨、
字幕逐句起止、混音参数、字体及export profile。使用FFmpeg固定稳定二进制身份和实际执行参数。
相同时间线重建须选片、顺序、时长、字幕及音轨关系一致；编码输出不承诺不同平台字节完全相同。

交付包：有字幕成片、无字幕成片、SRT/ASS字幕、dialogue/music/sfx stems、所选片段、
全部候选索引、时间线及依赖manifest、质量报告、来源/许可及交付说明。
manifest逐文件记录相对位置/hash/bytes/spec/status和固定引用，failed/superseded/cancelled不可冒充final。
全部视频/音轨完整解码；实际播放、Range拖动、完整下载和重启后访问通过。
受保护媒体入口按filename/subfolder/type定位，不依赖临时history；不得在URL暴露凭据。

默认验收竖屏1080×1920、24fps；原生生成/后期缩放分别记录，不能把缩放称为原生1080p。
音频48kHz立体声、目标−16 LUFS±1 LU、真峰值≤−1dBTP，字幕/对白/口型对齐误差≤100ms；
技术和逐镜实际观测两类证据都保存，缺能力不能通过。

镜像仅固定skill、wheel、控制插件及依赖；模型/素材/项目/凭据在外部卷。
skills发现用官方bundled root，启动不下载/升级、不覆盖已有数据；director纳入监督/健康及优雅停止。
发行manifest含source_commit、skill/wheel/archive hashes、依赖lock、节点/模型目录及SBOM、许可、
schema、验收镜像digest、实际验收refs和preview/formal_release_eligible。
发布验收后分发同一镜像，不重建同标签冒充。
DSH预发布时formal_release_eligible=false；正式稳定迁移独立规格/锁/回归/工作负载/回滚后再判定。
Git正常推送功能分支及main，远端查询两引用与交付提交一致；禁止强制覆盖或凭据进入内容。
