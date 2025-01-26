import React from 'react';
import { Card, CardContent, Typography, CircularProgress, Box } from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

// Modern, professional color palette
const COLORS = [
  '#2196F3', // Blue
  '#4CAF50', // Green
  '#FFC107', // Amber
  '#9C27B0', // Purple
  '#F44336', // Red
  '#00BCD4', // Cyan
  '#FF9800', // Orange
  '#795548', // Brown
  '#607D8B', // Blue Grey
  '#E91E63', // Pink
];

const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index, name, value }) => {
  const RADIAN = Math.PI / 180;
  // Position the label further out from the pie
  const radius = outerRadius * 1.2;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  
  // Calculate line end points
  const lineEnd = {
    x: cx + (outerRadius + 10) * Math.cos(-midAngle * RADIAN),
    y: cy + (outerRadius + 10) * Math.sin(-midAngle * RADIAN),
  };

  // Add percentage calculation
  const percentage = (percent * 100).toFixed(1);

  return (
    <g>
      {/* Line from pie to label */}
      <line
        x1={cx + outerRadius * Math.cos(-midAngle * RADIAN)}
        y1={cy + outerRadius * Math.sin(-midAngle * RADIAN)}
        x2={lineEnd.x}
        y2={lineEnd.y}
        stroke="#666"
        strokeWidth={1}
      />
      {/* Line to text */}
      <line
        x1={lineEnd.x}
        y1={lineEnd.y}
        x2={x}
        y2={y}
        stroke="#666"
        strokeWidth={1}
      />
      {/* Label text */}
      <text
        x={x}
        y={y}
        fill="#333"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
        fontSize="12px"
      >
        {`${name} (${value}, ${percentage}%)`}
      </text>
    </g>
  );
};

const UserStatsCard = ({ stats, loading, error, platform }) => {
  if (loading) {
    return (
      <Card>
        <CardContent sx={{ textAlign: 'center', py: 5 }}>
          <CircularProgress />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent sx={{ textAlign: 'center', color: 'error.main' }}>
          <Typography variant="body1">{error}</Typography>
        </CardContent>
      </Card>
    );
  }

  if (!stats) {
    return null;
  }

  const formatValue = (value) => {
    return value === 'N/A' || value === null || value === undefined ? 'N/A' : value;
  };

  // Transform language stats for the pie chart
  const chartData = Object.entries(stats.languageStats || {}).map(([name, value]) => ({
    name,
    value: Number(value)
  })).filter(item => item.value > 0);

  // Calculate total problems for percentage
  const totalProblems = chartData.reduce((sum, item) => sum + item.value, 0);

  // Add percentage to chart data
  chartData.forEach(item => {
    item.percent = item.value / totalProblems;
  });

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          {platform.charAt(0).toUpperCase() + platform.slice(1)} Profile Stats
        </Typography>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="body1" gutterBottom>
            <strong>Username:</strong> {stats.username}
          </Typography>
          <Typography variant="body1" gutterBottom>
            <strong>Rating:</strong> {formatValue(stats.rating)}
          </Typography>
          <Typography variant="body1" gutterBottom>
            <strong>Problems Solved:</strong> {formatValue(stats.solved)}
          </Typography>
          <Typography variant="body1" gutterBottom>
            <strong>Global Rank:</strong> {formatValue(stats.rank)}
          </Typography>
        </Box>

        {chartData.length > 0 && (
          <Box sx={{ width: '100%', height: 400, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Language Distribution
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={120}
                  fill="#8884d8"
                  labelLine={false}
                  label={<CustomLabel />}
                >
                  {chartData.map((entry, index) => (
                    <Cell 
                      key={entry.name} 
                      fill={COLORS[index % COLORS.length]}
                      stroke="#fff"
                      strokeWidth={2}
                    />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value, name, props) => {
                    const percentage = ((value / totalProblems) * 100).toFixed(1);
                    return [`${value} problems (${percentage}%)`, name];
                  }}
                  contentStyle={{ 
                    backgroundColor: '#fff',
                    borderRadius: '8px',
                    padding: '10px',
                    boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
                    border: 'none'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default UserStatsCard;
