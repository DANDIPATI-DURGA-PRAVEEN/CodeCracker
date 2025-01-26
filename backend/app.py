from flask import Flask, request, jsonify
from flask_cors import CORS
from platform_handlers import get_platform_handler
import logging
import requests

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

LEETCODE_API_URL = "https://leetcode.com/graphql"

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    try:
        data = request.json
        code = data.get('code', '')
        language = data.get('language', 'python')
        platform = data.get('platform', 'leetcode')
        
        logger.info(f"Received code analysis request for {language} code on {platform}")
        
        # Add your code analysis logic here
        # This is a placeholder response
        return jsonify({
            'errors': [],
            'suggestions': [
                f'Analyzing {language} code for {platform}',
                'Consider adding more comments',
                'Variable names could be more descriptive'
            ]
        })
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/user-stats/<platform>/<username>')
def get_user_stats(platform, username):
    try:
        if platform == 'leetcode':
            query = """
            query userProblemsSolved($username: String!) {
                matchedUser(username: $username) {
                    username
                    submitStats: submitStatsGlobal {
                        acSubmissionNum {
                            difficulty
                            count
                            submissions
                        }
                        totalSubmissionNum {
                            difficulty
                            count
                            submissions
                        }
                    }
                    profile {
                        ranking
                        reputation
                        starRating
                    }
                }
            }
            """
            
            headers = {
                'Content-Type': 'application/json',
                'Referer': 'https://leetcode.com'
            }
            
            response = requests.post(
                LEETCODE_API_URL,
                json={
                    'query': query,
                    'variables': {'username': username}
                },
                headers=headers
            )
            
            logger.info(f"Received response from LeetCode API: {response.status_code}")
            
            if response.status_code != 200:
                return jsonify({
                    'error': f'LeetCode API returned status code {response.status_code}'
                }), 400
                
            data = response.json()
            
            if 'errors' in data:
                return jsonify({
                    'error': data['errors'][0]['message']
                }), 400
                
            if not data.get('data', {}).get('matchedUser'):
                return jsonify({
                    'error': f'User "{username}" not found on LeetCode'
                }), 404
                
            return jsonify(data)
        else:
            handler = get_platform_handler(platform)
            stats = handler.get_user_stats(username)
            
            logger.info(f"Retrieved stats for {username}: {stats}")
            
            if 'error' in stats:
                return jsonify({'message': stats['error']}), 404
                
            return jsonify(stats)
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/profile', methods=['POST'])
def get_profile():
    try:
        data = request.json
        logger.info(f"Received request data: {data}")
        
        platform = data.get('platform')
        username = data.get('username')
        
        logger.info(f"Processing request for platform: {platform}, username: {username}")
        
        if not platform or not username:
            logger.warning("Missing platform or username")
            return jsonify({'error': 'Platform and username are required'}), 400
        
        handler = get_platform_handler(platform)
        logger.info(f"Using handler for platform: {platform}")
        
        stats = handler.get_user_stats(username)
        logger.info(f"Retrieved stats: {stats}")
        
        if 'error' in stats:
            logger.warning(f"Error in stats: {stats['error']}")
            return jsonify({'error': stats['error']}), 404
            
        return jsonify(stats), 200
        
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)
