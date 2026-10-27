# MASTER DEVELOPMENT PROMPT — MADX AGENT OS

## Mission: Transform Herald OS into a complete, independent MadX Agent OS distribution

You are acting as a principal Linux operating system architect, senior full-stack engineer, AI systems engineer, security engineer, DevOps specialist and premium UI/UX designer.

You have access to my locally cloned GitHub fork of Herald OS.

Your mission is to **fully transform this project into MadX Agent OS**, a distinct, polished, AI-native operating system belonging to the MadXCore ecosystem.

**This is NOT a cosmetic rebranding project.**

I want the existing operating system's capabilities preserved while its identity, desktop experience, system integration, tools and distribution infrastructure become MadX Agent OS.

Additionally, implement a sophisticated AI model manager, LoRA system, self-learning architecture, and controlled self-development capabilities.

Do not merely write a plan or generate mockups. Inspect the codebase, implement working code, validate it and deliver tested changes in manageable milestones.

---

# 1. Non-negotiable requirements

These requirements override all implementation shortcuts.

1. Preserve every existing, working user-facing Herald OS feature.
2. Preserve Hermes Agent integration, APIs, skills, memories, system tools and permissions.
3. Preserve the existing desktop, Linux integration, first-boot experience, services, package management, updates and rollback capabilities.
4. Replace Herald branding completely throughout the normal user-facing experience.
5. Migrate internal names, identifiers and paths safely rather than blindly replacing text.
6. Add real, functional AI extensions, not decorative or disconnected UI.
7. Maintain full compatibility with relevant Linux system components.
8. Protect existing user data and support safe migration.
9. Keep the system maintainable and capable of receiving upstream security fixes.
10. Produce working builds, tests, documentation and reproducible release artifacts.

**Never remove an existing feature simply because implementing its MadX replacement is difficult.**

If a feature cannot be migrated immediately, retain its working implementation until a tested replacement is available.

The final system must be at least functionally equivalent to the baseline and offer the new MadX capabilities.

# 2. Inspect and audit the entire repository

Before making changes, inspect the actual repository and do not assume the structure is identical to any previous version.

Read and analyze:

- README, LICENSE, NOTICE and SECURITY documentation
- Architecture and Linux build documentation
- Desktop application and shared packages
- Electron main process, preload, IPC and renderer
- React components, routes, hooks, state and themes
- Hermes client and bridge plugin
- Linux session, compositor, launcher, themes and commands
- Systemd services, first-boot scripts and update utilities
- Fedora bootc and OSTree configuration
- Installer, EFI handling and bootloader integration
- NVIDIA image and driver infrastructure
- Existing tests, CI workflows and release pipelines

Create `docs/madx/FEATURE_PARITY.md`.

It must inventory every discovered upstream feature, identify its implementation, map its MadX replacement and document validation.

Create `docs/madx/ARCHITECTURE.md` showing the complete proposed MadX architecture.

Establish a clean baseline before editing. Run all feasible existing checks and record their results.

# 3. Complete operating system rebranding

## Official identity

- **Operating system:** MadX Agent OS
- **Short name:** MadX OS
- **Parent ecosystem:** MadXCore
- **AI management application:** MadX AI Studio
- **AI orchestration interface:** MadX Core
- **Model and adapter manager:** MadX Models
- **Memory and skills manager:** MadX Intelligence
- **Update manager:** MadX Update
- **Version scheme:** MadX Agent OS 0.1.0-alpha, with subsequent semantic versions

Create one centralized branding configuration rather than scattering names and constants throughout the repository.

## Replace all visible branding

Fully rebrand the following wherever applicable:

- Desktop shell and application windows
- Launchers, taskbar, docks and menus
- Settings and About screens
- Welcome wizard and first-boot setup
- Login and lock screens
- Startup and shutdown graphics
- Plymouth splash screen
- System notifications and dialogues
- Application icons and metadata
- Window titles
- Terminal welcome information
- CLI help and user-facing messages
- Installer title and branding
- Boot menu descriptions
- System update and recovery screens
- Documentation, screenshots and release assets
- Default wallpapers and themes
- Build artifacts and release filenames

Audit the repository and generated packages for unexpected visible instances of Herald branding.

**The normal user experience must identify itself as MadX Agent OS, never Herald OS.**

## Internal infrastructure migration

Investigate all internal identifiers before changing them:

- Linux paths and directories
- Service and timer names
- Environment variables
- Desktop application IDs
- Executable and command names
- D-Bus identifiers
- Package names
- Bootc image identifiers
- Container registry references
- OCI metadata
- `os-release` information
- Firewall-zone identifiers
- Application resource paths
- Update and rollback scripts
- Hermes bridge installation paths

Design a migration strategy for each compatibility-sensitive identifier.

Where possible, move the final implementation to MadX-owned namespaces such as `madx-agent-os`, `madx-core` and `/usr/share/madx-agent-os`.

Keep temporary compatibility aliases where required, and remove them only when safe.

Do not allow renamed services to break first boot or prevent system startup.

## Legal and upstream obligations

Preserve all applicable upstream licenses, copyrights and notices.

Do not falsely claim that MadX authored third-party source code.

Put appropriate attribution in the Legal/Open Source Licenses section while keeping the operating system's product identity entirely MadX-branded.

Hermes Agent remains an independently maintained third-party agent engine. Preserve its identity where required by its licensing and integration contracts.

# 4. Premium MadX desktop experience

Create a distinct, modern desktop that feels like a polished commercial operating system.

## Visual direction

Use:

- Dark graphite and near-black surfaces
- Subtle silver and restrained cyan accents
- Premium glassmorphism
- Soft blur and depth
- Carefully controlled motion
- Consistent spacing and typography
- Modern, minimal iconography
- Refined transitions and microinteractions

Avoid excessive neon, extreme glow, clutter and unnecessary 3D effects.

The MadX monogram must be suitable for a website favicon, app launcher, splash screen and OS branding.

Use supplied brand assets when available. If an asset is missing, create an implementation-ready placeholder and clearly flag it for replacement.

Do not substitute a completely different identity without approval.

## Desktop components

Implement or enhance:

- MadX application launcher
- System search and command palette
- AI assistant side panel
- Taskbar/dock integration
- Window controls
- Notification center
- Quick settings
- Network, Bluetooth, battery and performance controls
- AI activity indicator
- Agent task monitor
- System resource monitor
- AI model status panel
- Light/dark styling infrastructure where practical
- Keyboard shortcuts
- Responsive settings panels

Preserve all existing working desktop controls and Linux integrations.

Meet accessibility requirements, including keyboard operation, readable contrast and reduced-motion preferences.

Avoid introducing performance-heavy animations that interfere with local model inference.

# 5. Hermes Agent — complete integration

**Hermes Agent must remain a core, fully functional part of MadX Agent OS.**

Do not replace its internal implementation with an inferior imitation.

Maintain compatibility with its supported APIs, plugins, tooling and configuration.

MadX Core should act as the integrated system-level interface to Hermes.

## Required capabilities

Preserve and integrate all existing supported functionality, including:

- Conversations and multi-turn context
- Tool and function calling
- File operations
- Application and desktop automation
- Terminal operations with permissions
- Web browsing and research tools
- Persistent memory
- Reusable skills
- Scheduled tasks
- Agent workflows and missions
- Tool execution history
- Agent configuration
- Model-provider configuration
- Permission prompts
- Existing Hermes bridge functionality

The UI must clearly indicate when an action is requested, approved, executing, completed or failed.

Do not represent an unconfigured capability as operational.

## MadX agent controls

Add a unified control panel for:

- Active model
- Context settings
- Enabled tools
- Skill permissions
- Memory settings
- Browser permissions
- File access scope
- Network access
- Command execution permissions
- Logs and audit history
- Scheduled automation
- Emergency stop

An agent must not have unrestricted root privileges by default.

System-level actions must use narrowly scoped, authenticated and auditable privilege escalation.

# 6. MadX Models — complete local AI model manager

Build a dedicated, functional application for managing local and cloud AI models.

## Local model functionality

Support configurable local inference backends, prioritizing:

- Ollama
- llama.cpp
- Other compatible local endpoints through an adapter interface

Provide:

- Model discovery
- Model installation/download
- Importing supported model files
- Model selection
- Model loading/unloading
- Model deletion
- Download progress
- Storage usage
- Model information
- Quantization information
- Context-size configuration
- Hardware utilization
- Performance metrics
- Tool-calling compatibility tests

Provide compatible GGUF model handling through supporting backends.

## Cloud model functionality

Support Hermes-compatible cloud providers and custom OpenAI-compatible endpoints.

Allow users to configure local-only, cloud-only and hybrid workflows.

Keep API credentials in appropriate secure storage.

Never expose credentials in logs or renderer output.

## Hardware awareness

Detect available:

- NVIDIA GPU
- GPU VRAM
- System RAM
- CPU
- Supported accelerators, including Intel NPU when an actual compatible runtime is available

For my development laptop, optimize sensible defaults around:

- NVIDIA RTX 4070 Laptop GPU with 8 GB VRAM
- Intel Core Ultra 7 155H
- 16 GB system RAM

Use memory-conscious defaults for 3B–4B-class quantized models.

Implement model unloading and resource checks so loading an LLM alongside ComfyUI does not unexpectedly exhaust VRAM.

NPU acceleration must be optional and should only be advertised when it is actually supported and tested.

# 7. MadX LoRA Studio — new integrated functionality

Create a fully functional LoRA management system.

This must support **both language-model LoRAs and image-generation LoRAs**, using separate compatible backends under a unified interface.

## LoRA import and upload

Implement:

- File selection and drag-and-drop
- Import from local storage
- Validation of extensions, file structure and metadata
- Supported Safetensors and backend-compatible adapter formats
- Model compatibility checking
- Adapter naming and tagging
- Model association
- Description and metadata display
- Version tracking
- Import errors and actionable diagnostics
- Duplicate detection
- Safe adapter storage

Do not assume all LoRA files are compatible with every model or backend.

Avoid insecure deserialization and arbitrary execution of code from imported adapter packages.

## LoRA activation

Users should be able to:

- Choose a base model
- View compatible adapters
- Activate an adapter
- Disable an adapter
- Adjust adapter strength when supported
- Save model/adapter presets
- View active configurations
- Test results before and after activation

Support multiple adapters only where the underlying inference backend genuinely supports it.

Use a backend integration appropriate to the model format, such as llama.cpp for compatible language-model adapters.

## Image-generation LoRAs

Integrate with ComfyUI through its supported API/workflow interfaces.

Provide:

- ComfyUI connection status
- Checkpoint discovery
- LoRA discovery
- Workflow selection
- LoRA strength controls
- Generation progress
- Output previews
- Saved presets
- Error recovery
- Output file management

Do not rebuild ComfyUI unnecessarily. Integrate with it reliably.

## LoRA training

Provide a separate training interface for compatible small language models.

Support an extensible LoRA/QLoRA training backend with:

- Dataset selection
- Training example validation
- Base-model compatibility checks
- Training parameters
- Training job queue
- GPU memory estimation
- Progress and loss metrics
- Checkpoints
- Cancellation
- Adapter export
- Evaluation results
- Rollback

Use practical settings appropriate to limited GPU memory.

Never imply that uploading a LoRA automatically retrains the underlying model.

# 8. MadX Intelligence — automatic learning

I want an AI that can improve its usefulness over time through memory, experience and validated reusable skills.

Implement three clearly separated mechanisms.

## A. Memory learning

The agent should be able to remember user-approved:

- Preferences
- Project architecture
- Coding standards
- Repeated corrections
- Long-term goals
- Successful solutions
- Task history and context

Make memory searchable, editable, exportable and deletable.

Distinguish facts from unverified assumptions.

## B. Skill learning

Integrate Hermes' existing memory and skill-development capabilities.

Add a MadX interface showing:

- Existing skills
- Newly proposed skills
- Skill versions
- Learned procedures
- Skill success/failure history
- Approval status
- Dependencies
- Skill rollback

The agent should be able to identify useful reusable workflows after completing tasks.

Run validation before promoting a generated skill into active use.

## C. Optional model fine-tuning

Implement a separate pipeline for actual weight adaptation through LoRA/QLoRA.

Architecture:

1. Collect user-approved training examples.
2. Filter duplicated, sensitive, invalid and low-quality data.
3. Construct versioned datasets.
4. Train adapters in isolated jobs.
5. Evaluate performance against a fixed baseline.
6. Present metrics to the user.
7. Require approval before activating a newly trained adapter.
8. Retain rollback capability.

Do not automatically fine-tune on all conversations or blindly train on the agent's own output.

A new adapter must demonstrate measurable improvement before it can replace an existing one.

# 9. MadX Self-Development Engine

This is an advanced new capability.

I want MadX Core to help extend its own software functionality without silently modifying critical operating system components.

## Self-development architecture

The agent may:

- Identify missing capabilities
- Research relevant documentation
- Propose new features
- Generate new plugins or skills
- Write source code in an isolated workspace
- Generate tests
- Run approved tests
- Compare performance
- Explain changes
- Prepare Git branches and pull requests

Create a **self-development dashboard** with a task queue, proposed changes, diffs, test reports and rollback information.

## Autonomous development workflow

Use the following controlled loop:

**Observe → Identify improvement → Plan → Implement in sandbox → Test → Evaluate → Request approval → Deploy → Monitor**

Sandbox generated code.

Require review before changes to privileged services, security policy, the operating system image, boot infrastructure or production agent tools.

Do not let the agent silently rewrite its own permission controls, disable its audit trail, execute arbitrary root commands or deploy unverified code.

Allow users to configure which safe tasks can run automatically and which require explicit approval.

## Developer capabilities

Include integrations for:

- Git
- GitHub workflows
- Code editing
- Test execution
- Build logs
- Dependency analysis
- Documentation generation
- Plugin generation
- Skill packaging
- Regression testing

Use these integrations to extend the system, not to replace the existing development features.

# 10. MadX system services and Linux architecture

Maintain the system's existing Fedora bootc architecture unless a replacement is technically justified and tested.

Preserve:

- System startup and shutdown
- Login and user sessions
- First-boot initialization
- Hermes service management
- Network and Bluetooth
- Firewall integration
- Desktop session services
- Package and application integration
- NVIDIA support
- User configuration
- System updates
- Rollbacks and recovery

Rename services and commands to MadX naming conventions only after checking every dependency.

Provide versioned migrations for configuration, systemd units and user data.

Implement a MadX system health dashboard showing service status and meaningful errors.

Preserve the ability to start and recover the OS even when Hermes or local AI backends are unavailable.

# 11. Fix installer reliability and bootloader problems

This is a critical project requirement.

My previous attempt to install the original Herald OS alpha release failed during an OSTree-based installation.

The installer created Linux partitions but crashed with an error involving:

`Bootloader write config: grub2-mkconfig: Child process exited with code 1`

Do not assume leftover Ubuntu files were the confirmed cause.

Investigate:

- Fedora/Anaconda and bootc-image-builder compatibility
- OSTree deployment creation
- GRUB configuration generation
- UEFI boot entry handling
- Shared EFI partitions
- Secure Boot compatibility
- Existing Windows dual-boot configurations
- Bootloader recovery after partial installation

Build automated tests where feasible.

## Critical host safety

My development PC currently runs Windows 11 successfully.

**Never modify my host SSD partitions, EFI partition, firmware entries or Windows boot configuration as part of this development task.**

Do not execute real disk installation commands on the host.

Use isolated virtual disks and virtual machines for installer testing.

A failed installer must not accidentally format, remove or overwrite unrelated partitions.

Support a clear partition-change preview and a safe cancellation process.

Validate installation and reboot behavior before declaring the installer ready.

# 12. Updates, rollback and release engineering

Make MadX Agent OS independently buildable and maintainable.

Implement or adapt:

- MadX-branded container image names
- Correct OCI metadata
- Own update channels
- Development and stable release separation
- System image builds
- NVIDIA-enabled image builds
- VM images
- Installer ISO generation
- Release checksums
- Artifact verification
- Compatible signature verification
- System rollback
- Failed-update recovery
- CI test gating
- Release notes
- Version reporting

Ensure update tools use the appropriate MadX-controlled registry and endpoints.

Do not publish artifacts or use credentials without authorization.

Keep an upstream reference remote and document how to merge upstream security and compatibility fixes into the MadX fork.

# 13. Security and reliability

Treat this as a real operating system, not an experimental webpage.

Required engineering practices:

- Least-privilege defaults
- Permission-gated AI tool execution
- Safe filesystem boundaries
- Secure API credentials
- Input validation
- Protection against malicious imported models and training files
- IPC validation
- Process isolation where appropriate
- Safe command execution
- Logging without leaking secrets
- Signed or verifiable release artifacts
- Rollback and recovery
- No unnecessary open network ports
- Explicit user approval for high-impact operations
- Meaningful error states
- No fake or misleading success indicators

Do not automatically grant unrestricted administrative access to the AI agent, even if the human user has a root account.

# 14. Testing and feature-parity requirements

Create automated tests at the appropriate layers:

- Unit tests
- React component tests
- Electron integration tests
- Hermes bridge tests
- API/backend integration tests
- Model manager tests
- LoRA compatibility tests
- Memory and skills tests
- Permission and security tests
- System service tests
- Build tests
- VM boot tests
- Installer tests
- Update and rollback tests

Compare the resulting system against the original working functionality.

Every upstream feature in the feature-parity inventory must have a tested status.

Do not mark a feature as complete merely because its user interface exists.

The final branding audit must distinguish between:

1. User-visible Herald references, which should be eliminated.
2. Temporary internal compatibility identifiers, which need documented migration.
3. Required legal attribution, which must remain.

Fix critical regressions before proceeding to release.

# 15. Exact execution strategy

Because this is a substantial engineering project, implement it incrementally without sacrificing the final architecture.

Work through these milestones:

**Milestone 0 — Audit and baseline**
- Inspect repository
- Document architecture
- Inventory features
- Record initial tests
- Identify system-critical dependencies

**Milestone 1 — Complete MadX identity**
- Rebrand visible desktop
- Rebrand icons and graphical assets
- Rebrand OS identity
- Migrate safe internal identifiers
- Verify original functionality

**Milestone 2 — MadX desktop and Hermes**
- Implement premium visual design
- Preserve and enhance Hermes integration
- Build unified permissions and agent-control UI
- Verify desktop and system services

**Milestone 3 — MadX Models**
- Implement local model management
- Add provider settings
- Implement hardware detection
- Validate inference and tool calling

**Milestone 4 — MadX LoRA Studio**
- Implement adapter importing
- Compatibility validation
- LoRA activation
- ComfyUI integration
- Fine-tuning interface and compatible backend

**Milestone 5 — MadX Intelligence**
- Persistent memory management
- Skill learning and approval workflows
- Controlled adapter-training pipeline
- Evaluation and rollback

**Milestone 6 — MadX Self-Development**
- Sandboxed plugin creation
- Code-generation workflows
- Automated tests
- Feature proposals
- Approval-based deployment

**Milestone 7 — Independent OS distribution**
- System-service migration
- MadX image and registry setup
- Installer troubleshooting
- VM validation
- CI/CD
- Reproducible release artifacts

At each milestone, make actual source-code changes and run relevant checks.

Do not stop after producing documentation.

Do not claim a milestone is complete if its functional tests have failed or could not be executed.

If a stage is too large for one coding session, leave the repository in a stable state, commit the completed work, document remaining tasks and provide the exact next implementation task.

# 16. Development rules

- Work on dedicated Git branches or worktrees.
- Commit changes in logically separated units.
- Avoid massive unreviewable changes.
- Prefer reusable modules over duplicated code.
- Use stable, documented integration boundaries.
- Avoid speculative dependency changes.
- Verify external APIs before relying on them.
- Keep modifications compatible with the targeted Linux environment.
- Never delete a feature simply to pass compilation.
- Do not overwrite my Windows installation.
- Do not deploy onto the host system.
- Do not push, merge or publish without authorization.

The source repository, implementation and build validation are the deliverables — not a collection of visual mockups.

# 17. Final deliverables

Produce:

1. A complete MadX Agent OS source codebase.
2. A unified MadX branding system.
3. Functional Hermes Agent integration.
4. A working local/cloud model manager.
5. A functional LoRA management system.
6. Integrated ComfyUI workflows.
7. Memory and skill-learning management.
8. A controlled self-development architecture.
9. Preserved and migrated Linux system services.
10. Tested OS image-building infrastructure.
11. VM-tested boot and installation functionality.
12. CI workflows and verifiable build artifacts.
13. Feature-parity and architecture documents.
14. Security documentation.
15. Tests and their actual results.
16. A complete changelog.
17. Clear instructions for continuing development and producing releases.

Only describe a feature as working after it has been implemented and validated.

## Final success criteria

**MadX Agent OS must feel like its own independent, premium AI-native operating system.**

The user should experience MadX branding throughout the operating system rather than Herald branding.

It must retain all existing functional capabilities, preserve Hermes integration, support real local AI workflows and provide the foundation for LoRA management, memory learning, skill development and controlled self-improvement.

The operating system must remain bootable, maintainable, secure and recoverable.

**Start by inspecting the actual repository and establishing the feature-parity baseline. Then begin implementation immediately. Do not stop at a theoretical development plan.**
