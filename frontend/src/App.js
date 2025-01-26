import React, { useState } from 'react';
import { Container, Box, TextField, Select, MenuItem, Button, Typography, FormControl, InputLabel } from '@mui/material';
import UserStatsCard from './components/UserStatsCard';

const API_URL = 'http://localhost:5000';

function App() {
  const [platform, setPlatform] = useState('');
  const [username, setUsername] = useState('');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!platform || !username) return;

    setLoading(true);
    setError(null);
    setStats(null);

    try {
      console.log('Fetching profile...', { platform, username });
      
      const response = await fetch(`${API_URL}/api/profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ platform, username }),
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);

      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch profile data');
      }

      if (data.error) {
        throw new Error(data.error);
      }

      setStats(data);
    } catch (err) {
      console.error('Error fetching profile:', err);
      setError(err.message || 'Failed to fetch profile data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          CodeCracker
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom color="text.secondary">
          Coding Profile Analyzer
        </Typography>
      </Box>

      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel id="platform-label">Select Platform</InputLabel>
          <Select
            labelId="platform-label"
            value={platform}
            label="Select Platform"
            onChange={(e) => setPlatform(e.target.value)}
            required
          >
            <MenuItem value="leetcode">LeetCode</MenuItem>
            <MenuItem value="codechef">CodeChef</MenuItem>
            <MenuItem value="codeforces">CodeForces</MenuItem>
          </Select>
        </FormControl>

        <TextField
          fullWidth
          label={`Enter ${platform || 'platform'} Username`}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          sx={{ mb: 2 }}
          required
          placeholder="Enter your username"
        />

        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={loading || !platform || !username}
        >
          {loading ? 'Fetching Profile...' : 'Fetch Profile'}
        </Button>
      </Box>

      <UserStatsCard
        stats={stats}
        loading={loading}
        error={error}
        platform={platform}
      />
    </Container>
  );
}

export default App;
