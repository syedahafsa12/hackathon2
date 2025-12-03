<!--
Sync Impact Report:
Version change: none → 1.0.0 (initial constitution)
Modified principles: Initial creation of 7 core principles
Added sections: Core Principles, Development Workflow, Testing Standards, Quality Gates, Governance
Removed sections: none
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section references this file
  ✅ spec-template.md - User stories align with spec-driven principle
  ✅ tasks-template.md - Testing tasks align with testing principle
Follow-up TODOs: none
-->

# Hackathon II Todo Evolution Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All features MUST begin with a complete specification before any implementation begins. Every feature requires:
- A detailed spec.md documenting user scenarios, requirements, and success criteria
- User acceptance scenarios written in Given-When-Then format
- Clear functional requirements with identifiers (FR-001, FR-002, etc.)
- Specifications MUST be reviewed and approved before proceeding to planning

**Rationale**: Specifications provide a clear contract between intent and implementation. They prevent scope creep, enable independent testing, and ensure all stakeholders understand what will be built before resources are committed.

### II. Clean Code Standards

All code MUST follow Python PEP 8 style guidelines and maintain high readability standards:
- Type hints MUST be used for all function signatures and class attributes
- Variable and function names MUST be descriptive and follow snake_case convention
- Class names MUST follow PascalCase convention
- Constants MUST be UPPERCASE with underscores
- Maximum line length of 88 characters (Black formatter standard)
- Docstrings MUST be provided for all public modules, classes, and functions

**Rationale**: Consistent coding standards reduce cognitive load, facilitate code reviews, and make the codebase accessible to all contributors. Type hints catch errors early and serve as inline documentation.

### III. Separation of Concerns

Architecture MUST maintain clear boundaries between business logic, data access, and presentation:
- Business logic MUST reside in service layer (src/services/)
- Data models MUST be defined separately (src/models/)
- UI/presentation code MUST be isolated from core logic
- No business rules in presentation layer
- No UI dependencies in business logic layer
- Use dependency injection where appropriate

**Rationale**: Separation of concerns enables independent testing, parallel development, easier refactoring, and reusability. Changes to one layer should not cascade to others unnecessarily.

### IV. Independent Testability (NON-NEGOTIABLE)

Every feature MUST be independently testable without requiring other features to function:
- Each user story MUST be implementable as a standalone unit
- Features MUST work in isolation with appropriate test fixtures
- Shared dependencies MUST be mockable
- Test data MUST be self-contained per feature
- Integration points MUST have clear contracts

**Rationale**: Independent testability enables iterative development, parallel work streams, and incremental delivery. It reduces debugging complexity and allows MVP validation at each stage.

### V. Documentation First

Documentation MUST be created alongside or before implementation:
- README.md MUST be maintained with setup and usage instructions
- Inline comments MUST explain "why" for complex logic, not "what"
- API contracts MUST be documented with examples
- Configuration options MUST be documented
- Architectural decisions MUST be captured in ADRs when significant

**Rationale**: Documentation-first thinking forces clarity of design. It ensures knowledge transfer, reduces onboarding time, and serves as a living specification of system behavior.

### VI. Iterative Evolution

Each development phase MUST build upon previous phases while maintaining backward compatibility:
- New features MUST NOT break existing functionality
- Database migrations MUST be reversible
- API changes MUST be versioned
- Deprecation warnings MUST precede breaking changes
- Feature flags MUST be used for gradual rollouts when appropriate

**Rationale**: Iterative evolution minimizes risk, enables continuous delivery, and maintains system stability. Users can adopt new features gradually without forced disruption.

### VII. AI-First Development with Claude Code (NON-NEGOTIABLE)

All implementation work MUST be performed using Claude Code, with NO manual code editing:
- Claude Code agents MUST execute all coding tasks
- Specifications drive Claude Code's implementation work
- Human review and approval required at key checkpoints
- Manual coding is prohibited to maintain consistency and auditability
- All code changes MUST be traceable to agent execution

**Rationale**: AI-first development ensures consistency, reduces human error, leverages Claude Code's capabilities fully, and creates an auditable trail of all implementation decisions. This principle is core to the Hackathon II methodology.

## Development Workflow

### Workflow Steps

1. **Specification** (`/sp.specify`): Create detailed spec.md with user stories and requirements
2. **Planning** (`/sp.plan`): Research and design architecture, document in plan.md
3. **Task Breakdown** (`/sp.tasks`): Generate granular, testable tasks in tasks.md
4. **Implementation** (`/sp.implement`): Execute tasks via Claude Code agents
5. **Testing**: Validate each user story independently
6. **Documentation**: Update README and inline docs
7. **Review**: Human checkpoint before merge
8. **Commit & PR** (`/sp.git.commit_pr`): Automated git workflow

### Checkpoints

- **Post-Specification**: User approval of spec.md required
- **Post-Planning**: Architectural review of plan.md required
- **Post-Implementation**: Feature validation against spec required
- **Pre-Merge**: Code review and test verification required

## Testing Standards

### Test Requirements

- **Unit Tests**: MUST cover critical business logic (when tests explicitly requested)
- **Integration Tests**: MUST verify feature works end-to-end (when tests explicitly requested)
- **Contract Tests**: MUST validate API contracts (when tests explicitly requested)
- **Test Independence**: Each test MUST be runnable in isolation
- **Test Data**: MUST be reproducible and self-contained

### Test-Driven Development (when tests requested)

- Tests MUST be written BEFORE implementation begins
- Tests MUST FAIL initially (red phase)
- Implementation makes tests pass (green phase)
- Refactoring improves code quality while keeping tests green

**Note**: Testing is OPTIONAL unless explicitly requested in feature requirements. When omitted, validation occurs through manual acceptance testing against spec criteria.

## Quality Gates

Before merging any feature:

- ✅ Specification approved and complete
- ✅ All acceptance criteria met
- ✅ Code follows PEP 8 and type hints present
- ✅ Documentation updated (README, inline comments)
- ✅ Manual or automated tests pass (as applicable)
- ✅ No manual code edits (AI-generated only)
- ✅ Backward compatibility maintained
- ✅ ADRs created for architectural decisions

## Governance

### Constitution Authority

- This constitution supersedes all other development practices
- All code reviews MUST verify compliance with constitution
- Violations MUST be documented and justified in plan.md Complexity Tracking table
- Amendments require documented rationale and user approval

### Amendment Process

1. Propose change with clear rationale
2. Document impact on existing features
3. Update constitution with version bump
4. Propagate changes to all dependent templates
5. Create migration plan if existing code affected
6. Obtain user approval before implementation

### Version Semantics

- **MAJOR**: Breaking changes to principles (e.g., removing NON-NEGOTIABLE principles)
- **MINOR**: New principles added or significant expansions
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance

- All PRs MUST pass constitution compliance check
- Complexity/violations MUST be justified in plan.md
- Runtime guidance follows this constitution
- Prompt History Records (PHRs) MUST be created for all user interactions
- Architectural Decision Records (ADRs) MUST be created for significant decisions

**Version**: 1.0.0 | **Ratified**: 2025-12-03 | **Last Amended**: 2025-12-03
