<!-- model-router:start -->
# Model Router — quality first

Handle trivial and tightly sequential work directly. Delegate when parallel evidence or independent judgment materially helps. Pick a specialist for each phase, not a single expensive model for the whole task.

- mr_scout: local evidence.
- mr_researcher: current external facts and documentation.
- mr_writer: assigned documentation and copy.
- mr_builder: bounded implementation.
- mr_tester: independent tests.
- mr_debugger: root cause and reproduction.
- mr_designer: visual and interaction review.
- mr_architect: architecture, high-impact plans and difficult decisions.
- mr_reviewer: independent verification.

## Checkpoints
Start with at most two concurrent agents. Give each a goal, exact inputs, constraints, acceptance criteria and expected evidence. Assign disjoint writable paths. On new facts, failed checks or changed scope, reclassify the next phase:
- unclear cause → debugger; architectural uncertainty or significant impact → architect.
- known cause and accepted plan → builder; independent tests → tester.
- visual work → designer; factual gaps → researcher; documentation → writer.
- failed verification → establish cause before retrying. Repeated failure or high impact → architect. Significant changes require reviewer; FAIL or UNVERIFIED is not a release approval.
- stop for human authorization before deployments, irreversible changes or sensitive operations. Never expand permissions or silently downgrade high-risk work.

The primary session integrates results, reports actual checks, and closes completed agents. Avoid nested delegation and speculative parallelism. If subagents or a configured model are unavailable, disclose the limitation and ask before changing the model or reducing scope. These instructions guide routing; they are not deterministic enforcement or a security boundary.
<!-- model-router:end -->
