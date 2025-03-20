# Claude Text Editor API

A FastAPI backend that integrates with Claude AI to provide text editor capabilities. This API allows applications to interact with Claude's text editor tool for viewing, editing, and creating text files.

## Features

- Chat with Claude AI via REST API
- File operations through Claude's text editor tool:
  - View file contents
  - Replace text in files
  - Create new files
  - Insert text at specific positions
  - Undo edits
- List files in the workspace
- Reset conversations
- Sample file creation for demonstration

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/claude-edit-file-tool.git
   cd claude-edit-file-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Running the API

Start the FastAPI application:

```bash
python main.py
```

The API will be available at http://localhost:8000, with interactive documentation at http://localhost:8000/docs.

## API Endpoints

### Chat

- `POST /api/chat`: Send a message to Claude and get a response

### File Operations

- `POST /api/file/operation`: Perform a file operation using the text editor tool
- `GET /api/files`: List files in the workspace directory
- `POST /api/sample`: Create a sample Python file for demonstration

### Conversation Management

- `POST /api/reset`: Reset the conversation with Claude

## File Operation Examples

### View a file

```json
{
  "command": "view",
  "path": "sample.py",
  "parameters": {}
}
```

### Replace text in a file

```json
{
  "command": "str_replace",
  "path": "sample.py",
  "parameters": {
    "old_str": "def calculate_factorial(n):",
    "new_str": "def calculate_factorial(n: int) -> int:"
  }
}
```

### Create a new file

```json
{
  "command": "create",
  "path": "hello.py",
  "parameters": {
    "file_text": "print('Hello, World!')"
  }
}
```

### Insert text at a specific line

```json
{
  "command": "insert",
  "path": "sample.py",
  "parameters": {
    "insert_line": 0,
    "new_str": "#!/usr/bin/env python3\n\"\"\"\nFactorial calculation module.\n\"\"\"\n\n"
  }
}
```

## Security Considerations

- File paths are validated to prevent directory traversal attacks
- Only certain file extensions are allowed
- Files are backed up before modifications
- The API should be protected in production environments
