# chlog
<a href="https://www.buymeacoffee.com/naheitsch" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Overview

chlog is a powerful and flexible CLI (Command-Line Interface) application written in Python, designed to leverage AI in generating meaningful changelogs between two git commits. It's a must-have tool for developers who want to automate their changelog generation process.

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)

## Requirements
- Python 3.7 or later
- Git installed in your system

## Installation

### From Source Code

1. Clone the repository:
    ```bash
    git clone https://github.com/nathanielheitsch/chlog.git
    ```
2. Navigate into the cloned repository:
    ```bash
    cd chlog
    ```
3. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the script:
    ```bash
    python main.py
    ```

## Usage

chlog requires two parameters:
1. `new_commit` (optional): The latest commit hash. By default, it is set to `None`.
2. `old_commit` (optional): The previous commit hash. By default, it is set to `None`.

### Basic usage:

```bash
python main.py [NEW_COMMIT] [OLD_COMMIT]
```

### Using an API Token:

If you wish to use an API token for AI services, you can do so with the `--token` option:

```bash
python main.py --token YOUR_API_TOKEN [NEW_COMMIT] [OLD_COMMIT]
```

### API Token Storage

While the `--token` option is available for single uses, chlog also supports persistently storing your API token as an environment variable for repeated use. Here's how you can set it up:

#### Unix/Linux/MacOS

Open your terminal, and add the following to your `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc` file:

```bash
export CHLOG_API_KEY="your-api-token"
```

Then, source the file:

```bash
source ~/.bashrc
```
Or, replace `~/.bashrc` with whichever file you appended the export line to.

#### Windows

In Powershell, you can set an environment variable like this:

```powershell
$env:CHLOG_API_KEY="your-api-token"
```

Remember to replace `"your-api-token"` with your actual API token.

For permanently setting the environment variable on Windows, follow these steps:

1. Right-click on Computer.
2. Click on 'Properties'.
3. Click on 'Advanced system settings'.
4. In the System Properties window, click on the 'Environment Variables' button.
5. Click on the 'New' button under the 'User variables' or 'System variables' section (depending on your needs), and enter `CHLOG_API_KEY` as the variable name and your actual API token as the variable value.

Now, whenever you use chlog, it will automatically read your API token from the environment variable `CHLOG_API_KEY`. This eliminates the need to input your API token each time you use the tool.

### Help:

If you need more information, use the `--help` option:

```bash
python main.py --help
```

This will provide you with the necessary information on how to use the application.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourgithubusername/chlog/issues).

## License

Distributed under the MIT License. See `LICENSE` for more information.
