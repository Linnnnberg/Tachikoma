# Archived Code

This directory contains archived versions of code that has been refactored, replaced, or is no longer actively used in the main codebase.

## simple_v1/

The original simplified implementation of the Tachikoma multi-agent system (Phase 1).

**Archived Date:** July 18, 2026

**Reason:** Consolidated into the enhanced `tachikoma/core/` architecture.

**Key Features Preserved:**
- LLM integration patterns (migrated to `tachikoma/core/llm.py`)
- Hugging Face optimization techniques
- Multi-agent conversation system
- Working conversation history management

**Historical Context:**
This was the initial working implementation that successfully integrated:
- Multiple LLM providers (OpenAI, Hugging Face, Mock)
- Real-time agent conversations with AI-generated responses
- Performance metrics and resource allocation
- Debate and voting mechanisms

**Why Archived:**
- Duplicate functionality with enhanced core system
- Core system provides superior multi-dimensional agent architecture
- LLM functionality has been extracted and integrated into core
- Maintaining two parallel systems was causing confusion

**Reference Use:**
Keep this archive for:
- Historical reference of development progression
- LLM integration patterns and examples
- Rollback capability if needed
- Learning from the Phase 1 implementation approach

## Using Archived Code

Do not import directly from archived code. If you need functionality from archived modules:

1. Check if it's already available in `tachikoma/core/`
2. Extract and adapt the needed functionality
3. Update to use the enhanced architecture patterns

## Archive Policy

- Archives are kept for historical reference only
- Do not modify archived code
- Archives may be cleaned up after major version releases
- Important patterns should be documented before archiving
