# Tachikoma Multi-Agent AI System

## Vision
Tachikoma is an advanced multi-agent AI system featuring dynamic, character-driven agents that collaborate while maintaining their individual principles. The system supports multi-dimensional agent architecture with roles, personalities, and political perspectives for realistic debate and decision-making.

## Core Features

### Multi-Dimensional Agents
- **Role-Based Expertise**: Agents defined by functional roles (Legal, Marketing, Technical, etc.)
- **Personality Traits**: Communication styles, risk tolerance, and collaboration preferences
- **Political Spectrum**: Optional ideological positioning for nuanced debates
- **Correlated Parameters**: Environmental stance, technology approach, regulation preferences

### Real-Time Collaboration
- **AI-Powered Conversations**: Agents use LLMs (Hugging Face, OpenAI) for dynamic responses
- **Multi-Agent Debates**: Watch agents discuss, debate, and reach consensus
- **Performance Tracking**: Monitor agent contributions and resource allocation
- **Visual Analytics**: Interactive charts showing agent relationships and metrics

### Streamlit Web Interface
- **Chat Interface**: Start conversations and watch agents collaborate
- **Agent Management**: Create, configure, and manage agents with templates
- **Visualizations**: Network graphs, performance metrics, diversity analysis
- **Real-Time Updates**: See conversations unfold in real-time

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/tachikoma.git
cd tachikoma

# Install dependencies
pip install -r requirements.txt

# Optional: Install LLM extras for Hugging Face models
pip install transformers torch
```

### Running the UI

```bash
# Launch the Streamlit web interface
streamlit run tachikoma/ui/app.py

# Or use the command (if installed via setup.py)
python -m streamlit run tachikoma/ui/app.py
```

The web interface will open at `http://localhost:8501`

### Basic Usage

1. **Create Agents** (Agents tab):
   - Use templates (Legal, Marketing, Technical, etc.)
   - Or create custom agents with roles and personalities

2. **Start Conversations** (Chat tab):
   - Enter a topic or question
   - Watch agents discuss and debate
   - View conversation history

3. **Analyze Results** (Visualization tab):
   - See agent relationships
   - Monitor performance metrics
   - Review diversity analysis

## Project Structure

```
tachikoma/
├── core/                    # Main agent system
│   ├── agent.py            # Multi-dimensional agent definitions
│   ├── orchestrator.py     # Agent coordination
│   ├── llm.py              # LLM integration (NEW)
│   ├── communication.py    # Inter-agent messaging
│   ├── scorer.py           # Performance tracking
│   └── suggester.py        # Role suggestions
├── ui/                      # Streamlit interface (NEW)
│   ├── app.py              # Main UI entry point
│   └── components/         # UI components
│       ├── chat.py         # Chat interface
│       ├── agents.py       # Agent management
│       └── visualization.py # Charts and graphs
├── config/                  # Configuration
├── utils/                   # Utilities
└── main.py                  # CLI entry point

examples/                    # Example scripts
docs/                        # Documentation
archive/                     # Archived implementations
```

## Configuration

### LLM Providers

**Mock Provider** (Default - No API required):
```python
# Perfect for testing without LLM API costs
# Uses template responses based on agent roles
```

**Hugging Face** (Free, Local):
```python
# Models: DialoGPT-small, DialoGPT-medium, DialoGPT-large
# No API key needed
# Requires: pip install transformers torch
```

**OpenAI** (API Key required):
```python
# Models: gpt-3.5-turbo, gpt-4, gpt-4-turbo
# Set API key in .env or configure in UI
```

### Environment Variables

Create a `.env` file:
```bash
# Optional: OpenAI API key
OPENAI_API_KEY=your-api-key-here

# Optional: Groq API key
GROQ_API_KEY=your-groq-key-here
```

## Examples

See the `examples/` directory for usage examples:

- `example_simple_phase1.py` - Basic multi-agent system
- `example_huggingface_quick.py` - Quick Hugging Face setup
- `example_llm_providers.py` - LLM provider comparison
- More examples in `examples/README.md`

## Technical Stack

- **UI Framework**: Streamlit 1.32+
- **LLM Integration**: Hugging Face Transformers, OpenAI API
- **Agent System**: Async Python with Pydantic models
- **Visualizations**: Plotly, NetworkX
- **Architecture**: Event-driven with multi-dimensional agents

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black tachikoma/

# Type checking
mypy tachikoma/
```

## Documentation

Full documentation available in the `docs/` directory:

- Architecture overview
- Multi-dimensional agent design
- LLM integration guide
- Performance metrics
- Development roadmap

## Roadmap

- ✅ Multi-dimensional agent architecture
- ✅ LLM integration (Hugging Face, OpenAI)
- ✅ Streamlit web interface
- ✅ Real-time conversations
- 🔄 Enhanced role suggestion engine
- 🔄 Consensus building algorithms
- 📋 Agent memory and context persistence
- 📋 Advanced debate protocols

## Contributing

Contributions welcome! Please check the `docs/` folder for guidelines.

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with the vision of creating sophisticated multi-agent systems that mirror real-world collaboration and decision-making processes.