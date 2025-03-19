# Claude Text Editor Chatbot

This project implements a chatbot that integrates Claude 3.7 Sonnet with text editor tool capabilities, allowing Claude to view and modify text files during conversation.

## Project Architecture

The Claude Text Editor Chatbot demonstrates a modular, extensible architecture leveraging the Anthropic Claude API's tool use capabilities. Key features include:

### Key Components

1. **Text Editor Tool Integration**
   - Enables Claude to view file contents
   - Supports precise text replacement
   - Allows creation of new files
   - Enables insertion of text at specific locations
   - Provides undo capabilities through file backups

2. **Security Measures**
   - Path validation to prevent directory traversal
   - Restriction to a dedicated workspace directory
   - Allowed file extension configuration
   - Automatic backup creation before modifications

3. **Modular Architecture**
   - Clear separation of concerns
   - Easy to extend with additional tools
   - Configurable settings

## Getting Started

### Prerequisites

- Python 3.8+
- Anthropic API key

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install anthropic python-dotenv
   ```
3. Set up your API key in the `.env` file (already present in your project)

### Usage

Run the application:

```bash
python main.py
```

Create a sample file with a deliberate syntax error:

```bash
python main.py --sample
```

## Command Interface

The chatbot supports several commands:

- `/help` - Show help message
- `/clear` - Clear the screen
- `/reset` - Reset the conversation
- `/sample` - Create a sample Python file with a syntax error
- `/workspace` - Print the workspace directory path
- `/exit` - Exit the chatbot
- `/list` - List files in the workspace directory

## Example Usage

1. Create a sample file:
   ```
   /sample
   ```

2. Ask Claude to check for errors:
   ```
   Please check the sample.py file for any syntax errors
   ```

3. Ask Claude to fix the errors:
   ```
   Can you fix the syntax error in sample.py?
   ```

4. Ask Claude to create a new file:
   ```
   Create a new file called hello.py that prints "Hello, World!"
   ```

## Project Structure

```
chatbot-left-taskpan/
├── .env                    # Environment variables (API key)
├── main.py                 # Application entry point
├── README.md               # Project documentation
├── src/                    # Source code
│   ├── __init__.py         # Package marker
│   ├── chatbot.py          # Main chatbot implementation
│   ├── config/             # Configuration
│   │   ├── __init__.py     # Package marker
│   │   └── settings.py     # Application settings
│   ├── tools/              # Tool implementations
│   │   ├── __init__.py     # Package marker
│   │   └── text_editor.py  # Text editor tool
│   └── utils/              # Utility functions
│       ├── __init__.py     # Package marker
│       └── file_utils.py   # File operation utilities
└── workspace/              # Working directory for file operations
    └── .backups/           # Backup directory for file modifications
```

## Architecture Highlights

1. **Modular Package Structure**
   - Clear separation of responsibilities
   - Easy to extend and maintain
   - Supports future tool integrations

2. **Security-First Approach**
   - Path restriction mechanisms
   - Backup-first file modification
   - Input validation

3. **Robust Error Handling**
   - Comprehensive error recovery
   - Detailed error messages
   - Graceful degradation

## License

This project is provided as-is with no specific license. Use at your own discretion.
