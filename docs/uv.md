# How to use uv

## Installing uv

On Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On Linux/macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
## Update uv

```bash
uv self update
```

## Initializing an empty project

```bash
uv init [name]
```

## Installing dependencies
Use when the project dependencies change in the repo (e.g., another user adds a new package)
```bash
uv sync
```

## Adding dependencies

```bash
uv add [package] # Add a dependecy
uv add --dev [package] # For packages useful in the development process
uv add --group [group] [package] # For custom dependency groups (e.g., docs)
```

## Removing dependencies

```bash
uv remove [package]
```
