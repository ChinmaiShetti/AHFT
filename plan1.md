# AHFT — MASTER ENGINEERING IMPLEMENTATION PROMPT

## 1. YOUR ROLE

Act as a senior embedded systems architect, firmware engineer, Python systems engineer, real-time systems researcher, ML engineer, and software testing specialist.

You are responsible for designing and implementing **AHFT (Adaptive Hardware Fuzzing Testbench)**.

Do not treat this as a simple ESP32 monitoring application or an ordinary IoT project.

AHFT is intended to become a research-oriented, adaptive, safety-constrained embedded-system testing framework that discovers, characterizes, reproduces, and eventually localizes failures in embedded hardware and firmware.

You must prioritize:
- Engineering correctness.
- Modular architecture.
- Reproducibility.
- Safety.
- Measurement reliability.
- Testability.
- Research validity.
- Extensibility.

I want a properly engineered working implementation, not a collection of disconnected code files or placeholder modules.

You must inspect the repository before making changes.

The GitHub repository has already been initialized at the root directory:

`AHFT/`

Work inside this existing repository. Do not create another nested AHFT repository.

---

# 2. PROJECT VISION

AHFT is an adaptive hardware-testing framework.

Its central operating principle is:

**Generate experiment → Validate safety → Execute on hardware → Collect measurements → Analyze failures → Update adaptive model → Generate next experiment.**

The framework should intelligently explore configurations of an embedded system to discover conditions that produce runtime failures, timing violations, resource exhaustion, communication errors, and eventually peripheral-level faults.

The long-term vision includes:
1. ESP32 firmware diagnostics.
2. Real-time scheduling and timing diagnostics.
3. Memory and resource diagnostics.
4. Communication interface diagnostics.
5. Peripheral and sensor diagnostics.
6. Actuator diagnostics.
7. Cross-component interaction testing.
8. Adaptive experiment generation.
9. Failure reproduction and minimization.
10. Evidence-based fault localization.

However, do not implement the entire long-term vision immediately.

We are deliberately developing the project in stages.

---

# 3. FINALIZED HARDWARE ARCHITECTURE

We have selected the following hardware architecture.

## A. Raspberry Pi 4 — AHFT Host Controller

The Raspberry Pi 4 acts as the intelligence, orchestration, and analysis layer.

Its responsibilities:

- Generate candidate experiments.
- Maintain experiment configurations.
- Validate candidate experiments using a safety kernel.
- Communicate with the ESP32.
- Manage experiment execution.
- Receive and parse telemetry.
- Analyze timing and resource measurements.
- Classify observed failures.
- Persist experiment history.
- Train and execute lightweight adaptive ML models in later stages.
- Compare adaptive testing against conventional testing strategies.
- Provide experiment visualization and reporting.

The Raspberry Pi should eventually operate independently, without requiring the development laptop.

## B. ESP32 — Device Under Test (DUT)

Initially, use one ESP32 development board.

The ESP32 executes experiments and performs local measurements.

Its responsibilities:

- Receive experiment configurations.
- Independently validate incoming commands.
- Create and manage FreeRTOS tasks.
- Execute controlled workloads.
- Perform bounded software fault injection.
- Measure execution time.
- Measure scheduling delays.
- Track deadline misses and jitter.
- Monitor heap and task stack usage.
- Detect watchdog events and resets.
- Collect telemetry.
- Return experiment results to the Raspberry Pi.
- Enter a safe state when an experiment is aborted or invalid.

The ESP32 must use native ESP-IDF APIs wherever practical.

## C. FreeRTOS

Use the FreeRTOS implementation integrated with ESP-IDF.

FreeRTOS is the execution environment on the ESP32, not a separate hardware component.

Use it for:
- Concurrent task execution.
- Task priorities.
- Task scheduling experiments.
- Task notifications.
- Queues and synchronization primitives where needed.
- Controlled task workload generation.
- Task monitoring.
- Watchdog integration.

Do not assume that every timing measurement made by FreeRTOS is inherently hard real-time.

Document actual timer resolution, scheduler behavior, tick limitations, and measurement overhead.

---

# 4. DEVELOPMENT ENVIRONMENT AND TECHNOLOGY STACK

## Raspberry Pi host

Preferred environment:

- Raspberry Pi OS Lite 64-bit.
- Python 3.11 or compatible stable version.
- PySerial.
- NumPy.
- Pandas.
- Scikit-learn.
- SQLite.
- Streamlit for dashboard functionality.
- Pytest for testing.
- Pydantic for configuration and data validation where appropriate.

The Raspberry Pi 4 has limited computational resources.

Design lightweight host-side services and avoid unnecessarily heavy dependencies.

Model training can initially be performed on the development laptop, with lightweight inference and experiment selection deployed to the Pi.

## ESP32 firmware

Use:

- ESP-IDF.
- C/C++.
- ESP-IDF integrated FreeRTOS.
- ESP timer APIs.
- ESP-IDF heap monitoring APIs.
- Task stack high-water-mark APIs.
- Watchdog APIs.
- ESP reset reason APIs.
- Native ESP-IDF UART/USB serial functionality appropriate for the selected board.

Use a consistent, reproducible ESP-IDF project structure.

Do not mix Arduino-specific APIs into native ESP-IDF firmware without a clearly justified reason.

## Communication

Use USB serial initially.

Use newline-delimited JSON (NDJSON).

Start with 115200 baud unless the selected hardware or driver requires otherwise.

The protocol must be versioned.

---

# 5. RESEARCH SCOPE FOR VERSION 1

Our initial research target is:

**Adaptive discovery and characterization of ESP32 firmware runtime failures under controlled operating conditions.**

The initial prototype should focus on the ESP32 itself.

Peripheral diagnostics are explicitly postponed until the core framework is validated.

Do not purchase or require additional sensors or peripherals for the initial milestone.

The initial experiment families should include:

## A. Scheduling experiments

Investigate:
- Task priorities.
- Number of competing tasks.
- Task execution durations.
- Scheduling delays.
- Task starvation.
- Scheduling interference.

## B. Timing experiments

Investigate:
- Periodic task execution.
- Release lateness.
- Execution time.
- Response time.
- Deadline misses.
- Jitter.
- Maximum period deviation.

## C. CPU workload experiments

Investigate:
- Controlled computational workload.
- Multiple competing tasks.
- Workload intensity.
- CPU interference.
- Timing degradation under increasing workload.

Do not assume that a loop iteration count corresponds directly to CPU utilization. Calibrate and report the actual measured behavior.

## D. Memory experiments

Investigate:
- Heap consumption.
- Minimum free heap.
- Bounded dynamic allocations.
- Allocation failures.
- Task stack high-water marks.
- Controlled memory pressure.

Never intentionally corrupt memory or destabilize the board through unbounded allocation.

## E. Runtime and recovery experiments

Investigate:
- Watchdog events.
- Controlled task stalls.
- Controlled task termination scenarios.
- Firmware reset detection.
- Reset reason classification.
- Recovery after interruption.
- Communication interruption and recovery.

Distinguish injected faults from naturally occurring failures.

---

# 6. HYBRID TESTING APPROACH

The long-term testing approach is hybrid.

This means both software-controlled experiments and physical operating-condition experiments.

For the initial release:

### Software experiments

Implement:
- Workload interference.
- Task scheduling variation.
- Controlled task delays.
- Bounded memory pressure.
- Simulated communication failures.
- Controlled watchdog-related scenarios.

### Physical experiments

Initially support only safe, controlled scenarios that can be validated with the available hardware:

- Power-cycle experiments.
- Controlled restart and recovery tests.
- Observation of boot and reset behavior.
- Safe environmental variation if suitable measurement equipment is available.

Do not implement dangerous electrical fault injection.

Do not deliberately create short circuits, overvoltage, uncontrolled undervoltage, excessive current draw, or conditions outside board specifications.

Physical electrical measurements can be added later with appropriate instrumentation.

---

# 7. SYSTEM ARCHITECTURE

Design the codebase around the following components.

## Raspberry Pi application

### Communication layer

- serial_bridge.py
- protocol.py
- connection_manager.py
- message_handler.py

Responsibilities:
- Serial connection management.
- Message framing.
- Serialization and deserialization.
- Protocol validation.
- ACK handling.
- Timeout handling.
- Reconnection.
- Duplicate message handling.
- Device reset detection.
- Firmware identification.

### Experiment layer

- experiment_config.py
- experiment_generator.py
- experiment_runner.py
- experiment_manager.py

Responsibilities:
- Experiment definitions.
- Candidate generation.
- Experiment lifecycle management.
- Execution coordination.
- Experiment IDs.
- Experiment status.
- Experiment timeout and abort behavior.

### Safety layer

- safety_kernel.py
- parameter_validator.py
- safety_limits.py

Responsibilities:
- Independent host-side safety validation.
- Parameter bounds.
- Experiment duration limits.
- Workload limits.
- Memory limits.
- Supported experiment types.
- Rejection reasons.
- Emergency abort handling.

The host safety kernel must validate every candidate before execution.

The ESP32 must independently validate every received command.

### Monitoring layer

- telemetry_parser.py
- timing_analyzer.py
- resource_analyzer.py
- failure_classifier.py

Responsibilities:
- Telemetry validation.
- Raw measurement processing.
- Timing metric computation.
- Resource analysis.
- Anomaly detection.
- Failure classification.

The host must recompute important metrics from raw telemetry instead of blindly trusting only the ESP32's summary.

### Adaptive layer

- dataset.py
- surrogate_model.py
- acquisition.py
- adaptive_engine.py

Responsibilities:
- Construct training datasets.
- Predict failure likelihood.
- Estimate uncertainty.
- Select promising experiments.
- Balance exploitation and exploration.
- Update the model after experiments.

This subsystem should be implemented only after a trustworthy baseline data pipeline exists.

### Storage layer

- database.py
- experiment_repository.py
- telemetry_repository.py

Use SQLite.

Persist:
- Experiment ID.
- Timestamp.
- Firmware version.
- Protocol version.
- Hardware identity.
- Experiment configuration.
- Safety decision.
- Execution status.
- Raw telemetry.
- Derived metrics.
- Failure labels.
- Model version.
- Selection strategy.
- Random seed where applicable.

### Evaluation layer

- random_baseline.py
- systematic_baseline.py
- benchmark_runner.py
- metrics.py

Responsibilities:
- Random testing.
- Systematic testing.
- Adaptive AHFT testing.
- Equal-budget comparisons.
- Repeated evaluation.
- Statistical analysis.

### Dashboard

Use Streamlit.

Eventually display:
- Experiment history.
- Current device status.
- Timing metrics.
- Resource metrics.
- Failure distribution.
- Experiment configurations.
- Adaptive model predictions.
- Comparison between testing strategies.

Do not make dashboard development a prerequisite for the first hardware milestone.

---

# 8. ESP32 FIRMWARE ARCHITECTURE

Organize the firmware into independent modules.

Suggested components:

### main.cpp

- Initialize ESP-IDF services.
- Initialize communication.
- Initialize monitors.
- Start the firmware execution environment.
- Manage startup state.

### communication/

- serial_handler.cpp
- command_parser.cpp

### experiment/

- experiment_executor.cpp
- experiment_validator.cpp
- experiment_state.cpp

### tasks/

- workload_tasks.cpp
- monitor_task.cpp
- telemetry_task.cpp

### monitoring/

- timing_monitor.cpp
- memory_monitor.cpp
- runtime_monitor.cpp
- reset_monitor.cpp

### fault_injection/

- fault_injector.cpp

### safety/

- safe_state.cpp

Use headers and implementation files where appropriate.

Do not put the entire implementation into main.cpp.

The firmware must have clear module interfaces and well-defined ownership of shared data.

Pay particular attention to concurrency safety.

Use appropriate FreeRTOS queues, task notifications, mutexes, or critical sections.

Avoid unnecessary dynamic allocation during timing-sensitive experiment execution.

Buffer telemetry locally and transmit after the measurement window wherever practical, to minimize serial instrumentation overhead.

---

# 9. MEASUREMENT AND TIMING CORRECTNESS

This is a particularly important part of the research.

Do not generate arbitrary timing numbers.

Use local ESP32 monotonic timing measurements.

Where appropriate, use esp_timer_get_time() or another justified high-resolution ESP-IDF timing mechanism.

Define:

- Scheduled release: S_i
- Actual start: A_i
- Actual finish: F_i
- Relative deadline: D
- Release lateness: L_i = A_i - S_i
- Execution time: E_i = F_i - A_i
- Response time: R_i = F_i - S_i

Deadline miss:

R_i > D

Inter-start interval:

I_i = A_i - A_(i-1)

For periodic scheduling, jitter can initially be characterized using the standard deviation of consecutive start intervals.

Also record maximum period deviation.

Document the exact statistical convention used.

Use absolute periodic scheduling rather than simply calling a relative delay after every execution, which can accumulate execution-time drift.

However, validate the actual scheduling precision and limitations of the selected FreeRTOS APIs.

Do not claim hard real-time guarantees without evidence.

Every experiment should have:
- Warm-up period.
- Measurement period.
- Controlled configuration.
- Experiment identifier.
- Validity status.
- Completion status.
- Error and reset information.

Record raw samples where feasible.

---

# 10. FAILURE CLASSIFICATION

Do not reduce all failures to one boolean internally.

Maintain distinct categories.

Initial taxonomy:

- deadline_miss
- excessive_release_lateness
- excessive_jitter
- task_starvation
- memory_pressure
- allocation_failure
- stack_low_watermark
- watchdog_event
- firmware_reset
- communication_timeout
- malformed_command
- telemetry_incomplete
- experiment_aborted
- unknown_anomaly

A single experiment can produce multiple observations.

Distinguish:
- Successful experiment.
- Valid experiment with detected anomaly.
- Failed experiment.
- Interrupted experiment.
- Invalid measurement.
- Unknown result.

Never classify missing or incomplete telemetry as a successful experiment.

Store evidence supporting each classification.

Avoid claiming root-cause identification when only a correlated symptom has been observed.

---

# 11. COMMUNICATION PROTOCOL

Design a versioned JSON-lines protocol.

Initial message types:

- ping
- pong
- identify
- device_info
- execute_experiment
- acknowledge
- experiment_started
- experiment_result
- telemetry_batch
- abort_experiment
- error
- heartbeat

Each experiment must have a unique identifier.

Handle:
- Duplicate IDs.
- Invalid parameters.
- Unsupported commands.
- Malformed JSON.
- Message size limits.
- Timeouts.
- Disconnection.
- ESP32 reset during execution.
- Incomplete experiment results.
- Protocol version mismatch.

A communication failure must never be silently interpreted as a successful hardware experiment.

Document the protocol in protocol/protocol_specification.md.

Provide machine-readable message schemas where useful.

---

# 12. ADAPTIVE INTELLIGENCE

Do not implement ML prematurely.

First establish reliable measurements and repeatable experiments.

When sufficient data exists, implement:

1. Experiment dataset construction.
2. Baseline failure prediction.
3. Surrogate model.
4. Uncertainty estimation.
5. Adaptive experiment selection.

Start with a lightweight Random Forest or Extra Trees model.

Explore an acquisition strategy combining:

A(x) = alpha * predicted_failure_probability
     + beta * uncertainty
     + gamma * novelty

This is a conceptual objective, not a requirement to treat uncalibrated tree variance as reliable uncertainty.

Validate uncertainty estimates and model probabilities.

Keep the following as input features:

- Sampling period.
- Number of competing tasks.
- Task priorities.
- Workload configuration.
- Experiment duration.
- Memory allocation configuration.
- Experiment type.

Avoid target leakage.

Do not use post-experiment measurements such as observed jitter, execution time, or deadline misses as pre-experiment prediction inputs.

Those are outcomes, not available experiment parameters.

Use fixed random seeds where applicable.

Version models and save training metadata.

---

# 13. RESEARCH EVALUATION

The eventual research comparison must include:

### Baseline 1 — Random testing

Select valid experiment configurations randomly.

### Baseline 2 — Systematic testing

Explore a predefined grid or structured parameter space.

### Baseline 3 — Adaptive AHFT

Use previous observations to guide experiment selection.

Compare all strategies under:
- Equivalent experiment budgets.
- Identical firmware.
- Identical hardware.
- Equivalent warm-up and measurement conditions.
- Comparable reset and recovery policies.
- Repeated independent trials.

Evaluate:

- Number of unique failures discovered.
- Experiments required per failure.
- Time required to discover failures.
- Failure reproduction rate.
- Failure minimization effectiveness.
- Detection and classification accuracy.
- Fault localization precision and recall when ground truth is available.
- Experiment execution overhead.
- Adaptive selection overhead.

Report variability across trials.

Do not invent experimental results or claim improvement without actual measurements.

Clearly distinguish seeded/injected faults from naturally observed failures.

---

# 14. INITIAL REPOSITORY STRUCTURE

Use this as the target structure, adapting it where necessary for idiomatic ESP-IDF conventions.

AHFT/
│
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
│
├── raspberry_pi/
│   ├── main.py
│   ├── ahft/
│   │   ├── communication/
│   │   ├── experiment/
│   │   ├── safety/
│   │   ├── monitoring/
│   │   ├── adaptive/
│   │   ├── storage/
│   │   └── evaluation/
│   └── dashboard/
│
├── esp32/
│   ├── CMakeLists.txt
│   ├── sdkconfig.defaults
│   └── main/
│       ├── CMakeLists.txt
│       ├── main.cpp
│       ├── communication/
│       ├── experiment/
│       ├── tasks/
│       ├── monitoring/
│       ├── fault_injection/
│       └── safety/
│
├── protocol/
│   ├── message_schema.json
│   └── protocol_specification.md
│
├── configs/
│   ├── hardware.yaml
│   ├── experiment.yaml
│   └── safety.yaml
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── hardware/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── models/
│
├── logs/
│
└── docs/
    ├── architecture.md
    ├── experiment_specification.md
    ├── fault_taxonomy.md
    └── evaluation_methodology.md

Do not create dozens of empty files just to match this tree.

Implement files when they have actual responsibilities and dependencies.

---

# 15. IMPLEMENTATION STRATEGY — FOLLOW STRICTLY

Do not try to implement the entire framework in one giant operation.

Work in milestones.

## MILESTONE 0 — REPOSITORY AND COMMUNICATION FOUNDATION

This is the first implementation target.

First inspect:
- Existing repository contents.
- Git status.
- Existing documentation.
- Installed development tools.
- Existing firmware project, if any.

Do not overwrite existing work without understanding it.

Create the minimal architecture needed for:

### Raspberry Pi side

- Serial connection.
- Protocol serialization and parsing.
- Connection state.
- Device identification.
- PING/PONG testing.
- Timeout handling.

### ESP32 side

- Native ESP-IDF project.
- Startup and initialization.
- Serial message reception.
- JSON command parsing.
- PING/PONG response.
- IDENTIFY response.
- Firmware and protocol version reporting.

### Required tests

- Protocol serialization tests.
- Protocol parsing tests.
- Invalid message tests.
- Timeout tests.
- Mock serial tests.
- Connection failure tests.

Deliverable:

A reliable, repeatable Raspberry Pi ↔ ESP32 communication system.

Do not proceed to complex experiment execution until this foundation is validated.

## MILESTONE 1 — FREE RTOS EXECUTION AND INSTRUMENTATION

Implement:
- Experiment executor.
- FreeRTOS workload tasks.
- Controlled task priorities.
- Timing monitor.
- Memory monitor.
- Runtime monitor.
- Reset monitoring.
- Telemetry reporting.

Create a repeatable baseline experiment.

Verify that measurements are internally consistent.

## MILESTONE 2 — SAFETY AND FAULT INJECTION

Implement:
- Host safety kernel.
- ESP32-side validation.
- Bounded workload generation.
- Controlled task delays.
- Controlled task stalls.
- Bounded memory pressure.
- Abort handling.
- Safe-state recovery.

Ensure fault injection is explicit, controlled, and independently validated.

## MILESTONE 3 — HOST ANALYSIS AND STORAGE

Implement:
- Telemetry parser.
- Timing analyzer.
- Resource analyzer.
- Failure classifier.
- SQLite schema.
- Repository layer.
- Experiment history.

Recompute important metrics from raw samples.

## MILESTONE 4 — ADAPTIVE ENGINE

Only after collecting trustworthy baseline data:

- Dataset builder.
- Surrogate model.
- Acquisition strategy.
- Adaptive engine.
- Model persistence.
- Experiment selection.

## MILESTONE 5 — BENCHMARKING

Implement:
- Random baseline.
- Systematic baseline.
- Adaptive AHFT benchmark.
- Repeated trials.
- Statistical evaluation.
- Result visualization.

## MILESTONE 6 — DASHBOARD

Implement Streamlit dashboard after the underlying data and analysis pipeline works.

## MILESTONE 7 — PERIPHERAL EXTENSIONS

Keep the architecture extensible for future sensors, SPI/I2C peripherals, actuators, and physical measurement instrumentation.

Do not implement these in the initial release.

---

# 16. ENGINEERING RULES

These rules are mandatory.

### A. No fake implementations

Do not create functions that return fabricated successful results.

Do not leave TODO placeholders while claiming a subsystem is complete.

If a feature is not implemented, explicitly identify it as pending.

### B. No unnecessary abstraction

Use modular design, but do not introduce complex design patterns without a clear need.

Keep the code understandable and maintainable.

### C. No arbitrary assumptions

When a hardware pin, board revision, ESP-IDF version, serial interface, or hardware capability is uncertain, inspect or ask.

Do not silently assume.

### D. Error handling

Handle malformed input, device resets, serial disconnections, invalid experiment parameters, incomplete telemetry, and unexpected runtime conditions.

### E. Safety

Never execute an experiment that violates configured safety limits.

Implement independent host and firmware validation.

### F. Logging

Use structured logging.

Record experiment IDs and useful context in logs.

### G. Reproducibility

Record firmware version, protocol version, configuration, random seed, and experiment metadata.

### H. Documentation

Document public interfaces, protocol messages, configuration parameters, important algorithms, and hardware setup.

### I. Testing

Every meaningful module should have appropriate tests.

Use mock serial interfaces for host-side testing.

Use hardware integration tests only when the physical device is available.

Never claim a hardware test passed if it was not actually run.

### J. Git hygiene

Preserve the existing repository and Git history.

Do not force-push, reset, or overwrite existing work.

Keep generated logs, virtual environments, build artifacts, and large datasets out of Git unless explicitly needed.

---

# 17. HOW I WANT YOU TO WORK WITH ME

I want you to act as an engineering collaborator, not merely a code generator.

For each milestone:

1. Inspect relevant existing files.
2. Explain the intended implementation briefly.
3. Identify dependencies and assumptions.
4. Implement the subsystem.
5. Run relevant tests.
6. Fix errors rather than ignoring them.
7. Update documentation.
8. Report exactly what works.
9. Report what remains incomplete.
10. Explain the next logical step.

Do not ask me to approve every trivial file creation or ordinary implementation detail.

Use reasonable engineering judgment.

However, stop and ask before:
- Purchasing or requiring new hardware.
- Making irreversible repository changes.
- Choosing between materially different hardware architectures.
- Executing potentially unsafe hardware experiments.
- Making assumptions that could compromise measurement validity.

When a decision is uncertain, state the assumption and its implications.

Do not expand scope without justification.

---

# 18. FIRST TASK — START NOW

Begin with MILESTONE 0.

Do not implement ML.
Do not implement the dashboard.
Do not implement peripheral diagnostics.
Do not create unnecessary empty modules.

First inspect the existing AHFT repository.

Then:

1. Summarize its existing structure and current state.
2. Propose the minimal initial implementation architecture.
3. Identify the expected development tools and hardware dependencies.
4. Implement the Raspberry Pi-side communication foundation.
5. Implement the ESP32-side PING/PONG and IDENTIFY firmware.
6. Add unit and mock integration tests.
7. Add clear instructions for flashing the ESP32 and running the host communication test.
8. Run every test that can be run in the available environment.

If physical hardware is unavailable, implement mock-based verification and clearly state that actual hardware validation remains pending.

At the end, provide:
- Files created and modified.
- Architecture implemented.
- Commands to install dependencies.
- Commands to build and flash ESP32 firmware.
- Commands to run the host application.
- Test results.
- Known limitations.
- Exact next milestone.

**The ultimate objective is to leave me with a technically sound, reproducible, extensible AHFT framework that can grow from ESP32 runtime testing into adaptive embedded-system hardware fuzzing and diagnostics.**

Start by inspecting the existing repository. Do not assume it is empty.