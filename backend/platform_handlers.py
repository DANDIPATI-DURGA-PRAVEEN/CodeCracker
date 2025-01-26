import requests
from bs4 import BeautifulSoup
import json
import time

class PlatformHandler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

class LeetCodeHandler(PlatformHandler):
    def get_user_stats(self, username):
        try:
            # GraphQL query for user profile
            query = """
            query userPublicProfile($username: String!) {
                matchedUser(username: $username) {
                    username
                    submitStats: submitStatsGlobal {
                        acSubmissionNum {
                            difficulty
                            count
                            submissions
                        }
                    }
                    profile {
                        ranking
                        reputation
                    }
                    languageProblemCount {
                        languageName
                        problemsSolved
                    }
                }
            }
            """

            # Make the GraphQL request
            response = self.session.post(
                'https://leetcode.com/graphql',
                json={
                    'query': query,
                    'variables': {
                        'username': username
                    }
                },
                headers={
                    'Content-Type': 'application/json',
                    'Referer': f'https://leetcode.com/{username}',
                    'Origin': 'https://leetcode.com'
                }
            )

            # Print response for debugging
            print(f"LeetCode API Response Status: {response.status_code}")
            print(f"LeetCode API Response: {response.text[:500]}")  # Print first 500 chars of response

            if response.status_code != 200:
                return {'error': 'Failed to fetch data from LeetCode'}

            data = response.json()
            user_data = data.get('data', {}).get('matchedUser')

            if not user_data:
                return {'error': 'User not found'}

            # Process language statistics
            language_stats = {}
            for lang in user_data.get('languageProblemCount', []):
                if lang['problemsSolved'] > 0:
                    language_stats[lang['languageName']] = lang['problemsSolved']

            # Calculate total solved problems
            submit_stats = user_data.get('submitStats', {}).get('acSubmissionNum', [])
            total_solved = sum(item['count'] for item in submit_stats if item.get('count'))

            return {
                'username': username,
                'rating': user_data.get('profile', {}).get('reputation', 'N/A'),
                'solved': total_solved,
                'rank': user_data.get('profile', {}).get('ranking', 'N/A'),
                'languageStats': language_stats
            }

        except Exception as e:
            print(f"LeetCode Error: {str(e)}")
            return {'error': str(e)}

class HackerRankHandler(PlatformHandler):
    def get_user_stats(self, username):
        try:
            print(f"Fetching HackerRank stats for user: {username}")
            
            # Get profile data using REST API
            api_url = f'https://www.hackerrank.com/rest/hackers/{username}/profile'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': f'https://www.hackerrank.com/{username}',
                'Origin': 'https://www.hackerrank.com'
            }
            
            profile_response = self.session.get(api_url, headers=headers)
            print(f"Profile response status: {profile_response.status_code}")
            
            if profile_response.status_code == 404:
                return {'error': 'User not found'}
            
            if profile_response.status_code != 200:
                return {'error': 'Failed to fetch profile data'}
            
            try:
                profile_data = profile_response.json()
                if not profile_data.get('model'):
                    return {'error': 'User not found'}
                profile_data = profile_data['model']
            except Exception as e:
                print(f"Error parsing profile data: {e}")
                return {'error': 'Failed to parse profile data'}
            
            print(f"Profile data: {profile_data}")
            
            # Get submission statistics
            submissions_url = f'https://www.hackerrank.com/rest/hackers/{username}/recent_challenges'
            submissions_response = self.session.get(submissions_url, headers=headers)
            
            language_stats = {}
            solved_count = profile_data.get('total_solved_challenges', 0)
            
            if submissions_response.status_code == 200:
                try:
                    submissions_data = submissions_response.json()
                    for challenge in submissions_data.get('models', []):
                        lang = challenge.get('language', 'Unknown')
                        if lang not in language_stats:
                            language_stats[lang] = 0
                        language_stats[lang] += 1
                except Exception as e:
                    print(f"Error parsing submissions: {e}")
            
            # If no solved count from profile, use language stats
            if not solved_count and language_stats:
                solved_count = sum(language_stats.values())
            
            # Get additional stats
            contest_url = f'https://www.hackerrank.com/rest/hackers/{username}/contest_participation'
            contest_response = self.session.get(contest_url, headers=headers)
            
            rating = 0
            rank = 'N/A'
            
            if contest_response.status_code == 200:
                try:
                    contest_data = contest_response.json()
                    contests = contest_data.get('models', [])
                    if contests:
                        latest_contest = contests[0]
                        rating = latest_contest.get('contest_rating', 0)
                        rank = latest_contest.get('global_rank', 'N/A')
                except Exception as e:
                    print(f"Error parsing contest data: {e}")
            
            print(f"HackerRank stats found - Rating: {rating}, Rank: {rank}, Solved: {solved_count}")
            print(f"Language stats: {language_stats}")
            
            return {
                'username': username,
                'rating': rating,
                'solved': solved_count,
                'rank': rank,
                'languageStats': language_stats
            }
            
        except Exception as e:
            print(f"HackerRank Error: {str(e)}")
            return {'error': str(e)}

class CodeChefHandler(PlatformHandler):
    def get_user_stats(self, username):
        try:
            print(f"Fetching CodeChef stats for user: {username}")
            url = f'https://www.codechef.com/users/{username}'
            response = self.session.get(url)
            
            if response.status_code != 200:
                return {'error': 'User not found'}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get rating
            rating_div = soup.find('div', {'class': 'rating-number'})
            rating = rating_div.text.strip() if rating_div else 'N/A'
            
            # Get global rank
            rank_div = soup.find('div', {'class': 'rating-ranks'})
            rank = rank_div.find('strong').text if rank_div else 'N/A'
            
            # Get problems solved
            problems_solved = 0
            language_stats = {}
            
            # Find all problem sections
            for section in soup.find_all('section', {'class': 'problems-solved'}):
                # Look for both 'Fully Solved' and 'Partially Solved' sections
                for header in section.find_all(['h5', 'h6']):
                    if 'Fully Solved' in header.text:
                        problems_div = header.find_next_sibling('div')
                        if problems_div:
                            problems = problems_div.find_all('a')
                            problems_solved += len(problems)
                            
                            # Count language statistics
                            for problem in problems:
                                lang_span = problem.find('span', {'title': 'Language'})
                                if lang_span:
                                    lang = lang_span.text.strip()
                                    language_stats[lang] = language_stats.get(lang, 0) + 1
            
            print(f"CodeChef stats found - Rating: {rating}, Rank: {rank}, Problems: {problems_solved}")
            print(f"Language stats: {language_stats}")
            
            return {
                'username': username,
                'rating': rating,
                'solved': problems_solved,
                'rank': rank,
                'languageStats': language_stats
            }
            
        except Exception as e:
            print(f"CodeChef Error: {str(e)}")
            return {'error': str(e)}

class CodeForcesHandler(PlatformHandler):
    def get_user_stats(self, username):
        try:
            # Get user info
            info_url = f'https://codeforces.com/api/user.info?handles={username}'
            info_response = self.session.get(info_url)
            
            if info_response.status_code != 200:
                return {'error': 'User not found'}

            info_data = info_response.json()
            if info_data['status'] != 'OK':
                return {'error': 'Failed to fetch user data'}

            # Get submission statistics
            submissions_url = f'https://codeforces.com/api/user.status?handle={username}&from=1&count=100'
            submissions_response = self.session.get(submissions_url)
            
            language_stats = {}
            total_solved = 0
            solved_problems = set()

            if submissions_response.status_code == 200:
                submissions_data = submissions_response.json()
                if submissions_data['status'] == 'OK':
                    for submission in submissions_data['result']:
                        if submission['verdict'] == 'OK':
                            problem_id = f"{submission['problem']['contestId']}{submission['problem']['index']}"
                            if problem_id not in solved_problems:
                                solved_problems.add(problem_id)
                                lang = submission['programmingLanguage']
                                language_stats[lang] = language_stats.get(lang, 0) + 1
                                total_solved += 1

            user_info = info_data['result'][0]
            return {
                'username': username,
                'rating': user_info.get('rating', 'N/A'),
                'solved': total_solved,
                'rank': user_info.get('rank', 'N/A'),
                'languageStats': language_stats
            }

        except Exception as e:
            print(f"CodeForces Error: {str(e)}")
            return {'error': str(e)}

def get_platform_handler(platform):
    handlers = {
        'leetcode': LeetCodeHandler,
        'hackerrank': HackerRankHandler,
        'codechef': CodeChefHandler,
        'codeforces': CodeForcesHandler
    }
    
    handler_class = handlers.get(platform.lower())
    if handler_class:
        return handler_class()
    raise ValueError(f'Unsupported platform: {platform}')
