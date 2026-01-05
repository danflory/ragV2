echo "=================================================="
echo "🛡️  GRAVITAS SYSTEMS CHECK"
echo "=================================================="

# 1. FORMATTING
echo -e "\n🎨 [1/4] Running Black..."
black app/ tests/

# 2. LINTING
echo -e "\n🧹 [2/4] Running Ruff..."
ruff check app/ tests/

# 3. TYPE CHECKING
echo -e "\n🔬 [3/4] Running Mypy..."
mypy app/ tests/ --ignore-missing-imports

# 4. UNIT TESTING
echo -e "\n🧪 [4/4] Running Pytest..."
pytest