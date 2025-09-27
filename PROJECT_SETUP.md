# Tachikoma Project Setup

## Project Structure

```
Tachikoma/
├── tachikoma/                 # Main package
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Main entry point
│   ├── core/                 # Core system components
│   │   ├── __init__.py
│   │   ├── orchestrator.py   # Main orchestrator (to be created)
│   │   ├── agent.py          # Agent classes (to be created)
│   │   ├── scorer.py         # Resource scoring (to be created)
│   │   ├── suggester.py      # Role suggestion (to be created)
│   │   └── communication.py  # Inter-agent communication (to be created)
│   ├── agents/               # Agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py     # Base agent class (to be created)
│   │   ├── character_templates.py  # Character templates (to be created)
│   │   └── agent_factory.py  # Agent factory (to be created)
│   ├── ui/                   # User interface components
│   │   ├── __init__.py
│   │   ├── main_interface.py # Main Gradio interface (to be created)
│   │   ├── agent_management.py  # Agent management UI (to be created)
│   │   └── visualization.py  # Resource visualization (to be created)
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   ├── logging.py        # Logging utilities ✅
│   │   ├── config.py         # Config utilities (to be created)
│   │   ├── export.py         # Export utilities (to be created)
│   │   └── validation.py     # Validation utilities (to be created)
│   ├── config/               # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py       # Main settings ✅
│   │   ├── character_config.py  # Character config (to be created)
│   │   └── scoring_config.py # Scoring config (to be created)
│   └── tests/                # Test suite
│       ├── __init__.py
│       └── test_basic.py     # Basic tests ✅
├── requirements.txt          # Python dependencies ✅
├── setup.py                  # Package setup ✅
├── dev_setup.py             # Development setup script ✅
├── env.example              # Environment variables example ✅
├── .gitignore               # Git ignore rules ✅
├── README.md                # Project documentation ✅
├── HF_Space_MultiAgent_Setup_Guide.txt  # Analysis document ✅
├── Tachikoma_Project_Todo_List.md       # Project todo list ✅
└── PROJECT_SETUP.md         # This file ✅
```

## Quick Start

### 1. Run Development Setup
```bash
python dev_setup.py
```

This will:
- Create a virtual environment
- Install all dependencies
- Create necessary directories
- Set up pre-commit hooks
- Create .env file from example

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Unix/Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Configure Environment
Edit the `.env` file with your API keys and preferences:
```bash
# Copy from example
cp env.example .env
# Edit with your values
nano .env  # or use your preferred editor
```

### 4. Run Tests
```bash
python -m pytest
```

### 5. Start Development
```bash
python -m tachikoma.main
```

## Development Workflow

### 1. Code Structure
- **Core modules** go in `tachikoma/core/`
- **Agent implementations** go in `tachikoma/agents/`
- **UI components** go in `tachikoma/ui/`
- **Utilities** go in `tachikoma/utils/`
- **Configuration** goes in `tachikoma/config/`
- **Tests** go in `tachikoma/tests/`

### 2. Adding New Features
1. Create the module in the appropriate directory
2. Add imports to the `__init__.py` file
3. Write tests for the new functionality
4. Update documentation

### 3. Testing
- Run all tests: `python -m pytest`
- Run specific test: `python -m pytest tachikoma/tests/test_basic.py`
- Run with coverage: `python -m pytest --cov=tachikoma`

### 4. Code Quality
- Format code: `black tachikoma/`
- Lint code: `flake8 tachikoma/`
- Type check: `mypy tachikoma/`

## Dependencies

### Core Dependencies
- **gradio>=4.38.0** - UI framework
- **pandas>=2.2.2** - Data manipulation
- **groq>=0.9.0** - LLM API
- **pydantic>=2.0.0** - Data validation
- **asyncio>=3.4.3** - Async programming

### Development Dependencies
- **pytest>=7.4.0** - Testing framework
- **black>=23.0.0** - Code formatting
- **flake8>=6.0.0** - Linting
- **mypy>=1.5.0** - Type checking
- **pre-commit>=3.3.0** - Git hooks

## Configuration

The system uses environment variables for configuration. See `env.example` for all available options.

Key configuration areas:
- **API Keys**: Groq API key for LLM access
- **System Limits**: Maximum agents, timeouts, etc.
- **UI Settings**: Theme, visualization options
- **Performance**: Caching, concurrency limits
- **Logging**: Log levels and file locations

## Next Steps

1. **Complete Project Setup** ✅
2. **Character Analysis** - Define agent character templates
3. **Scoring Analysis** - Design resource scoring algorithms
4. **Architecture Analysis** - Design event-driven architecture
5. **UI Analysis** - Plan enhanced Gradio interface
6. **Communication Analysis** - Research inter-agent protocols

See `Tachikoma_Project_Todo_List.md` for the complete development roadmap.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the project root and virtual environment is activated
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Configuration Issues**: Check `.env` file and environment variables
4. **Test Failures**: Check that all required modules are created

### Getting Help

- Check the logs in `tachikoma.log`
- Run tests to identify issues
- Review the todo list for next steps
- Check the analysis documents for design decisions

---

**Status**: Project setup complete ✅  
**Next Phase**: Analysis and Planning  
**Estimated Time to Next Milestone**: 2-3 weeks

