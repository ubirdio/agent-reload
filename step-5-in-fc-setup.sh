echo "Installing deps..."
apt-get update && apt-get install -y ca-certificates > /dev/null

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null

echo "Running program..."
./.local/bin/uv run example.py
