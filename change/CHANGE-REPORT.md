# CHANGE REPORT (w4)

Window: c291e796..ddefc45f (1548 commits, 4788 files) — master@{10day}...master@{7day}

Packages changed: 310 total (302 product / 8 vendor+other)
Product packages: minor 187, patch 115

## New packages in window (31)
- @deepseek-ai/dsh-api-terminal-controller (packages/api/terminal-controller)
- @deepseek-ai/dsh-browser-use (packages/browser-use/browser-use)
- @deepseek-ai/dsh-client-ui-plugin-manager (packages/client/ui-plugin-manager)
- @deepseek-ai/dsh-client-ui-settings-unarchive-sessions (packages/client/ui-settings-unarchive-sessions)
- @deepseek-ai/dsh-client-ui-sidebar-browser (packages/client/ui-sidebar-browser)
- @deepseek-ai/dsh-client-ui-sidebar-terminal (packages/client/ui-sidebar-terminal)
- @deepseek-ai/dsh-compaction-image-offload (packages/compaction/compaction-image-offload)
- @deepseek-ai/dsh-computer-use (packages/computer-use/computer-use)
- @deepseek-ai/dsh-experimental-auto-review (packages/experimental/auto-review)
- @deepseek-ai/dsh-experimental-browser-use-chrome-devtools-mcp (packages/experimental/browser-use-chrome-devtools-mcp)
- @deepseek-ai/dsh-experimental-browser-use-playwright-mcp (packages/experimental/browser-use-playwright-mcp)
- @deepseek-ai/dsh-experimental-browser-use-runtime (packages/experimental/browser-use-runtime)
- @deepseek-ai/dsh-experimental-browser-use-stagehand-native (packages/experimental/browser-use-stagehand-native)
- @deepseek-ai/dsh-experimental-computer-use-cua-driver-mcp (packages/experimental/computer-use-cua-driver-mcp)
- @deepseek-ai/dsh-experimental-computer-use-cua-driver-native (packages/experimental/computer-use-cua-driver-native)
- @deepseek-ai/dsh-experimental-ptc-runtime-python (packages/experimental/ptc-runtime-python)
- @deepseek-ai/dsh-fs-ssh (packages/ssh/fs-ssh)
- @deepseek-ai/dsh-hmr (packages/boot/hmr)
- @deepseek-ai/dsh-lazy-require (packages/util/lazy-require)
- @deepseek-ai/dsh-mcp-resources (packages/mcp/mcp-resources)
- @deepseek-ai/dsh-office-to-pdf (packages/document/office-to-pdf)
- @deepseek-ai/dsh-plugin-manager (packages/boot/plugin-manager)
- @deepseek-ai/dsh-ptc-runtime (packages/ptc-runtime/ptc-runtime)
- @deepseek-ai/dsh-ptc-runtime-node (packages/ptc-runtime/ptc-runtime-node)
- @deepseek-ai/dsh-sandbox-ssh (packages/ssh/sandbox-ssh)
- @deepseek-ai/dsh-skill-office (packages/skill/skill-office)
- @deepseek-ai/dsh-ssh (packages/ssh/ssh)
- @deepseek-ai/dsh-subprocess-ssh (packages/ssh/subprocess-ssh)
- @deepseek-ai/dsh-tool-present (packages/deliverables/tool-present)
- @deepseek-ai/dsh-workflow-ptc (packages/workflow/workflow-ptc)
- @deepseek-ai/dsh-workspace-changes (packages/deliverables/workspace-changes)

## Sample classified changes
- **patch** @deepseek-ai/dsh-acp: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **patch** @deepseek-ai/dsh-acp-app: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-agent: feat(agent): await initialization through agent/created
- **patch** @deepseek-ai/dsh-agent-default-model: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-agent-instructions: feat(llm): default DeepSeek to Messages with Files parity
- **minor** @deepseek-ai/dsh-agent-loop: feat(llm): default DeepSeek to Messages with Files parity
- **patch** @deepseek-ai/dsh-agent-loop-testkit: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-agent-presets: feat(creator): use Plugin Manager for persistent plugins
- **minor** @deepseek-ai/dsh-agent-tool-presentation: feat(code-runtime): complete sandboxed Node execution and Session fixtures
- **patch** @deepseek-ai/dsh-anonymous-user-id: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-api-gateway: feat(desktop): load bundled Web UI before backend readiness
- **minor** @deepseek-ai/dsh-api-remotes: feat(web): manage plugins over the #4182 manager from the sidebar page
- **minor** @deepseek-ai/dsh-api-session-controller: feat(client): open subagent chats in sidebar
- **minor** @deepseek-ai/dsh-api-settings-controller: feat(settings): resolve namespaces per named scope
- **minor** @deepseek-ai/dsh-api-terminal-controller: feat(web): give user terminals system-user permissions
- **minor** @deepseek-ai/dsh-api-workspace-controller: feat(workspace): restore archived sessions from a settings page
- **minor** @deepseek-ai/dsh-api-workspace-files: feat(document): decouple shared Office conversion from preview
- **minor** @deepseek-ai/dsh-app-boot: feat(web): host plugin configuration on the Plugins page
- **patch** @deepseek-ai/dsh-atomic-write: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **patch** @deepseek-ai/dsh-attachment: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-attachment-local: Clarify token counts after aspect-preserving image projection
- **patch** @deepseek-ai/dsh-authorization: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-base: feat: coordinate profile management through dsh-hmr
- **minor** @deepseek-ai/dsh-bash-local: feat(subprocess): carry a duplex control pipe through managed launches
- **minor** @deepseek-ai/dsh-bash-sandbox: feat(code-runtime): execute Node programs through confined processes
- **minor** @deepseek-ai/dsh-benchmarks: feat(web): restore sidebar layouts and reclaim unattended terminals
- **patch** @deepseek-ai/dsh-brand: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-browser-use: feat(browser-use): add per-Session experimental browser backends
- **patch** @deepseek-ai/dsh-chunked-list: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-client-connection: feat(desktop): add ordinary and mandatory update flows
- **patch** @deepseek-ai/dsh-client-file-upload: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-client-hmr: feat: coordinate profile management through dsh-hmr
- **minor** @deepseek-ai/dsh-client-locale: Revert "feat(client): optimize code block previews and source highlighting"
- **minor** @deepseek-ai/dsh-client-modules: feat(client): lazy-load PDF and terminal runtimes
- **patch** @deepseek-ai/dsh-client-resources: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **patch** @deepseek-ai/dsh-client-store: refactor(client): bind Session UI through providers
- **minor** @deepseek-ai/dsh-client-test-runtime: feat(client): add reusable component factories
- **minor** @deepseek-ai/dsh-client-ui-agent-preset: feat(creator): use Plugin Manager for persistent plugins
- **patch** @deepseek-ai/dsh-client-ui-approval: fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2
- **minor** @deepseek-ai/dsh-client-ui-attachment: release(dsh): 0.1.6-alpha.2
