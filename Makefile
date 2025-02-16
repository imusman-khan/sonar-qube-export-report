# Command to run the main Python script
run:
	@echo "Running the Python application..."
	PYTHONPATH=. python -B src/main.py

# Poetry commands
install:
	@echo "Installing dependencies using Poetry..."
	poetry install --no-root

# Command to format Python code using Black
format:
	@echo "Formatting Python code using Black..."
	black .

# Default command
.PHONY: install run format