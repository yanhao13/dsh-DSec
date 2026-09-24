# Preview release: v0.1.6-alpha.2

Released: September 17, 2026

## Highlights

**Sidebar terminals, browser, and subagent chat:** the right sidebar gains interactive terminals (with system-user permissions and theme following), a Sidebar Browser for web tabs, and subagent chat sessions — alongside plan-artifact previews and document/image/PDF previews that open automatically, plus the ability to reclaim unattended terminals and restore archived sessions.

**Desktop distribution and updates:** a refined Windows install experience ships with caption navigation, localized menus, and native dialogs for fatal recovery, running on a thin Electron shell; a standalone Python Office runtime and a shared office-to-PDF pipeline (with bounded queues and caching) power document previews across clients.

**Model routing:** DeepSeek moves to the Messages protocol by default with Files parity, the V4 Flash and V4 Flash Vision Exp default models are dropped, and a durable image-offload watermark lands for session logs.

**Browser and computer use:** experimental per-session browser-use backends arrive, extending automation surfaces through Chrome DevTools, Playwright, and Stagehand drivers.

**Plugins, profiles, and sessions:** global plugins are managed from the sidebar and a dedicated Plugins page with live reload, profiles launch via a `dsh <profile>` shorthand, subagent delegation limits are configurable in the GUI, and archived sessions can be restored from settings.

## What's Changed

- feat(client): open subagent chats in sidebar [#4417](https://github.com/deepseek-ai/deepseek-harness/pull/4417)

- feat(web): add interactive sidebar terminals [#3864](https://github.com/deepseek-ai/deepseek-harness/pull/3864)

- feat(web): add Sidebar Browser tabs [#4379](https://github.com/deepseek-ai/deepseek-harness/pull/4379)

- feat(web): keep plan artifacts and automatically open sidebar previews [#4414](https://github.com/deepseek-ai/deepseek-harness/pull/4414)

- feat(web): restore sidebar layouts and reclaim unattended terminals [#4206](https://github.com/deepseek-ai/deepseek-harness/pull/4206)

- feat(workspace): restore archived sessions from a settings page [#4098](https://github.com/deepseek-ai/deepseek-harness/pull/4098)

- feat(desktop): 普通更新、强制升级与 Windows 安装体验 [#4033](https://github.com/deepseek-ai/deepseek-harness/pull/4033)

- feat(desktop): integrate Windows caption navigation and localized menus [#4407](https://github.com/deepseek-ai/deepseek-harness/pull/4407)

- feat(desktop): use native dialogs for fatal recovery [#4263](https://github.com/deepseek-ai/deepseek-harness/pull/4263)

- feat(desktop): bundle standalone Python Office runtime [#4276](https://github.com/deepseek-ai/deepseek-harness/pull/4276)

- feat(document): shared office-to-pdf conversion with bounded queues and caching [#4282](https://github.com/deepseek-ai/deepseek-harness/pull/4282)

- feat(browser-use): add experimental per-Session backends [#4092](https://github.com/deepseek-ai/deepseek-harness/pull/4092)

- feat(llm): add Messages protocol support to DeepSeek [#3682](https://github.com/deepseek-ai/deepseek-harness/pull/3682)

- feat(llm): default DeepSeek to Messages with Files parity [#4089](https://github.com/deepseek-ai/deepseek-harness/pull/4089)

- feat(llm): drop the V4 Flash and V4 Flash Vision Exp default models [#4313](https://github.com/deepseek-ai/deepseek-harness/pull/4313)

- feat(session, llm): durable image offload watermark [#3440](https://github.com/deepseek-ai/deepseek-harness/pull/3440)

- feat(web): manage global plugins from the sidebar [#3596](https://github.com/deepseek-ai/deepseek-harness/pull/3596)

- feat(web): host plugin configuration on the Plugins page [#4376](https://github.com/deepseek-ai/deepseek-harness/pull/4376)

- feat(subagent): configure delegation limits in the GUI [#4317](https://github.com/deepseek-ai/deepseek-harness/pull/4317)

**Full Changelog:** https://github.com/deepseek-ai/deepseek-harness/compare/master@{10day}...master@{7day}
