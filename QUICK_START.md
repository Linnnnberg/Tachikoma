# Tachikoma - Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Launch the UI

```bash
# Method 1: Direct
streamlit run tachikoma/ui/app.py

# Method 2: Using main.py
python tachikoma/main.py --ui

# Method 3: Default
python tachikoma/main.py
```

## Using the Interface

### 1. Create Agents (Agents Tab)

**Use Templates:**
- Legal Consultant
- Marketing Strategist
- Technical Architect
- Financial Advisor
- Policy Advisor

**Or Create Custom:**
- Define role (name, domain, responsibilities, expertise)
- Add personality (communication style, risk tolerance, collaboration)
- Optional: Add political profile and context tags

### 2. Start Conversations (Chat Tab)

1. Enter a topic or question
2. Set max conversation turns (2-10)
3. Click "Start Conversation"
4. Watch agents discuss and debate
5. View conversation history

**Example Topics:**
- "Should we invest in AI technology?"
- "How should we approach sustainability in our business?"
- "What are the risks of expanding internationally?"

### 3. View Analytics (Visualization Tab)

- **Agent Overview**: Metrics and domain distribution
- **Agent Network**: Relationship graph
- **Performance**: Charts and radar plots
- **Diversity**: Role, political, and communication style analysis

## LLM Providers

### Mock Provider (Default)
- No setup required
- Uses template responses
- Perfect for testing

### Hugging Face (Free, Local)
```bash
pip install transformers torch
```
- Select "Hugging Face" in sidebar
- Choose model size (small/medium/large)
- Click "Load Hugging Face Model"

### OpenAI (API Key Required)
- Select "OpenAI" in sidebar
- Enter API key
- Choose model (gpt-3.5-turbo, gpt-4, gpt-4-turbo)
- Click "Configure OpenAI"

## Examples

Check the `examples/` directory for code examples:

```bash
# Basic multi-agent system
python examples/example_simple_phase1.py

# Hugging Face integration
python examples/example_huggingface_quick.py

# LLM provider comparison
python examples/example_llm_providers.py
```

## Troubleshooting

**UI doesn't start:**
```bash
pip install streamlit plotly networkx
```

**LLM errors:**
- Check API key in `.env` or UI configuration
- Verify internet connection for online models
- For Hugging Face: ensure `transformers` and `torch` are installed

**Import errors:**
```bash
pip install -r requirements.txt
```

## Next Steps

1. Explore different agent combinations
2. Try different LLM providers
3. Experiment with political diversity in debates
4. Check `docs/` for detailed documentation
5. Review `examples/` for code usage

## Support

- Documentation: `docs/` directory
- Examples: `examples/` directory
- Integration test: `python test_integration.py`
- Summary: See `REORGANIZATION_SUMMARY.md`

Enjoy using Tachikoma! 🚀
