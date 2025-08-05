# Patrick - EinsteinDB-GPT3 Integration

This directory contains the EinsteinDB-GPT3 integration components, including the server implementation and related tools.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- MySQL/MariaDB server (for database operations)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=einsteindb
   ```

## Running the Server

### Start the EinsteinDB Server

```bash
# Make the startup script executable
chmod +x start_all.sh

# Start all components
./start_all.sh
```

This will start:
1. The EinsteinDB HTTP server on port 8000
2. The QNoether component

### Test the Server

In a new terminal, run the test script:

```bash
python test_server.py
```

## Debugging

### Common Issues

1. **Port Already in Use**:
   If port 8000 is already in use, you can change it in `start_all.sh`.

2. **Database Connection Issues**:
   - Ensure MySQL/MariaDB is running
   - Verify the database credentials in the `.env` file
   - Check if the database exists and is accessible

3. **Missing Dependencies**:
   If you encounter any import errors, make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

### Logs

- Server logs are written to `einsteindb_server.log` in the server directory
- Application logs are written to the console

## Project Structure

- `src-EinsteinDBGPT3/`: Contains the EinsteinDB-GPT3 server implementation
- `src-QNoether/`: Contains the QNoether component for query optimization
- `einstAI-toolbox/`: Contains additional tools and utilities
- `scripts/`: Contains utility scripts for running benchmarks and tests

## License

This project is licensed under the MIT License - see the LICENSE file for details.
