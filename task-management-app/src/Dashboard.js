// src/components/Dashboard.js
import React from 'react';
import './Dashboard.css';
import { Box, Grid, Typography, Card, CardContent, Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import dashboardImage from './Dashboard.png';

const Dashboard = () => {
  const taskStatuses = [
    { title: "Critical Task", count: 1, color: "error.main" },
    { title: "Pending Tasks", count: 2, color: "warning.main" },
    { title: "Completed Tasks", count: 3, color: "success.main" },
  ];

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4">Welcome Teesha Saxena!</Typography>
      <Grid container spacing={2} sx={{ marginTop: 2 }}>
        {taskStatuses.map((status) => (
          <Grid item xs={4} key={status.title}>
            <Card sx={{ backgroundColor: status.color, color: 'white' }}>
              <CardContent>
                <Typography variant="h5">{status.count}</Typography>
                <Typography>{status.title}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
        <Grid item xs={12}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{ backgroundColor: '#3f51b5', color: 'white' }}
          >
            Add a Task
          </Button>
        </Grid>
        <img 
        src={dashboardImage} 
        alt="Dashboard Overview" 
        className="dashboard-image"  // Optional: Add a class for styling
      />
      </Grid>
    </Box>
  );
};

export default Dashboard;
