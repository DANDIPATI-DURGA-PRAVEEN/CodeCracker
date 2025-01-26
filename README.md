# CodeCracker - Coding Profile Analyzer

CodeCracker is a web application that allows users to analyze their coding profiles from various competitive programming platforms including LeetCode, CodeChef, and CodeForces. It provides detailed statistics about problems solved and language distribution in an interactive and visually appealing way.

![CodeCracker Interface](https://github.com/DANDIPATI-DURGA-PRAVEEN/CodeCracker/raw/master/frontend/public/screenshot.png)

## Features

- **Multi-Platform Support**: Analyze profiles from:
  - LeetCode
  - CodeChef
  - CodeForces

- **Comprehensive Statistics**:
  - Total problems solved
  - Platform-specific ratings
  - Global rank
  - Language-wise distribution of solutions

- **Interactive Visualization**:
  - Beautiful pie charts showing language distribution
  - Detailed tooltips with problem counts and percentages
  - Clean and modern Material-UI interface

## Technology Stack

### Frontend
- React.js
- Material-UI for styling
- Recharts for data visualization
- Axios for API calls

### Backend
- Python Flask
- BeautifulSoup4 for web scraping
- Requests library for API calls

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.7 or higher)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DANDIPATI-DURGA-PRAVEEN/CodeCracker.git
   cd CodeCracker
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python app.py
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm start
   ```

3. Open your browser and visit `http://localhost:3000`

## Usage

1. Select a coding platform (LeetCode, CodeChef, or CodeForces)
2. Enter your username for that platform
3. Click "Fetch Profile" to see your statistics
4. View your comprehensive coding statistics including:
   - Problems solved
   - Rating
   - Global rank
   - Language distribution

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Durga Praveen Dandipati** - [GitHub Profile](https://github.com/DANDIPATI-DURGA-PRAVEEN)

## Acknowledgments

- Thanks to all the coding platforms for providing the data
- Material-UI for the beautiful components
- Recharts for the visualization library
