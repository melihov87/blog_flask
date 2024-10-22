echo "Running flake8..."
flake8 .
if [ $? -ne 0 ]; then
  echo "Code style check failed. Commit aborted."
  exit 1
fi

echo "Code style check passed."

echo "Running pylint..."
pylint .
if [ $? -ne 0 ]; then
  echo "Pylint check failed. Commit aborted."
  exit 1
fi

echo "Pylint check passed."

echo "Running mypy..."
mypy .
if [ $? -ne 0 ]; then
  echo "Type check failed. Commit aborted."
  exit 1
fi

echo "Mypy type check passed."
