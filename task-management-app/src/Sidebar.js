// src/components/Sidebar.js
import React from 'react';
import './Sidebar.css';
import { List, ListItem, ListItemIcon, ListItemText, Drawer, Box } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import TaskIcon from '@mui/icons-material/Task';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';

const Sidebar = () => {
  return (
    <Drawer variant="permanent">
      <Box sx={{ width: 250, backgroundColor: '#1A202C', color: 'white', height: '100%' }}>
        <List>
          <ListItem>
            <ListItemText primary="Task Manager" sx={{ color: 'white', textAlign: 'center', fontWeight: 'bold' }} />
          </ListItem>
          <ListItem button>
            <ListItemIcon><HomeIcon sx={{ color: 'white' }} /></ListItemIcon>
            <ListItemText primary="Home" />
          </ListItem>
          <ListItem button>
            <ListItemIcon><TaskIcon sx={{ color: 'white' }} /></ListItemIcon>
            <ListItemText primary="Tasks" />
          </ListItem>
          <ListItem button>
            <ListItemIcon><SettingsIcon sx={{ color: 'white' }} /></ListItemIcon>
            <ListItemText primary="Settings" />
          </ListItem>
          <ListItem button>
            <ListItemIcon><LogoutIcon sx={{ color: 'white' }} /></ListItemIcon>
            <ListItemText primary="Logout" />
          </ListItem>
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
