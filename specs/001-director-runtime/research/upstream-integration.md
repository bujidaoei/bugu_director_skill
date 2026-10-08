# DSH / ai_drama / ComfyUI 集成研究

研究基准日期：2026-10-09（Asia/Shanghai）。本文件区分“固定源码已证实”“现有部署项目已实现”与“bugu 需要实现”。只读检查 `D:/bugu_projects/ai_drama`、`D:/bugu_projects/deepseek-harness` 及上游官方源码，没有启动、安装、升级或覆盖既有系统，没有调用生成接口，也没有把历史工作负载成功当作本项目验收。

## 1. 结论与正式发布边界

可落地路线是“可发现的 skill 包 + 自有 director 运行时 + DSH 官方扩展接口上的薄 bridge + 可替换的媒体执行适配器”。skill 负责创作规则；director 持有项目、冻结版本、审批、任务台账、预算、恢复和交付事实；DSH 提供会话和交互；ComfyUI 提供图执行。单个 Markdown skill 无法承担可靠调度、权限隔离和断点恢复。

当前 `ai_drama` HEAD 为 `db62e56c57716e19f69659ce361ec3c83059fcff`。组件锁选择 ComfyUI `0.39.0`、DSH `0.2.1-alpha.1`，锁已将 `formal_release_eligible` 标记为 `false`。DSH 的 [固定发布](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.1) 明确为 Pre-release；[上游安全说明](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/SAFETY.zh.md) 也明确其预览与未审计状态。正式生产/企业正式交付门禁保持受阻。

2026-10-09 直接读取 npm 官方注册表：30 个 `@deepseek-ai/dsh` 版本中，没有不含预发布后缀的 `x.y.z` 版本；`alpha=0.2.1-alpha.1`，`next/latest=0.2.0-rc.2`。`latest` 标签不等于稳定版。浏览 GitHub releases 第 1–3 页及空第 4 页，已发布条目均为预发布。GitHub REST API 此次受公开出口限流，未伪称取得 API 的完整 release JSON，转用实际页面及 npm 元数据交叉核实。

ComfyUI [v0.39.0](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.39.0) 为正式 release，提交 `b0b743566f65daafc423b4fea8a2fbda94b3384a`。该事实证明版本身份；不证明 bugu 的工作流、GPU、角色一致性、视频质量已经验收。取得稳定 DSH 后仍须独立升级调研、迁移、回归、真实 GPU 与回滚验收，不能改上游产物或把现有预览改名为正式版。

## 2. 固定版本身份

| 组件 | 已检查身份 | 归属与状态 | 证据位置 |
| --- | --- | --- | --- |
| ai_drama | `db62e56c57716e19f69659ce361ec3c83059fcff` | 本地部署源码快照 | `components.lock.json`、`runtime/profile`、`Dockerfile` |
| DSH | `dsh-v0.2.1-alpha.1` / `5badb15009ae1756c3afe0ae0cef1faafc290ccc` | DeepSeek 上游正式发布的预发布包，非稳定版 | `components.lock.json` 的 dsh 块；`runtime/dsh/package-lock.json` |
| ComfyUI | `v0.39.0` / `b0b743566f65daafc423b4fea8a2fbda94b3384a` | Comfy-Org 上游稳定 release | `components.lock.json` 的 comfyui 块；上游 release 和固定 `server.py` |
| dsh-comfyui | `0.5.4` / npm gitHead `3440ad6787f5de4b76925a7f3766388d96786380` | `fandc520/dsh-comfyui` 作者发布的社区插件 | npm 元数据、`runtime/profile/pnpm-lock.yaml`、固定 tarball |
| dshmarket | `1.66.9` / npm gitHead `e03c7a035596c96b51b47ad2e44209bc6029334d` | `dsh-market/dsh-market` 社区插件 | npm 元数据、`runtime/profile/pnpm-lock.yaml` |

历史 `ai_drama` 文档中的“官方插件”应理解为使用该插件作者的原发布包，不能推导为 DeepSeek 官方维护或认证。二者都需要独立供应链和兼容验收；当前 seed 对 `dsh-comfyui@0.5.4` 与 `@ai-drama/dsh-web-search-bing@1.0.0` 显式放行精确 DSH `0.2.1-alpha.1`，不是泛版本兼容保证。版本、integrity、源码 SHA-256 和检查范围见 [机器证据](../evidence/upstream-research.json)。

本地 `D:/bugu_projects/ComfyUI` HEAD 是另一提交 `65787d668397d230bf5839d69a0a7239e2dad378` 且没有 v0.39.0 本地标签，因此关键语义使用从固定上游提交获取的原始 `server.py` / `execution.py` / `main.py` 核实，没有误将本地目录冒认镜像锁定基线。

## 3. DSH skill 安装与命名

产品/仓库名保留 `bugu_director_skill`；DSH 主入口统一为 **`bugu-director-skill`**。上游名字正则为 `^[a-z0-9]+(?:-[a-z0-9]+)*$`，下划线不合法，没有禁止 `-skill` 后缀的规则。依据 [skill 源码](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/skill/skill/src/index.ts#L30) 与 [固定技能文档](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/docs/subsystems/skills.zh.md)。

本地 provider 只枚举根目录下的 `<name>/SKILL.md` 或 `<name>.md`，不递归发现任意 `**/SKILL.md`。SKILL.md 必须带 YAML frontmatter `name` 和 `description`；缺失、非法名字和非法调用策略被忽略并记录日志。所有阶段子 skill 必须处于同一级扫描根目录，或作为入口按需读取的 references；不能把深层技能目录当作可自动发现的技能。

同 scope 的优先级为项目 `.dsh/skills`（100）、项目 `.agents/skills`（200）、`customSkillDirs`（300）、用户 `$DSH_HOME/skills`（400）、用户 agents 根（500）、配置 `bundledSkillDir`（600）。项目根取最近 `.git` 祖先；不同 scope 最近层先赢。自定义制作项目可以在项目根覆盖同名随包 skill，因此启动时要记录最终解析来源、skill digest 和包版本，发现覆盖后不得继续宣称镜像原装规则。

镜像建议将已校验发布包装到不可变 `/opt/bugu-director/skills`，通过官方 filesystem provider 的 `bundledSkillDir` 显式挂载，或由自有 provider 注册；不将 `runtime/profile` 中任意深层目录假设为发现根。运行资料在持久卷，技能升级使用独立版本目录和显式迁移，不能启动时覆盖用户 skill。发现与正文读取分别验收：catalog 出现入口不等于正确执行其正文。

具体接口见 [filesystem provider](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/skill/skill-filesystem/src/index.ts#L250)：配置 `customSkillDirs` / `bundledSkillDir`，`ctx.skills.snapshot({cwd,scope})` 识别 complete 与来源，再 `ctx.skills.get(name,{cwd,scope,signal})` 获取完整定义。provider 报错可能返回不完整目录，不能把空结果当作技能确实不存在。

## 4. Web、headless 与权限的实际语义

[headless 官方接口](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/bundle/headless/README.md) 是一次任务、无 GUI、无端口的执行器：`dsh --profile headless --json --session-id <existing-id> <task>`。不传 session-id 创建新会话；传未知 id 报错，不会创建假恢复会话。`--json` 是事件流；退出 0 只表示 agent turn completed，不能直接标记镜头、媒体或阶段验收通过。

恢复约束见 [runner](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/bundle/headless/src/index.ts#L211)：cwd 必须一致；不接管正被进程拥有的会话；不能直接驱动子代理/fork 会话；未组合的 agent preset 不能收养。headless 基线没有 Web 的 preset roster。故不能把一个 semi Web 会话随意切换 headless 继续，更不能把 headless 文本结果当作业务状态机。

固定源码没有 `approve(all)` API 或 CLI。上游真实配置是 `DSH_PERMISSION_MODE=danger-full-access`，base 配置将 sandbox mode 设为 danger-full-access 并将 approval policy 设为 `never`。`never` 的意义是“所有需要额外审批的请求自动拒绝”；它不等于“全部批准”。不需升级审批的广权限操作可执行，其他工具 guard 仍能拒绝调用。依据 [base 配置 229–262 行](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/bundle/base/cordis.patch.yml#L229) 和 [approval 定义及拒绝实现](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/interaction/user-approval/src/index.ts#L58)。

`auto` / `semi` 是制作业务授权，与 DSH sandbox/approval 旋钮分离：首次由用户选择并保存授权版本，auto 在约定资源/供应商/制作目标内自行决策；semi 每阶段冻结产物后等待人工明确认可。用户要求开放一切制作权限，可赋予所有制作工具权限；若赋予同 UID 完整宿主 shell，任何同主机密钥、台账、浏览器会话和 localhost 服务都可能被该 agent 读取或调用，不能同时宣称不可伪造人类审批。需要强防伪时，semi 的模型执行面使用限定工具和工作区访问，审批签发/私钥置于独立服务身份或隔离控制面；容器内部同 UID 的 0600 文件不是对 full-access agent 的隔离。

## 5. 半自动审查的可信 bridge

上游确有 `ctx.userQuestions.ask()`，可由自有 tool handler 直接调用，不能依赖 agent 向 shell 传 `approved=true`。主 agent 的桥接 handler 先由 director 读取冻结版本，再构建完整 review detail（做了什么、可查看素材、风险、未达项、改动范围），调用 `ask({agent:exec.agent,signal:exec.signal,questions:[...]})`。界面提供“同意本版本，继续”和“要求修改”及自由文本，模型参数不提供 approval verdict。依据 [问答服务](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/interaction/user-questions/src/index.ts#L273)、[Web answerer](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/client/ui-user-questions/src/client/index.ts#L208) 与 [转发 scope 校验](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/api/remotes/src/index.ts#L62)。

handler 得到真实 Web answerer 响应后，重新校验 review 仍为当前冻结版本，直接通过私有 bridge-to-director 通道签发绑定 `project_id`、`stage_id`、revision、input digest、artifact digest、review nonce、question/call identity 和用户响应的 receipt；该新 receipt 不是 DSH 已有功能，需要本项目实现。审核中产物变化使 receipt 失效；replay、跨项目、跨阶段、已用 nonce 和 stale revision 全拒绝。批准状态不得由模型写 JSON、由 agent 提供字符串、由 shell CLI 任意设置。

上游 `ask` 的确绑定 live root agent；runtime-owned child agent 不能直接问用户。默认 blocking 问答无接受 answerer 时失败；有限 timed 模式可返回 pending，超时、跳过、取消、空回答、断连均不是批准。需强依赖答案时使用无限等待语义；无答案的阶段始终 `awaiting_review`。固定 [工具问答文档](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/interaction/tool-ask-user/README.md) 说明 timed `timeout:-1` 支持无限等待。恢复 durable question 是 `ask_user_question` 的特定日志投影；在自有工具里调用问答 seam 不自动获得该投影，必须由 director 保存 pending review，并在恢复时重新展示相同冻结材料。不能误称任意自有 ask 都有上游自动恢复。

自然语言体验可保留：用户在官方 question card 的 custom 字段详细说明修改，bridge 保存原文形成修订要求；明确同意由确定选项完成。普通聊天中的“可以/满意”若由 LLM 二次解释，会成为未经结构化确认的授权猜测，不能直接签发 receipt。后续可增加受认证客户端的确认卡片，将聊天输入作为待确认草稿，再由人明确提交。上游问答 waterfall 本身允许其他 answerer，因此部署时还须审计该 scope 下的应答者清单；不能把任何插件返回的回答都当作身份认证证据。

## 6. 视觉与视频输入能力

DSH 支持文件和 image 内容块，现有内容类型没有核心 video/audio 块。通用文件上传成功不证明模型理解视频；必须由 director 入库后使用受控 ffprobe/ffmpeg 获取真实容器信息、抽帧/镜头候选与音轨，再通过真实视觉模型观察，保留 timecode 和原文件 SHA-256。远程视频链接需要下载来源、大小/时长、权限/可达性、安全重定向和格式检测，不直接把链接当成已读证据。

能力探测应解析当前调用路由 `agent.session.requestHeader()?.config`，缺失时回退 `agent.options.provider/model`，然后 `await ctx.llm.resolveModelInfo(provider,model,signal)`；只有返回 `inputModalities` 明确含 `image` 才可进入图片视觉分析。未知/缺失拒绝声明图像已看。上游 [read-image.ts 112–130 行](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/fs/tool-fs/src/read-image.ts#L112) 已采用该检查；[精确模型解析](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/llm/llm/src/index.ts#L725) 不以 catalog 名称猜测能力。

声明 image 能力还须用项目真实图片做最小读取验收，验证供应商路由、凭据、实际图片请求和答案引用。声明层探测与真实请求失败分别记录。文字模型可以继续剧本开发，却不能给角色一致性、镜头缺陷或视频完整性作视觉通过结论；缺视觉供应商时是能力阻塞，不用文本“模拟看图”。

## 7. DSH 并发并非制作队列

上游每个 agent step 默认最多 10 个 parallel-safe 工具调用；只有 `isConcurrencySafe(...) === true` 才能重叠，不声明、异常或 exclusive 调用成为屏障。PTC 的 `maxParallelSubCalls` 同样默认 10，可配置为 1。依据 [tool registry](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/tools/src/index.ts#L685)、[执行分类](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/tools/src/index.ts#L1296)、[agent-loop scheduler](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/tool-calls.ts#L132)。

这些约束只覆盖一次模型步骤的工具调度；它们不是跨 agent/project 的 GPU 互斥、持久任务队列、供应商速率限制或预算预留。director 需要独立 JobStore、事务性资源预留、并发上限、GPU/后端 lease、heartbeat 与恢复策略。CPU 素材分析/下载可在边界内并行，受同一 GPU 内存约束的工作流应由后端统一排队，不能因为 DSH 默认 10 就假定可跑 10 个视频。半自动的尚未批准 stage 即使有空闲 worker 也不能出队。

## 8. ComfyUI 提交、状态与恢复

[官方 HTTP/WebSocket 路由文档](https://docs.comfy.org/development/comfyui-server/comms_routes) 与固定 [server.py](https://github.com/Comfy-Org/ComfyUI/blob/b0b743566f65daafc423b4fea8a2fbda94b3384a/server.py#L1080) 证实：`POST /prompt` 验证 API-format graph 后入队，返回 prompt_id；`GET /queue` 区分 running/pending；`GET /history/{prompt_id}` 读历史；WebSocket 是进度通道；`POST /interrupt` 可指定 prompt_id；不同层级状态不能混同。

v0.39.0 允许客户端提供 canonical UUID `prompt_id`（server.py:1098–1112），但没有幂等去重：每次有效 POST 都调用 `prompt_queue.put`（1139），[PromptQueue.put](https://github.com/Comfy-Org/ComfyUI/blob/b0b743566f65daafc423b4fea8a2fbda94b3384a/execution.py#L1307) 直接 heap push。预先记录 UUID 有助于丢响应时查询，不能允许重复 POST，也不能承诺 exactly-once GPU execution。

queue、currently_running、history 是 [进程内 list/dict](https://github.com/Comfy-Org/ComfyUI/blob/b0b743566f65daafc423b4fea8a2fbda94b3384a/execution.py#L1296)，history 有淘汰逻辑（1335–1336）；重启或清空历史不证明任务失败或从未运行。固定 [main.py](https://github.com/Comfy-Org/ComfyUI/blob/b0b743566f65daafc423b4fea8a2fbda94b3384a/main.py#L564) 启一条 prompt_worker 线程，官方 execution 是执行器，不替 director 保存商业制作状态。

director 应在发网络请求前原子保存请求 fence、精确 graph/input/parameter digest、backend identity 与预定 prompt UUID（若适配器支持）；网络提交只尝试一次。receipt 丢失、timeout、5xx、无效响应保留 `unknown`，只读查询原身份，禁止自动重新生一个镜头。完成时保存成功 terminal observation、原始输出引用、实际文件长度/哈希/媒体元数据；完整解码成功且产物归属可证明后才进入质量审核。history 丢失后可以依据已持久化且重验的原 terminal 证据恢复，只有一个文件存在或名字相似不够。

## 9. dsh-comfyui 与媒体展示

直接核验了 npm 0.5.4 固定 tarball（SHA-256 `05be6bfc20e453f5f879cdd2814ca951b4aec0f66919493ea2abc900ad44b4ad`），未安装它。发布源码 `lib/routes.js:1129–1159` 的 `/comfyui/workflows/run` 接收 `{id,parameters}` 并返回 `{ok,promptId,workflowName}`；`lib/index.js:168–183` 从保存 library 的 graph 重新绑定参数并提交。该 route 不提供“以已冻结 graph digest 原子运行”的 contract，library 并发编辑需要冻结副本或 quiescence；不能拿先前查到的 catalog digest 宣称提交时仍相同。

`/comfyui/jobs/media` 在 history 缺失时将 running 与 pending 都返回 `queued`（lib/routes.js:1435–1443）；必须再查 `/comfyui/queue` 的 exact promptId；查询之间 race 无 terminal 证据时仍 unknown。社区插件核心 client queuePrompt 可发 promptId，但保存 workflow run route 不暴露该参数，也没有通用 dedup；不能未经源码依据声称可经现有 route 预定 UUID。

社区插件只为 `comfyui_run`、`comfyui_workflow` 两个自有名字注册 `tool.call.toolview`（发布 client/client.js:5046–5059），不会自动渲染 bugu 自有工具。bugu bridge 需独立客户端插件，使用官方 slot 生命周期为自己的工具结果注册图片/视频/音频预览与下载。模型结果保留结构化文本/文件引用；浏览器 presentation metadata 与真实终态/文件身份分别校验。不能将视频 Markdown 链接等同于原生可播放验收。

媒体引用必须是当前认证浏览器来源的受控 route，可重新构建 output filename/subfolder/type 的安全引用；拒绝 traversal、意外绝对 URL、temp 产物或任意远程 host。`/comfyui/media` 能根据保存文件引用读取而不依赖 volatile history，适合作为展示来源；原始文件仍要进入 director 持久项目存储。社区插件 `sameOrigin`（lib/http.js:29–36）缺 Origin 时允许非浏览器调用；same-origin 判断不是用户认证或任务所有权。需复用既有认证代理边界并单独验收，不能公开未认证生成/删除 route。

## 10. ai_drama 现有集成点与不能误用的历史代码

当前 seed 由 `Dockerfile:45–50` 拷贝 runtime/dsh 与 runtime/profile，通过 `scripts/install.sh:119–139` 按冻结 npm/pnpm 锁安装到 `/opt/dsh` 与 `/opt/dsh-seed`。持久目录由 `scripts/config.py:173–174` 指向 `<data>/dsh`；`scripts/start.py:522–527` 初始化 profile、写运行 overlay 后以 web profile 启动。`scripts/dsh_profile.py:301–307` 在 seed marker 不符时拒绝覆盖，不能仅 COPY 一个新包后期待已有卷自动变成新版本。

当前 active profile 是 `@deepseek-ai/dsh-base`、`@deepseek-ai/dsh-web-app`、`@ai-drama/dsh-web-search-bing`、`dsh-comfyui`、`dshmarket`。`runtime/production-plugin` 源码虽留在仓库，**未在当前 profile/seed 依赖与 bundles 中启用**；`scripts/dsh_profile.py:222–247` clean-seed 检查禁止旧 production payload 混入。历史 request-fence、terminal artifact、媒体卡片代码可作为已研究的设计材料，不能冒称当前 director 已实现或已安装，也不能直接复活旧包破坏干净基线。

后续 bugu 镜像集成应在 `ai_drama` 独立 Spec Kit feature/PR 中完成，明确改变现有“干净默认”合同：选择可选 derivative image 或显式 director profile，而非给现有官方核心默认 stealth install。要扩展 seed 插件清单和严格 admission、锁定 bugu 发布包及上游依赖、安装新的 bridge、Supervisor 管理独立 director service、持久挂载项目数据与数据库、健康与 readiness、受认证媒体 route、离线升级/回滚。当前允许的插件集合不会自动容纳任意 bugu 包，必须显式设计 migration。

`skillsDir`（scripts/dsh_profile.py:472）是传给 dsh-comfyui 的 workflow skill pack 目录，**不是** DSH 核心 filesystem provider 的 bundledSkillDir。需要分别配置两者，避免看似放入 skill 却主入口不可发现。升级不得删除既有用户 workflows、provider 设置、会话、输入/输出；迁移失败应保持旧 runtime/profile，可复原确切匹配的旧锁与数据版本。

## 11. 可实施架构选择

| 层 | 责任 | 固定边界 |
| --- | --- | --- |
| skill package | 首次模式选择、输入路由、创作阶段规则、优质导演知识、修订规则 | 禁止自己写“任务已完成/人类已批准”作为事实 |
| DSH bridge | 官方 tools.register/guard、skills、llm capability、userQuestions、客户端媒体卡片 | 只接受 project/stage identity；冻结材料与审批 verdict 由服务器持有 |
| director service | Project/Stage/Asset/Shot/Job/Review/Delivery、事务状态机、预算、lease、恢复、修订与交付 | 只有已证实终态与 hash 绑定的 receipt 能推进 stage |
| backend adapters | ComfyUI API graph、社区 workflow library、外部图片/视频/TTS 服务、FFmpeg | 每后端明确能力、输入格式、提交/查询/取消/unknown 语义，不强迫通用四宫格 |
| immutable package/image | 版本、依赖锁、许可证、技能摘要、source/artifact hashes、SBOM | 源码/镜像不含用户作品、provider 凭据与生产台账 |

ComfyUI-native graph adapter 优先保证冻结 graph 的执行身份；社区 workflow adapter 用于既有 DSH 工作流互通，明确源 revision 未可证明时的边界。不要调用社区插件私有包 subpath 或修改 converter 以绕过不支持 graph。四宫格是分镜审查与某些生成后端的输入策略；若模型只支持单图首帧或首尾帧，应先抽取带索引的单格素材并按模型能力绑定，不能保证四格直接连续生成同一视频。

首发设计为单部署、单项目状态 authority，SQLite 事务与原子产物发布；多 worker 共享状态时仍须租约、唯一键、乐观版本和 durable request fence。以后横向扩展迁移到支持共享事务的服务数据库与对象存储，通过同一 contract，不把本地 SQLite 放在不支持锁语义的网络盘声称 HA。

## 12. 真实验收计划及本轮未执行项

本轮完成源码/版本研究，没有执行 DSH 启动、browser、GPU、远程供应商或成片验收。以下测试必须在实施任务中保持未完成，真实运行后才记录通过。

| 验收 | 真实输入/触发 | 必须保存的证据 | 通过条件 |
| --- | --- | --- | --- |
| skill 安装 | 空卷镜像与现有持久 profile 的显式迁移 | 镜像 digest、固定锁、catalog 来源、正文 digest、迁移前后 hash | 入口 bugu-director-skill 可自然语言调用；无用户文件覆盖；重启保留 |
| auto 文本入口 | 真实短篇剧本，用户首次选择 auto | 授权记录、阶段事实、任务/输入/图 digest | 阶段自动推进；资源边界一致；不将 exit0 当媒体验收 |
| semi 闭环 | 真阶段材料→不同意→修改→明确同意 | 官方 question response、review receipt、版本/hash | 拒绝/超时/断连不推进；修订使旧 receipt 失效 |
| 防伪审批 | agent tool arg approved、shell 构造、stale/cross-project/replay | 拒绝日志、隔离权限检查 | 模型执行面无法签发/覆写 receipt；使用全OS权限时如实记录防伪边界 |
| 图片能力 | 几张真实角色/风格图；text-only 与 image 路由 | 精确模型 metadata、真实 image 请求、观察记录 | 无能力明确阻塞视觉结论；有能力可关联具体输入与观察 |
| 视频入口 | 用户本地视频与可访问的真实视频链接 | 来源、容器探测、SHA-256、timecode 抽帧与音轨 | 视频确实读取分析；坏格式/超限/安全重定向正确处理 |
| 单个 GPU job | 已审 workflow、真实模型与素材 | graph/参数/模型/节点版本、submit receipt、terminal history、完整解码与媒体 hash | 真实输出可播放且身份对应；不使用测试 fixture 冒认GPU结果 |
| 网络不确定 | 真实提交前后丢响应、轮询 outage | 预写 fence、prompt identity、只读恢复轨迹 | 无重复 POST；unknown 不冒认失败/完成 |
| 重启恢复 | stage审核中、排队/生成中、完成后分别重启 | 数据与session备份、租约状态、terminal/artifact复验 | 可安全继续；已完成且原证据存在不重复消费GPU |
| 修镜头 | 一个镜头存在真实身份/动作/帧异常 | defect、限定修订范围、先后hash、失效依赖 | 只重做受影响镜头；最终统一色彩/声音/字幕 |
| 交付 | 真实多镜头终版 | 规范目录、manifest、hash、可播放文件、README | 全片与各片段可取、已审状态清楚、缺失项不宣称完整 |
| 回滚与门禁 | 固定旧/新镜像与真实数据备份 | 镜像身份、迁移/回滚记录、release gate输出 | 可恢复；当前DSH预发布正式门禁失败；稳定版升级后另验 |

质量测试应至少覆盖两个不同题材/制作形态、一个有身份连续性的多镜头短片，以及一次局部修复；某个既有 H3 workflow 的历史成功不能证明通用导演系统或全部后端成功。商用质量阈值由项目用户标准冻结，自动审查不得把美观分数当作身份/时序/真实交付证据。

## 13. 尚需独立研究的阻塞

- DSH 稳定 release 及安全状态仍阻塞正式交付，不能通过选择 alpha 或代码兼容绕过。
- 本项目 director 与审批 bridge 尚未实现，不能标记安装/半自动/断点恢复已验收。
- 当前 ai_drama clean 默认与 bugu 镜像集成须独立规格变更，不在本轮覆盖部署。
- 每一图片、视频、TTS、字幕/口型后端均需明确版本、许可、模型/节点/资源需求及真实工作负载；通用适配 contract 不代表未验收的供应商可用。
- 公网 DSH Settings 在历史规格中仍有受支持能力限制；现有代理和 --trusted-host 能力不等价于受支持 settings 管理。制作 bridge 不修改上游 Settings 或伪造 host ownership。
- 强人类审批证据与模型同 UID 完整 OS 权限不能同时作强安全承诺；需要部署能力隔离及实际攻击路径验收。
