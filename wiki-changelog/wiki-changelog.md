# Wiki Changelog — deepseek-harness (master@{10day}...master@{7day})

**Source repository:** `https://github.com/deepseek-ai/deepseek-harness` (resolved from `git remote get-url origin`)

**Window:** master@{10day} → master@{7day} · 1548 commits in range (1033 kept after noise-merge filtering) · grouped daily.

## 2026-08-19

**3 commits.** 0 feature changes, 2 fixes.

### 🐛 Bug Fixes
- fix(session-controller): address review feedback on cold Inbox commands ([6bfda7a](https://github.com/deepseek-ai/deepseek-harness/commit/6bfda7a0e53f64d60c40266dbec189d383bd5b69))
- fix(session-controller): resume cold sessions for Inbox commands ([6322bb9](https://github.com/deepseek-ai/deepseek-harness/commit/6322bb96e8457c8dcdb5553f2caf010ab1e7bde1))

### 🔄 Refactoring
- refactor(agent): back Inbox with a durable projection ([4b0af96](https://github.com/deepseek-ai/deepseek-harness/commit/4b0af96838e2eaa335b415f22c68f74cb57e47ae))

## 2026-08-21

**3 commits.** 0 feature changes, 0 fixes.

### 🔄 Refactoring
- test(session-projection): scope projection assertions ([0aee112](https://github.com/deepseek-ai/deepseek-harness/commit/0aee112c6fd400e9fd29cb4af7f5d52a4483e723))
- test: trim unrelated inbox changes ([09fab78](https://github.com/deepseek-ai/deepseek-harness/commit/09fab78863215c24888e09da8e3b280bc0efe97b))
- refactor(agent): remove inbox service ([4d5ccf3](https://github.com/deepseek-ai/deepseek-harness/commit/4d5ccf39ef4717c5829d9afcddaeaae38bca9ae1))

## 2026-08-24

**1 commits.** 0 feature changes, 0 fixes.

### 📝 Documentation
- docs(session-projection): keep registry contract unchanged ([015d7e0](https://github.com/deepseek-ai/deepseek-harness/commit/015d7e0752801b9d22c0288af57268bebb542b2c))

## 2026-08-26

**5 commits.** 0 feature changes, 2 fixes.

### 🐛 Bug Fixes
- fix(session-controller): derive queues from projections ([5b9b7c5](https://github.com/deepseek-ai/deepseek-harness/commit/5b9b7c59ddc582d09763b7d4ec39c7646f6009ce))
- fix(agent): validate durable inbox reconstruction ([fb3f3ff](https://github.com/deepseek-ai/deepseek-harness/commit/fb3f3ff162308f5dd11e826b748fe1e57d38d98f))

### 🔄 Refactoring
- refactor: ban ambiguous origin label ([71d50b4](https://github.com/deepseek-ai/deepseek-harness/commit/71d50b4a8481ae36c714b316e81286d94a8b7002))
- test: cover projection-aware session helpers ([bfb1198](https://github.com/deepseek-ai/deepseek-harness/commit/bfb119850b3f9da72ca6b20314cc244050677cf9))

### 📝 Documentation
- docs: refresh Claude SDK notices ([bfaa403](https://github.com/deepseek-ai/deepseek-harness/commit/bfaa403b7cd3e64567aa0297d0059b4bbb138ca5))

## 2026-08-27

**4 commits.** 0 feature changes, 2 fixes.

### 🐛 Bug Fixes
- fix(ui-conversation): dispose Inbox projection subscription ([ba51e54](https://github.com/deepseek-ai/deepseek-harness/commit/ba51e5483e95b2f8d24bdffd04834f0f5d1337b6))
- fix(web): restore pending Inbox after restart ([8c8c5b2](https://github.com/deepseek-ai/deepseek-harness/commit/8c8c5b2680f1e4ac8d4f8ef7fa808acdfa2829bb))

### 🔄 Refactoring
- test(session-controller): cover control stream disposal ([16654be](https://github.com/deepseek-ai/deepseek-harness/commit/16654bee727f639c7a35e3849cef83195da2abc3))

### 📝 Documentation
- docs: refresh module graph ([76d5f79](https://github.com/deepseek-ai/deepseek-harness/commit/76d5f797a85273336386f308e92f7ef4936a14e3))

## 2026-08-29

**4 commits.** 1 feature changes, 1 fixes.

### 🆕 Features
- feat(permission): add Auto review mode ([b3b7e00](https://github.com/deepseek-ai/deepseek-harness/commit/b3b7e00449dbd28db4ae7ea440fdfca71e1b0ae8))

### 🐛 Bug Fixes
- fix(permission): close auto review gaps ([64fa60d](https://github.com/deepseek-ai/deepseek-harness/commit/64fa60d3d4f929df4fc31bea37ceebae69e325b5))

### 🔄 Refactoring
- test(ui-tool): trim redundant Auto denial matrix ([068c6ca](https://github.com/deepseek-ai/deepseek-harness/commit/068c6ca3ffede7ed3d6f558765d361939f400fd6))
- refactor(permission): simplify Auto review ownership ([e6ae1bc](https://github.com/deepseek-ai/deepseek-harness/commit/e6ae1bc7515a2b40180acccece3b889a1b1ec739))

## 2026-08-31

**1 commits.** 0 feature changes, 1 fixes.

### 🐛 Bug Fixes
- fix(web): localize Auto review descriptions ([07e4ceb](https://github.com/deepseek-ai/deepseek-harness/commit/07e4ceb011161c41879c8b5efa880e9e85f39d63))

## 2026-09-02

**1 commits.** 0 feature changes, 0 fixes.

### 📝 Documentation
- docs: propose logging each request's image projection ([1516c60](https://github.com/deepseek-ai/deepseek-harness/commit/1516c6018d1dae32715f950cda4225ff41c8a626))

## 2026-09-03

**6 commits.** 2 feature changes, 2 fixes.

### 🆕 Features
- feat(session, llm): durable image offload watermark ([345b5cd](https://github.com/deepseek-ai/deepseek-harness/commit/345b5cdc6f920034a8a7bf50a644a6a99330e8ca))
- feat(auto-review): enforce per-call authorization ([535d7ea](https://github.com/deepseek-ai/deepseek-harness/commit/535d7eab3ae9267f7fc28129ba9ec27bda2d001d))

### 🐛 Bug Fixes
- fix(auto-review): align review and teardown boundaries ([681b0b6](https://github.com/deepseek-ai/deepseek-harness/commit/681b0b66a97b977b445fb05ce970bfdef4b36e5c))
- fix(permission): tighten Auto review validation ([1ec5f21](https://github.com/deepseek-ai/deepseek-harness/commit/1ec5f21e82bee420e1fcdaedf8949032d2a18c30))

### 🔄 Refactoring
- test(snapshot): canonicalize Auto review PTC fixture ([92cb99e](https://github.com/deepseek-ai/deepseek-harness/commit/92cb99e9e9585b36c2bce523474392346922e91e))

### 📝 Documentation
- docs: propose a durable image offload watermark ([c1b1cd2](https://github.com/deepseek-ai/deepseek-harness/commit/c1b1cd2984f673f2946168f4319d050a9dcd195e))

## 2026-09-04

**27 commits.** 9 feature changes, 10 fixes.

### 🆕 Features
- feat(web): simplify the plugin manager and drop the plugin list tab ([a7302ee](https://github.com/deepseek-ai/deepseek-harness/commit/a7302ee69e1d7d1965d8c3d7fe5a1c89a4d75c68))
- feat(web): show what an install removed and why the Host refused a change ([ac51707](https://github.com/deepseek-ai/deepseek-harness/commit/ac517078ca8e8443e349d58d16637f64abfae8cb))
- feat(plugins): judge an install after pnpm, restore the manifest on failure, run one mutation at a time ([e3386d1](https://github.com/deepseek-ai/deepseek-harness/commit/e3386d110577c60afb5d0056005a3221104558f2))
- feat(boot): own row ids across the stack instead of prefixing external bundles ([5d74250](https://github.com/deepseek-ai/deepseek-harness/commit/5d742503eaafbd2523b207ab0fd674460730b052))
- feat(auto-review): enforce risk-classified review ([d381a3c](https://github.com/deepseek-ai/deepseek-harness/commit/d381a3c6f4cc539921b989db24910b960c5b1990))
- feat(web): manage plugins and per-preset settings from the browser ([1570eee](https://github.com/deepseek-ai/deepseek-harness/commit/1570eeeaee2676f457314f06f0e1db515a69c2f8))
- feat(settings): resolve namespaces per named scope ([80ea5fc](https://github.com/deepseek-ai/deepseek-harness/commit/80ea5fcdf5609dae605eff3e612ffd43661119e1))
- feat(plugins): plugin manager, preset user layers, and the patch-file writer ([dc969e2](https://github.com/deepseek-ai/deepseek-harness/commit/dc969e2ee857a777ca9a5c9aa2b3f2bdaea13e19))
- feat(boot): isolate external bundles and expose the booted profile ([d419e7e](https://github.com/deepseek-ai/deepseek-harness/commit/d419e7e553b17799e7f6c2c8c8a96044e57a79ae))

### 🐛 Bug Fixes
- fix(auto-review): stabilize allow response protocol ([3993d36](https://github.com/deepseek-ai/deepseek-harness/commit/3993d36c6968c444031c89cea7c72a720d9c8f94))
- fix(boot): re-probe records an older probe format wrote ([e234dc7](https://github.com/deepseek-ai/deepseek-harness/commit/e234dc75fd8d2609a9e32baa4ee2001959015e29))
- fix(boot): a plugin is a package that declares itself to dsh ([1ef796f](https://github.com/deepseek-ai/deepseek-harness/commit/1ef796fcf947a1fc3647b300d17e8995ef4266bb))
- fix(auto-review): reinforce reviewer output contract ([8481e02](https://github.com/deepseek-ai/deepseek-harness/commit/8481e02b368bb5959df9ec20587f847e028b08a7))
- fix(permissions): harden auto disposal migration ([11c4fa1](https://github.com/deepseek-ai/deepseek-harness/commit/11c4fa1b0a37749b0da5d0dc8fcd91c8089304e1))
- fix(auto-review): scope logged calls by step ([dae5844](https://github.com/deepseek-ai/deepseek-harness/commit/dae5844f93c60d9c366bb89afc9ceddbd3696135))
- fix(auto-review): stabilize reviewer decisions ([5a99cd9](https://github.com/deepseek-ai/deepseek-harness/commit/5a99cd9a47576517b0526fb6a44037b37049ba9a))
- fix(auto-review): carry lifecycle cancellation to dispatch ([0df80cd](https://github.com/deepseek-ai/deepseek-harness/commit/0df80cdf4127daa2263ed9cf17225d0c3f493a47))
- fix(web): keep an install or confirmation alive across the reads its own changes trigger ([84bed2e](https://github.com/deepseek-ai/deepseek-harness/commit/84bed2e7444abfe57646ef621c3b05194cc92814))
- fix(plugins): recognize the harness cordis copy by package directory ([6407ed8](https://github.com/deepseek-ai/deepseek-harness/commit/6407ed8a441b71568bee25acd4a2b86aeabc000a))

### 📝 Documentation
- docs(auto-review): clarify teardown ordering ([3879243](https://github.com/deepseek-ai/deepseek-harness/commit/3879243d623687c17bcc6bf43391d5ef3cee4d5d))
- docs(auto-review): avoid deterministic output claim ([ca8d65e](https://github.com/deepseek-ai/deepseek-harness/commit/ca8d65e5c4ace22a7206d23008697426856fd9a0))
- docs: refresh auto review event listeners ([96c29c2](https://github.com/deepseek-ai/deepseek-harness/commit/96c29c2e6ad13cc72db2ea0c35e4386b89be276b))

### 🔧 Configuration
- chore(docs): bring the Chinese event catalog along with the regenerated source links ([b1a1b1a](https://github.com/deepseek-ai/deepseek-harness/commit/b1a1b1a7aba21f439b6e329bbdad630e4edfeb75))
- chore(docs): regenerate the module graph and event catalog for the plugin manager's agent dependency ([3dd4a9a](https://github.com/deepseek-ai/deepseek-harness/commit/3dd4a9a8737ca7ecffaa3ccbb6faaa3fa7fdc395))
- ci(e2e): isolate auto certification ([91b504e](https://github.com/deepseek-ai/deepseek-harness/commit/91b504e63e900d825e1ac9d1bbece0e206a87650))
- ci(e2e): serialize shared-key real-model tests ([e686325](https://github.com/deepseek-ai/deepseek-harness/commit/e6863256f788e4391b76a5676c15be43025bf606))
- chore(docs): regenerate the config catalog after the plugin manager import change ([d926d39](https://github.com/deepseek-ai/deepseek-harness/commit/d926d39a1bc0ad71429be670c0ce22213c928ee6))

## 2026-09-05

**26 commits.** 3 feature changes, 8 fixes.

### 🆕 Features
- feat(web): count line and exceptions first for a pack's components ([e9c5a9d](https://github.com/deepseek-ai/deepseek-harness/commit/e9c5a9d2f1fb5fa85f3054a4c2521a57f51eba12))
- feat(web): move a preset's capabilities and settings onto its detail page ([d7d7b30](https://github.com/deepseek-ai/deepseek-harness/commit/d7d7b301d522df6bee6377183b67b2de9c422d78))
- feat(web): trim the plugin manager cards to name, one-liner, and switch ([a53fb14](https://github.com/deepseek-ai/deepseek-harness/commit/a53fb1497d603b0dd74e2d9fe54104c7acdc1378))

### 🐛 Bug Fixes
- fix(include): detach inserted rows so re-applying a patch list mounts the same tree ([8357838](https://github.com/deepseek-ai/deepseek-harness/commit/8357838bc5b0a9f2d2cf78efd4b055c5092c555e))
- fix(boot): report the package probe over IPC and validate what crosses the boundary ([0f95351](https://github.com/deepseek-ai/deepseek-harness/commit/0f95351405bf98b0a85bd89614b3454ee2364d91))
- fix(boot): commit a recomposition only once the root include accepts it ([0caceb2](https://github.com/deepseek-ai/deepseek-harness/commit/0caceb2ced28f17bec2ab0efac9c8aabe8b99bcc))
- fix(boot): compose external bundles in written order with one wrapper per target ([0914a15](https://github.com/deepseek-ai/deepseek-harness/commit/0914a152ff035ed8053c69a312a5b50265c073b6))
- fix(web): drop the duplicated manager stylesheet copy and keep the theme gate's border rules ([0606682](https://github.com/deepseek-ai/deepseek-harness/commit/060668290c2739916213f7e11de259194d24bf35))
- fix(web): pass the component filter class in the form the Input primitive accepts ([2ab225a](https://github.com/deepseek-ai/deepseek-harness/commit/2ab225a1086ae1d19b52fe9aec77db407d7712a0))
- fix(web): trash icon for preset row deletion, drop the not-mounted line ([0c40a81](https://github.com/deepseek-ai/deepseek-harness/commit/0c40a810cb1fd1820eeb73b24fd54a377f974c27))
- fix: align delegated preset snapshots ([c7fbe07](https://github.com/deepseek-ai/deepseek-harness/commit/c7fbe079f07385ec445cd0d1ccda20fdd297e856))

### 🔄 Refactoring
- refactor(boot): read a row failure's stage from the Loader's typed error ([d5613da](https://github.com/deepseek-ai/deepseek-harness/commit/d5613da2cb639d8116142332d06084d84496e53d))
- test(preset): cover the composition inventory's silent patch warning, anonymous inserts, and a layer gone before the read ([fe8c6a3](https://github.com/deepseek-ai/deepseek-harness/commit/fe8c6a365b9e6ddc0159666e4a391559a3123a05))
- refactor(plugins): name the install verb add, as the CLI does ([4cb2d7a](https://github.com/deepseek-ai/deepseek-harness/commit/4cb2d7abb50ee1b78be61ec9c4bea7c29b07a8ea))
- test(plugins): call the manager's add verb in the unresolvable-bundle case ([4d8e9c2](https://github.com/deepseek-ai/deepseek-harness/commit/4d8e9c222b6309562de7ba7e0d538cefaef51ba0))
- test(plugins): a staged package may declare a stage the profile refuses ([cc04382](https://github.com/deepseek-ai/deepseek-harness/commit/cc04382160de36657b76cddcbaf402fbe77ab8da))
- test(plugins): cover the removal of a bundle the profile cannot resolve ([26c4a32](https://github.com/deepseek-ai/deepseek-harness/commit/26c4a324a1127c14a0c1d647856c25b55998da0d))
- refactor(plugins): share the child close settlement with the package probe ([f43259f](https://github.com/deepseek-ai/deepseek-harness/commit/f43259f9de2244eada97584b7095fe1a939c081c))
- test(boot): cover the inventory's runtime attribution of rows and recorded failures ([1fd4743](https://github.com/deepseek-ai/deepseek-harness/commit/1fd4743154704cff73f70e983af8c10a25ada218))
- test(plugins): let the bare Loader assign the inventory spec's row ids ([cd1de58](https://github.com/deepseek-ai/deepseek-harness/commit/cd1de5867c84af61969dca400895603b92505379))
- refactor(web): build the plugin manager on the shared ui-primitives controls ([0af7ca4](https://github.com/deepseek-ai/deepseek-harness/commit/0af7ca4c10934118cbddcd2050e62c0b19afefa5))
- refactor(web): off components of a pack as chips grouped by reason ([ce9337d](https://github.com/deepseek-ai/deepseek-harness/commit/ce9337db4ed50009c53e13d8dd9158bc6e6ee059))
- test(web): align Auto denial goldens with composer ([492c374](https://github.com/deepseek-ai/deepseek-harness/commit/492c37494acaa961973a53a84eec385e968dc95a))

### 📝 Documentation
- docs(boot): describe declared ids, author-facing manifest keys, and refresh the catalogs ([613adbb](https://github.com/deepseek-ai/deepseek-harness/commit/613adbb23183d04c6c8f1e780b8759007a87e6f3))

### 🔧 Configuration
- chore(docs): regenerate the Cordis catalog for the manager's add verb ([eb818f9](https://github.com/deepseek-ai/deepseek-harness/commit/eb818f9c925e2d8016259737067a8a1a484ba448))
- chore(docs): regenerate the config catalog and make the patch-file README sketch compile ([6721308](https://github.com/deepseek-ai/deepseek-harness/commit/67213084d6476b24582d7c1046d420867e11c666))

## 2026-09-06

**4 commits.** 0 feature changes, 3 fixes.

### 🐛 Bug Fixes
- fix(web): revoke withdrawn permission choices ([fdeeace](https://github.com/deepseek-ai/deepseek-harness/commit/fdeeacef74ecb1b94663159ec14ac56a9a0a2a12))
- fix(permission): simplify Auto identity and teardown ([197161e](https://github.com/deepseek-ai/deepseek-harness/commit/197161e6608e6753e4715de4c5f75eaa0c8422c1))
- fix(auto-review): align risk policy and core certification ([2505fca](https://github.com/deepseek-ai/deepseek-harness/commit/2505fcaf97075801f8d90743aa37f5ae6be4044f))

### 🔄 Refactoring
- test(permission): cover Auto lifecycle and inheritance boundaries ([0861ee1](https://github.com/deepseek-ai/deepseek-harness/commit/0861ee11f737cafb279857373ae8884ceea422fa))

## 2026-09-07

**24 commits.** 4 feature changes, 6 fixes.

### 🆕 Features
- feat(web): switch a plugin pack's components one by one ([f4f7349](https://github.com/deepseek-ai/deepseek-harness/commit/f4f734964ad283ac19e95d67c1c6e6734558d795))
- feat(web): use Messages for the default DeepSeek provider ([c258d3c](https://github.com/deepseek-ai/deepseek-harness/commit/c258d3cf4ed76a2c0449c2d5dcbf37eaf8cb7b14))
- feat(web): configure DeepSeek Messages beside Chat Completions ([d282869](https://github.com/deepseek-ai/deepseek-harness/commit/d28286938d54c28f0144dc8a9d5bf9ce0af4ed2a))
- feat(llm): add DeepSeek Anthropic Messages adapter ([34154b6](https://github.com/deepseek-ai/deepseek-harness/commit/34154b6861160eb892985789eb65451487f57121))

### 🐛 Bug Fixes
- fix(ci): preserve trusted legacy policy during preflight rollout ([2eeab3e](https://github.com/deepseek-ai/deepseek-harness/commit/2eeab3e65fe34a619e61c6e36ed5452da60f015a))
- fix(ci): avoid unnecessary issue policy Project reads and lifecycle runs ([108c870](https://github.com/deepseek-ai/deepseek-harness/commit/108c87008b9c36e29acf8f4e4c1cb6bbc7526131))
- fix(llm): degrade unusable Messages replay metadata ([74ef3f0](https://github.com/deepseek-ai/deepseek-harness/commit/74ef3f05107e7819a8b60fbf12e4e65bf2dec92f))
- fix(web): remove Messages endpoint helper text ([57c6e7e](https://github.com/deepseek-ai/deepseek-harness/commit/57c6e7e9b2da5c1766a11b5f66755f114b22ad76))
- fix(session): tolerate contentless synthetic messages ([fdbeedd](https://github.com/deepseek-ai/deepseek-harness/commit/fdbeeddc367de3387b45eeb61b504ed20d9f673c))
- fix(boot): own the rows a config override sets, queue recompositions, and let records follow the configuration ([aaf58eb](https://github.com/deepseek-ai/deepseek-harness/commit/aaf58eb5bfdd4db30bec2cf0959b50c778fb5cff))

### 🔄 Refactoring
- refactor(ci): separate issue policy rules transport and lifecycle owners ([845acdb](https://github.com/deepseek-ai/deepseek-harness/commit/845acdb3b7f6f41431204cfcf111b2b6f8c870c0))
- test(llm-retry): cover the surface node that derives no message ([e44eb89](https://github.com/deepseek-ai/deepseek-harness/commit/e44eb8906534e0a1f573fe717d54b343f6ee4c8e))
- refactor(session, llm): cut the image offload surface to its callers ([523ae08](https://github.com/deepseek-ai/deepseek-harness/commit/523ae08a2dba1f5b531516389ce34f01fe434849))
- refactor(plugin-manager): split the manager module by responsibility ([e0841be](https://github.com/deepseek-ai/deepseek-harness/commit/e0841bec015e144e2a08bec011289320b04293a4))
- refactor(app-boot): fold the patch-file parser and writer into app-boot ([7af9c25](https://github.com/deepseek-ai/deepseek-harness/commit/7af9c25737c36681adaa74739705d5ee5535d21e))
- refactor(plugin-manager): move plugin management out of the Web host ([7b713ca](https://github.com/deepseek-ai/deepseek-harness/commit/7b713ca83b42d8f3832d232825d5d24471ed8036))
- refactor(session): fold the image offload helpers into surface.ts and index.ts ([ab93bfd](https://github.com/deepseek-ai/deepseek-harness/commit/ab93bfd90c8570b3f3544bc304853e1a34859ca2))
- refactor(llm): recover IMAGE_OFFLOAD_REQUIRED in llm-retry instead of a new plugin package ([fcb976d](https://github.com/deepseek-ai/deepseek-harness/commit/fcb976d3dc639beea216d487f70cb1af5de01090))
- refactor(agent-presets): remove the global-tool-mask package nothing composes ([4276497](https://github.com/deepseek-ai/deepseek-harness/commit/42764971ca4942904de4e23279e5272bf927cfbb))
- refactor(llm): move image offload planning into a plugin and trim the change surface ([8c7b023](https://github.com/deepseek-ai/deepseek-harness/commit/8c7b023d6ce919544ac53aad562970849e8c1fc4))
- test(snapshot): follow persona prefix config ([74f3808](https://github.com/deepseek-ai/deepseek-harness/commit/74f380806f6b0d14c8706e794ac4c5d7f355f659))
- test(session): close image offload coverage gaps ([5e277c2](https://github.com/deepseek-ai/deepseek-harness/commit/5e277c211169ef59b692765a95049604ed1b4287))
- test(inventory): compare listed entries in id order, as a digit-only assigned id reorders the store ([66a9d0e](https://github.com/deepseek-ai/deepseek-harness/commit/66a9d0e7c3c7325d6b6306641e0bdd71ec074d67))

### 📝 Documentation
- docs(plugin-manager): make the README examples self-contained ([8a0aecc](https://github.com/deepseek-ai/deepseek-harness/commit/8a0aecccccb8d38f9e4aff1ea0c77dc4aa35c326))

## 2026-09-08

**46 commits.** 8 feature changes, 16 fixes.

### 🆕 Features
- feat(web): render each pnpm run of an install as a terminal ([07589e1](https://github.com/deepseek-ai/deepseek-harness/commit/07589e1c326521f8785c1052969aa55100abc981))
- feat(plugin-manager): name the profile directory on install-log chunks ([6605c4d](https://github.com/deepseek-ai/deepseek-harness/commit/6605c4de48227148b29ee15a9bcd6a1a5b278179))
- feat(plugin-manager): keep pnpm's colours and name the command on install-log chunks ([080e22e](https://github.com/deepseek-ai/deepseek-harness/commit/080e22ee036bb4d89d942f1532c236ea73a8853d))
- feat(web): ask before switching a row off that other rows depend on ([107d076](https://github.com/deepseek-ai/deepseek-harness/commit/107d07614afe40ee5060da67c9ccbbf90f3c6499))
- feat(web): read a row's wait for a service as one state ([6148b6d](https://github.com/deepseek-ai/deepseek-harness/commit/6148b6ddba8315d452aa3a8e9038160763eb3e9b))
- feat(web): group the plugin list by packs and plugins, and quiet the row states ([acbb8e0](https://github.com/deepseek-ai/deepseek-harness/commit/acbb8e0a0692a15229d569b63d0c7482440cb345))
- feat(web): style a pack's rows as entries and drop the done notice ([2df9414](https://github.com/deepseek-ai/deepseek-harness/commit/2df9414138e8b2b91dcb12d2379c6309c79ce0a4))
- feat(web): give every plugin package its own page ([483e6b4](https://github.com/deepseek-ai/deepseek-harness/commit/483e6b4920f00794e5e7555e35d34e009be4fb95))

### 🐛 Bug Fixes
- fix: include package-index links and align residual metadata ([3b27563](https://github.com/deepseek-ai/deepseek-harness/commit/3b27563290a9fbda9a477d36d1a2fd47e1d97d62))
- fix(web): count the scoped mutate branch and draw the breadcrumb separator as a hairline ([e1c3ec0](https://github.com/deepseek-ai/deepseek-harness/commit/e1c3ec00e2ee43bbc46e6e8be3bed126a724ab1c))
- fix(app-boot): keep the probe's stderr tail across reads of any size ([a8f2e84](https://github.com/deepseek-ai/deepseek-harness/commit/a8f2e849469984006bf4ef8a0f299b28fded548e))
- fix(app-boot): record user-disabled bundles in the profile manifest ([07878ae](https://github.com/deepseek-ai/deepseek-harness/commit/07878ae1d3f9a251ef992d84c90e4d9aef901912))
- fix(web): name the package-group title field as a key ([2f181a7](https://github.com/deepseek-ai/deepseek-harness/commit/2f181a75ef104676d58404c6af9be1e27089a6ec))
- fix(web): name the confirmation copy map's fields as keys ([3787829](https://github.com/deepseek-ai/deepseek-harness/commit/3787829d759a6723a6269145feba040dbf592060))
- fix(plugin-manager): ask the runtime which rows the user disabled ([5694e50](https://github.com/deepseek-ai/deepseek-harness/commit/5694e505482eac2ccaa62425957219e99b09b238))
- fix(boot): answer user-disabled entries from the profile runtime ([c73d88e](https://github.com/deepseek-ai/deepseek-harness/commit/c73d88e4e55306f7e62850a812e16a034ef20476))
- fix(boot): judge a package's cordis copy by package directory ([792a684](https://github.com/deepseek-ai/deepseek-harness/commit/792a68468f619ffabecf857e70c4de1a4022fd7f))
- fix(boot): commit user-disabled rows with the composition and name a user row's trust ([20102bc](https://github.com/deepseek-ai/deepseek-harness/commit/20102bcd527bc1136ba1a3829e21febfb5e5028f))
- fix(boot): harden the package probe's child ([6bc5e97](https://github.com/deepseek-ai/deepseek-harness/commit/6bc5e978ae05774dabb844a6d49b742981f5198e))
- fix(boot): keep disabled bundles disabled across runs and catch config-override duplicates ([5f0ad7c](https://github.com/deepseek-ai/deepseek-harness/commit/5f0ad7c4b1cb2dafa966753fbf75484768ae84cb))
- fix(web): show an install's removal runs in its dialog ([e23030c](https://github.com/deepseek-ai/deepseek-harness/commit/e23030cb306a2fe11af0f6b6e68390c67ac52441))
- fix(web): ask what depends on a row or a pack before any dialog opens ([e37f47f](https://github.com/deepseek-ai/deepseek-harness/commit/e37f47fc536375b54409726d11c3bf814666537f))
- fix(boot): drop a row's recorded wait once its service appears ([4d83c2c](https://github.com/deepseek-ai/deepseek-harness/commit/4d83c2c71fb956c79fa8031d57350c252271cb46))
- fix(web): drop the grid rules the row restyle left behind ([ddb15a1](https://github.com/deepseek-ai/deepseek-harness/commit/ddb15a11a40752dbc4ef8c9f7722915ff4e512f9))

### 🔄 Refactoring
- refactor: align instruction and job helper symbols ([6c3c306](https://github.com/deepseek-ai/deepseek-harness/commit/6c3c3064c39a6836eec6c408d5f10109839dd930))
- refactor(web): share the enable switch, the notice line and the form observer plumbing ([ea624de](https://github.com/deepseek-ai/deepseek-harness/commit/ea624def34d16057ae4f4c7f824173539cbd2f0d))
- refactor(settings): keep each event's literal dispatch at its call site, share only the delivery loop ([e5196d8](https://github.com/deepseek-ai/deepseek-harness/commit/e5196d85ed778d282c7df2ee22f3f91be19d846c))
- refactor(settings): share the contained event fan-out between commit and document updates ([ff94876](https://github.com/deepseek-ai/deepseek-harness/commit/ff94876574416949fd872407886f16798123d6e6))
- refactor(boot): keep containment and composition internals off the package root ([afa57ae](https://github.com/deepseek-ai/deepseek-harness/commit/afa57ae09373d41f65d11dcd155290dcc310f191))
- test(web): compose the scaffold's stack with its user-disabled rows ([af2ebda](https://github.com/deepseek-ai/deepseek-harness/commit/af2ebda8923ff39b135b16be1285c03b4d6e90b3))
- test(inventory): give the runtime its install anchor ([22f92a8](https://github.com/deepseek-ai/deepseek-harness/commit/22f92a8297769ce4ce550eb806af171411570689))
- test(boot): type the id-less group row in the ownership spec ([d6f5160](https://github.com/deepseek-ai/deepseek-harness/commit/d6f5160591da63ec00664971357e5eae6e8631be))
- test(web): refresh Messages composer and timezone snapshots ([914dec6](https://github.com/deepseek-ai/deepseek-harness/commit/914dec6fea4671bfcb6bd84e7ba21caf5b40c8d5))
- refactor(compaction): own image offload as a compaction executor ([4779f05](https://github.com/deepseek-ai/deepseek-harness/commit/4779f054b6c8b6e0a503106d4164fc11cfbbaa60))
- refactor(llm-retry, session): offload images by surface replacement instead of a watermark event ([6329c53](https://github.com/deepseek-ai/deepseek-harness/commit/6329c53a3737c3db12a362b10322699415e0d016))
- test(web): align Messages snapshot with Sidebar ([fa48b10](https://github.com/deepseek-ai/deepseek-harness/commit/fa48b101d2dc004a622c6ebc389694d6f55b7a32))
- test(llm-retry): follow agent loop testkit dependencies ([52386ec](https://github.com/deepseek-ai/deepseek-harness/commit/52386ec6fbb381333c65862c6170bcfb6a5e345b))

### 📝 Documentation
- docs: correct surviving package and service references ([739285c](https://github.com/deepseek-ai/deepseek-harness/commit/739285c813e4e7387920646409afe50f72e411a6))
- docs(plugin-manager): name the disabled-bundle record the installer keeps ([aee2d84](https://github.com/deepseek-ai/deepseek-harness/commit/aee2d84cc555ec7589ab8b3c6f68ee50e5c8343a))
- docs(plugin-manager): keep the package summaries within the summary budget ([ca291b0](https://github.com/deepseek-ai/deepseek-harness/commit/ca291b010012145dea566e2340292bc70af78cb1))
- docs(llm): drop the last watermark wording from llm-streaming and the retry test title ([6b673ae](https://github.com/deepseek-ai/deepseek-harness/commit/6b673aedf5b938697888327479fc756d101261f4))
- docs(plugin-manager): give the README installer example its colour option ([5953d29](https://github.com/deepseek-ai/deepseek-harness/commit/5953d2920c1a8e7dd74b74564e481970e6fb9c95))
- docs(graphs): list app-boot among the consumers of internal/status ([43ba51d](https://github.com/deepseek-ai/deepseek-harness/commit/43ba51d585a49ee8db3d999aec3a948ab87f89a6))

### 🔧 Configuration
- chore(llm-deepseek-messages): align version with master ([1f88b9c](https://github.com/deepseek-ai/deepseek-harness/commit/1f88b9cd8f9db5ef1ecf67a4a8911c8577d51ee1))
- chore(client): regenerate the slot catalog after the master merge ([9d9b39a](https://github.com/deepseek-ai/deepseek-harness/commit/9d9b39a41bcc014b9e91c44f7438122bd119230b))
- chore(plugin-manager): follow the root version bump ([7868fdc](https://github.com/deepseek-ai/deepseek-harness/commit/7868fdcf3bb1ae2fd0d05449148cc6d1955e1b5c))

## 2026-09-09

**85 commits.** 15 feature changes, 40 fixes.

### 🆕 Features
- feat(boot): distinguish required startup failures ([bd4cfc7](https://github.com/deepseek-ai/deepseek-harness/commit/bd4cfc7c46102be71a2794f2e3084c6c001f5a3f))
- Remove nonessential remnants of Cordis PR 932 ([d225dbb](https://github.com/deepseek-ai/deepseek-harness/commit/d225dbba5034298505246fa81625d30e3db994a4))
- feat(trajectory): add a PTC code inspector ([632b8e1](https://github.com/deepseek-ai/deepseek-harness/commit/632b8e19b4ba1297bc8c5931ab209b8d010d8ed2))
- feat(trajectory): remember JSON string wrapping preference ([3a32c61](https://github.com/deepseek-ai/deepseek-harness/commit/3a32c617a3436f0e9451a0dd08dfe75b62255294))
- Adapt current consumers to nontransactional Cordis Loader ([2abb542](https://github.com/deepseek-ai/deepseek-harness/commit/2abb542a222032b1ad3c5abd7bb65ffffe15b8de))
- Revert #932 transactional Cordis reload changes ([e07f41d](https://github.com/deepseek-ai/deepseek-harness/commit/e07f41d5fd8ca172287fda0f923b4d1f69c592f3))
- feat(client): expand reasoning-only assistant output by default ([1549483](https://github.com/deepseek-ai/deepseek-harness/commit/1549483397c82551a2d28e2be3e78aabc494aa77))
- feat(client): show expanded JSON strings as raw text ([819c2b2](https://github.com/deepseek-ai/deepseek-harness/commit/819c2b2442c8025534747b28eeb3ae3501da4d2a))
- feat(web): add interactive sidebar terminals ([e15a9b1](https://github.com/deepseek-ai/deepseek-harness/commit/e15a9b1beccdfdeee11eee72d5c489752cde7f2d))
- feat(client): improve trajectory JSON string display ([18739de](https://github.com/deepseek-ai/deepseek-harness/commit/18739de7c62b9cfa25c1fffd056e8c7c83e8960b))
- feat(agent): await initialization through agent/created ([9b7a8cc](https://github.com/deepseek-ai/deepseek-harness/commit/9b7a8ccc9fabc2e87386acf7f8b0741baf978022))
- feat(headless): add stdin task, --session-id, and --json run events ([ba6a90d](https://github.com/deepseek-ai/deepseek-harness/commit/ba6a90d2f2087c567e26620d1fcd30d6fa048d81))
- feat(web): move plugin management to the sidebar's Plugins panel ([0aeebb0](https://github.com/deepseek-ai/deepseek-harness/commit/0aeebb017ef777b1adf8e4cbb91fb8b0c0811b89))
- feat(permission): add experimental Auto review ([55e5390](https://github.com/deepseek-ai/deepseek-harness/commit/55e53907ab90ab8319e591d04d3af51cdc70f5f8))
- feat(llm-deepseek-messages): support in-history system prompt updates ([e5feedd](https://github.com/deepseek-ai/deepseek-harness/commit/e5feedd14f0ab6b4495d97b2e7b9aa61a32965dc))

### 🐛 Bug Fixes
- fix: address concrete terminology review findings ([2b05a43](https://github.com/deepseek-ai/deepseek-harness/commit/2b05a43eca47bb7fc581d85ebe6dd2881900e38b))
- fix(web-app): gate readiness on required startup entries ([97d1f7c](https://github.com/deepseek-ai/deepseek-harness/commit/97d1f7c20397e94881b5bdd6e38f1f3d48538fcb))
- fix(boot): limit required IDs to application endpoints ([7fd41b8](https://github.com/deepseek-ai/deepseek-harness/commit/7fd41b833b7a16bf748d8b22d8cb314960be9b92))
- fix(boot): preserve failure policy on nontransactional Loader ([f4a7dd6](https://github.com/deepseek-ai/deepseek-harness/commit/f4a7dd607709025bc3ad19dab8ffbb038cd13962))
- fix(headless): omit step usage when any attempt lacks a sample ([a69933d](https://github.com/deepseek-ai/deepseek-harness/commit/a69933d3e5684923fee21002a4c69c41b456884a))
- fix(headless): close the v11 review gaps in the json run surface ([980b4b7](https://github.com/deepseek-ai/deepseek-harness/commit/980b4b77af0b3b263becceb79c406aa358e1a8ba))
- fix(headless): count the line terminator inside the 32 KiB event cap ([b3f6c5e](https://github.com/deepseek-ai/deepseek-harness/commit/b3f6c5e9913f44948299a29d00b3597c83c259e9))
- fix(headless): require the query service for every --session-id run ([755b44b](https://github.com/deepseek-ai/deepseek-harness/commit/755b44bbcdb58b10dc6f4b7380e7b98edaabc756))
- fix(web): restore terminal snapshots across host and sidebar lifecycles ([d28625c](https://github.com/deepseek-ai/deepseek-harness/commit/d28625c6d5397cac5046d08eb3440348b7cd6c56))
- fix(trajectory): identify PTC calls from recorded tool metadata ([b685878](https://github.com/deepseek-ai/deepseek-harness/commit/b6858789f0513079fcd16fbbe4bfe6348e489076))
- fix(client): isolate JSON copy feedback and guard string measurement ([e7fc4e8](https://github.com/deepseek-ai/deepseek-harness/commit/e7fc4e8fdc34a375ff5a4883bfa98766bb4fc855))
- fix(agent-loop): preserve standalone inbox registration ([0ed47fe](https://github.com/deepseek-ai/deepseek-harness/commit/0ed47fe860262cb434ceeb94fdb3e97edc523e5d))
- fix(snapshots): preserve released inline image fixture ([5b8c445](https://github.com/deepseek-ai/deepseek-harness/commit/5b8c445eebef155f7934ac0faec033fbe9a4c224))
- fix(headless): fail closed on malformed preset records and unroundtrippable args ([7a4a55f](https://github.com/deepseek-ai/deepseek-harness/commit/7a4a55f30b6794db0fb482445a28a2e95bd176d3))
- fix(headless): require persistence for every --session-id path ([a5c21a6](https://github.com/deepseek-ai/deepseek-harness/commit/a5c21a69b8abe545981faad7a3bda0041aa36de2))
- fix(headless): fail loud when --session-id would create a non-durable session ([b3756a8](https://github.com/deepseek-ai/deepseek-harness/commit/b3756a89d1d1bd5bd5f6c7e30c6f0d1b8eeead9f))
- fix(trajectory): show turn and ordinal step in detail titles ([f36e1a3](https://github.com/deepseek-ai/deepseek-harness/commit/f36e1a3d1d1f4c291b010636b84eb2ea8bf8aca5))
- fix(trajectory): expand preview thinking by default ([f0810ed](https://github.com/deepseek-ai/deepseek-harness/commit/f0810edd7fc6a6467d3ee7d25b6c07d3deff9d9e))
- fix(web): harden sidebar terminal lifecycle and recovery ([0a52560](https://github.com/deepseek-ai/deepseek-harness/commit/0a525601a76ea0f37faab1ad29e9eb11b2319c6e))
- fix(headless): cap the bounding recursion depth and route error events through the line cap ([3488db7](https://github.com/deepseek-ai/deepseek-harness/commit/3488db77bfee956768147b88941ac521469b0656))
- fix(headless): bound whole events, re-check adoption after resume, tighten --json scan ([0ca42f3](https://github.com/deepseek-ai/deepseek-harness/commit/0ca42f3b7892cd9369be2011969856d60c8de71c))
- fix(web): preserve newer projections across control baselines ([813ad96](https://github.com/deepseek-ai/deepseek-harness/commit/813ad965f9f478da6832672501447b08e32d17c5))
- fix(web): align terminal preview, styles, and snapshots ([00b16cb](https://github.com/deepseek-ai/deepseek-harness/commit/00b16cb63ae571093ef54183cbc1ce026476666c))
- fix(client): use a collapse icon for expanded JSON strings ([c6fb28a](https://github.com/deepseek-ai/deepseek-harness/commit/c6fb28a16468c6e36e8c5d36ccaf9d1e2afff5f9))
- fix(trajectory): clarify overview overflow and tighten spacing ([e4f0871](https://github.com/deepseek-ai/deepseek-harness/commit/e4f0871b80b2d0218c94e207aa87d71be720a149))
- fix(trajectory): narrow Chinese role column ([ac09b7b](https://github.com/deepseek-ai/deepseek-harness/commit/ac09b7b51980219614ba3300064a064c27b8a980))
- fix(headless): publish the shared chunk and read the session's current preset ([3797127](https://github.com/deepseek-ai/deepseek-harness/commit/3797127eb2813791915a8394b6a5232adde10ad1))
- fix(agent): preserve initialization failure during teardown ([0fb509f](https://github.com/deepseek-ai/deepseek-harness/commit/0fb509f54497623f16f3dc402d8340d820c1c0d5))
- fix(client): restore assistant timing from recorded streams ([e779831](https://github.com/deepseek-ai/deepseek-harness/commit/e779831f403239d3a3cc3313be7b6bc4580d7596))
- fix(web): invalidate projections before opening control snapshots ([9cd0c70](https://github.com/deepseek-ai/deepseek-harness/commit/9cd0c703dfc473e55d732b28000735f10cb30781))
- fix(headless): address re-review findings on the machine-readable run surface ([45032ea](https://github.com/deepseek-ai/deepseek-harness/commit/45032ea1bdaad57f5ceb4360beff5a405217592f))
- fix(ptc): preserve literal braces in generated SDK prompts ([96a1749](https://github.com/deepseek-ai/deepseek-harness/commit/96a1749db6cc0c6912ce90204ac46cb01085e009))
- fix(trajectory): hide timing source in overview ([0e468a6](https://github.com/deepseek-ai/deepseek-harness/commit/0e468a62f6f3512024471a025dd70f7b4332c327))
- fix(agent-team): append durable identity reminders after fork history ([291b890](https://github.com/deepseek-ai/deepseek-harness/commit/291b890a1aac608f742260bf7969d73b1e1981e8))
- fix(web): discard projection state across host generations ([f3332af](https://github.com/deepseek-ai/deepseek-harness/commit/f3332af2a441e03db2ddc655e7995d371cf103fd))
- fix(web): declare the conversation agent project reference ([e101c44](https://github.com/deepseek-ai/deepseek-harness/commit/e101c448e54faefddce27ba63a60abd275759abb))
- fix(headless): project committed content and scope live adoption ([ba6e198](https://github.com/deepseek-ai/deepseek-harness/commit/ba6e19809dd9e21ec08dafdd8dc6ae560c508f3c))
- fix(web): reconcile durable inbox recovery with master ([72f2e71](https://github.com/deepseek-ai/deepseek-harness/commit/72f2e71070925993edab0de8e59a20fe5df60f4c))
- fix(auto-review): preserve nested trajectory errors and optional peer ([ad93e2f](https://github.com/deepseek-ai/deepseek-harness/commit/ad93e2f6020fd49a751d8a97e795c3974522b5c7))
- fix(permission): revoke stale Auto choices and simplify review paths ([41fbde8](https://github.com/deepseek-ai/deepseek-harness/commit/41fbde80348c3a22eac6c940b3c8a459a79cd960))

### 🔄 Refactoring
- test(boot): cover startup diagnostic variants ([f308742](https://github.com/deepseek-ai/deepseek-harness/commit/f3087420507ec0d26c1583f7201f3e4eca50b159))
- test(boot): type fixture fiber state ([941267b](https://github.com/deepseek-ai/deepseek-harness/commit/941267b197709fcab1b2980dcbcbdd7914a7102e))
- test(boot): keep required fixture failures fatal ([fbcad25](https://github.com/deepseek-ai/deepseek-harness/commit/fbcad258ad1c7c5406d4d8fc3a64ed0a533b7b9a))
- refactor(client): remove unused JSON disclosure locale keys ([29c09d3](https://github.com/deepseek-ai/deepseek-harness/commit/29c09d320fd9d2325c034ed1bcc15bc01354486c))
- test(trajectory): pin thinking defaults when switching records ([2bc1a7e](https://github.com/deepseek-ai/deepseek-harness/commit/2bc1a7e347174c2bf14bc8d0e661f150ff101a3e))
- refactor(client): share the line wrapping icon ([573b044](https://github.com/deepseek-ai/deepseek-harness/commit/573b0443207a7d214255b85e30f35db2ee815a34))
- test(chat): collapse live thinking before checking its tail ([a9b5fae](https://github.com/deepseek-ai/deepseek-harness/commit/a9b5faef0b3cad409ea3331105fdb571823416bd))
- test(trajectory): omit absent optional fixture fields ([508490b](https://github.com/deepseek-ai/deepseek-harness/commit/508490b531324bb611ae91463b1ed4874d66934c))
- test(client): cover raw JSON strings and wrapping preferences ([9c6b282](https://github.com/deepseek-ai/deepseek-harness/commit/9c6b282535675cf2a1d62c1e07a346d6425b046c))
- test(trajectory): expect ordinal step detail titles ([5230c60](https://github.com/deepseek-ai/deepseek-harness/commit/5230c6052572af05ceb80fe301a23a1c79dd7862))
- test(client): cover assistant thinking disclosure defaults ([a73aca1](https://github.com/deepseek-ai/deepseek-harness/commit/a73aca1978c22adbd8927ce08472cc1d9628b7c8))
- test(ptc): strengthen literal prompt assertions ([e1f0911](https://github.com/deepseek-ai/deepseek-harness/commit/e1f09116187d64cc1b800f838d4d3a8db53a6250))
- refactor(ptc): share the prompt section return type ([5a673b8](https://github.com/deepseek-ai/deepseek-harness/commit/5a673b8a59b3b0eb7962587019f37998ec032133))
- test(agent): complete awaited creation migration ([aeb1341](https://github.com/deepseek-ai/deepseek-harness/commit/aeb13413c71e0b20a0440d617e7e82ebd88b7ae9))
- test(ptc): align workspace snapshot with shared SDK prompt ([e4be27d](https://github.com/deepseek-ai/deepseek-harness/commit/e4be27d1d9f3929d470c9bbd0f97c36e736972fa))
- test(headless): close per-file coverage on the run projection ([0e7361a](https://github.com/deepseek-ai/deepseek-harness/commit/0e7361a4890238756ccb312a1d0285baeaeaa954))
- style(web): open a package's page from its whole card and move its actions into the head ([8249d54](https://github.com/deepseek-ai/deepseek-harness/commit/8249d54e477be5065d912a4af63e354ede3aed4e))
- refactor(web): rename ui-settings-plugin-manager to ui-plugin-manager ([0897483](https://github.com/deepseek-ai/deepseek-harness/commit/08974835d704d074cc7e07f302c7657df2c9a84c))
- style(web): open a package's page from its title and clamp card descriptions ([34a2797](https://github.com/deepseek-ai/deepseek-harness/commit/34a279743df17bd9cc668818fe6c99be498408f9))
- style(web): centre the plugin management column ([541dee4](https://github.com/deepseek-ai/deepseek-harness/commit/541dee461bbf4dbac9720f76b66efcd90f2414b6))
- test(web): refresh the preset-detail golden for master's tool-present row ([5d90477](https://github.com/deepseek-ai/deepseek-harness/commit/5d90477cb1f738e53f4f1ce1633490cd029a408e))

### 📝 Documentation
- docs(headless): regenerate module graph for the run projection ([8662afb](https://github.com/deepseek-ai/deepseek-harness/commit/8662afb530c7195f5b8b2a3761854f76eb9aa634))
- docs(headless): regenerate event producer graph and restore model-selection note ([d5fe1fb](https://github.com/deepseek-ai/deepseek-harness/commit/d5fe1fb887441fe0a16fc0c79f72ab7a722ed8b8))
- docs: mirror the regenerated event matrix rows in the zh copy ([e755084](https://github.com/deepseek-ai/deepseek-harness/commit/e755084dfbd4835ee3e35872c3b2559137fa03e4))
- docs: regenerate the event producer-consumer matrix after the master merge ([e070e1e](https://github.com/deepseek-ai/deepseek-harness/commit/e070e1e0747fec467a13d2d15c68f4ac92e27055))
- docs(architecture): point the external-bundle paragraph at the app-boot README ([5528446](https://github.com/deepseek-ai/deepseek-harness/commit/5528446814ed684f28a2ff41d80762063b982394))

### 🔧 Configuration
- ci: re-trigger the pull-request run after the superseded run was dropped ([d2dc505](https://github.com/deepseek-ai/deepseek-harness/commit/d2dc505830c00d2bc17df798e15f93e45952c080))
- chore(client): regenerate the slot catalog after the master merge ([dd3e690](https://github.com/deepseek-ai/deepseek-harness/commit/dd3e690ef88651b413ab788f307aa51336803b46))
- merge: reconcile experimental Auto review implementation ([9cfb120](https://github.com/deepseek-ai/deepseek-harness/commit/9cfb120a638de24a6a2e6e4e5a1c6d7d32cad702))
- chore(plugin-manager): align the package versions with release 0.1.5-alpha.1 ([8d8a69f](https://github.com/deepseek-ai/deepseek-harness/commit/8d8a69f4238dafc9bfba3eee84cad6a6730038de))

## 2026-09-10

**52 commits.** 10 feature changes, 18 fixes.

### 🆕 Features
- feat(desktop): integrate native Windows installer design ([52bc792](https://github.com/deepseek-ai/deepseek-harness/commit/52bc79284f04119145568951385d13605e5eeb93))
- Classify disabled expression errors in startup audits ([25d5efc](https://github.com/deepseek-ai/deepseek-harness/commit/25d5efcd86f8b7ede90dfc47e67d3bb1684cbb3d))
- Require Web modules and connection during startup ([f5b5a9d](https://github.com/deepseek-ai/deepseek-harness/commit/f5b5a9da5108d4f17906bbc7015609cb6a5d734c))
- Retain awaited client cleanup after rebase ([39e6e6f](https://github.com/deepseek-ai/deepseek-harness/commit/39e6e6fb891dc9e83b73cb4a67f72187cc5d93fb))
- Align client boot import failure test with reverted Loader ([0e65054](https://github.com/deepseek-ai/deepseek-harness/commit/0e6505454e868c08fa3418d0a773da3655bb1d73))
- feat(sidebar): refine the connection indicator states and styling ([626fa81](https://github.com/deepseek-ai/deepseek-harness/commit/626fa816a5be314f26b64b5399b61f1cbc5a1547))
- feat(compaction): record image offload decisions without message replacement ([b5e7fca](https://github.com/deepseek-ai/deepseek-harness/commit/b5e7fca4a53892b7c26eaca7c7d1fe1b91229fa1))
- feat(headless): require --session-id to name an existing Session ([ea84ad3](https://github.com/deepseek-ai/deepseek-harness/commit/ea84ad31b6474cabbc8befe774703ee0e6119789))
- Preserve nested plugin errors after Cordis revert ([2376d21](https://github.com/deepseek-ai/deepseek-harness/commit/2376d210bd776d2a529fc4e0e4342b7a83ed7510))
- feat(llm): sync V41 Messages catalog and keep Web on Chat Completions ([4af56cf](https://github.com/deepseek-ai/deepseek-harness/commit/4af56cf808f522f4c737d50b1fc102ce91abcc30))

### 🐛 Bug Fixes
- fix(desktop): preserve installer dependencies and validate keyboard navigation ([9255b08](https://github.com/deepseek-ai/deepseek-harness/commit/9255b08ed3f641fba1deee7d3619af5acf876983))
- fix(app-boot): bound cyclic startup error diagnostics ([4cd20c1](https://github.com/deepseek-ai/deepseek-harness/commit/4cd20c1a1eb11b0b1e2e84466a34896f2de5e944))
- fix(ci): derive Windows standby store from workspace volume ([e46cb49](https://github.com/deepseek-ai/deepseek-harness/commit/e46cb49103ef35f4ee3dc12f4fc201906f849737))
- fix(desktop): separate default port and replace plugin update prompt ([8345ac1](https://github.com/deepseek-ai/deepseek-harness/commit/8345ac129ea269dd7b26dd84f9960db290bbebce))
- fix(workspace): pause current ordering in manual mode ([4857614](https://github.com/deepseek-ai/deepseek-harness/commit/4857614be0fb4c11668ad195ce5e6f4b3c336a58))
- fix(sidebar): keep one reconnect label and confirm recovery from visibility ([11ca802](https://github.com/deepseek-ai/deepseek-harness/commit/11ca8020cdf3b367168536a1b343ac2348c08a95))
- fix(web): shorten English question skip label ([69db89f](https://github.com/deepseek-ai/deepseek-harness/commit/69db89f84899f3a6bcf36affa48a8179ebe5d5de))
- fix(web): shorten Chinese question skip label ([2eed936](https://github.com/deepseek-ai/deepseek-harness/commit/2eed93628c0f447cbc2c38e4068fe13165d7ec2a))
- fix(headless): waive the deferred Session history read ([71b2cc8](https://github.com/deepseek-ai/deepseek-harness/commit/71b2cc80aa219f9211cd245de280e4bb37a0a47b))
- fix(ci): canonicalize browser dependency scan roots ([464e1cc](https://github.com/deepseek-ai/deepseek-harness/commit/464e1cce496617d98f6c3afed156517dee0ca00d))
- fix(headless): keep --json stderr free of commander's error print ([31be030](https://github.com/deepseek-ai/deepseek-harness/commit/31be030ccca14355eb9e8dee3653818f44f739ae))
- fix(boot): adapt plugin manifests to public package metadata ([fcb3882](https://github.com/deepseek-ai/deepseek-harness/commit/fcb3882e28c56356cba9050fd1ef39697efdd851))
- fix(llm-deepseek): 请求图片按 V4.1 token 网格投影 ([06c4915](https://github.com/deepseek-ai/deepseek-harness/commit/06c491508f5f2fa78afc6b0a3e8e9f6dc3fccfa9))
- fix(agent-team): include identity only in the initial task ([4491da1](https://github.com/deepseek-ai/deepseek-harness/commit/4491da13740ea8f4b749949dc228bf558ae9d06d))
- fix(headless): refuse a live Agent identity and finish the adopt-only docs ([9bcb1e2](https://github.com/deepseek-ai/deepseek-harness/commit/9bcb1e214c176a5e3e6fa8132cf314ce7ccf47d8))
- fix(workspace): derive recency independently of manual order ([8423b27](https://github.com/deepseek-ai/deepseek-harness/commit/8423b270e3fb129841bad581184cbc0473f738f8))
- fix(headless): align the adopt-only docs and prove resume end to end ([127d2c8](https://github.com/deepseek-ai/deepseek-harness/commit/127d2c8eb5ab8e64e3b220062dbe5d735d78ae42))
- fix(agent-team): keep member identity in durable reminders ([b76fe34](https://github.com/deepseek-ai/deepseek-harness/commit/b76fe343fe15275f967988786f106d10e9b86a68))

### 🔄 Refactoring
- refactor(desktop): share profile initialization and plugin management ([8c2fa73](https://github.com/deepseek-ai/deepseek-harness/commit/8c2fa73ceb7bd2b2719003beb72bdf82c552c562))
- refactor(desktop): run shared Web UI in a thin Electron shell ([e84a4e8](https://github.com/deepseek-ai/deepseek-harness/commit/e84a4e857ea227c13003c9421c7fb3130f503a78))
- test(workspace): stabilize sidebar captures and update blank placement ([a17f073](https://github.com/deepseek-ai/deepseek-harness/commit/a17f0733b1f17dd462011248c6c344b0748cfca5))
- test(python): restore concat through its spy ([884485e](https://github.com/deepseek-ai/deepseek-harness/commit/884485e7e6edec1a3633bef0a2ce2abd8cedfa09))
- test(python): make stray fragment coverage deterministic ([7bce0c2](https://github.com/deepseek-ai/deepseek-harness/commit/7bce0c26f5a2c752c70cfa56a8625f74f63b6264))
- test(web): pin the static connection pill in the lifecycle browser snapshot ([b044e45](https://github.com/deepseek-ai/deepseek-harness/commit/b044e45438a0bc9e8db44efbf2518363944d9cc1))
- test(sidebar): pin the refined connection indicator behavior and docs ([16e9865](https://github.com/deepseek-ai/deepseek-harness/commit/16e986548e8f39061a8b1d1f9999aa147f7a4e67))
- refactor(headless): move the runner process hooks out of the package entry ([3be1ea1](https://github.com/deepseek-ai/deepseek-harness/commit/3be1ea10b9a49261056c23a96257aa0a04824e6f))
- refactor(headless): keep the startup process seam out of the public entry ([6d05765](https://github.com/deepseek-ai/deepseek-harness/commit/6d057654051380fd6c0cf95e07beaf2844c25a40))
- test(web): retain historical Messages replay after provider consolidation ([59c1ee7](https://github.com/deepseek-ai/deepseek-harness/commit/59c1ee7c82cafa5c6e043dcce886bb4d26208cdd))
- refactor(llm): unify DeepSeek protocol implementations ([6a137ea](https://github.com/deepseek-ai/deepseek-harness/commit/6a137ea702ac13f201bbdfd12656da061596e8a7))
- refactor(attachment): 求解器留在 llm-deepseek，存储层只接收目标尺寸 ([ba30b73](https://github.com/deepseek-ai/deepseek-harness/commit/ba30b73f7b387d153ee46744ad1e8babd5d5debd))
- test(sdk): reuse serial creation header snapshots ([0600fa4](https://github.com/deepseek-ai/deepseek-harness/commit/0600fa405b0269a08aa9484a910d60b6521f0035))
- test(agent-loop): drop duplicate creation disposal case ([efa5294](https://github.com/deepseek-ai/deepseek-harness/commit/efa5294c0044298a76e39985b66bdafaba96abd0))
- refactor(agent): keep registry registration startup-only ([11656ca](https://github.com/deepseek-ai/deepseek-harness/commit/11656ca683a5c6efe0f2188a6ac2230a0152ba0d))
- refactor(loader-smoke): model the smoke cwd as a discriminated input ([9098a58](https://github.com/deepseek-ai/deepseek-harness/commit/9098a58f94f15e1c9b9f6ac08c32d408a1bdbb06))
- test(workspace): pin persisted mode ordering in Web replay ([6e94ee4](https://github.com/deepseek-ai/deepseek-harness/commit/6e94ee4fb9f58e2087d5cba458844a842b78fb93))
- test(agent-team): avoid racing initial admission settlement ([271268a](https://github.com/deepseek-ai/deepseek-harness/commit/271268a440c5779a37c2e7bc4cb3f3e260d2f161))

### 📝 Documentation
- docs(core): update session start source event reference ([8af1cb7](https://github.com/deepseek-ai/deepseek-harness/commit/8af1cb79f455991bed2396ea1f3fe95ca78b05e8))
- docs: refresh module graph after manifest merge ([8bdd473](https://github.com/deepseek-ai/deepseek-harness/commit/8bdd47366fef69f32a72d8f4a591981d0b440064))
- docs(headless): correct the adopt-only wording and lockfile attribution ([9b330b6](https://github.com/deepseek-ai/deepseek-harness/commit/9b330b653f1f5f2552ab21698c4509c06e08a054))
- docs: 同步请求图片投影文档与 Agent Note ([e17a736](https://github.com/deepseek-ai/deepseek-harness/commit/e17a736cc3823463dbdb00994bf4b979bf2f18ad))
- docs(agent-team): regenerate the message dependency graph ([d769e2d](https://github.com/deepseek-ai/deepseek-harness/commit/d769e2d1571f5d5f850c84ed7ec96eae1457f809))

### 🔧 Configuration
- merge: incorporate latest master into thin Electron branch ([b373c45](https://github.com/deepseek-ai/deepseek-harness/commit/b373c45648c638165b96783ecd975201a60e4885))

## 2026-09-11

**117 commits.** 15 feature changes, 43 fixes.

### 🆕 Features
- feat(ssh): checkpoint POSIX helper and remote providers ([4fb0fda](https://github.com/deepseek-ai/deepseek-harness/commit/4fb0fdac680a38a8832b555f94afe120af571262))
- feat(ptc): expose per-program timeout and sandbox approval controls ([a248cc4](https://github.com/deepseek-ai/deepseek-harness/commit/a248cc4e6460c212bf1ecf0df13e1b2f206472fa))
- feat(code-runtime): complete sandboxed Node execution and Session fixtures ([8e19ec4](https://github.com/deepseek-ai/deepseek-harness/commit/8e19ec4962767d795462b63e27cfcff4b3cf5138))
- feat(code-runtime): execute Node programs through confined processes ([75ed8da](https://github.com/deepseek-ai/deepseek-harness/commit/75ed8da3e0c9103b3b2174b2981b7129e1fba21d))
- feat(subprocess): carry a duplex control pipe through managed launches ([d8efd4f](https://github.com/deepseek-ai/deepseek-harness/commit/d8efd4f8cd59191465ff99beac82f56b9ffe1cf6))
- feat(ui-commands): swap the feedback command icon to a paper plane ([351b399](https://github.com/deepseek-ai/deepseek-harness/commit/351b3996396d4d35bd5dee59e927896784dd3567))
- feat(session): verify persistence type history ([1e9b05d](https://github.com/deepseek-ai/deepseek-harness/commit/1e9b05d35628f305cc35a17628a943bfb8515f31))
- feat(workspace-changes): record only git repositories and add the recorded card scenario ([0f8457a](https://github.com/deepseek-ai/deepseek-harness/commit/0f8457a017e3ff1ebbeff3e2e58b49bd57486da1))
- feat(web): record turn file changes with git snapshots and render the changed-files card ([f937f4e](https://github.com/deepseek-ai/deepseek-harness/commit/f937f4e23b1f4ee76e73e8f87f8c48a1ff8898ed))
- feat(desktop): apply designer icons to apps and Windows setup ([e12fbbc](https://github.com/deepseek-ai/deepseek-harness/commit/e12fbbcbb30d2c2f0480faeddb53ff7b632345ed))
- Use Electron Node runtime and replace Windows installations by directory ([bebf88d](https://github.com/deepseek-ai/deepseek-harness/commit/bebf88de4f97de4431c41604e17d2f47a2edcff6))
- feat(ci): cap blame approval weight at quarter ownership ([6e60940](https://github.com/deepseek-ai/deepseek-harness/commit/6e60940dedaa76101d4db08422afb6fda5f26938))
- feat(ci): weight approvals by production blame ownership ([cef92ed](https://github.com/deepseek-ai/deepseek-harness/commit/cef92ed40ba9884c9efd57c564a47f4385a680ba))
- Clarify token counts after aspect-preserving image projection ([f0f1988](https://github.com/deepseek-ai/deepseek-harness/commit/f0f1988a7a30c6722f61caa0817e22944cdc7088))
- feat(web): start the turn-level code diff card for #3501 ([d995331](https://github.com/deepseek-ai/deepseek-harness/commit/d99533177274d3019b3ea14a381a5b84b56b727a))

### 🐛 Bug Fixes
- fix(client-test-runtime): isolate client instances ([a475a65](https://github.com/deepseek-ai/deepseek-harness/commit/a475a65bed54537903c3f87e4afb84b01dfc4329))
- fix(tools): omit an absent Session during runtime policy resolution ([f6904f4](https://github.com/deepseek-ai/deepseek-harness/commit/f6904f4615f22b60c9d42560aad028501f3e0b83))
- fix(subprocess): create control carriers for overlapped Windows I/O ([83a4567](https://github.com/deepseek-ai/deepseek-harness/commit/83a45679dfcfc3e447872c6286ae747ccae5069a))
- fix(session): infer persistence change decisions for agents ([6e294b1](https://github.com/deepseek-ai/deepseek-harness/commit/6e294b1c274215198da594ed8c5c493cade7725f))
- fix(documentpreview): fit images to the pane and polish binary and loading states ([f210305](https://github.com/deepseek-ai/deepseek-harness/commit/f2103056891212c9018b9fb2a4438939eeb5e60a))
- fix(session): harden and automate persistence change review ([a0a7e2c](https://github.com/deepseek-ai/deepseek-harness/commit/a0a7e2c11cd96cc0c65a3d594374443d8f08bfee))
- fix(terminal-bash): bound retained storage and status reads ([68f9708](https://github.com/deepseek-ai/deepseek-harness/commit/68f9708e02efc0c65b74e4ce77af857898b123eb))
- fix(web): use installation records for plugin management ([17ce091](https://github.com/deepseek-ai/deepseek-harness/commit/17ce0910c4e0d50fbf57ca6ead4a13dec4a37c02))
- fix(boot): restore consumer-owned startup requirements ([f747ada](https://github.com/deepseek-ai/deepseek-harness/commit/f747ada426c68f1677aa6e6c3f16ecd1c9b87007))
- fix(plugins): resolve root state from plugin callers and report live failures ([52c215e](https://github.com/deepseek-ai/deepseek-harness/commit/52c215ee559a71629dab327fd68024bd9fa06623))
- fix(boot): inject loader for plugin-scoped recomposition ([fa240e7](https://github.com/deepseek-ai/deepseek-harness/commit/fa240e737273d22350319de4a3374f77a00e17a5))
- fix(agent-team): raise default teammate limit to 16 ([bfa6cc0](https://github.com/deepseek-ai/deepseek-harness/commit/bfa6cc01aa75df6dc9e796bdf94e9c625aab502d))
- fix(plugins): notify only changed diagnostics and remove stale probe cleanup ([eaecfd5](https://github.com/deepseek-ai/deepseek-harness/commit/eaecfd59bf40200dcbdbb4b3b255bae4c8f03074))
- fix(ci): use HTTPS Ubuntu sources for browser dependencies ([b916f45](https://github.com/deepseek-ai/deepseek-harness/commit/b916f455af43d875923585d90a37048e0e1a7084))
- fix(web): draw the changed-files header tile with the design's angle-bracket mark ([51de5bb](https://github.com/deepseek-ai/deepseek-harness/commit/51de5bbc4defd536364077b57d0a7bd571be6daa))
- fix(permission): tick only on a real generation change ([eb6373d](https://github.com/deepseek-ai/deepseek-harness/commit/eb6373d711e6833c0f2a68dd7296dc01de530e87))
- fix(subprocess): settle consumed empty scopes before exit notification ([dafff8e](https://github.com/deepseek-ai/deepseek-harness/commit/dafff8e51cbd309237dc486a467a283fd1668898))
- fix(ci): use HTTPS Ubuntu archives on Blacksmith ([ca53514](https://github.com/deepseek-ai/deepseek-harness/commit/ca53514562103fb33daca29f9a06c6b5fb679859))
- fix(plugin-inventory): require the runtime diagnostics dependency ([8279761](https://github.com/deepseek-ai/deepseek-harness/commit/8279761268a1f86637314e25c3a39f2fc20e6ca3))
- fix(desktop): track extraction in directory installer ([4fa238b](https://github.com/deepseek-ai/deepseek-harness/commit/4fa238bb5fbd172ede1056ca1e4912fe36e95421))
- fix(permission): drop the picker only on a catalog invalidation ([4a935ed](https://github.com/deepseek-ai/deepseek-harness/commit/4a935ed8fd79606dc1ff8f994d7845012367e8c3))
- fix(desktop): track installer work and complete progress smoothly ([188f72c](https://github.com/deepseek-ai/deepseek-harness/commit/188f72cd58c4e1807252bea65763e4973f8252c6))
- fix(desktop): align installer progress with worker stages ([6cc3431](https://github.com/deepseek-ai/deepseek-harness/commit/6cc34319e55a5d99a4b84036d465b2f31547fb4c))
- fix(desktop): keep installer progress and completion responsive ([00ca76d](https://github.com/deepseek-ai/deepseek-harness/commit/00ca76dd219b2c944c06598548f6411a86910fc3))
- fix(boot): expose profile recomposition settlement to observers ([8c33df5](https://github.com/deepseek-ai/deepseek-harness/commit/8c33df5d8e4f94fd7464e990795ab96c3ec5319d))
- fix(permission): keep the picker retryable after a failed catalog read ([e995d71](https://github.com/deepseek-ai/deepseek-harness/commit/e995d71a0e16c9de35cbfedd29c887384cc9dbd1))
- fix(session): align browser fixture forks and legal log regressions ([88c3d05](https://github.com/deepseek-ai/deepseek-harness/commit/88c3d05fbf1cc896835a3eafe06f5b66d2d96758))
- fix: expose the projection registration async disposer ([4e71939](https://github.com/deepseek-ai/deepseek-harness/commit/4e7193945da43bbc59d9abc12d6f17b38f2e86eb))
- fix(workspace): retain blank manual positions during reconnect ([11248ea](https://github.com/deepseek-ai/deepseek-harness/commit/11248ea949cf44aab1c55e13d4789d90b0d6fb68))
- fix(session): use the selected turn end as the fork cut ([973bea8](https://github.com/deepseek-ai/deepseek-harness/commit/973bea82040a28f4462d4c4bcad648b180b0e9d2))
- fix(auto-review): clear the master integration gates ([6b19923](https://github.com/deepseek-ai/deepseek-harness/commit/6b19923ad5fd0e94105a0bfe18861b4ba2ac1d71))
- fix(session): retain fork tail until the first inbox change ([0f8552d](https://github.com/deepseek-ai/deepseek-harness/commit/0f8552df7fea960ce53ec48e8faeb5cbd71e6149))
- fix(agent-team): disable direct subagent tools in Team profiles ([41196ae](https://github.com/deepseek-ai/deepseek-harness/commit/41196ae591f5b5b87aacfef6a8f0f0b24182d262))
- fix(ci): handle scope termination races and cyclic process snapshots ([18a1955](https://github.com/deepseek-ai/deepseek-harness/commit/18a1955b7e3b940c002144ea377313d408f1d123))
- fix(experimental): align the Auto review package version with the release ([d8c5489](https://github.com/deepseek-ai/deepseek-harness/commit/d8c54899b7c03d6c2c2864557e157748adb016bb))
- fix(ci): retain pending status during blame evaluation ([4563910](https://github.com/deepseek-ai/deepseek-harness/commit/4563910ff4ad4891e671a503ad81f00ee542ae68))
- fix(session): stop forks at the selected turn end ([896a6c3](https://github.com/deepseek-ai/deepseek-harness/commit/896a6c3e475fa88c1b5a7583e30028648ff24bcc))
- fix(workspace): make manual session order browser-local ([d19d23c](https://github.com/deepseek-ai/deepseek-harness/commit/d19d23cf86ad2666907909fce5b9f99cc0d9d4f5))
- fix(desktop): address shared runtime review and CI regressions ([ae84dd3](https://github.com/deepseek-ai/deepseek-harness/commit/ae84dd3381897b935bd7ff773267c620669ef774))
- fix(compaction): preserve summary diagnostics on cancellation ([73e10fb](https://github.com/deepseek-ai/deepseek-harness/commit/73e10fb80c439cb2024709003f1717506fa3f89e))
- fix(compaction): recover durable image offload in summary requests ([debb4b9](https://github.com/deepseek-ai/deepseek-harness/commit/debb4b9a9c14e87f0a9bc66c2cd99d8146c30057))

### 🔄 Refactoring
- test(ui-message-feedback): use RemoteMock ([77db566](https://github.com/deepseek-ai/deepseek-harness/commit/77db56687b4e3f237ea41876e04c66af2b5a5d07))
- refactor(code-runtime): name the Node runtime provider ([f95f7ec](https://github.com/deepseek-ai/deepseek-harness/commit/f95f7ec8dca975666cc81a9da256fcf8cc321f80))
- test(subprocess): cover source-only control launches and refresh generated references ([96e12dd](https://github.com/deepseek-ai/deepseek-harness/commit/96e12ddaf4e2d85f0785e17e22f4c830853e66bd))
- test(subprocess): cover control disposal and runner forwarding ([63d462f](https://github.com/deepseek-ai/deepseek-harness/commit/63d462f28bcb178952e19a76483f8e6b759e57e8))
- test(subprocess): type binary reads and native test spies precisely ([1e5259c](https://github.com/deepseek-ai/deepseek-harness/commit/1e5259c463bdc48a86f633daac47497ec5267792))
- test(subprocess): close control endpoint after the write callback ([3ccb898](https://github.com/deepseek-ai/deepseek-harness/commit/3ccb898cd56c803e8cde5f9f1ecfe7db251b85ff))
- test(subprocess): verify control inheritance and document channel ownership ([b9dfb8d](https://github.com/deepseek-ai/deepseek-harness/commit/b9dfb8da1c53906c64f9ea0a46f1a3c59428d5ae))
- refactor(e2b): retire remote execution providers ([c49db8b](https://github.com/deepseek-ai/deepseek-harness/commit/c49db8bc8c2924e115308692d34af7539288e7bb))
- perf(terminal-bash): retain scrollback incrementally ([cea837e](https://github.com/deepseek-ai/deepseek-harness/commit/cea837e06525384855e3b8b8231c2400bc3cb85b))
- test(web): cover live bundle toggles through the plugin Remote ([ecf8bfc](https://github.com/deepseek-ai/deepseek-harness/commit/ecf8bfcccba400947a34fc397789dad728a89c46))
- test(permission): pin the disposed guard on the invalidation tick ([62dd508](https://github.com/deepseek-ai/deepseek-harness/commit/62dd508cb0f67d4eec249741ae4c63ee482083bc))
- refactor(conversation): move default views to its own module ([4191570](https://github.com/deepseek-ai/deepseek-harness/commit/41915703cc47624e2ad17708495d433dd6cc143b))
- refactor(conversation): extract default views component ([f4dbec9](https://github.com/deepseek-ai/deepseek-harness/commit/f4dbec93df83864adbdbacb24161651bfdbd4cd1))
- refactor(conversation): move main panel to its own module ([8f5b1d7](https://github.com/deepseek-ai/deepseek-harness/commit/8f5b1d71e3c2256d7fddc4069ecbd7f9db4bdf4a))
- refactor(conversation): move content component to its own module ([0db88bd](https://github.com/deepseek-ai/deepseek-harness/commit/0db88bd58d833851addc07714030794b112f24f7))
- refactor(conversation): extract content component ([2477554](https://github.com/deepseek-ai/deepseek-harness/commit/2477554471d71933d574e68d199d840c59472ab5))
- refactor(conversation): extract main panel component ([0220ec4](https://github.com/deepseek-ai/deepseek-harness/commit/0220ec49896dbf38f092b69df2d6a4c580437dcd))
- refactor(boot): remove unpublished probe remnants and notes ([2670655](https://github.com/deepseek-ai/deepseek-harness/commit/26706559b2db41c799b1a7329237849a667b1f4b))
- test(web): align Team fixture with shipped delegation tools ([589cc7a](https://github.com/deepseek-ai/deepseek-harness/commit/589cc7ae87946c739e212e071981e9f944576e53))
- refactor(desktop): inherit shared Web profile defaults ([587c21d](https://github.com/deepseek-ai/deepseek-harness/commit/587c21d06b20ab5f18a0c33083b7330d821763ec))
- test(boot): exercise startup policy through installed bundle provenance ([96ba84e](https://github.com/deepseek-ai/deepseek-harness/commit/96ba84e15dd897f6457feec06dba825a12f9819f))
- test(agent-team): follow the DeepSeek protocol module move ([5731647](https://github.com/deepseek-ai/deepseek-harness/commit/57316476982c7fc20033c6b0402549c6f6fa7d84))
- refactor(plugins): manage static declarations and native row outcomes ([b351ca0](https://github.com/deepseek-ai/deepseek-harness/commit/b351ca0578293b6e947a524267db0291bf6e0e9e))
- refactor(boot): use native entry diagnostics and static plugin declarations ([1144cf1](https://github.com/deepseek-ai/deepseek-harness/commit/1144cf1e8e55a45f89d2a96a249075ac03995dd4))
- test(web): follow the settled-loader startup audit ([1de37dd](https://github.com/deepseek-ai/deepseek-harness/commit/1de37ddc2b1fbd782ad5551c3d445a9acff4d5bc))
- test: type the stored projection fixture as format events ([401c3ef](https://github.com/deepseek-ai/deepseek-harness/commit/401c3ef9770978a64e78ca0ef41b5bb7dd4f0a57))
- test: complete projection fixtures and configuration catalog ([1d4d22c](https://github.com/deepseek-ai/deepseek-harness/commit/1d4d22c1ff126b3c43fade32596ddf7bc9cda58a))
- refactor: move image offload projection into its plugin ([413ac14](https://github.com/deepseek-ai/deepseek-harness/commit/413ac14b16ab25f6a666ad467c6123273b587e58))
- test(boot): cover Web failure recovery and inject module routes ([eb9da89](https://github.com/deepseek-ai/deepseek-harness/commit/eb9da8930e2752e4d4bc8927be03c9386da83fca))
- refactor(workspace): derive flat rows only after ordering ([3a48b62](https://github.com/deepseek-ai/deepseek-harness/commit/3a48b623440df29ea51e963994de6ae7e286ecbd))
- test(desktop): remove obsolete fs-ext payload smoke ([6b05ed5](https://github.com/deepseek-ai/deepseek-harness/commit/6b05ed53e9470aec1a5da9e460fd0e42ae3ebeab))
- test(ci): control Python stray UTF-8 fragment delivery ([40e39f4](https://github.com/deepseek-ai/deepseek-harness/commit/40e39f467365c7aef02d55acbde3b8ac4a5c5049))
- test(terminal): await PowerShell prompt delivery ([96ee6e4](https://github.com/deepseek-ai/deepseek-harness/commit/96ee6e49f98997eb40c40946b7279949c48d26cc))
- test(llm): opt in Messages system-update e2e ([e5e9037](https://github.com/deepseek-ai/deepseek-harness/commit/e5e9037dfbff854b7f34558154b1d285f391d073))
- test(boot): keep headless running after optional MCP startup failure ([464334b](https://github.com/deepseek-ai/deepseek-harness/commit/464334bc4c72ff7bfb7e352438d738985111f56e))
- test(llm): pin Messages e2e to its official endpoint ([6ad0ddb](https://github.com/deepseek-ai/deepseek-harness/commit/6ad0ddb899b42f4755fc0a05f7001c0a482138cc))
- refactor(app-boot): keep required startup policy private ([6894e93](https://github.com/deepseek-ai/deepseek-harness/commit/6894e93a121d36c4d09807d66248f545c8c815d8))
- test(desktop): canonicalize pnpm fixture paths on Windows ([7fe6acd](https://github.com/deepseek-ai/deepseek-harness/commit/7fe6acdf8b1c2b3ec1234dcef93f46b85eaa8b73))
- test(compaction): record summary image recovery through ACP ([08dba5f](https://github.com/deepseek-ai/deepseek-harness/commit/08dba5f5f6db7427e8ac39ce769b42f69da2c667))

### 📝 Documentation
- docs(subprocess): record the Windows duplex pipe requirement ([c45d722](https://github.com/deepseek-ai/deepseek-harness/commit/c45d722d7b673ee90eef961dae4fb23c9bf235d8))
- docs(ci): preserve current Issue label repair semantics ([f6e0d42](https://github.com/deepseek-ai/deepseek-harness/commit/f6e0d429e7c26e1b6c4b94007270f789cd5e00c7))
- docs: clarify retained proxy and execution-world requirements ([63a16e2](https://github.com/deepseek-ai/deepseek-harness/commit/63a16e254d66b2a5cb3a4acbba8da067c80d9592))
- docs(plugins): align event references after metadata cleanup ([0443cd8](https://github.com/deepseek-ai/deepseek-harness/commit/0443cd8ad3a086614b24fa8c636f50a15b100b13))
- docs(permission): describe dismissal as a catalog invalidation ([14bdce3](https://github.com/deepseek-ai/deepseek-harness/commit/14bdce3644612a1604fd1340d019122b7b75d6e0))
- docs: normalize plugin decision note headers ([acb448e](https://github.com/deepseek-ai/deepseek-harness/commit/acb448e0c7cef9839e3619ca5bbecf5166b943f4))
- docs: refresh the paired Session API record ([9358100](https://github.com/deepseek-ai/deepseek-harness/commit/93581008aadac5349d7fc07bf2f3a581b9dbc908))
- docs: sync the projection disposer signature ([653a416](https://github.com/deepseek-ai/deepseek-harness/commit/653a4164b800c4d3bc8808e8be5e9271a74f5312))
- docs(boot): document startup and reload failure behavior ([85c37d1](https://github.com/deepseek-ai/deepseek-harness/commit/85c37d19508636db5d58a100474740b9f76c74db))

### 🔧 Configuration
- merge: align plugin event reference pairs ([23324b2](https://github.com/deepseek-ai/deepseek-harness/commit/23324b2b94b687587e8fe487036e5801379b49ed))
- merge: align plugin event documentation ([eda5fab](https://github.com/deepseek-ai/deepseek-harness/commit/eda5fabfbfa119db12297ac17f52d1b32e844a0f))
- merge: restore startup requirements across plugin management UI ([e812aa6](https://github.com/deepseek-ai/deepseek-harness/commit/e812aa66b1ad1120d8aada9917a78801d20a8b2c))
- merge: propagate consumer-owned startup requirements ([dac1950](https://github.com/deepseek-ai/deepseek-harness/commit/dac1950ac8b509109e791332239f5cbd1b923094))
- merge: restore startup requirements from plugin stack base ([2b40a9d](https://github.com/deepseek-ai/deepseek-harness/commit/2b40a9d8194de77834b22401bcf234a377a60676))
- merge: propagate plugin diagnostics cleanup to web ([3f9c25e](https://github.com/deepseek-ai/deepseek-harness/commit/3f9c25eb1d528d69a2097c4ab505f895311d1963))
- chore(workspace-changes): align the package version with the root after the master merge ([63f1f6e](https://github.com/deepseek-ai/deepseek-harness/commit/63f1f6eca470c07b83bcd8dd9624e6aca5800e47))
- merge: adapt plugin management UI to native entry outcomes ([8c3ddf0](https://github.com/deepseek-ai/deepseek-harness/commit/8c3ddf097107c6e36bbdf935d7ba47d653088fef))
- build: admit pure message projection leaves in browser bundles ([325c8d8](https://github.com/deepseek-ai/deepseek-harness/commit/325c8d880abf22a3474fea7489f321a6e265b300))
- ci: route runtime and LLM e2e through Blacksmith failover ([fd0dce2](https://github.com/deepseek-ai/deepseek-harness/commit/fd0dce2f205094fbe377a64d55385f1fcf62d89d))
- chore(compaction): mark existing history read for deferred migration ([c59d285](https://github.com/deepseek-ai/deepseek-harness/commit/c59d285f99e78ee567f9af6dcffa5dea87e2444b))

## 2026-09-12

**107 commits.** 13 feature changes, 37 fixes.

### 🆕 Features
- feat(browser-use): add per-Session experimental browser backends ([e1612c2](https://github.com/deepseek-ai/deepseek-harness/commit/e1612c2fdc951b764336cd328662d015c9770d85))
- feat(llm): default DeepSeek to Messages with Files parity ([b0641b8](https://github.com/deepseek-ai/deepseek-harness/commit/b0641b83fc14a9c5de87c0bf8415019672646581))
- feat(workspace): restore archived sessions from a settings page ([5f773a0](https://github.com/deepseek-ai/deepseek-harness/commit/5f773a0ded81f29c5b23809e4065d6103238cb84))
- feat(mcp): add scoped resources and server instructions ([3ba5b6e](https://github.com/deepseek-ai/deepseek-harness/commit/3ba5b6eb046325245031271dfb4d280d7cadf191))
- feat(mcp): negotiate modern protocols with the official SDK ([489c3ac](https://github.com/deepseek-ai/deepseek-harness/commit/489c3ac71552cc49b6067686b60dbd9e9a2822b5))
- feat(release): publish all experimental packages ([42c5b65](https://github.com/deepseek-ai/deepseek-harness/commit/42c5b656431144cc3206482780c9e0eb409b97a3))
- feat(release): use a private denylist for experimental packages ([6e30e1a](https://github.com/deepseek-ai/deepseek-harness/commit/6e30e1a3007595d179f198abefebc12019d73f8f))
- Fix offline reference checks and preserve native pack inputs ([b905d39](https://github.com/deepseek-ai/deepseek-harness/commit/b905d399df1cbf66b4374b9fc0f5fd83170d5c35))
- feat: enforce maintained repository reference policy ([6b65138](https://github.com/deepseek-ai/deepseek-harness/commit/6b651380a7afd2a8ece5df3ef166e3a6a8388b2a))
- feat: add computer use with Cua Driver providers ([af4ad05](https://github.com/deepseek-ai/deepseek-harness/commit/af4ad05845219691bef9b633f91cbd96cb89772e))
- feat(ssh): authenticate streams and join remote process cleanup ([72226bd](https://github.com/deepseek-ai/deepseek-harness/commit/72226bd061aa5822815c0f8e7f5166a1c29cadec))
- feat(ptc): present provider execution guidance in logged program schema ([2a08bf6](https://github.com/deepseek-ai/deepseek-harness/commit/2a08bf6ab96b40a32ce9738f537d2fc92e74294e))
- feat(sidebar-files): restore the tree's scroll position across tab switches ([004dcee](https://github.com/deepseek-ai/deepseek-harness/commit/004dceed5e12ae511643920da3d3dc6f7949ef67))

### 🐛 Bug Fixes
- fix(client-modules): resolve the owning Loader instance ([c1504a2](https://github.com/deepseek-ai/deepseek-harness/commit/c1504a2aa6df3f733e4b454df0cd4718f2f3f1d6))
- fix(llm): harden Messages transport and Files parity ([7d3dab6](https://github.com/deepseek-ai/deepseek-harness/commit/7d3dab66a2bd617e89dd0d183d09a2c4423b8f8c))
- fix(mcp): expose scoped resource server names to the model ([834bd55](https://github.com/deepseek-ai/deepseek-harness/commit/834bd55a59221286e244bb250b674b79eb1263aa))
- fix(mcp): own transports through protocol negotiation ([3785b68](https://github.com/deepseek-ai/deepseek-harness/commit/3785b68ecfb2a5bfb1e2f7e69838437f67d6413a))
- fix(ci): preserve recorded npm resolution during vendor rescoping ([55fc8b9](https://github.com/deepseek-ai/deepseek-harness/commit/55fc8b91e4563ea562128e13b1d681f5ce262f3a))
- fix(ci): canonicalize browser notice roots with native realpath ([0e060aa](https://github.com/deepseek-ai/deepseek-harness/commit/0e060aa67534c1d4e3457ada5d377b658a12ff21))
- fix(ci): skip product graph capture during dependency analysis ([5b491e8](https://github.com/deepseek-ai/deepseek-harness/commit/5b491e8cc632566d00da5bf7473a80ab1a122c84))
- fix: cover supported experimental isolation inputs ([22c5ae6](https://github.com/deepseek-ai/deepseek-harness/commit/22c5ae6abc7bc9f7113c89289ebbdd5d3d63a1e3))
- fix(subprocess): preserve direct outcomes on signal failure ([71334b9](https://github.com/deepseek-ai/deepseek-harness/commit/71334b9c7813cad301739433ccc84297bcedfa85))
- fix(session): validate generated release facts ([4adfe00](https://github.com/deepseek-ai/deepseek-harness/commit/4adfe002070fe5d19bf42d5a2b8073a5654f930e))
- fix(subprocess): confirm direct SIGKILL after group delivery ([c07df5a](https://github.com/deepseek-ai/deepseek-harness/commit/c07df5aa65fc37f822b211e27ddc51b6e1e7d6ce))
- fix(subprocess): await direct fallback settlement before scope failure ([4b99ace](https://github.com/deepseek-ai/deepseek-harness/commit/4b99ace8fb5ce7b1e057b23b119f92ebf2d2dd5c))
- fix: deduplicate dependency JSON and isolate npm configuration ([7900404](https://github.com/deepseek-ai/deepseek-harness/commit/79004045413a712135a838bc673261d5dafddbc4))
- fix(computer-use): cancel image admission and fix source snapshots ([cd97419](https://github.com/deepseek-ai/deepseek-harness/commit/cd97419e810245decb57fcf904e62d249b850f15))
- fix(deps): retain locked PDF canvas optional dependencies ([3058471](https://github.com/deepseek-ai/deepseek-harness/commit/305847127a49d9a5c56d9e9f4ca62d65f2a67cde))
- fix(ssh): keep completion cleanup under release ownership ([28c4daa](https://github.com/deepseek-ai/deepseek-harness/commit/28c4daa66c0db21a0bee52fad09f3d992231963f))
- fix(ssh): propagate output closure and bound exit observations ([ac43c26](https://github.com/deepseek-ai/deepseek-harness/commit/ac43c2656f6afd34bb72297f37f12b33d9720b80))
- fix(ssh): retain failed results and join all process cleanup ([d3fa703](https://github.com/deepseek-ai/deepseek-harness/commit/d3fa7030ef3368e44e38a2a5224f5e269c89ab2f))
- fix(ssh): preserve remote filenames in file URLs ([d951a49](https://github.com/deepseek-ai/deepseek-harness/commit/d951a490385ccfecdca612d21259d6007cd1045b))
- fix(ssh): reject timeouts above the native timer range ([1c5a201](https://github.com/deepseek-ai/deepseek-harness/commit/1c5a201af8288cc8a25139da13ee947e2eecfec9))
- fix(ssh): disable signal-triggered helper inspection ([969e968](https://github.com/deepseek-ai/deepseek-harness/commit/969e968e0e900ab613bf079d38e0928860df0dff))
- fix(ssh): join authenticated stream teardown and validate package closure ([561bfc3](https://github.com/deepseek-ai/deepseek-harness/commit/561bfc3bbb16567368f3dc787fa4ef7e52e979c3))
- fix(ssh): join transport cleanup and preserve collected output ([abb7c6a](https://github.com/deepseek-ai/deepseek-harness/commit/abb7c6a49d93fc7a4959b488cbeb7a81c8b14270))
- fix(shell): include confinement preparation in foreground deadlines ([73e38e1](https://github.com/deepseek-ai/deepseek-harness/commit/73e38e1758fe5ebdc914f6d6d002142a1eb5ce21))
- fix(preview): provide the native realpath callback alias ([f72c2e0](https://github.com/deepseek-ai/deepseek-harness/commit/f72c2e019dafd1a8e78373c64e1577a75a2ad2ba))
- fix(fs): preserve physical traversal in directory entry paths ([58b67dc](https://github.com/deepseek-ai/deepseek-harness/commit/58b67dcb5a30013e93489d6645285a3d84c88455))
- fix(fs): share native path rooting between resolve and lstat ([4c7b690](https://github.com/deepseek-ai/deepseek-harness/commit/4c7b6902e332f020b99f7a48468b5cf320a06545))
- fix(fs): preserve native Windows drive-relative path resolution ([573f525](https://github.com/deepseek-ai/deepseek-harness/commit/573f525c33303183848b48c921b76db059be4b4f))
- fix(code-runtime): preserve native temp setup and preview activation ([091cbcd](https://github.com/deepseek-ai/deepseek-harness/commit/091cbcdbfbbcd6ded193d1adae408f8648da3b6f))
- fix(code-runtime): support SEA startup and immediate control writes ([7f5eb6d](https://github.com/deepseek-ai/deepseek-harness/commit/7f5eb6db9a2121eaa86aebb12713bc648d59af9f))
- fix(code-runtime): separate model environment from native startup paths ([98d3af0](https://github.com/deepseek-ai/deepseek-harness/commit/98d3af0683f689748771a6d9f017122829b76b37))
- fix(code-runtime): preserve native startup paths and preview packaging ([a6f7eea](https://github.com/deepseek-ai/deepseek-harness/commit/a6f7eeadc6ab9d8de6421c952b0db590ef6ef44c))
- fix(sandbox): pin ACL source resolution and recognize Node denials ([b35a3b2](https://github.com/deepseek-ai/deepseek-harness/commit/b35a3b29eb6e024839b47b7d34fead805543148b))
- fix(sandbox): resolve source preload independently of command cwd ([5bebc7c](https://github.com/deepseek-ai/deepseek-harness/commit/5bebc7c5047a04f47997ac85b0efaab5c82e9872))
- fix(subprocess): await control endpoint closure during disposal ([562e7f3](https://github.com/deepseek-ai/deepseek-harness/commit/562e7f364e1761ef7ffb7850ed42c874dd22fddd))
- fix(subprocess): separate process quiescence from caller control streams ([838da1d](https://github.com/deepseek-ai/deepseek-harness/commit/838da1d07e0552edeef46917708a1cda38a105be))
- fix(documentpreview): draw pdf page placeholders on the skeleton token ([adbe7e6](https://github.com/deepseek-ai/deepseek-harness/commit/adbe7e6395342004eeeeeb0f8465ad18b3c8d184))

### 🔄 Refactoring
- test(session-controller): migrate remaining Remote fixtures ([9b09191](https://github.com/deepseek-ai/deepseek-harness/commit/9b091919e2fd90af59bd6a37d358331d9af6933c))
- refactor(llm): inherit Messages defaults and verify live parity ([accafa5](https://github.com/deepseek-ai/deepseek-harness/commit/accafa5fb2e67b9ea7a29c6214002b8ab0c73f2c))
- test(ci): align external-agent and workflow endpoint fixtures ([aef56a3](https://github.com/deepseek-ai/deepseek-harness/commit/aef56a31088633b5b898366be234c736ff6f594d))
- test(ci): exercise Messages defaults in runtime smokes ([ece35a1](https://github.com/deepseek-ai/deepseek-harness/commit/ece35a1a38c1e735abb3e61286e45ade7de22e15))
- test: canonicalize browser notices fixture paths ([a280cf3](https://github.com/deepseek-ai/deepseek-harness/commit/a280cf34f53b5691068932bdc2d6d2438f9860d1))
- test: canonicalize Windows Vite fixture roots ([00b2470](https://github.com/deepseek-ai/deepseek-harness/commit/00b2470eb6c8ed6dbeb3befbdd55446ef438e96e))
- test(release): cover packed experimental worker consumers ([b5d463c](https://github.com/deepseek-ai/deepseek-harness/commit/b5d463ca5c4eac1d2e6b48891c81598888d3e437))
- test(release): cover baseline package discovery ([251210d](https://github.com/deepseek-ai/deepseek-harness/commit/251210d517b593d61b007c045920cf418d7cbf41))
- test: isolate Git config without a Windows device path ([35dbd84](https://github.com/deepseek-ai/deepseek-harness/commit/35dbd84ac4d61d4455c31f20d5a55c147da68b51))
- test: separate independent policy gate registration cases ([1b4e1ac](https://github.com/deepseek-ai/deepseek-harness/commit/1b4e1ac076d8e232c780f7ee958328a8b7cc2299))
- test(ci): cover control requests and fix cross-volume fixtures ([fabbcf8](https://github.com/deepseek-ai/deepseek-harness/commit/fabbcf8c7616a335bbb21eec89a5fbb900f6bad6))
- refactor(ptc): align runtime packages and services with PTC naming ([7c9bb59](https://github.com/deepseek-ai/deepseek-harness/commit/7c9bb5914cedec80e46197a8c894037fcfd12faf))
- test(ssh): preserve stream reads across supported Node versions ([e892c1a](https://github.com/deepseek-ai/deepseek-harness/commit/e892c1abf50058b134de5dea3b4b8ff0aafb255f))
- refactor(ssh): retain TLS ownership of raw socket errors ([c6e531e](https://github.com/deepseek-ai/deepseek-harness/commit/c6e531e45b0190eacf86109ff493c9dafca73266))
- test(ssh): isolate backend availability from helper dispatch ([b5fd914](https://github.com/deepseek-ai/deepseek-harness/commit/b5fd914306d67fa9f65f7bfd90b09dc0a4f429c2))
- refactor(sandbox): await cancellable process preparation ([32de441](https://github.com/deepseek-ai/deepseek-harness/commit/32de4412dc34e44c75602ee837a52a7bb85852c0))
- test(runtime): cover async preparation in built and Windows paths ([fd9d333](https://github.com/deepseek-ai/deepseek-harness/commit/fd9d333fbe48b2313ae57e037994c2b79f1cc5d0))
- test(fs): exercise byte reads with a live cancellation signal ([0a7a69e](https://github.com/deepseek-ai/deepseek-harness/commit/0a7a69ec547cd4eceb4a4304195620319c072664))
- refactor(sandbox): await cancellable preparation in process consumers ([caa6960](https://github.com/deepseek-ai/deepseek-harness/commit/caa69608fb693dab4aa0605110b0bd4a69a4d79b))
- test(ptc): refresh portable denial and shared runtime schema fixtures ([fc7f7dd](https://github.com/deepseek-ai/deepseek-harness/commit/fc7f7ddda6403038a936ea8f0c49cd9715582a68))
- test(ptc): make sandbox denial recording portable and cover execution descriptors ([4d4e333](https://github.com/deepseek-ai/deepseek-harness/commit/4d4e333676d587e6ca18cd2182bc5b9d3d957c05))
- test(ptc): include program approval scenario in host type checking ([a299911](https://github.com/deepseek-ai/deepseek-harness/commit/a29991144a633dafdc7cd50135edfc8ec21d27a0))
- test(ptc): pin provider usage guidance in recorded program schemas ([c05e095](https://github.com/deepseek-ai/deepseek-harness/commit/c05e0953efbc35af094c9c9b6a50b6cdcca10467))
- test(ptc): record approved program execution and document per-call controls ([c6b9597](https://github.com/deepseek-ai/deepseek-harness/commit/c6b959783a0ad7654b7b33f59f1e97991f6d33ef))
- test(code-runtime): observe native temp through inherited Windows handles ([e21060d](https://github.com/deepseek-ai/deepseek-harness/commit/e21060defe07e4fb8a56c66badeaafc1b4e8fcd5))
- test(code-runtime): align UI binding fixture and shared diagnostic ownership ([2344830](https://github.com/deepseek-ai/deepseek-harness/commit/2344830cfda6c4bed639332ba9b29a70c1631530))
- test(code-runtime): gate native enforcement cases on backend availability ([bef3c26](https://github.com/deepseek-ai/deepseek-harness/commit/bef3c261750357ccb58ad6c6b0a8c3299870a1d6))
- test(tools): cover PTC standing policy and sandbox outcomes ([ca7f3a5](https://github.com/deepseek-ai/deepseek-harness/commit/ca7f3a523d6e04bdb24012d91f493eaae04c145d))
- test(code-runtime): complete sandboxed process coverage and catalogs ([fc5cb0f](https://github.com/deepseek-ai/deepseek-harness/commit/fc5cb0f649c16bd3319cf4b1dec32d67be0984eb))
- test(subprocess): cover retained control endpoint teardown ([e53c526](https://github.com/deepseek-ai/deepseek-harness/commit/e53c526320da10502214116e29368e967d3a830b))
- test(subprocess): type rejected lifecycle results as unknown ([f5ef951](https://github.com/deepseek-ai/deepseek-harness/commit/f5ef951ec5abba163e8a7b30df415c8cf4dd45c6))
- test(ci): await final colors and build compactable history ([6523678](https://github.com/deepseek-ai/deepseek-harness/commit/65236780d1e9a83e6fb2c252564fac60a631b64c))
- test(persistence): budget heavy integration cases for CI ([0b368df](https://github.com/deepseek-ai/deepseek-harness/commit/0b368dfe78c33218033b4d0ac1db54fe3f5b6d06))
- test(session): protect persistence digests from harmless reordering ([70a3be6](https://github.com/deepseek-ai/deepseek-harness/commit/70a3be6f2029b51a38a895d1f643041f1050ce34))

### 📝 Documentation
- docs(browser-use): explain the Stagehand action timer limit ([0752a09](https://github.com/deepseek-ai/deepseek-harness/commit/0752a09ae6b50ee8fd87a5bc71e0d0a752a90bdf))
- docs(mcp): explain resource providers and server instructions ([aec2d5e](https://github.com/deepseek-ai/deepseek-harness/commit/aec2d5e5f04099f6c4f2f50caa258edb307fbc24))
- docs(mcp): align bridge note with SDK-owned discovery ([f6e7166](https://github.com/deepseek-ai/deepseek-harness/commit/f6e7166762f3f239a40fe300a865fa99a8e73139))
- docs(mcp): describe subsystem roles and configuration ([395f79b](https://github.com/deepseek-ai/deepseek-harness/commit/395f79b772e6864105e78ac4f9f34a0aaae708f1))
- docs(subprocess): record signal error isolation and fixture safety ([dd55f38](https://github.com/deepseek-ai/deepseek-harness/commit/dd55f38614d89615b4825fc306a8609f400ab2b2))
- docs(session): use tags throughout historical release records ([2d5391e](https://github.com/deepseek-ai/deepseek-harness/commit/2d5391eede6685d943c8674316196c5d9ac95769))
- docs(session): backfill alpha and RC persistence history ([aea077a](https://github.com/deepseek-ai/deepseek-harness/commit/aea077ac75469aa82e961f7956c9851e9efab5d3))
- docs(session): define the LogicalSession refactor plan (#3654) ([a630265](https://github.com/deepseek-ai/deepseek-harness/commit/a630265a0246cc93e3180eda02809a159a1be79d))
- docs: retain hosted run identities without organization URLs ([c6721f9](https://github.com/deepseek-ai/deepseek-harness/commit/c6721f992e9cc324f9dc7b88f3240ae4dafce57b))
- docs: generate published npm dependency catalog ([313768f](https://github.com/deepseek-ai/deepseek-harness/commit/313768f520deb080a3dc00aed58087ccc4277ca6))
- docs(ptc): align runtime terminology and naming decision links ([83d121c](https://github.com/deepseek-ai/deepseek-harness/commit/83d121c8c01ed8153cdbd6d71aa8ff6276418ed1))
- docs(ssh): generate the shared-instance dependency graph ([119d44f](https://github.com/deepseek-ai/deepseek-harness/commit/119d44fc4cb241916f1ac07117a0d643e2a9f27d))
- docs(ssh): record the administrative timer range ([c886f26](https://github.com/deepseek-ai/deepseek-harness/commit/c886f26b913400b11974c80d4f04558ff75717d4))
- docs(ssh): define trusted runtime installation prerequisites ([7673f90](https://github.com/deepseek-ai/deepseek-harness/commit/7673f90d18c581b62070d93fd49f5490b02c48d5))
- docs(ptc): refresh persistence source references after master rebase ([c5de252](https://github.com/deepseek-ai/deepseek-harness/commit/c5de252f8c70d642f953c555bb0bbf344d81f059))
- docs(code-runtime): refresh confined runtime dependency graph ([09e3346](https://github.com/deepseek-ai/deepseek-harness/commit/09e334622d082af1abad22df0f025444bbc9fb64))
- docs(testing): record compaction fixture calibration ([ff03531](https://github.com/deepseek-ai/deepseek-harness/commit/ff03531b973b8ece837066739a287c4f4816aee2))
- docs(session): acknowledge Auto review error metadata ([ee9ae1d](https://github.com/deepseek-ai/deepseek-harness/commit/ee9ae1d0e09d255b8997242751ff53e581e23967))
- docs(auto-review): name delegation records explicitly ([2d9e3a1](https://github.com/deepseek-ai/deepseek-harness/commit/2d9e3a175fb3deb51abff34094a3bed86825b568))

### 🔧 Configuration
- ci(web): verify composed profiles, live registries, and bundle inputs ([8f14f98](https://github.com/deepseek-ai/deepseek-harness/commit/8f14f98a1a158d6647c829181ef86c125d146ceb))
- ci(release): keep experimental packages out of the default product ([f34dd86](https://github.com/deepseek-ai/deepseek-harness/commit/f34dd86285409939228dc8d77b4d32ef085b88e7))
- chore: enforce maintained repository reference policy ([0b7f0b0](https://github.com/deepseek-ai/deepseek-harness/commit/0b7f0b072b6cdfba54bdbd536e29df8b6c4c2b88))
- chore(session): refresh persistence references after master merge ([f85b328](https://github.com/deepseek-ai/deepseek-harness/commit/f85b328450f7841b897d2ee455a08c8b1326c1e3))

## 2026-09-13

**33 commits.** 3 feature changes, 9 fixes.

### 🆕 Features
- feat(boot): add profile resolution modes ([6aa2e46](https://github.com/deepseek-ai/deepseek-harness/commit/6aa2e4633c226f5475edfbf8e44cb460ae8cd623))
- feat(mcp): activate profile resource tools for configured servers ([e084689](https://github.com/deepseek-ai/deepseek-harness/commit/e08468954abf09fbd14e2f34bc50c52c36ed7c24))
- feat(presets): disable ralph in the default compositions ([7398534](https://github.com/deepseek-ai/deepseek-harness/commit/73985344cda013ef1d784a55c314d7bebcb4afee))

### 🐛 Bug Fixes
- fix(browser-use): initialize MCP clients without new core APIs ([b84a822](https://github.com/deepseek-ai/deepseek-harness/commit/b84a8226bd5016e6bcd2662a96f1b4a056352e59))
- fix(browser-use): integrate current MCP resources and snapshots ([e41511d](https://github.com/deepseek-ai/deepseek-harness/commit/e41511d84415b20fa9a41fd9809b80107ca5653f))
- fix(browser-use): close lifecycle gaps and isolate replay fixtures ([d1e32e4](https://github.com/deepseek-ai/deepseek-harness/commit/d1e32e481a93ab54092468272cd5f4c8759ac150))
- fix(workspace): keep the newest archive set from stale replies ([76941d0](https://github.com/deepseek-ai/deepseek-harness/commit/76941d0085c79137fb1f94e75195c09314c99c48))
- fix(coverage): fail loud when the canonicalizer gets no coverage data ([10930a0](https://github.com/deepseek-ai/deepseek-harness/commit/10930a02053581ddaedef2af87a6d2ec9393fce4))
- fix(coverage): canonicalize partition locations before the blob merge ([c171a7a](https://github.com/deepseek-ai/deepseek-harness/commit/c171a7a9a28958df24f80138c181238ed72f765f))
- fix(workflow): close lifecycle and CI integration gaps ([34f80b8](https://github.com/deepseek-ai/deepseek-harness/commit/34f80b8e6ec633c6891607d865acafcb97afa3c8))
- fix(workflow): execute orchestration in the sandboxed PTC runtime ([35af869](https://github.com/deepseek-ai/deepseek-harness/commit/35af8698c24c1b7654cd5c83dcbec224e50f2337))
- fix(docs): address persistence format history review ([765c87f](https://github.com/deepseek-ai/deepseek-harness/commit/765c87fb87a2004bf5eae1db2601e8d0a0d33377))

### 🔄 Refactoring
- test(client): preserve migrated fixture semantics ([e179c4a](https://github.com/deepseek-ai/deepseek-harness/commit/e179c4ae14a5f9493b7bbc8ef7da89d9af6f79f0))
- refactor(client): remove fixture-only API residue ([c0e8252](https://github.com/deepseek-ai/deepseek-harness/commit/c0e8252afee27e43f2e6d0cc09511398da92300c))
- test(file-upload): cover unnamed byte uploads ([7e331d7](https://github.com/deepseek-ai/deepseek-harness/commit/7e331d72eddf548d6303937ea1c7b2e77291b7cb))
- refactor(client): replace browser fixture with RemoteMock ([5541ae0](https://github.com/deepseek-ai/deepseek-harness/commit/5541ae0d2d89b5b1d8866963378974d7c3dcda0c))
- test(web): run fixture browser cases through Host ([eb2cb66](https://github.com/deepseek-ai/deepseek-harness/commit/eb2cb668a54476cc8b46433db4e16b8451d3c336))
- test(web): expect the unarchive verb and the archived-sessions nav row ([ae34320](https://github.com/deepseek-ai/deepseek-harness/commit/ae34320a5bc4c505f64a19226145de8224e651ba))
- test(sidebar-documentpreview): cover the visible-label loading branch and drop the stale single-viewer control from the seeded-history golden ([25e6e97](https://github.com/deepseek-ai/deepseek-harness/commit/25e6e976b7c532108c6062c5774dc031ab8af480))
- test(mcp): align snapshots with Ralph disabled by default ([004ef35](https://github.com/deepseek-ai/deepseek-harness/commit/004ef350102d7d8e442be701ad521eb40e106904))
- test(mcp): align resource snapshots with shipped defaults ([b5376e3](https://github.com/deepseek-ai/deepseek-harness/commit/b5376e3d021c17ba05fc26e41e9aeb1553f6d8a0))
- test(mcp): include resources in minimal profile expectations ([815a5eb](https://github.com/deepseek-ai/deepseek-harness/commit/815a5eb01e1d039b076c3ba962e518df07a07fc6))
- test(file-reference): publish restored workspace fixtures atomically ([deb0d7e](https://github.com/deepseek-ai/deepseek-harness/commit/deb0d7e1b5521c690fb78e8455c2eecc66333fb2))
- test(ci): pin gallery time and dispose projection cache fixtures ([c837024](https://github.com/deepseek-ai/deepseek-harness/commit/c8370240a8f9bcccf287f5337d17ca1cc2903db5))

### 📝 Documentation
- docs(testing): correct fixture migration guidance ([f258024](https://github.com/deepseek-ai/deepseek-harness/commit/f258024b4d909836dfaf2d6024dc80a013f7308f))
- docs(testing): retire browser fixture references ([566db0b](https://github.com/deepseek-ai/deepseek-harness/commit/566db0b6cb234de1350e398d8c0ac1dd5e2b9502))
- docs(agent-notes): cite issue 3974 as plain text to satisfy the repository-references gate ([f7e010a](https://github.com/deepseek-ai/deepseek-harness/commit/f7e010a70ab0f7cb34462faf5593028a9833d2c7))
- docs(session): nest historical formats under persistence changes ([3807099](https://github.com/deepseek-ai/deepseek-harness/commit/38070996c129ea38321a8b8d35d24cd0f9cf8584))
- docs(session): backfill and gate persistence format references ([b08f6c4](https://github.com/deepseek-ai/deepseek-harness/commit/b08f6c421bfe60d01a387eddf86f457365710eb9))
- docs(mcp): clarify resource discovery and profile verification ([4c6b2c0](https://github.com/deepseek-ai/deepseek-harness/commit/4c6b2c02af7b7e66877b3237f0d46a39112dc420))
- docs(presets): state the web-app disable in the present tense ([c7d2e99](https://github.com/deepseek-ai/deepseek-harness/commit/c7d2e99b8e7d87b37069417e00af40272df823fe))
- docs(presets): name the new id in the ralph restore recipe ([d49192b](https://github.com/deepseek-ai/deepseek-harness/commit/d49192b6acd1c7e9a06c775d5bfa17f313a61f75))

### 🔧 Configuration
- chore(cordis): regenerate the client slot catalog ([e1ee806](https://github.com/deepseek-ai/deepseek-harness/commit/e1ee806226d600a066fbabb803b85b87d41d5514))

## 2026-09-14

**133 commits.** 20 feature changes, 45 fixes.

### 🆕 Features
- feat: coordinate profile management through dsh-hmr ([d06e6b5](https://github.com/deepseek-ai/deepseek-harness/commit/d06e6b551968410944524d87967e7b5514bfc517))
- feat: add current-profile plugin manager service and Web controls ([98b92b6](https://github.com/deepseek-ai/deepseek-harness/commit/98b92b683c39fc60771daa774492105c2d3e8076))
- feat(desktop): run runtime host from asar ([fa7d551](https://github.com/deepseek-ai/deepseek-harness/commit/fa7d5519f55c56e75ed72135e35ae9f1bc3d65cd))
- feat(cli): force runtime resolution in pkg builds ([c917a4e](https://github.com/deepseek-ai/deepseek-harness/commit/c917a4e0bd8590ce043861d50fb3ffec0db202e0))
- feat(web): cancel plugin installation with Host confirmation ([bdc496c](https://github.com/deepseek-ai/deepseek-harness/commit/bdc496cc06c8bee7fd18b0f6b671608d89ff9ae6))
- feat(plugins): cancel installations after process and file cleanup ([ff1f3f7](https://github.com/deepseek-ai/deepseek-harness/commit/ff1f3f72a1eb9132684ca49971cc00814c16cb88))
- feat(web): apply client plugin changes without reloading ([fb0fb48](https://github.com/deepseek-ai/deepseek-harness/commit/fb0fb4803381072525f2f9edd06b3e6ca3de6f4e))
- feat(session): default session-log upload on outside recorded-session lanes ([2389b65](https://github.com/deepseek-ai/deepseek-harness/commit/2389b65246022b3d2553ba3e188621dd2059ef38))
- feat(web): pin Think and compaction headers sticky while scrolling ([67271a9](https://github.com/deepseek-ai/deepseek-harness/commit/67271a921b6739e85a7a1b03ddd1d5c812e7a886))
- feat(web): launch terminals from provider guide menus ([4012092](https://github.com/deepseek-ai/deepseek-harness/commit/4012092d249569bb6438d206663b5e4af57353c6))
- feat(workspace-changes): keep change summaries on the Host for the Session's lifetime ([dde4dcc](https://github.com/deepseek-ai/deepseek-harness/commit/dde4dccbd2ff5356875772d791f088d5c5d86488))
- feat(desktop): bundle release-bound workspace runtimes ([0c88492](https://github.com/deepseek-ai/deepseek-harness/commit/0c884926465b2758837cab657eadfff5a463fa19))
- feat(web): follow application theme in sidebar terminals ([1daed09](https://github.com/deepseek-ai/deepseek-harness/commit/1daed09185a7d729afc274bb2ded0d8e9ff7849e))
- feat(web): show common shells by default ([249c8d1](https://github.com/deepseek-ai/deepseek-harness/commit/249c8d156595d80473ad86f01097608be00f3eca))
- feat(desktop): load platform packaging settings from local dotenv files ([c47a2c1](https://github.com/deepseek-ai/deepseek-harness/commit/c47a2c16b4b1944b581bc5ac08c0a25f3980facd))
- feat(docs): add fullscreen Mermaid diagram viewer ([b0ec8ce](https://github.com/deepseek-ai/deepseek-harness/commit/b0ec8cef32eef78d18091270534ff02d0cf0a343))
- feat(web): choose and remember terminal shells ([33d89ae](https://github.com/deepseek-ai/deepseek-harness/commit/33d89aee7745f462263bd5be532fe802431ece71))
- feat(workspace-changes): keep snapshot objects in a private store under the Harness home ([d663427](https://github.com/deepseek-ai/deepseek-harness/commit/d6634272d5b0dc5df4312dd39dcc5afc1f9eccef))
- Refresh merged SDK recordings and persistence documentation ([2b1dabe](https://github.com/deepseek-ai/deepseek-harness/commit/2b1dabec86b4283180e160486beb71b931a4dc83))
- Update image tests for split adapters and durable offload failures ([27d52a4](https://github.com/deepseek-ai/deepseek-harness/commit/27d52a4edb2a2c5073e7b09f3a9425deb1e13bdf))

### 🐛 Bug Fixes
- fix(web): hold a compaction summary's code banner below the pinned header ([b416ac9](https://github.com/deepseek-ai/deepseek-harness/commit/b416ac99e464b7293ae7df32dfd09b7bd0470366))
- fix: preserve manager failures and support worker preview imports ([5a9c159](https://github.com/deepseek-ai/deepseek-harness/commit/5a9c159c2716cea25727c892500d4675d8543962))
- fix: remove inactive bundles after incomplete installation ([8e32751](https://github.com/deepseek-ai/deepseek-harness/commit/8e327513baaafc4df590c82f411264ea1b0cc66e))
- fix(pkg): restore VFS Dirent reads ([1b56c86](https://github.com/deepseek-ai/deepseek-harness/commit/1b56c865fa7c59a029e74c25a639ec5c48081ee4))
- fix(plugins): join package removal when the manager is disposed ([70f6f30](https://github.com/deepseek-ai/deepseek-harness/commit/70f6f30817415913737ed08727b7262eb81697f8))
- fix(boot): treat null exports as legacy resolution ([0de6187](https://github.com/deepseek-ai/deepseek-harness/commit/0de61878b329c4e030bd6f3d60a4c3303a6b9c44))
- fix(boot): bind internal ESM default resolver ([32e6e87](https://github.com/deepseek-ai/deepseek-harness/commit/32e6e872f6d7799d03eb6e8484c1fd3a45e878bb))
- fix(app-boot): align remaining runtime resolution edges ([0d4b097](https://github.com/deepseek-ai/deepseek-harness/commit/0d4b097375a017c62f75a0ee9fcb8f8999cb9c35))
- fix(boot): preserve selected explicit path errors ([69ab657](https://github.com/deepseek-ai/deepseek-harness/commit/69ab6575d10d9b5110a758ab5c7a4202d6d22896))
- fix(boot): preserve selected package failures ([3cacc0e](https://github.com/deepseek-ai/deepseek-harness/commit/3cacc0e69adbd8142c2bdd89c4d8156ea8da2ec1))
- fix(boot): cover profile resolution edge cases ([c75f667](https://github.com/deepseek-ai/deepseek-harness/commit/c75f66782202a4e14088d80299569072957bbb27))
- fix(presets): isolate package lookup failures ([db098c8](https://github.com/deepseek-ai/deepseek-harness/commit/db098c8a240dad10827f213408c6d8d8ca71b553))
- fix(boot): align runtime profile resolution with links ([013aead](https://github.com/deepseek-ai/deepseek-harness/commit/013aead5c9bd78b42327ca8eef11bef4e2db5940))
- fix(boot): align runtime and link resolution ([6823f8a](https://github.com/deepseek-ai/deepseek-harness/commit/6823f8a00c04b18d016ce9ae8c534f7a52021938))
- fix(boot): drop stale workflow worker dependency ([aa4c46e](https://github.com/deepseek-ai/deepseek-harness/commit/aa4c46edeb0e7e7ebe7d6a4c8584a733593efac7))
- fix(plugins): preserve observed exit codes on cancellation ([cf992b5](https://github.com/deepseek-ai/deepseek-harness/commit/cf992b52f96dc33781726b502f6a123d3a1d8d81))
- fix(plugins): publish shared subprocess installation chunks ([eca54e9](https://github.com/deepseek-ai/deepseek-harness/commit/eca54e94a73c3fa6a7e3b76e63e5571a0987bd30))
- fix(web): share pending loads across matching graph notifications ([b49f57c](https://github.com/deepseek-ai/deepseek-harness/commit/b49f57ca12cb0cf4461fed2dbdcbc8b5e1d51106))
- fix(session): pin the disabled upload branch in the real-API extension test ([7da882d](https://github.com/deepseek-ai/deepseek-harness/commit/7da882dbebd90e055c6162b526b1cabae241b73a))
- fix(session): keep upload defaults independent of test runners ([31ec6bc](https://github.com/deepseek-ai/deepseek-harness/commit/31ec6bc7e38d55263380a0f903f9d714ce9b01aa))
- fix(chat): revert historical timing recovery from #3880 ([251ef01](https://github.com/deepseek-ai/deepseek-harness/commit/251ef01acfc7240082055443255551a02156dbd6))
- fix(chat): restore collapsed thinking by default ([3db1085](https://github.com/deepseek-ai/deepseek-harness/commit/3db1085da2dbad579886c388543c5430daf1a959))
- fix(session): keep the recorded-session marker check branch-free ([6ce915d](https://github.com/deepseek-ai/deepseek-harness/commit/6ce915d3fce169f1833cb82e28c704b37ed674c5))
- fix(desktop): prepare and sign usable bundled runtimes ([9413105](https://github.com/deepseek-ai/deepseek-harness/commit/9413105c3165a4f8e06fc18dcc89121e08c47c03))
- fix(web): preserve terminal colors and cursor contrast ([8004378](https://github.com/deepseek-ai/deepseek-harness/commit/80043785c41ca03a7ad5f2242744a48e4fabdbff))
- fix(client): bound contextual diff comparison work ([f50309b](https://github.com/deepseek-ai/deepseek-harness/commit/f50309b5d9dbe18ea59f3c6eb4a4166db66b3ed0))
- fix(web-sidebar): resolve review feedback on document preview polish ([f51adda](https://github.com/deepseek-ai/deepseek-harness/commit/f51addaa0d36f562c1425fb720db68cf5ab6dc30))
- fix(client): render actual changes in contextual diff cards ([242410c](https://github.com/deepseek-ai/deepseek-harness/commit/242410cf4b94ddfdf7f8528f6e4f74d924c2c971))
- fix(web): list only installed packages on the sidebar Plugins page ([2d660bf](https://github.com/deepseek-ai/deepseek-harness/commit/2d660bf078a22ac789f4244e99b44aa0603c0001))
- fix(browser-use): await existing Agent creation lifecycle ([6caeb50](https://github.com/deepseek-ai/deepseek-harness/commit/6caeb505c505c73d954a1dc04abe4098c3574dce))
- fix(docs): align Mermaid viewer accessible titles ([91f6733](https://github.com/deepseek-ai/deepseek-harness/commit/91f67330969acb2142fe8725350c4a480546fb94))
- fix(subagent): keep settlement notices text-only ([29debb8](https://github.com/deepseek-ai/deepseek-harness/commit/29debb8b24b57997e7918f6c597d4415721df670))
- fix(web): remove preset UI injection from global plugin manager ([c89e0cb](https://github.com/deepseek-ai/deepseek-harness/commit/c89e0cbdbd6854aaeeea956fdde371b638a27da6))
- fix(web): keep Windows PowerShell in terminal choices ([1ddd7e0](https://github.com/deepseek-ai/deepseek-harness/commit/1ddd7e08c3af9a6e734f5449c02d24a024b758c4))
- fix(desktop): hide context menu shortcut labels ([6711bb9](https://github.com/deepseek-ai/deepseek-harness/commit/6711bb9e246c6a695452c39947a85e966cde1a25))
- fix(test): use block bodies for void browser callbacks ([f0463cf](https://github.com/deepseek-ai/deepseek-harness/commit/f0463cf80ddc3c60594f6c7a7c119d17605c4d5e))
- fix(desktop): add native text context menus ([3ceb5af](https://github.com/deepseek-ai/deepseek-harness/commit/3ceb5af4d7f285564c27a57463c0805086c7660e))
- fix(workspace-changes): resolve canonical paths lazily and make the tests portable ([86a1bf1](https://github.com/deepseek-ai/deepseek-harness/commit/86a1bf1e80ef4ddf821da2c934b5764685f90a48))
- fix(docs): keep Mermaid wheel zoom anchored to the pointer ([cd0cc91](https://github.com/deepseek-ai/deepseek-harness/commit/cd0cc91382d7d6f5cfa0c2c5caee21c5c1dbf881))
- fix(web): align terminal launcher controls and guide appearance ([11b2114](https://github.com/deepseek-ai/deepseek-harness/commit/11b211478684e9923cc6eade66fdc82300b0289b))
- fix(web): keep line counts visible after a changed-files row opens ([7f5f4e7](https://github.com/deepseek-ai/deepseek-harness/commit/7f5f4e778a56568a161599a9e57d163c06c84b12))
- fix(ui): keep markdown table height stable on hover ([55a17d2](https://github.com/deepseek-ai/deepseek-harness/commit/55a17d2e576961997ab8a3e72ef6626f80524108))
- fix(workspace-changes): count argument-derived hunks, isolate per-turn state, and harden git handling ([8ea92ce](https://github.com/deepseek-ai/deepseek-harness/commit/8ea92ce9b5af81be3c40e556f2c811d5d6d92884))
- fix(workspace-changes): resolve the types subpath to source and complete exported JSDoc ([3010cb3](https://github.com/deepseek-ai/deepseek-harness/commit/3010cb3dbad4cad5d035cb886305855add554365))
- fix(web): remember shell choices before terminal startup ([37e5d8c](https://github.com/deepseek-ai/deepseek-harness/commit/37e5d8c4aac1ac5c97c9ac61382faf9c17568f63))

### 🔄 Refactoring
- perf(web): defer client combo assembly ([4228672](https://github.com/deepseek-ai/deepseek-harness/commit/42286726c8f852b45e09e692be44f01f3973acc5))
- test(desktop): avoid unsafe asymmetric matchers ([344a3c9](https://github.com/deepseek-ai/deepseek-harness/commit/344a3c9257d62b7f66d3bae04623d0f6cc41a61d))
- refactor: keep profile launch context data-only and HMR backend-scoped ([438c862](https://github.com/deepseek-ai/deepseek-harness/commit/438c862feae59cebcc3b4c2ee43e2cbd101dd42e))
- refactor(boot): use addon-managed native cache ([c3a66d9](https://github.com/deepseek-ai/deepseek-harness/commit/c3a66d9cd23f149370e45ae8e114173c0d2eff3c))
- test(boot): use native path canonicalization ([2fc6992](https://github.com/deepseek-ai/deepseek-harness/commit/2fc699255fff6f16fc81940bb3fa65282816afa3))
- test(boot): canonicalize Windows resolver paths ([a663bbf](https://github.com/deepseek-ai/deepseek-harness/commit/a663bbf4b8da1b6083ea23357a727e9fcd89f0f4))
- test(boot): cover explicit fallback failures ([9c914df](https://github.com/deepseek-ai/deepseek-harness/commit/9c914dfea9db5fd9f2b1b64d9e4398f4b1a8c025))
- refactor(web): isolate draft editor implementation without behavior changes ([b5abe6c](https://github.com/deepseek-ai/deepseek-harness/commit/b5abe6cf2969c273d7e1ac7470637bdf2eb057c1))
- test(plugins): verify CLI interruption and document recovery ([f511455](https://github.com/deepseek-ai/deepseek-harness/commit/f511455e14305f3eb533b4ab7d7460e6b95440c3))
- test(chat): pin restored timing through settlement and reload ([24a4c88](https://github.com/deepseek-ai/deepseek-harness/commit/24a4c8885952b22956a12046f4e2f779bd9e94d3))
- test: fix upload expectations and exited process cleanup ([0eb87a4](https://github.com/deepseek-ai/deepseek-harness/commit/0eb87a459079a12340bca55d72a545ddc050371c))
- test(sdk): declare upload policy for existing replay compositions ([9532ed3](https://github.com/deepseek-ai/deepseek-harness/commit/9532ed3b288fe4752188cdf91d8ed167f2762a31))
- test(session): cover environment-aware upload defaults ([b35d728](https://github.com/deepseek-ai/deepseek-harness/commit/b35d728d426c88e05c6d53f9413c1e9360380cd2))
- test(web): cover terminal cursor theme binding ([578e1e4](https://github.com/deepseek-ai/deepseek-harness/commit/578e1e428fde9eac0f85460441cf65ff4a7f80b6))
- refactor(web): keep Gateway argument handling unchanged ([ab6bb7b](https://github.com/deepseek-ai/deepseek-harness/commit/ab6bb7b86f8a6ecde60b47e20bf4bdfc1713339e))
- test(desktop): fix runtime CI fixtures across platforms ([5105c77](https://github.com/deepseek-ai/deepseek-harness/commit/5105c77706adabb17ecb9059ab90eafb31b2d288))
- refactor(boot): derive bundle enablement from selected layers ([90dddfb](https://github.com/deepseek-ai/deepseek-harness/commit/90dddfbf0892c24ca21d063d2a78e824a650fb8b))
- test(web): give the clickable-links gallery its own native-open overlay ([620c52c](https://github.com/deepseek-ai/deepseek-harness/commit/620c52ca666f3bce7c64d57d3540707c2ef1fb46))
- test(client): guard contextual diff replay against page errors ([53786d6](https://github.com/deepseek-ai/deepseek-harness/commit/53786d6415c31c561ee46e9d92a39c5e01d35ee9))
- refactor(agent-loop): remove duplicate Inbox projection registration ([cbf9fbc](https://github.com/deepseek-ai/deepseek-harness/commit/cbf9fbc29e3680612c32e62965534aa0cdb29834))
- test(workflow): await host child starts before cancellation ([7e8d42d](https://github.com/deepseek-ai/deepseek-harness/commit/7e8d42d12251340266e9ffe90ee3e5604521ca22))
- test(session): await every successful cache replacement ([88e0a5a](https://github.com/deepseek-ai/deepseek-harness/commit/88e0a5acd1ca5d08870b440d522bd72fd98860c4))
- test(session): exclude interval fallback from mandatory checkpoint ([3ba25cd](https://github.com/deepseek-ai/deepseek-harness/commit/3ba25cd4cbc1fe2e2b390ad34b6ababe0a659f37))
- test(session): await durable turn-end cache checkpoints ([a90d8df](https://github.com/deepseek-ai/deepseek-harness/commit/a90d8df582353ed1b809ee16e5ee83a60a29acc5))
- refactor(browser-use): defer DSH inference integration ([16f97e2](https://github.com/deepseek-ai/deepseek-harness/commit/16f97e2dfb3201d138a249ee4ce24e6ead4a25be))
- refactor(web): manage bundles without module composition actions ([d515500](https://github.com/deepseek-ai/deepseek-harness/commit/d5155007e040c1a4aeb372fe278e831aac32d7a5))
- refactor(plugins): retain bundle management and existing row toggles ([95e2da7](https://github.com/deepseek-ai/deepseek-harness/commit/95e2da7416f156abd7d4efee3b33f48b10f3ebe6))
- refactor(boot): limit package metadata to bundle management ([d31c59b](https://github.com/deepseek-ai/deepseek-harness/commit/d31c59b3b2ba8b03601268959f62abd6dacf9107))
- test(subagent): reuse Messages fixtures and clarify notice contracts ([1d26330](https://github.com/deepseek-ai/deepseek-harness/commit/1d26330415fb49f64d4529a4ef5852ebd5bd110e))
- refactor(web): separate preset management from global plugins ([6a6796f](https://github.com/deepseek-ai/deepseek-harness/commit/6a6796f48d294748f1d3e9d11ab5816420ef4d76))
- refactor(plugins): limit manager operations to the global profile ([07f9daa](https://github.com/deepseek-ai/deepseek-harness/commit/07f9daa55aab1c5dec2d28b21f7fbb091f1763af))
- refactor(docs): simplify Mermaid fullscreen viewer controls ([ece25ff](https://github.com/deepseek-ai/deepseek-harness/commit/ece25ff8e64448242302080c9897caae5f034a5e))
- test(web): refresh the Auto-review trajectory golden for PTC summaries ([1119fa2](https://github.com/deepseek-ai/deepseek-harness/commit/1119fa254466ea3b5f490e48fc8b2d1f840c5164))
- refactor(deliverables): simplify path helpers, hunk classification, and card status ([fa8938d](https://github.com/deepseek-ai/deepseek-harness/commit/fa8938d202bbd3b5d9a4f2f9f1633f27ecc2960b))
- refactor(boot): keep bundle analysis internal ([8fc785d](https://github.com/deepseek-ai/deepseek-harness/commit/8fc785de3aeb204d23940ecf70f21f4ecbfd9a93))
- test(web): guard fitting table geometry across interaction ([8ab3579](https://github.com/deepseek-ai/deepseek-harness/commit/8ab3579e063ff08d02c3c4e52ad4c4c20495d35c))
- refactor(deliverables): group tool-present and workspace-changes under packages/deliverables ([f800ea4](https://github.com/deepseek-ai/deepseek-harness/commit/f800ea46e5f2524ab12891d4a5f72b11e0c50d44))
- test(web): keep the sentence the right-Sidebar scenario waits for ([904e589](https://github.com/deepseek-ai/deepseek-harness/commit/904e589573911745c41d0b3e3a885e43194f37e9))
- test(web): mock retained terminals in assembled fixtures ([0a0563c](https://github.com/deepseek-ai/deepseek-harness/commit/0a0563cc9b0cb55634b9f85d75343548e562ed3d))
- test(web): update table hover scrollbar expectation ([6d81d0f](https://github.com/deepseek-ai/deepseek-harness/commit/6d81d0fdbd51841b62b45077d5b554fd1a65bbd2))
- test(plugins): cover portable read failures and refresh the module graph ([b0a2aa7](https://github.com/deepseek-ai/deepseek-harness/commit/b0a2aa7ec0cdb010a6d26832dbfbfaa871817912))
- test(web): refresh the changed-files golden for the decorative header glyph ([cdfd8ab](https://github.com/deepseek-ai/deepseek-harness/commit/cdfd8ab5b0f7886701a5509b11b16a3f41163626))
- refactor(preset): name overlay row fields explicitly ([83747b2](https://github.com/deepseek-ai/deepseek-harness/commit/83747b255f2aec40ea1e13ba6346c4299bf88d42))

### 📝 Documentation
- docs(boot): remove private native cache lifecycle ([d435044](https://github.com/deepseek-ai/deepseek-harness/commit/d4350442e814e41248c9488b94d2d36b65888358))
- docs(profile-resolution): clarify review assumptions ([662bdf3](https://github.com/deepseek-ai/deepseek-harness/commit/662bdf3833f4ceaeb28305cf5689ea54ef4d69ac))
- docs(web): define two-stage draft editor isolation ([218db70](https://github.com/deepseek-ai/deepseek-harness/commit/218db70b757af4bc378ab3e469d878f6b377da8b))
- docs(trajectory): clarify timing and thinking ownership ([d7a83ca](https://github.com/deepseek-ai/deepseek-harness/commit/d7a83ca5d6b369827e464f73f088990a1d66243b))
- docs: align historical timer reference with master ([6d835df](https://github.com/deepseek-ai/deepseek-harness/commit/6d835dfe474e5f10b35f66cf6e0603c5cde47dc1))
- docs: align Chinese session-log source reference ([ac917f4](https://github.com/deepseek-ai/deepseek-harness/commit/ac917f4df39f7730239e90dfb24af5612b24bbf3))
- docs: refresh session-log config source reference ([4885f90](https://github.com/deepseek-ai/deepseek-harness/commit/4885f907698bbc4fe375d94bb4c0d850eeb27f07))
- docs: mark removed workflow timer reference as historical ([5141675](https://github.com/deepseek-ai/deepseek-harness/commit/51416750532149499eae97b256b8fded63bfca7a))
- docs(architecture): condense launch overview after integration ([bf74907](https://github.com/deepseek-ai/deepseek-harness/commit/bf749078fbe697ec586fa6a98093de93c6f5845e))
- docs(cli): describe preserved bundle activation choices ([379fc28](https://github.com/deepseek-ai/deepseek-harness/commit/379fc281267c571e759bfe37e80303b6b3b05043))
- docs(subagent): align settlement notice descriptions ([b86b89d](https://github.com/deepseek-ai/deepseek-harness/commit/b86b89da94a19683bfbbcc8f11d50766beb0cf87))
- docs: trim repeated Inbox recovery rationale ([15e9861](https://github.com/deepseek-ai/deepseek-harness/commit/15e9861e8a22eca17abfbb61f8e46ab144b76feb))
- docs: revert unrelated timer-note path repair ([9ca343b](https://github.com/deepseek-ai/deepseek-harness/commit/9ca343b3169a62d8097e2f985fa5e80a000e25e7))
- docs(browser-use): refresh auxiliary event type acknowledgement ([ebe3ee4](https://github.com/deepseek-ai/deepseek-harness/commit/ebe3ee4d4c7d1364a6932cbec09ca57ba0f9c2bf))
- docs(browser-use): clarify conditional tool ordering ([52a8f7a](https://github.com/deepseek-ai/deepseek-harness/commit/52a8f7a759eebf995f938729b459b4b51ebdd841))
- docs(browser-use): refresh provider dependency graph ([9845c54](https://github.com/deepseek-ai/deepseek-harness/commit/9845c543c0b8498d51a0cd6d91994f3b41e7de91))
- docs(deliverables): add the subsystem page the package-group gate requires ([722008a](https://github.com/deepseek-ai/deepseek-harness/commit/722008aeeb2e3394b24ef559bce7baa0df33d25a))
- docs(config): refresh the workspace-changes catalog entry after the source moved ([88d40e2](https://github.com/deepseek-ai/deepseek-harness/commit/88d40e28ab4571fb830b6ddd4d77c368e17b23f9))
- docs(settings): refresh the generated module graph ([4373a42](https://github.com/deepseek-ai/deepseek-harness/commit/4373a4255234487ca00b4ef0d73294cbd56f424c))
- docs(api): refresh terminal dependency graph ([3219a2d](https://github.com/deepseek-ai/deepseek-harness/commit/3219a2d8e125aa7f8f04071f23f77b8879cc3bf5))
- docs(persistence): refresh format facts after acknowledging the workspace/changes event ([0d2fcf2](https://github.com/deepseek-ai/deepseek-harness/commit/0d2fcf22dc75b40a0a816cf87190678dafbc64b8))

### 🔧 Configuration
- release(dsh): 0.1.6-alpha.1 ([ea53423](https://github.com/deepseek-ai/deepseek-harness/commit/ea53423b60d0c0c6cea8bf0bdc68a758de2aff97))
- chore(runtime): upgrade builtin loader to 0.1.6 ([0bade5a](https://github.com/deepseek-ai/deepseek-harness/commit/0bade5a01012f0355837f556b75adcab27f2c3c9))
- chore(cli): restore profile resolver lockfile entry ([123272b](https://github.com/deepseek-ai/deepseek-harness/commit/123272b05e6d07b01aae37344a09295786d98da2))
- chore: remove duplicate cold-session test include ([f6e145c](https://github.com/deepseek-ai/deepseek-harness/commit/f6e145c1ea6c708d1e516b62d3d7fa9d3033f529))

## 2026-09-15

**115 commits.** 26 feature changes, 49 fixes.

### 🆕 Features
- feat(subagent): cap live continuable activations per root at 16 ([16620a3](https://github.com/deepseek-ai/deepseek-harness/commit/16620a3a70626e278b8a6fa29004b5de60fb4b39))
- feat(web): approve blocked install scripts from the install dialog ([c13d21f](https://github.com/deepseek-ai/deepseek-harness/commit/c13d21fb95c9e66f87199d7b25df87945c876088))
- feat(plugins): ship Auto review as an optional bundle ([8059d76](https://github.com/deepseek-ai/deepseek-harness/commit/8059d76ea36cc5388b9572fc2df48a79c6ac65bb))
- feat: support weighted approval delegation ([e2ae941](https://github.com/deepseek-ai/deepseek-harness/commit/e2ae9411cb91fa02df228762265c5f4408af0a15))
- feat(plugins): ship optional bundles switched off and guide the install dialog ([bc0ecae](https://github.com/deepseek-ai/deepseek-harness/commit/bc0ecae21f0accaf3cddf58b861b094ce34f2e59))
- feat(client): lazy-load PDF and terminal runtimes ([a5c224f](https://github.com/deepseek-ai/deepseek-harness/commit/a5c224f9b1cce5f4672e67e5010828e9d602ea36))
- Revert "fix(web): insert pasted composer text as line-break nodes" ([f036743](https://github.com/deepseek-ai/deepseek-harness/commit/f0367432d46eb15f7d3ad0859e8d28095fa92976))
- feat(deliverables): compare each changed file from the card ([a79b97e](https://github.com/deepseek-ai/deepseek-harness/commit/a79b97ecca459afd9f60f9cb0e522e7bc39e37dd))
- feat(web): group sidebar workspaces by parent folder ([d492b2c](https://github.com/deepseek-ai/deepseek-harness/commit/d492b2cd3649aea42d995d1ca0966558cde8ae7a))
- feat(ci): add author approval credit from merged PRs ([b5a6905](https://github.com/deepseek-ai/deepseek-harness/commit/b5a6905832bce3d924c1b6fe7b87e6a84986b3aa))
- feat(docs): present Markdown actions in a split-button menu ([eb59250](https://github.com/deepseek-ai/deepseek-harness/commit/eb59250ce9f47e8b7dbca58b8e99da84984d65ee))
- feat(cli): support profile command shorthand ([1d6534a](https://github.com/deepseek-ai/deepseek-harness/commit/1d6534a810164f1d7a8ba33d2ede78cd70c59edb))
- feat(desktop): replace failure pages with native recovery dialog ([dfb07a0](https://github.com/deepseek-ai/deepseek-harness/commit/dfb07a038ca3d14bc0059982f34e247db311d123))
- feat(web): manage plugins over the #4182 manager from the sidebar page ([4d1adb8](https://github.com/deepseek-ai/deepseek-harness/commit/4d1adb85412b3cebd95238eafe99fa479c2838f3))
- feat(web): open Markdown file links in sidebar previews ([1ec62af](https://github.com/deepseek-ai/deepseek-harness/commit/1ec62afbdb3dc2d65f45e0f923a125a36f645c70))
- feat(docs): add page Markdown copy and view actions ([23135e6](https://github.com/deepseek-ai/deepseek-harness/commit/23135e62dcac1f2f8fd8a5ab5b55e351d5bdc025))
- feat(docs): add independent platform command tabs ([bcb49ad](https://github.com/deepseek-ai/deepseek-harness/commit/bcb49ade821e83372e978c199e9be3b98fd175e0))
- feat(workspace-changes): summarize file-tool edits outside a git repository ([c48f420](https://github.com/deepseek-ai/deepseek-harness/commit/c48f4203d9b6cc3d85dcd15c3e64ded4a37b8be0))
- feat(desktop): load bundled Web UI before backend readiness ([4feb87d](https://github.com/deepseek-ai/deepseek-harness/commit/4feb87da34c74a1e799b707472bbbb4606f4ab0d))
- feat(client): give the shared menu family its keyboard model ([f46b025](https://github.com/deepseek-ai/deepseek-harness/commit/f46b025fd5b21de74167192f1fbf48958265180a))
- feat(client): accept and leave with Enter, Tab, and Escape in the composer ([c47a469](https://github.com/deepseek-ai/deepseek-harness/commit/c47a469aec945f719fbbab6877ba9eecd63bce3c))
- feat(web): configure model image input in settings ([3df6f92](https://github.com/deepseek-ai/deepseek-harness/commit/3df6f92d03722821b406e88691f8009afdb20829))
- feat(web): guide plugin installation with a pre-install check and classified failures ([ac2bed3](https://github.com/deepseek-ai/deepseek-harness/commit/ac2bed35e2abb446a7b6cc200fe3a3967bb223c5))
- feat(util): add caller-relative lazy require ([eb8cc59](https://github.com/deepseek-ai/deepseek-harness/commit/eb8cc594b3fd90fe8ad8c128576f5c9e29c491dc))
- feat(web): restore sidebar layouts and reclaim unattended terminals ([b25c5ad](https://github.com/deepseek-ai/deepseek-harness/commit/b25c5ad82e73ebb02a59a25f7336086246ee50b4))
- feat(desktop): macOS hidden titlebar with vibrancy sidebar ([f2db686](https://github.com/deepseek-ai/deepseek-harness/commit/f2db686404efdab18d24bdf8e21a1bf78725451a))

### 🐛 Bug Fixes
- fix(desktop,client): preserve folder creation and verify picker wiring ([ea5f1dc](https://github.com/deepseek-ai/deepseek-harness/commit/ea5f1dce4ad4f8c87281ea943c6fd60f36d0a05b))
- fix(desktop,client): attach workspace folder dialogs to the application window ([73dcae2](https://github.com/deepseek-ai/deepseek-harness/commit/73dcae2915192262138d94765dafb5f8f2300f2e))
- fix(experimental): declare react as a build input of the agent team client ([b017b28](https://github.com/deepseek-ai/deepseek-harness/commit/b017b2861c352dee480171d1ef5b19f8f4392ef3))
- fix: authenticate and reconcile approval delegations ([3e9b6ad](https://github.com/deepseek-ai/deepseek-harness/commit/3e9b6ad94e00b4ece813ffba4ef91925ade7794d))
- fix: dismiss prior reviews when delegating approval ([60d26ac](https://github.com/deepseek-ai/deepseek-harness/commit/60d26ac4ab4e111f7846be17b18d7afe940fceaf))
- fix(web): start the approval retry with a fresh log and keep the install dialog in view ([5e5f0a2](https://github.com/deepseek-ai/deepseek-harness/commit/5e5f0a239398200e26456cfc07757223c1e2ea36))
- fix(client): version lazy chunks by build generation ([7fb4cb4](https://github.com/deepseek-ai/deepseek-harness/commit/7fb4cb4c8e535f06377c663e8576d4ec29d1f47a))
- fix(client): satisfy chunk loader test lint ([45c74c5](https://github.com/deepseek-ai/deepseek-harness/commit/45c74c54837490976e36ba0589776b58111d423b))
- revert(client): remove eager chunk scanning ([7f5385b](https://github.com/deepseek-ai/deepseek-harness/commit/7f5385bf013ad3210050f99816cd92fc36f67dc9))
- fix(client): preserve lazy chunk runtime semantics ([d28807e](https://github.com/deepseek-ai/deepseek-harness/commit/d28807e05c0d79296f589625256d90883b64fef9))
- fix(client): align lazy chunk metadata ([ee9f43b](https://github.com/deepseek-ai/deepseek-harness/commit/ee9f43bc5d60bb2131713c5bd31afbd86bcf3723))
- fix(plugin-manager): address approval review and remove agent notices ([a5dea50](https://github.com/deepseek-ai/deepseek-harness/commit/a5dea502a6a437d0e3cb7fb2d4cdd22acda85558))
- fix(desktop): clean profile core packages before production startup ([09be5f7](https://github.com/deepseek-ai/deepseek-harness/commit/09be5f750a2e548268e49ef039df93ee8a14def9))
- fix(desktop): bound fatal diagnostics and restore failed package operations ([791f731](https://github.com/deepseek-ai/deepseek-harness/commit/791f731c08641f99eabd7857bd3463a48a23a9a2))
- fix(desktop): support Node 26 runtime archive extraction ([f4b7a59](https://github.com/deepseek-ai/deepseek-harness/commit/f4b7a5948c7d5fab681c72a7889f222a90385547))
- fix(docs): keep platform commands readable in MPA builds ([7aca916](https://github.com/deepseek-ai/deepseek-harness/commit/7aca91667923b40f1dce6abc594eb086e1b1e6db))
- fix(web): insert pasted composer text as line-break nodes ([96da25c](https://github.com/deepseek-ai/deepseek-harness/commit/96da25c8f5385dddb58c19090e1546c0b3d126cb))
- fix(web): reword the plugin install dialog and name failed actions ([d50f062](https://github.com/deepseek-ai/deepseek-harness/commit/d50f062c646259d26c7d885ba0575e6bf4c49431))
- fix(web): show the full package name on a bundle's page ([5c8b4e5](https://github.com/deepseek-ai/deepseek-harness/commit/5c8b4e583425e3f21c14530336dd1664131e3a71))
- fix(web): polish the plugin page, detail page, and rail per design ([c6b81a7](https://github.com/deepseek-ai/deepseek-harness/commit/c6b81a75fdca3fbf13345665753f0627a81896e3))
- fix(plugin-manager): approve blocked dependency builds before retrying ([ffffac3](https://github.com/deepseek-ai/deepseek-harness/commit/ffffac3cba7d0df0b9ce907d068cedecd83421f1))
- fix(web): keep plugin cards in title order across switches ([0d4b32f](https://github.com/deepseek-ai/deepseek-harness/commit/0d4b32f0773e374b62719c657071d6d0f4ca8a11))
- fix(docs): preserve menu activation across pointer focus changes ([423e86f](https://github.com/deepseek-ai/deepseek-harness/commit/423e86ff7d88e7d40b0eeb98b81bd4c1b93b889e))
- fix(workspace-changes): review round on the served summaries ([c8bc104](https://github.com/deepseek-ai/deepseek-harness/commit/c8bc10440be3d1fa494e025a373f9c6d4e7f0589))
- fix(docs): address Markdown actions review feedback ([38b2bf2](https://github.com/deepseek-ai/deepseek-harness/commit/38b2bf2f6c204ceade053ef11275386f9fba2730))
- fix(llm): resolve Messages endpoint suffix (#4241) ([bd421cc](https://github.com/deepseek-ai/deepseek-harness/commit/bd421cce7bab7bf203b201ad5cd6e9aa9ebcecb5))
- fix(cli): address profile shorthand review feedback ([7d4188b](https://github.com/deepseek-ai/deepseek-harness/commit/7d4188b45033a51abfd5af1ec9328489909be7f5))
- fix(workspace-changes): count an appended line as one addition ([da6e3f9](https://github.com/deepseek-ai/deepseek-harness/commit/da6e3f9edf7a31e47a5495ae15e6f2516587e2cd))
- fix(docs): preserve UTF-8 in raw Markdown navigation ([cb464f1](https://github.com/deepseek-ai/deepseek-harness/commit/cb464f18943ad48080eabad94e00d61503717bb1))
- fix(ci): address production blame approval review ([794b658](https://github.com/deepseek-ai/deepseek-harness/commit/794b65840173c97117a97b2019249d5b707fd3d7))
- fix(plugin-manager): keep package operations outside HMR ([08021a1](https://github.com/deepseek-ai/deepseek-harness/commit/08021a16d8d011dcb9b596e56d54e987670c950b))
- fix(plugin-manager): clean failed installs and address critical review findings ([61665c3](https://github.com/deepseek-ai/deepseek-harness/commit/61665c3454c269190acc14691c05e5ea4fa7a818))
- fix(web): address model image settings review ([41e591b](https://github.com/deepseek-ai/deepseek-harness/commit/41e591b3e4e941792ef723c79a83e32e3cbf5d73))
- revert: restore original CLI profile boot exports ([830c826](https://github.com/deepseek-ai/deepseek-harness/commit/830c82687bef09b2fb6d83c70c4ceace2a797882))
- fix(ui): keep transcript resize handles unobtrusive ([1bec11e](https://github.com/deepseek-ai/deepseek-harness/commit/1bec11e3668926d5e749093079fb7e14588460f1))
- fix(client): keep a launcher-opened menu open through its own focus track ([21a7859](https://github.com/deepseek-ai/deepseek-harness/commit/21a785902bf053802525ce21d0726c996b95638a))
- fix(ci): validate Web injection payload and cover macOS sidebar controls ([9ce6d98](https://github.com/deepseek-ai/deepseek-harness/commit/9ce6d98e11a1f7efc191d5098c566be0829788b0))
- fix(web): forward client graphs without Host lifecycle waits ([6d05c95](https://github.com/deepseek-ai/deepseek-harness/commit/6d05c9557f94e01f90f4372f3b6f3ca93976615a))
- fix(client): answer the review bot's findings on the keyboard hand-offs ([b263581](https://github.com/deepseek-ai/deepseek-harness/commit/b263581e920a58f1df8e8570c3f56b650ea336a1))
- fix(cli): expose only the shared profile runner API ([255374a](https://github.com/deepseek-ai/deepseek-harness/commit/255374afa156c524d9fb7e7e6885d7c7eabe80d0))
- fix(client): tighten the keyboard hand-offs, and drop the dialog Escape layering ([5c3081e](https://github.com/deepseek-ai/deepseek-harness/commit/5c3081eeaa95968854aa59acfb45a40765692bbc))
- fix(web): reconcile pending plugin revisions and preserve bootstrap ([2c9375e](https://github.com/deepseek-ai/deepseek-harness/commit/2c9375e5096ebd03883b17ac4fff3c975dded23a))
- fix(hmr): retain consecutive profile configuration changes ([b77c19c](https://github.com/deepseek-ai/deepseek-harness/commit/b77c19c376275cea7e7a2e9f2d41b9cc6850c028))
- fix(client): keep the ring on the triggers and off the menu rows ([4fc515c](https://github.com/deepseek-ai/deepseek-harness/commit/4fc515cb6802c957b9794584498ff7d6fb0ef91e))
- fix(client): keep the browser ring on the focused menu row ([449a461](https://github.com/deepseek-ai/deepseek-harness/commit/449a4610d7fe906a69ca3e666dbd008d4d62ece2))
- fix(web): clarify external app availability for delivered files ([0976569](https://github.com/deepseek-ai/deepseek-harness/commit/0976569d16c229367384ea4691ab82ef2b2112fe))
- fix(web): isolate terminal bindings and validate saved layouts ([281723b](https://github.com/deepseek-ai/deepseek-harness/commit/281723bed8320f27ba914867045f726917d9c2c3))
- fix(session-controller): reconcile list cache in linear time ([53046b2](https://github.com/deepseek-ai/deepseek-harness/commit/53046b21b429a15c1ecda9a90fa0c7c9678f7ef8))
- fix(hmr): match Node module paths and contain startup reload failures ([ca4db9c](https://github.com/deepseek-ai/deepseek-harness/commit/ca4db9c75593273170c729cba1b42a18b3a257f7))

### 🔄 Refactoring
- test(desktop,client): keep picker composition coverage with its feature ([48dd4b3](https://github.com/deepseek-ai/deepseek-harness/commit/48dd4b3bea9c87091de3db413312099be258b7cf))
- refactor(plugins): name bundles by their package name only ([a9fe93f](https://github.com/deepseek-ai/deepseek-harness/commit/a9fe93fc0b11195131dbd841213ff880208635cf))
- test(web): resolve the built app-boot when a scaffold launches ([e22c631](https://github.com/deepseek-ai/deepseek-harness/commit/e22c63185af2eccf23d6d1039683ac3aaf24c7c7))
- test(client): count the plugin page's two glyphs in the icon set ([15eb952](https://github.com/deepseek-ai/deepseek-harness/commit/15eb952733b7322a27ff3b506b956f1490b0579f))
- refactor(web): keep the plugin manager's store state types package-private ([430f88d](https://github.com/deepseek-ai/deepseek-harness/commit/430f88d1c57ae6be056facbecfbcab208fefd6f5))
- refactor(plugins): read a bundle's one-liner from the package description only ([79729c3](https://github.com/deepseek-ai/deepseek-harness/commit/79729c34228e65997bfdd10a4a8fdddca9461b61))
- refactor(plugins): name the optional bundles in the launcher, not the installation manifest ([fa32020](https://github.com/deepseek-ai/deepseek-harness/commit/fa320209aba737c407b74fe6ecbf89e2e6114aa6))
- refactor(plugins): stop announcing patch generations applied outside the manager ([f04c265](https://github.com/deepseek-ai/deepseek-harness/commit/f04c2657255b04284d10f6b6d5465621d87ae022))
- refactor(app-boot): drop the root Include lookup by id ([c3c7a4f](https://github.com/deepseek-ai/deepseek-harness/commit/c3c7a4f4123e1bbaa18d4f98ce91291f5155ed73))
- test(client): cover lazy chunk loader branches ([b98d5c8](https://github.com/deepseek-ai/deepseek-harness/commit/b98d5c8003b0429744a40367dd54811a8dd88c76))
- perf(client): load split bundles on demand ([b1471fd](https://github.com/deepseek-ai/deepseek-harness/commit/b1471fd73c200d46a3b3ac0e9268fb0d9c50a5f9))
- perf(api-gateway): avoid duplicate client input parsing ([7c74636](https://github.com/deepseek-ai/deepseek-harness/commit/7c74636892dba950e752cc6961517f62f428ac6e))
- perf(llm): avoid aggregate pi-ai runtime import ([75a56be](https://github.com/deepseek-ai/deepseek-harness/commit/75a56be10cb3b2efdae23357f2e9e6540e0f8d2b))
- refactor(desktop): remove unused recovery IPC paths ([89a8940](https://github.com/deepseek-ai/deepseek-harness/commit/89a89408c6ee082de564d034f6da511d824c090b))
- test(web): synchronize composer selection before deletion ([6db9466](https://github.com/deepseek-ai/deepseek-harness/commit/6db9466c4e0702167c5750e705aec96980c7cc8c))
- test(plugin-manager): canonicalize pnpm fixture workspace paths ([f9756ed](https://github.com/deepseek-ai/deepseek-harness/commit/f9756edac06c1fa2a09ffc801b53b02b21a74d58))
- refactor(web): derive workspace hierarchy automatically from paths ([db2e03b](https://github.com/deepseek-ai/deepseek-harness/commit/db2e03b89d552f679d025d41c0bf56a3093ff607))
- test(plugin-manager): install packed addon for build approval coverage ([8848e1e](https://github.com/deepseek-ai/deepseek-harness/commit/8848e1e94fa6325d1141786bd49991c3e938fd39))
- refactor(web): unify workspace grouping controls and row highlights ([e706da7](https://github.com/deepseek-ai/deepseek-harness/commit/e706da74241c8e41fa4f004f82e563996caad6d0))
- test(web): disambiguate workspace rows during reconnect ([f3c0ae6](https://github.com/deepseek-ai/deepseek-harness/commit/f3c0ae620b4e3fa8050a35cfe96f80ad89c0fa56))
- test(subprocess): verify owned exit listeners on disposal ([cc872a3](https://github.com/deepseek-ai/deepseek-harness/commit/cc872a39b9ac7793a918a5ce85d9a66570e9c5b9))
- test(web): register file-link scenario in host compilation ([25525dc](https://github.com/deepseek-ai/deepseek-harness/commit/25525dc49547ff136d274d2d32681e4b9d36cd73))
- test(web): finish sidebar transitions before preview capture ([9e611c9](https://github.com/deepseek-ai/deepseek-harness/commit/9e611c90a31c35d3c7ea14a572417d425b67725e))
- test(web): verify keyboard file navigation and capture preview ([7bc0154](https://github.com/deepseek-ai/deepseek-harness/commit/7bc0154bfc898634bdda97a04c9adcaafca7ed08))
- test(web): refresh the changed-files golden for master's edit-card counts and desktop copy ([2a77c59](https://github.com/deepseek-ai/deepseek-harness/commit/2a77c59a49d762323073e786b7eb65b33e823486))
- refactor(client): compute the menu's keyboard region once per key ([afbe3a4](https://github.com/deepseek-ai/deepseek-harness/commit/afbe3a4b1d49823b0563b13514faa5e7a737a7b4))
- test(subprocess-local): cover configured ZDOTDIR without zsh ([149ed69](https://github.com/deepseek-ai/deepseek-harness/commit/149ed6991232c825f6e9d69d7341b9aae77c87b2))
- refactor(hmr): own profile reload lifecycle through YAML ([abd765a](https://github.com/deepseek-ai/deepseek-harness/commit/abd765a6001ff9d9c9772b8b407e0b7f18fe25ab))
- perf(typert): materialize generated schemas on first use ([e459e32](https://github.com/deepseek-ai/deepseek-harness/commit/e459e3263733075bd806d9ba6dd92bbc4bf3983f))
- perf(runtime): defer optional native dependencies ([232ab76](https://github.com/deepseek-ai/deepseek-harness/commit/232ab768a94d5b18c683f60285907f5891a190f5))
- test(subprocess): refresh terminal activity API snapshot ([a2112c0](https://github.com/deepseek-ai/deepseek-harness/commit/a2112c07e4f72439b9b80c75a788feed0447aed7))
- test(ci): repair packed inventory context fixture ([dcf1d27](https://github.com/deepseek-ai/deepseek-harness/commit/dcf1d274d93508322fe6d6fb32af6dfca29fcce4))

### 📝 Documentation
- docs(desktop,client): align native directory picker summaries ([21c7828](https://github.com/deepseek-ai/deepseek-harness/commit/21c782867843b960d8138444d678fb33b14b72a3))
- docs: synchronize translated subagent event references ([2d24d80](https://github.com/deepseek-ai/deepseek-harness/commit/2d24d80d5ff38b5e7687ce549d77494115a1feb0))
- docs(config): refresh generated catalog pairing ([72aaad5](https://github.com/deepseek-ai/deepseek-harness/commit/72aaad53fdaf92b05657d18da4557a2782647d4e))
- docs: refresh plugin manager dependency graph ([ef49857](https://github.com/deepseek-ai/deepseek-harness/commit/ef4985792d1d7f01e28e0fd52c339d3b811bf08e))
- docs(desktop): remove stale runtime and reload descriptions ([57af1f0](https://github.com/deepseek-ai/deepseek-harness/commit/57af1f0013e4a7ba587451dcd8e866013423dce3))
- docs(client): drop a reverted implementation from the note's evidence list ([3065f9c](https://github.com/deepseek-ai/deepseek-harness/commit/3065f9cc27e7074c629b1e4527d962518439a3ec))
- docs(client): record the SessionInput focus addition in the note ([4b8a47a](https://github.com/deepseek-ai/deepseek-harness/commit/4b8a47a1987c38b56e04d1fc6dec905943ad0f47))
- docs(web): clarify client plugin reload failures ([1fec9ad](https://github.com/deepseek-ai/deepseek-harness/commit/1fec9adb61006173edfdf9a76f6a648cb1eb9d71))

## 2026-09-16

**120 commits.** 25 feature changes, 50 fixes.

### 🆕 Features
- feat(document): decouple shared Office conversion from preview ([9d2a3bf](https://github.com/deepseek-ai/deepseek-harness/commit/9d2a3bf2b7987e82d29c715fec2b772f9f3fc66a))
- feat(web): let the install dialog's close control stop a running install ([57a705f](https://github.com/deepseek-ai/deepseek-harness/commit/57a705fa7eb5201e3fc85e2fd15fbd5bc68a7553))
- feat(web): open a row's configuration from its name and label the guide examples ([62c66da](https://github.com/deepseek-ai/deepseek-harness/commit/62c66dad02da9d16d55fd83aae83853950b67b3e))
- feat(web): host plugin configuration on the Plugins page ([90af311](https://github.com/deepseek-ai/deepseek-harness/commit/90af3110b722a83b0815450c83f47154ce4b5422))
- feat(web): unify Subagent settings UI ([ea2651b](https://github.com/deepseek-ai/deepseek-harness/commit/ea2651b86b54058c762dead066434371ffbad91a))
- feat(client): cover mainstream sites in known-site link marks ([214ab45](https://github.com/deepseek-ai/deepseek-harness/commit/214ab45932b18a3bf2413732e4f3c450d5601490))
- feat(desktop): open Feishu login DevTools with F12 ([6d05e76](https://github.com/deepseek-ai/deepseek-harness/commit/6d05e76b897cb30dbe7d46a35d40ab1529fa961d))
- feat(client): lead known-site links with the site's own mark ([59456db](https://github.com/deepseek-ai/deepseek-harness/commit/59456dbb5b92f25516f3d8e4de6b2b5ee3231499))
- feat(preview): consume shared Office conversion independently ([54d268c](https://github.com/deepseek-ai/deepseek-harness/commit/54d268c409e501726e61977a6878f2b94821d314))
- feat(desktop): add native About menu and panel ([1be847f](https://github.com/deepseek-ai/deepseek-harness/commit/1be847f736075589869dab02e94cf27a444e6526))
- feat(creator): use Plugin Manager for persistent plugins ([ed32f57](https://github.com/deepseek-ai/deepseek-harness/commit/ed32f57f88ef6bba983e30a0b434fe5d77e5773b))
- feat(desktop): enable standalone Office skills ([fa518ec](https://github.com/deepseek-ai/deepseek-harness/commit/fa518ecd89feece78557720caf91f9b45fc80e32))
- feat(web): make Workspace tree an explicit grouping option ([b432223](https://github.com/deepseek-ai/deepseek-harness/commit/b432223364e85248b50bf03beef977c3f10168d7))
- feat(deliverables): review one turn's changed files in a single tab ([fc10bc1](https://github.com/deepseek-ai/deepseek-harness/commit/fc10bc18e018d624b2fd7da2ddddacfef492c1f1))
- Raise author approval credit to 1.1 at 100 merged PRs ([c7e7e8b](https://github.com/deepseek-ai/deepseek-harness/commit/c7e7e8bc18b5f0bac3fb00ba6def00aeb5dc0d6a))
- Keep desktop package launchers out of the Host execution PATH ([3e6d931](https://github.com/deepseek-ai/deepseek-harness/commit/3e6d93171d590cbd97208d9f3738b42dbb0f635a))
- feat(web): give user terminals system-user permissions ([ab695ef](https://github.com/deepseek-ai/deepseek-harness/commit/ab695ef4cf4c798840506e45503ffd75c38cc47a))
- feat(web): unify model input controls and catalog inheritance ([cc39423](https://github.com/deepseek-ai/deepseek-harness/commit/cc394230bfd124b7e163eb593ff9e1dcce948f9c))
- feat(web): guide file references with concise colon labels ([fbc6abc](https://github.com/deepseek-ai/deepseek-harness/commit/fbc6abcfd42f6dc8d465218c750f97855119e750))
- feat(desktop): ship standalone Python Office runtime ([869a3f6](https://github.com/deepseek-ai/deepseek-harness/commit/869a3f6d27b96470db22e05154584d32f180e591))
- feat(subagent): own editable delegation limits in the backend ([a69bcf3](https://github.com/deepseek-ai/deepseek-harness/commit/a69bcf36369c1f2f4fb18ef7b7a22592de3c76f9))
- feat(subagent): edit delegation limits in plugin settings ([845115d](https://github.com/deepseek-ai/deepseek-harness/commit/845115d0f8ab65c1db888848201c9f881aea9a0f))
- feat(llm): remove the V4 Flash and V4 Flash Vision Exp defaults ([f2beb99](https://github.com/deepseek-ai/deepseek-harness/commit/f2beb99c3bf84021e644cfb5ee3bae2b20593107))
- feat(desktop): add ordinary and mandatory update flows ([63dd8fb](https://github.com/deepseek-ai/deepseek-harness/commit/63dd8fb80d7cadccb727e83bc1cadebdfa55449d))

### 🐛 Bug Fixes
- fix(web): reject Mermaid image nodes before layout ([aaa62b0](https://github.com/deepseek-ai/deepseek-harness/commit/aaa62b09dcfc19a2d8a0476673fb3be48f714457))
- fix(web): keep preview failures readable and trim unrelated scope ([63b5403](https://github.com/deepseek-ai/deepseek-harness/commit/63b5403a43aa1b965f975609fea1276bd623af7e))
- fix(client): size chat previews from diagrams and defer source rendering ([9b9a60f](https://github.com/deepseek-ai/deepseek-harness/commit/9b9a60f43942235bb5ef74f5b10ca25c03e55f94))
- fix(web): update Subagent parallelism copy ([6affc44](https://github.com/deepseek-ai/deepseek-harness/commit/6affc4499295fdb849ffe1a700f7d5b127b57403))
- fix(document): select Office engines from declared native targets ([a69639a](https://github.com/deepseek-ai/deepseek-harness/commit/a69639a20088c80da8600fb4188337acb6e028f3))
- fix(desktop): complete the macOS menu defaults ([b9fde8d](https://github.com/deepseek-ai/deepseek-harness/commit/b9fde8d0639f85ddd5c3c76e715bddf0b3b26eb4))
- fix(cli): complete startup diagnostics before exiting ([053cad9](https://github.com/deepseek-ai/deepseek-harness/commit/053cad9442670418a348f99ca6229a4fa0e9decf))
- fix(desktop): declare the standard macOS window menus ([3809949](https://github.com/deepseek-ai/deepseek-harness/commit/380994942d4fe0018c90cf45776095b07c72f681))
- fix(desktop): make Windows mandatory update window movable ([b3795cb](https://github.com/deepseek-ai/deepseek-harness/commit/b3795cb99f7796f4e43e1b293fcf35939a21ef2a))
- fix(cordis): dispose only the registered logger exporter ([ac2f890](https://github.com/deepseek-ai/deepseek-harness/commit/ac2f890291a0c1f5b8bc785fca2ae39005343819))
- fix(cli): save full startup diagnostics under DSH_HOME logs ([18260e3](https://github.com/deepseek-ai/deepseek-harness/commit/18260e3b0c5e1e2941a0bc15ecf7696f3ced4a22))
- fix(desktop): present installer welcome and package 0.1.6-alpha.1.20260916.2 ([c624c2e](https://github.com/deepseek-ai/deepseek-harness/commit/c624c2eff07f3806f8e4a26881908ea00e602790))
- fix(deliverables): satisfy the static gates and Windows tests ([974d027](https://github.com/deepseek-ai/deepseek-harness/commit/974d0271c00698fdf3e6113a37f11f2e24c615ae))
- fix(cli): group startup failures and pending services ([38fb1a1](https://github.com/deepseek-ai/deepseek-harness/commit/38fb1a11f9130af504c916528395b9516a717ca7))
- fix(subprocess): hide Windows shell console windows at creation ([f8b1309](https://github.com/deepseek-ai/deepseek-harness/commit/f8b1309fe55ad29d54451886049d0c541be94d5a))
- fix(desktop): clarify profile recovery scope and diagnostics ([04794bd](https://github.com/deepseek-ai/deepseek-harness/commit/04794bd90e501d524f2d1ed8ca7f509ca0dca3c7))
- fix(boot): timestamp profile patch backups ([60058f1](https://github.com/deepseek-ai/deepseek-harness/commit/60058f118b25962e2ae0ff9f1412820218c42867))
- fix(creator): address plugin workflow review findings ([8c5ae87](https://github.com/deepseek-ai/deepseek-harness/commit/8c5ae870c26bb6c1bf0eef869594b40316f30393))
- fix(desktop): back up profile patches during recovery ([8d5c7e4](https://github.com/deepseek-ai/deepseek-harness/commit/8d5c7e4e2af23acb4ed67561b5c4faeb6353fafb))
- fix(web): allow opening the sidebar before the first message ([7f2d7b1](https://github.com/deepseek-ai/deepseek-harness/commit/7f2d7b1791b8def05fbd74443652cbb69464928a))
- fix(desktop): preserve the dsh base in dated test versions ([a221579](https://github.com/deepseek-ai/deepseek-harness/commit/a2215799b8ccf8ace7fae4fe1fafebca3ab26083))
- fix(deliverables): scroll the split review columns sideways together ([26e2196](https://github.com/deepseek-ai/deepseek-harness/commit/26e2196a8629560dd7992b0a02f8bde156a525e4))
- fix(plugin-manager): request approval for single-call full access ([9a83772](https://github.com/deepseek-ai/deepseek-harness/commit/9a837725600abefc0e071cb1f88a7582b431f602))
- fix(deliverables): open the review from the card header and scroll unwrapped split columns separately ([91d9346](https://github.com/deepseek-ai/deepseek-harness/commit/91d9346aa11e2b4a62dcaaaf8ed083afc16b7947))
- fix(plugin-manager): require full access for agent tool calls ([470d4aa](https://github.com/deepseek-ai/deepseek-harness/commit/470d4aae1110389094f520a96e05dbe898ddae6a))
- fix(web): address Workspace tree review feedback ([5ec3368](https://github.com/deepseek-ai/deepseek-harness/commit/5ec33682856f0a655cfc2e45ca148a49455d4198))
- fix(creator): bound visual verification and refresh module graph ([7342687](https://github.com/deepseek-ai/deepseek-harness/commit/7342687170b24c4d17017ed50944ecc4f83b5799))
- fix: carry session writer failures by typed remote code ([5c369a0](https://github.com/deepseek-ai/deepseek-harness/commit/5c369a0a1f179e1e503e8d5356136483de16e080))
- fix(web): isolate model settings tests and update input guide ([f568355](https://github.com/deepseek-ai/deepseek-harness/commit/f5683559a5d8cc334e2416d93bb6e38491fcbb60))
- fix(office): validate strict and corrupt OOXML ([82ab876](https://github.com/deepseek-ai/deepseek-harness/commit/82ab876331c57736aed15af05e461401e5a15df4))
- fix: load optional persistence errors only with its service ([eb57fdb](https://github.com/deepseek-ai/deepseek-harness/commit/eb57fdb9c63e2c8484aecd7b2a8ba357df77500d))
- fix(desktop): show a local document while the policy login page loads ([08b75ad](https://github.com/deepseek-ai/deepseek-harness/commit/08b75ade4088c1436c26e26d7e3f801c26a9952a))
- fix(desktop): tighten the update entry label and downloaded detail ([a3d2cb4](https://github.com/deepseek-ai/deepseek-harness/commit/a3d2cb400b44806cc51e15950724295359d7154b))
- fix(client): yield the enclosing tooltip to a nested one ([daf185f](https://github.com/deepseek-ai/deepseek-harness/commit/daf185fd24dd3d4670556d062ebeff697a5da4ea))
- fix: explain session writer contention in toasts ([e0f170b](https://github.com/deepseek-ai/deepseek-harness/commit/e0f170b8d046a92cfd4288b89bf42d42f95abaac))
- fix(desktop): upload releases with Tencent COS SDK ([e6c507d](https://github.com/deepseek-ai/deepseek-harness/commit/e6c507d65f0a3787bb038e78db2f91121144334b))
- fix(llm): tolerate malformed historical Messages tool input ([1f030b3](https://github.com/deepseek-ai/deepseek-harness/commit/1f030b3c1c5aa7164a42f483075c80fe29559f41))
- fix(workspace-changes): list oversized pairs, bound capture reads, and resolve paths through symlinked ancestors ([2440937](https://github.com/deepseek-ai/deepseek-harness/commit/2440937459ea30c5b3425393ac281ac28c2aa994))
- fix(sandbox): accept repeated effective permission modes ([61c548e](https://github.com/deepseek-ai/deepseek-harness/commit/61c548e200ab00e6eceaf81bce3a819c195f393c))
- fix(subagent): map capacity refusal and clarify one-shot scope ([0eed02d](https://github.com/deepseek-ai/deepseek-harness/commit/0eed02d44771e25fe7abb2f6df799ac27b4dc1b0))
- fix(ptc): limit Electron selector to startup and budget native tests ([a66d81e](https://github.com/deepseek-ai/deepseek-harness/commit/a66d81e33f7938bc678f7cda94101a666d69d9b6))
- fix(ptc): preserve Electron Node mode when launching programs ([a139e6e](https://github.com/deepseek-ai/deepseek-harness/commit/a139e6e9e1ef3cbce7c191682b85c0c86ebacce0))
- fix(desktop): preflight Windows signing before builds ([bfe6beb](https://github.com/deepseek-ai/deepseek-harness/commit/bfe6beb517ebd121633b81b1d76fa2d68fe83792))
- fix(web): localize built-in plugin names and descriptions ([6bc7938](https://github.com/deepseek-ai/deepseek-harness/commit/6bc7938a151dd68544c336ce757208a7de0d7fd9))
- fix(subagent): default to eight live continuable children ([d7f9d3a](https://github.com/deepseek-ai/deepseek-harness/commit/d7f9d3a773544b68568ff25f0508a70643627ec1))
- fix(desktop): isolate Windows signature inspection modules ([c781e85](https://github.com/deepseek-ai/deepseek-harness/commit/c781e85e92f90c9132fe5ec668e763ce6e95b7f1))
- fix(desktop): prepare unattended macOS signing from required p12 ([9fefcd7](https://github.com/deepseek-ai/deepseek-harness/commit/9fefcd7c0645e357dfe6b7939bc43ebed5f9e749))
- fix(desktop): preserve verified runtime signatures during packaging ([b06ea72](https://github.com/deepseek-ai/deepseek-harness/commit/b06ea72226100960314298ebf025cb3e57987f26))
- fix(desktop): sign bundled Windows runtime before validation ([b37687c](https://github.com/deepseek-ai/deepseek-harness/commit/b37687c1412738417e7d431d9d7a3ce47a3f9ec0))

### 🔄 Refactoring
- test(web): update shared code action accessibility snapshots ([078e113](https://github.com/deepseek-ai/deepseek-harness/commit/078e11389a2c36c4d7b46f59d7218dea0105077e))
- refactor(document): consolidate Office conversion into office-to-pdf ([1166900](https://github.com/deepseek-ai/deepseek-harness/commit/11669006e6af481d764666f98b1275f2c19f59a2))
- refactor(document): name Office PDF conversion explicitly ([a193b51](https://github.com/deepseek-ai/deepseek-harness/commit/a193b51c96e71d5041ccb8c897cc305cec24034a))
- style(web): remove Subagent section divider ([78f4c5a](https://github.com/deepseek-ai/deepseek-harness/commit/78f4c5ae329f1491058f629954e4b30cbbc9081f))
- style(web): soften Subagent help icons ([a8de4c3](https://github.com/deepseek-ai/deepseek-harness/commit/a8de4c334eab74cac8680f46141dc8296d4983b8))
- refactor(web): share the card head and page top on the Plugins page ([a63dd80](https://github.com/deepseek-ai/deepseek-harness/commit/a63dd809a2b5ed22f27569e2fc856bbca50e83b3))
- test(bench): set trajectory navigation budget to 650 ms ([5e942d3](https://github.com/deepseek-ai/deepseek-harness/commit/5e942d39eb539fb3555b7192bae62b181f56d2a8))
- refactor(client): take known-site link marks from simple-icons ([f018fe8](https://github.com/deepseek-ai/deepseek-harness/commit/f018fe8f10c2b372a675f6a289d13b49bdf9863a))
- test(web): refresh the present-svg golden for the review-opening card ([c1f9d19](https://github.com/deepseek-ai/deepseek-harness/commit/c1f9d19658d356cafe112bc563de1c1b427c2ef0))
- test(web): match the terminal close response without unsafe JSON access ([d1e93e5](https://github.com/deepseek-ai/deepseek-harness/commit/d1e93e5482080d36d19a10dcf0f5f9fd1ad6f2eb))
- test(web): await terminal close acknowledgement before cleanup assertions ([51a9382](https://github.com/deepseek-ai/deepseek-harness/commit/51a9382b610dad0398e8070a944ccabe8cb1e088))
- test(web): update blank session header snapshots ([b0542ec](https://github.com/deepseek-ai/deepseek-harness/commit/b0542ec0e2e4d616d7e3c66cebe188723ef2f9d4))
- refactor(boot): name the profile pnpm invocation explicitly ([3cd6782](https://github.com/deepseek-ai/deepseek-harness/commit/3cd67821140939cf159b6d2b13f024a48b719412))
- test(web): refresh Creator skill instructions card ([2fc6e38](https://github.com/deepseek-ai/deepseek-harness/commit/2fc6e38d2b23eafe373605a6bfc56974b585fc3c))
- test(plugin-manager): keep approval assertions type-safe ([d86da2e](https://github.com/deepseek-ai/deepseek-harness/commit/d86da2e31cf6daaaa089d7fd6126cdfbcbb85ffd))
- test(creator): align Web fixtures with persistent plugin management ([040be00](https://github.com/deepseek-ai/deepseek-harness/commit/040be00cb41d5e58ffecfa0071576a9247274e36))
- refactor(web): clarify model input docs and strengthen tests ([5d51ba5](https://github.com/deepseek-ai/deepseek-harness/commit/5d51ba5a9c3e54192fb9a45eddc7a0537bce57d4))
- test(creator): refresh Python restart tool inventory ([74e5694](https://github.com/deepseek-ai/deepseek-harness/commit/74e5694e6bad5cde879bb39503eaafb6ce326416))
- test(creator): replace retired Cordis tool scenarios ([92da029](https://github.com/deepseek-ai/deepseek-harness/commit/92da029f6d8dd4aa82aa9eae8227acbd47bf2059))
- test(web): cover model draft and provider input defaults ([2a5c227](https://github.com/deepseek-ai/deepseek-harness/commit/2a5c227199c08defdcefae3e1353aa8d8971ea93))
- test(acp): refresh the fs-same-mode fixture for the write operation metadata ([a1ac837](https://github.com/deepseek-ai/deepseek-harness/commit/a1ac8371de7286ed9799a02cddf6698911754093))
- test(ui-deliverables): preserve file-reference prompt evaluations ([f25f352](https://github.com/deepseek-ai/deepseek-harness/commit/f25f3527ef6aeba787f2e06150ede8096e3c059b))
- style(desktop): wrap dialog mock after rebase ([285da0f](https://github.com/deepseek-ai/deepseek-harness/commit/285da0fa64230198fc439a7ebfea8b0ccdadcf82))
- test(web): align shipped file-reference guidance expectation ([ed0ae77](https://github.com/deepseek-ai/deepseek-harness/commit/ed0ae7786d7ab70319de018384e8dfbfc450ed1c))
- test(pwsh): align repeated sandbox mode expectations ([aea150a](https://github.com/deepseek-ai/deepseek-harness/commit/aea150a17ede800f7065a9e485cde32b2193af1a))
- test(llm): point the keyless onboarding case at a listed model ([a55b082](https://github.com/deepseek-ai/deepseek-harness/commit/a55b08233f34ccfdb38943fbeea10feb2cd073b5))

### 📝 Documentation
- docs(office-to-pdf): link the bounded conversion decision ([e30a391](https://github.com/deepseek-ai/deepseek-harness/commit/e30a391326bbfafcc916771aa2539d5a7a9e1234))
- docs(office-to-pdf): clarify conversion and engine package ownership ([773d743](https://github.com/deepseek-ai/deepseek-harness/commit/773d743bce81e49248e34406ea81baa146216ee7))
- docs(document): refresh shared conversion module graph ([43839d1](https://github.com/deepseek-ai/deepseek-harness/commit/43839d12095497807569d76044481aedd186a1f9))
- docs(desktop): trim the macOS menu prose ([403c9b7](https://github.com/deepseek-ai/deepseek-harness/commit/403c9b74f478b766a66161299f6c03c484c103be))
- docs(client): state the known-site suffix count correctly ([7eede14](https://github.com/deepseek-ai/deepseek-harness/commit/7eede143bd483558c0a6b889737aed51809a9ddf))
- docs(preview): follow renamed conversion decision ([b307cbf](https://github.com/deepseek-ai/deepseek-harness/commit/b307cbffab0db54158b706f35f7ea47e9b252905))
- docs(web): propose consistent trajectory attachment presentation ([17dd9f0](https://github.com/deepseek-ai/deepseek-harness/commit/17dd9f0e29511c7e3e9f942b6de4b864cf47065f))
- docs(desktop): confirm release version before packaging ([a609246](https://github.com/deepseek-ai/deepseek-harness/commit/a609246a3591ec7578032b7237f44e314f6305c7))
- docs(subagent): regenerate settings dependency graph ([6b63916](https://github.com/deepseek-ai/deepseek-harness/commit/6b63916d9c2995b666919e4b39d4d0f51758a5fe))

### 🔧 Configuration
- merge: resolve event catalog conflicts with master ([3766f4a](https://github.com/deepseek-ai/deepseek-harness/commit/3766f4af953958b2a6fc48415659d7726075f6b9))
- release(dsh): 0.1.6-alpha.1.20260916.1 ([69bf9f9](https://github.com/deepseek-ai/deepseek-harness/commit/69bf9f90540328b7788d2bf038d948b3f6503caa))
- merge: preserve Desktop test release base versions ([c13cc07](https://github.com/deepseek-ai/deepseek-harness/commit/c13cc074fd42c41c67a431c67c5207d187e3ccd7))
- merge: align session toast fix with latest master ([73c2300](https://github.com/deepseek-ai/deepseek-harness/commit/73c2300ce4be0fe684ce58f959b49d42554c6bed))

## 2026-09-17

**116 commits.** 18 feature changes, 40 fixes.

### 🆕 Features
- feat: resolution mode link to runtime ([9ddef32](https://github.com/deepseek-ai/deepseek-harness/commit/9ddef327a40dc8d128a1d8b912fc17677ddf0ed8))
- feat(client): open subagent chats in sidebar ([e62587c](https://github.com/deepseek-ai/deepseek-harness/commit/e62587c163befc43cf6f8584ef77c498e85501b4))
- feat(web): reveal a clipped sidebar session title on hover (#4423) ([6564808](https://github.com/deepseek-ai/deepseek-harness/commit/65648082a37a93bb2bd1daff314f09b23ccb0fca))
- Restore sealed diagram preview note ([e0427f3](https://github.com/deepseek-ai/deepseek-harness/commit/e0427f38e98472a6ec2556f9a2df0b6b7eb32179))
- Revert "feat(client): optimize code block previews and source highlighting" ([81e05ab](https://github.com/deepseek-ai/deepseek-harness/commit/81e05abaaba6c06f4a9d00d7e5d3b1790c6e0b65))
- Fix Desktop async window-state lint ([3cbb944](https://github.com/deepseek-ai/deepseek-harness/commit/3cbb9442fa5ea33fdb13b5551ff93a8391acd950))
- Remove obsolete Desktop lint suppressions ([9541849](https://github.com/deepseek-ai/deepseek-harness/commit/954184934aa9a1c6fcdbc029381f8888670d34d6))
- feat(web): show a concise plan summary in the review card ([7de3757](https://github.com/deepseek-ai/deepseek-harness/commit/7de3757badcc8742725318fb02c806a8802901b1))
- feat(client): refine Sidebar Browser controls ([ef1218a](https://github.com/deepseek-ai/deepseek-harness/commit/ef1218ac242553dab5ee391bbd53e5eee1733286))
- feat(client): open message links in Sidebar Browser ([8968fed](https://github.com/deepseek-ai/deepseek-harness/commit/8968fedec21760d8aff71d3fb5d894d271d47e7f))
- feat(web): ship Sidebar Browser ([1e42aec](https://github.com/deepseek-ai/deepseek-harness/commit/1e42aec10ee71d8a14095c0b0c064129958ec647))
- feat(client): add Sidebar Browser ([9fed351](https://github.com/deepseek-ai/deepseek-harness/commit/9fed351d3df0f06d98de0936d5ad841223284e13))
- feat(web): open submitted plans automatically with artifact cards ([1e1dd43](https://github.com/deepseek-ai/deepseek-harness/commit/1e1dd43fee55967cda239eeecabfce1c2e816002))
- feat(client): add reusable component factories ([c094b66](https://github.com/deepseek-ai/deepseek-harness/commit/c094b663fb2934b6bd905ea66bd2ac5a20133d07))
- feat(web): move context usage into composer stats ([b6726fe](https://github.com/deepseek-ai/deepseek-harness/commit/b6726fe79dffa02ae61360ee44f5f7fe39ab5092))
- feat(web): keep submitted plans in chat and open them in sidebar ([f6428a1](https://github.com/deepseek-ai/deepseek-harness/commit/f6428a164ef67e76ad57ba856bb615a31504b5e6))
- feat(desktop): integrate Windows caption navigation and localized menus ([5c2cc19](https://github.com/deepseek-ai/deepseek-harness/commit/5c2cc19efd3bfb4304fca651915dc1da003205e2))
- feat(client): add ownership lifecycle primitives ([c52ef9f](https://github.com/deepseek-ai/deepseek-harness/commit/c52ef9fadae73fe4bc058703fb6266a1979d76e3))

### 🐛 Bug Fixes
- fix: test ([e68f5d5](https://github.com/deepseek-ai/deepseek-harness/commit/e68f5d5abaf0742df6e8c8f813340ea8f6415fe7))
- fix: revert desktop ([d9a55c7](https://github.com/deepseek-ai/deepseek-harness/commit/d9a55c7c0d3cd95a18c8cac67185c3d348630bf6))
- fix: budget doc ([896f0b7](https://github.com/deepseek-ai/deepseek-harness/commit/896f0b7ec5740bd9d39c42bb62c2254c841ee634))
- fix(client): preserve round sidebar action ([49b9ccb](https://github.com/deepseek-ai/deepseek-harness/commit/49b9ccbfcdafac4e0bf9c5e83275f88f782271a5))
- fix(session-reference): preserve title fallback ([34a4312](https://github.com/deepseek-ai/deepseek-harness/commit/34a43129a619703e217b301561832e4b11458936))
- fix(client): keep sidebar integration optional ([871f332](https://github.com/deepseek-ai/deepseek-harness/commit/871f33297163bb0e8663020f88f81283ac5e7cb2))
- fix(client): satisfy sidebar chat gates ([4f38c60](https://github.com/deepseek-ai/deepseek-harness/commit/4f38c607972ff2c526706b87dc81b66006dca346))
- fix(client): align subagent sidebar references ([da7dc34](https://github.com/deepseek-ai/deepseek-harness/commit/da7dc34f7d20c1b8ed562463c37a7c3cc7c6f198))
- fix(web): identify plan preview tabs with a plan icon ([3fb29e0](https://github.com/deepseek-ai/deepseek-harness/commit/3fb29e08030c2cddf50b738f9992c36294d34d9a))
- fix(web): restore the plain plan review status dot ([38bfc29](https://github.com/deepseek-ai/deepseek-harness/commit/38bfc29876d274da804146b3075422716d16535f))
- revert(web): remove raw disclosure reset on record selection ([03f93dc](https://github.com/deepseek-ai/deepseek-harness/commit/03f93dc2a56b2a4d12f8350f5226dcf5b00d3e49))
- fix(web): preview unlogged plans and preserve subagent history addresses ([46b4f94](https://github.com/deepseek-ai/deepseek-harness/commit/46b4f94802cecde76fe6ef347696d5cb3774fd55))
- fix(desktop): close update review copy and documentation gaps ([e03f58c](https://github.com/deepseek-ai/deepseek-harness/commit/e03f58c6e9b1c3b95e37c74d2ebd85158abcc988))
- fix(web): keep trajectory thumbnail status readable ([70b4237](https://github.com/deepseek-ai/deepseek-harness/commit/70b4237c00fe4b807ab4a261e34bd35f43cd9568))
- fix(desktop): align plugin cleanup notes and cover profile locks ([8c81181](https://github.com/deepseek-ai/deepseek-harness/commit/8c81181bce81fd7c722678baf5ba3c3d788c1229))
- fix(web): collect submitted plans in the final turn artifacts ([577e4a0](https://github.com/deepseek-ai/deepseek-harness/commit/577e4a036d89f4b77da62e141df2dfdbf28c5183))
- fix(desktop): classify update failures and refresh recovered Host ([25b6f86](https://github.com/deepseek-ai/deepseek-harness/commit/25b6f868cae6eea3c4161508000af4b4a333d028))
- fix(client): handle Sidebar Browser navigation fallbacks ([80f90e6](https://github.com/deepseek-ai/deepseek-harness/commit/80f90e61d38482c4024f5fa2b230a57986ce9b03))
- fix(client): align Sidebar Browser security docs ([3dff381](https://github.com/deepseek-ai/deepseek-harness/commit/3dff3813d80c30d2a8d2b8e637a520736b69c139))
- fix(client): clarify Subagent capacity help text ([646aadc](https://github.com/deepseek-ai/deepseek-harness/commit/646aadc52c24f4ea7ac7cedfe371183b2a350e3c))
- fix(web): keep composer context details within the viewport ([ae4fc75](https://github.com/deepseek-ai/deepseek-harness/commit/ae4fc751eb41306076129014284ff1056f1bd2eb))
- fix(preview): preserve PDF text layer rotation ([afe85c1](https://github.com/deepseek-ai/deepseek-harness/commit/afe85c1cfdadbf95bf6aeef5ccfc224c0940cff2))
- fix(web): hide built-in profile bundles from plugin cards ([05e6758](https://github.com/deepseek-ai/deepseek-harness/commit/05e675863bdf219ed7f7ebf53865c7036e7a6b7f))
- fix(desktop): verify installed update ASAR runtime layout ([e8a3bc7](https://github.com/deepseek-ai/deepseek-harness/commit/e8a3bc701ad7060db49e4a5e63b53ae32b328ec7))
- fix(web): align plan card borders and cover review identity ([472ddfa](https://github.com/deepseek-ai/deepseek-harness/commit/472ddfa7aec2709d890a500054d5645fd408a2af))
- fix(desktop): defer caption menus until the application mounts ([3f41c6c](https://github.com/deepseek-ai/deepseek-harness/commit/3f41c6c02f0af9b0c6160fdc58d2d9424c283c6a))
- fix(client): regenerate slot catalog ([7852631](https://github.com/deepseek-ai/deepseek-harness/commit/7852631012ead5cef3bb7e9b0a5ee8b9107b1bdc))
- fix(desktop): release mandatory modal on install quit and bind DPAPI upload target ([d1585ab](https://github.com/deepseek-ai/deepseek-harness/commit/d1585abdd9a047cfc062f3efb5a6ad78e51bade8))
- fix(desktop): preserve caption editing and navigation across overlays ([e36bdaa](https://github.com/deepseek-ai/deepseek-harness/commit/e36bdaa914ada04f5ca24305451fcecdf9c7a6b3))
- fix(desktop): explain listener conflicts with exit and restart recovery ([e62a0e3](https://github.com/deepseek-ai/deepseek-harness/commit/e62a0e3e5def300471cb4725c539040925692fff))
- fix(web): reset raw attachment disclosures on record selection ([9119f14](https://github.com/deepseek-ai/deepseek-harness/commit/9119f145224d8239e9db564e28d55ff632fbaebe))
- fix(web): unify trajectory attachment presentation ([1da97f3](https://github.com/deepseek-ai/deepseek-harness/commit/1da97f30f815fecb95dc3f7ee5a078931d154f3d))
- fix(boot): keep startup metadata out of ordinary error output ([a9b7491](https://github.com/deepseek-ai/deepseek-harness/commit/a9b7491cf83281b7b0131108d609aa77b2930d3a))
- fix(web): address file-reference review feedback ([51e9e15](https://github.com/deepseek-ai/deepseek-harness/commit/51e9e1599d416ceeef5bcce13f210e8bae52bb57))
- fix(web): preserve compact math and inspector typography ([039415d](https://github.com/deepseek-ai/deepseek-harness/commit/039415d5a46a933f8a1a7a964b35f88361ca48e3))
- fix(web): keep Thinking tables below the collapse header ([7d9166e](https://github.com/deepseek-ai/deepseek-harness/commit/7d9166ea4004e9b2f6f58f27912ca64328d55cf7))
- fix(web): render Thinking with compact Markdown ([e5038fc](https://github.com/deepseek-ai/deepseek-harness/commit/e5038fcf9e6bc4b02c92c52c17a1d155ecc35617))
- fix(subagent): default delegation depth to one ([04a3c30](https://github.com/deepseek-ai/deepseek-harness/commit/04a3c30a04114d1fba29a72b114debfd2072cfcc))
- fix(workspace-changes): ignore scrubbed ambient Git config ([4233590](https://github.com/deepseek-ai/deepseek-harness/commit/4233590de6d1a3cbaa4d8db888116a85f634315d))

### 🔄 Refactoring
- test(cli): cover runtime profile defaults and sync docs ([0ea8900](https://github.com/deepseek-ai/deepseek-harness/commit/0ea890044fbc54fd24b4ca492b3f54ad58f77137))
- refactor(client): move sidebar chat to subagent ([d05b429](https://github.com/deepseek-ai/deepseek-harness/commit/d05b42980b8508d4285d106fdcc9c36387cdb53c))
- test(client): cover sidebar chat edge paths ([c6c3ad9](https://github.com/deepseek-ai/deepseek-harness/commit/c6c3ad935d37f17d1697ef33430373e293d9d825))
- refactor(web): route Markdown file navigation through delegate provider ([4c54612](https://github.com/deepseek-ai/deepseek-harness/commit/4c546124b95ce0d9bfac04deb552ac7dd3bc4e33))
- test(web): strengthen plan dismissal checks and clarify review contracts ([5d173b1](https://github.com/deepseek-ai/deepseek-harness/commit/5d173b170d2e883bf53ffeb98ac9adb1dcdee5bf))
- test(web): snapshot the plan review summary and two actions ([2394816](https://github.com/deepseek-ai/deepseek-harness/commit/2394816cc16ae71cb61f4c0d19f61e015d93f46c))
- refactor(web): drop the plugin-list dot for an active fiber ([f91d5e3](https://github.com/deepseek-ai/deepseek-harness/commit/f91d5e310d349d960f0267a5590873d20af0f193))
- perf(client): defer offscreen diagram previews ([34bc53e](https://github.com/deepseek-ai/deepseek-harness/commit/34bc53eff80b53e6ab95d1f57415f53de14415d5))
- test(web): refresh Thinking code block controls snapshot ([bd1904d](https://github.com/deepseek-ai/deepseek-harness/commit/bd1904da0e46ef05e371bd23d3d7860462af7380))
- test(web): place plan cards after the completed reply ([11637ac](https://github.com/deepseek-ai/deepseek-harness/commit/11637ac48ec03dc44db84db9285425000e10ab78))
- test(web): open inline-code links in Sidebar Browser ([9637a4d](https://github.com/deepseek-ai/deepseek-harness/commit/9637a4d0514af090034557cab8d929b6ee116eb7))
- refactor(desktop): remove standalone plugin manager ([4b64741](https://github.com/deepseek-ai/deepseek-harness/commit/4b6474133ac1fe29bdd7d7125eee3f31b627ae83))
- test(web): cover automatic plan previews on narrow screens ([a096637](https://github.com/deepseek-ai/deepseek-harness/commit/a096637d017a63145dd0fa5c29457f704ef55b14))
- test(web): settle complete folder queries before drilling ([0dbe49a](https://github.com/deepseek-ai/deepseek-harness/commit/0dbe49a893edf5ba18dedc50370df20f7997e335))
- test(web): snapshot artifact-style plans and automatic previews ([e68bc53](https://github.com/deepseek-ai/deepseek-harness/commit/e68bc539b81550d384bffec92f25edfd40af3a20))
- test(web): refresh Subagent summary in plugin manager snapshots ([5c507b1](https://github.com/deepseek-ai/deepseek-harness/commit/5c507b12c6079be3dc3a2ddb9fea8e63dfc1a73f))
- test(preview): cover retries while resource is unavailable ([10dc97c](https://github.com/deepseek-ai/deepseek-harness/commit/10dc97ca041bcc33e95d43918f8e6947b1269963))
- refactor(preview): keep renderer loading format independent ([4de7612](https://github.com/deepseek-ai/deepseek-harness/commit/4de7612f3998ff7362d37f9ca4c95dbcb5acf9e1))
- test(web): cover plan resource cancellation and sidebar bindings ([ab834ac](https://github.com/deepseek-ai/deepseek-harness/commit/ab834ac667884f5baa906186818c5c11d8e08d96))
- refactor(preview): align Office content discriminant ([bbd5fa2](https://github.com/deepseek-ai/deepseek-harness/commit/bbd5fa2cf48f4cfe0d2effa142b459c12f5406ef))
- refactor(preview): name Office loading mode explicitly ([ab0f04c](https://github.com/deepseek-ai/deepseek-harness/commit/ab0f04cbac398c49d7fb2d570e0c05e432ae9808))
- test(desktop): pin supported platform in startup tests ([eb10557](https://github.com/deepseek-ai/deepseek-harness/commit/eb10557199f3a017ed5675cd59122cad83ebb72e))
- refactor(preview): let Office own document loading ([2e779ca](https://github.com/deepseek-ai/deepseek-harness/commit/2e779cafcaa0da89a4d50535200ae492a4d04009))
- test(desktop): use native file URL for login placeholder ([38d3750](https://github.com/deepseek-ai/deepseek-harness/commit/38d375070f705c10f121493519052a5b8bc54a02))
- test(desktop): keep publisher test source-plane only ([fed28b6](https://github.com/deepseek-ai/deepseek-harness/commit/fed28b62451ee9fbfe3ee212c0bf05714ff49ca5))
- test(desktop): cover update indicator fallback states ([ddc1e28](https://github.com/deepseek-ai/deepseek-harness/commit/ddc1e28e1792512afa7cb30e115d25bd0e23c839))
- refactor(document): consolidate Office preview remotes ([880c186](https://github.com/deepseek-ai/deepseek-harness/commit/880c186146638aa45204cdc3556dd5b56d6eefab))
- test(desktop): stub update listeners in host disconnect fixture ([593db4e](https://github.com/deepseek-ai/deepseek-harness/commit/593db4e0b7e592c86b7aca7e0230b4ea467b3c39))
- test(web): cover trajectory attachment presentation ([212f5f9](https://github.com/deepseek-ai/deepseek-harness/commit/212f5f9ccc7e18d70de56698dfc217c7ec3a27e5))
- refactor(workspace-files): keep bounded reads within readAll ([12302ac](https://github.com/deepseek-ai/deepseek-harness/commit/12302ac6c3b15700a3dc9e83d9b51a517ff23edf))
- refactor(workspace-files): reuse bounded reads and return raw Host bytes ([b911efe](https://github.com/deepseek-ai/deepseek-harness/commit/b911efef39c02ee3d4e1c95ee996e527fa96b33e))
- refactor(preview): pass raw Office bytes and share source checks ([f9aa94a](https://github.com/deepseek-ai/deepseek-harness/commit/f9aa94a161dffd19d411a634ebd349710784078a))
- test(client): migrate Session reference coverage ([6d3b5d4](https://github.com/deepseek-ai/deepseek-harness/commit/6d3b5d4526f5077d28252ccdf6e86cae0d56d24c))
- refactor(client): bind Session UI through providers ([b9b14dc](https://github.com/deepseek-ai/deepseek-harness/commit/b9b14dc05e83874760494e3ece8623ebbfcb382a))
- refactor(gateway): retain Session contexts through dispatch ([1bf048e](https://github.com/deepseek-ai/deepseek-harness/commit/1bf048eb71e91efcafaa03a14652f316e955df78))
- refactor(session-controller): own Client Session generations ([6830e14](https://github.com/deepseek-ai/deepseek-harness/commit/6830e1460d0f09ed48fc976efc6193e67d345faf))

### 📝 Documentation
- docs: refresh module graph ([3e136c2](https://github.com/deepseek-ai/deepseek-harness/commit/3e136c2f303d5b31f707bb42638eca26053fd9ba))
- docs(web): remove raw disclosure reset guarantees ([70ba425](https://github.com/deepseek-ai/deepseek-harness/commit/70ba425ba2cdaac6b411de94a3587973b6282b0e))
- docs: preserve mechanical and local edit exemptions ([adce1b4](https://github.com/deepseek-ai/deepseek-harness/commit/adce1b4b5c87fcc75d9fbcad47344ec687ef342d))
- docs: keep agent note criteria edits minimal ([926534c](https://github.com/deepseek-ai/deepseek-harness/commit/926534c44b2f5aa20c34a8c87619e6da526194d9))
- docs: require lasting rationale before creating agent notes ([730bcc7](https://github.com/deepseek-ai/deepseek-harness/commit/730bcc7c856141e09566c35c835b1109dd6c90a6))
- docs(web): describe trajectory thumbnail status feedback ([9836c4d](https://github.com/deepseek-ai/deepseek-harness/commit/9836c4daafcb3643b520c72c31b2db8a213dd3b0))
- docs(client): update Sidebar Browser behavior ([45958f1](https://github.com/deepseek-ai/deepseek-harness/commit/45958f12df5332c232ce315d474a40d12e71efd9))
- docs(client): document Sidebar Browser ([66edeb8](https://github.com/deepseek-ai/deepseek-harness/commit/66edeb85af5366344b97f9bc11275531dbf9e953))
- docs(web): record implemented trajectory attachment presentation ([f176327](https://github.com/deepseek-ai/deepseek-harness/commit/f176327afc2f97a56cd3b1d9647b4502c243d3f7))
- docs: pin browse picker for agent web automation ([c885d9f](https://github.com/deepseek-ai/deepseek-harness/commit/c885d9f8626b2f3ac27f4a8296bb86f3cad6d05b))
- docs(client): document explicit Session ownership ([2438bdd](https://github.com/deepseek-ai/deepseek-harness/commit/2438bdd4d6420f87d21fc6ec4bfa7f8f03e1849b))

### 🔧 Configuration
- release(dsh): 0.1.6-alpha.2 ([6b1808f](https://github.com/deepseek-ai/deepseek-harness/commit/6b1808f432adfa96ab6c2f033e158ca230422e16))
- merge(web): sync master for trajectory attachments ([4f3f737](https://github.com/deepseek-ai/deepseek-harness/commit/4f3f73799618f9819fd89b5c6280d0d2c412efcc))
- chore(ci): trim delegate review dismissal message ([f2c5c2a](https://github.com/deepseek-ai/deepseek-harness/commit/f2c5c2a6a236e304df318e48793c8cfbdc36d8ae))
- chore: move file-reference evaluation to personal repository ([7c55730](https://github.com/deepseek-ai/deepseek-harness/commit/7c55730a97e55711d5a5ecc5eb64faa0c2e7b801))
- merge(web): sync latest trajectory markdown changes ([641253e](https://github.com/deepseek-ai/deepseek-harness/commit/641253e730d941f69a132138062cd01416eb208f))
- chore(release): restore merge-target prerelease version ([371054b](https://github.com/deepseek-ai/deepseek-harness/commit/371054b072e59886d0953f4216e3bc28fe7f9e36))
- merge: sync latest master into desktop updates ([c06d271](https://github.com/deepseek-ai/deepseek-harness/commit/c06d2719d00432d95c409e13ad5bd9693e548616))
- merge: sync master into continuable activation limits ([9fcf9f7](https://github.com/deepseek-ai/deepseek-harness/commit/9fcf9f7b11d3e54df8427ed837fe64334051d6a5))
