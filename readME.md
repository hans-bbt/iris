Here's the English documentation in markdown format:

# Agent System - iris

## What is this?

This is an autonomous agent system called "iris" that uses the DeepSeek API to execute commands on an Ubuntu system. The agent can interpret natural language tasks, generate appropriate terminal commands, execute them, and iteratively work towards completing complex objectives.

### Key Features:
- **Natural Language Processing**: Accepts tasks in plain English
- **Command Execution**: Runs commands in an Ubuntu terminal with admin privileges
- **Iterative Problem Solving**: Can perform multiple steps to complete a task
- **DeepSeek Integration**: Uses DeepSeek's language model for intelligent command generation
- **Conversation Memory**: Maintains context across interactions
- **Error Recovery**: Handles command failures and adapts strategies

## How to Use

### Basic Usage

1. **Run the script directly:**
```bash
python3 agent_system.py
```

2. **Provide a task as command line argument:**
```bash
python3 agent_system.py "install and configure nginx web server"
```

3. **Interactive mode:**
```bash
python3 agent_system.py
# Then enter your task when prompted
```

### Operation Flow

1. The system starts and loads API configuration
2. You provide a task description (e.g., "install Docker and run a Redis container")
3. The agent:
   - Sends the task to DeepSeek API
   - Receives command suggestions
   - Parses and executes commands in the terminal
   - Shows results
   - Decides next steps based on output
   - Continues until task completion or maximum iterations reached

4. The agent automatically stops when:
   - Task is completed successfully
   - User types "exit", "quit", or "结束"
   - Maximum iterations (20) is reached
   - Critical error occurs

## Configuration

### API Configuration

The system requires DeepSeek API access. You can configure it in several ways:

#### Option 1: Configuration File (Recommended)
Create a file named `api.txt` with the following format:
```
https://api.deepseek.com
your_api_key_here
```

**Configuration file search locations (in order):**
1. Path provided via `api_config_path` parameter
2. `~/agent/api.txt`
3. `~/agent1/api.txt`
4. `/home/hbt/agent1/api.txt`
5. `/etc/agent/api.txt`
6. Current directory `api.txt`

#### Option 2: Interactive Input
If no configuration file is found, the system will prompt for:
```
API Key: [your_api_key]
```

### System Requirements

- **Python 3.x**
- Required packages:
  ```bash
  pip install openai
  ```

- **Operating System**: Ubuntu (tested on Ubuntu with admin privileges)
- **User Context**: Commands run as user `hbt` with password `hbt`

### Environment Setup

1. **Clone or download the script:**
```bash
mkdir -p ~/agent
cd ~/agent
# Place agent_system.py here
```

2. **Set up API configuration:**
```bash
mkdir -p ~/agent1
echo -e "https://api.deepseek.com\nYOUR_ACTUAL_API_KEY" > ~/agent1/api.txt
chmod 600 ~/agent1/api.txt
```

3. **Make executable (optional):**
```bash
chmod +x agent_system.py
```

### Customization

You can modify these parameters in the code:

1. **API Settings** (in `__init__` method):
   - Change the DeepSeek model: `model="deepseek-chat"`
   - Adjust temperature: `temperature=0.7`
   - Modify token limit: `max_tokens=2000`

2. **System Behavior** (in `run` method):
   - Change max iterations: `max_iterations = 20`
   - Modify conversation history length: currently 20 messages
   - Adjust output truncation limits

3. **Command Execution** (in `execute_command` method):
   - Change timeout: currently 600 seconds (10 minutes)
   - Modify command parsing logic in `parse_command_from_response`

## Security Notes

⚠️ **Important Security Considerations:**

1. **Admin Privileges**: The system executes commands with admin permissions
2. **API Key Protection**: Keep your API key secure in configuration files
3. **Command Review**: The agent generates and executes commands automatically
4. **Network Access**: Requires internet access for API calls
5. **System Impact**: Can make significant changes to your system

**Recommended Safety Measures:**
- Test in a virtual machine or container first
- Review generated commands before execution in critical environments
- Implement command allow-lists for production use
- Monitor disk usage and system resources

## Example Tasks

Here are some example tasks you can try:

```bash
# System operations
python3 agent_system.py "check disk usage and clean up temporary files"

# Software installation
python3 agent_system.py "install Python 3.11 and set up a virtual environment"

# Service management
python3 agent_system.py "install and start PostgreSQL service"

# File operations
python3 agent_system.py "find all .log files older than 30 days and compress them"

# Docker operations
python3 agent_system.py "install Docker and run a MySQL container"
```

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check internet connectivity
   - Verify API key is valid
   - Ensure configuration file format is correct

2. **Permission Denied Errors**
   - Ensure user `hbt` has appropriate sudo privileges
   - Check if password authentication is required

3. **Command Execution Timeout**
   - Commands timeout after 10 minutes by default
   - For longer operations, modify the timeout in `execute_command`

4. **Memory Issues**
   - Conversation history is limited to 20 messages
   - Output is truncated to prevent excessive memory usage

### Debug Mode

Add print statements to debug:
```python
# In execute_command method, add:
print(f"Full output: {output}")
```

## Limitations

1. **Platform Specific**: Designed for Ubuntu; may not work on other OS without modification
2. **Command Parsing**: Relies on simple heuristics to extract commands from API responses
3. **Error Handling**: Basic error recovery; may get stuck in loops with complex failures
4. **Resource Usage**: Each iteration calls the DeepSeek API, which may incur costs
5. **Security**: No built-in command validation; relies on the language model's judgment

## License & Attribution

This agent system uses the DeepSeek API. Ensure you comply with:
- DeepSeek's terms of service
- API usage policies and rate limits
- Data privacy regulations in your jurisdiction

---

**Note**: This is an autonomous system. Always review and understand the commands it generates before using in production environments. The creators are not responsible for any system damage or data loss resulting from using this tool.
