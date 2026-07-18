# Tachikoma Examples

This directory contains example scripts demonstrating various features of the Tachikoma multi-agent AI system.

## Available Examples

### Basic System Examples

#### `example_usage.py`
Basic usage example showing how to initialize and use the Tachikoma system with fundamental features.

#### `example_simple_phase1.py`
Simple Phase 1 system demonstration with basic multi-agent functionality including:
- Creating simple agent teams (Legal, Marketing, Technical)
- Messaging system between agents
- Debate and voting mechanisms
- Performance tracking
- Resource allocation
- Scenario simulation

#### `example_detailed_phase1.py`
Detailed Phase 1 demonstration with comprehensive examples of:
- Agent creation with different roles and personalities
- Advanced messaging and communication
- Complex debate scenarios
- Detailed performance metrics
- Resource allocation strategies

### LLM Integration Examples

#### `example_llm_providers.py`
Demonstrates different LLM provider integrations:
- Hugging Face model usage
- Multiple provider support
- Provider fallback mechanisms
- Configuration options

#### `example_llm_comparison.py`
Compares different LLM providers and models:
- Performance comparison
- Response quality analysis
- Speed benchmarking
- Cost analysis

#### `example_huggingface_test.py`
Comprehensive Hugging Face integration testing:
- Model loading and initialization
- Multi-agent conversation generation
- Response quality testing
- Memory and performance optimization

#### `example_huggingface_quick.py`
Quick start guide for Hugging Face integration:
- Minimal setup
- Fast testing
- Basic conversation examples

### Metrics and Performance Examples

#### `example_dynamic_metrics.py`
Dynamic metrics and performance tracking:
- Real-time performance monitoring
- Resource allocation optimization
- Agent scoring and ranking
- System performance analysis

## Running Examples

All examples can be run directly from the command line:

```bash
# From the project root
python examples/example_simple_phase1.py

# Or from the examples directory
cd examples
python example_simple_phase1.py
```

## Prerequisites

Make sure you have installed all required dependencies:

```bash
pip install -r requirements.txt
```

For LLM examples, you may need to:
1. Set up API keys (Groq, OpenAI, etc.) in your `.env` file
2. Download Hugging Face models for offline usage
3. Configure LLM provider settings in `tachikoma/config/settings.py`

## Example Progression

For new users, we recommend running examples in this order:

1. **Start here**: `example_simple_phase1.py` - Understand basic concepts
2. **LLM basics**: `example_huggingface_quick.py` - See AI conversations
3. **Advanced features**: `example_detailed_phase1.py` - Explore full capabilities
4. **Metrics**: `example_dynamic_metrics.py` - Understand performance tracking
5. **Providers**: `example_llm_providers.py` - Learn about different LLM options

## Troubleshooting

### Common Issues

**Import Errors**
If you encounter import errors, ensure you're running from the project root:
```bash
cd /path/to/Tachikoma
python examples/example_name.py
```

**LLM Errors**
- Check your API keys in `.env` file
- Verify internet connection for online models
- Ensure Hugging Face models are downloaded for offline usage

**Performance Issues**
- Some examples may take time to load models
- Monitor memory usage with large language models
- Consider using smaller models for testing

## Contributing

When adding new examples:
1. Name them descriptively: `example_<feature>_<description>.py`
2. Include docstrings explaining what the example demonstrates
3. Add entry to this README
4. Keep examples focused on specific features
5. Include error handling and helpful messages

## Notes

- Examples use the simplified `tachikoma.simple.*` modules for ease of use
- Production applications should use the enhanced `tachikoma.core.*` modules
- Examples may use mock data or simplified scenarios for demonstration purposes
