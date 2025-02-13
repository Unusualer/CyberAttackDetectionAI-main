import React, { useState } from 'react';
import { styled, useTheme } from '@mui/material/styles';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  IconButton,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Avatar,
  Menu,
  MenuItem,
  useMediaQuery,
  Tooltip,
  Badge,
  alpha,
  Divider,
  CssBaseline,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Security as SecurityIcon,
  People as PeopleIcon,
  Settings as SettingsIcon,
  ExitToApp as LogoutIcon,
  NotificationsNoneOutlined as NotificationsIcon,
  Search as SearchIcon,
  Shield as ShieldIcon,
  ChevronLeft as ChevronLeftIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import useAuthStore from '../store/authStore';

const drawerWidth = 280;

const SearchBox = styled('div')(({ theme }) => ({
  position: 'relative',
  width: 260,
  height: 40,
  backgroundColor: '#1a2234',
  borderRadius: 8,
  display: 'flex',
  alignItems: 'center',
  padding: '0 12px',
  gap: 8,
  '& .MuiSvgIcon-root': {
    color: '#64748b',
    fontSize: 20,
  },
  '& input': {
    border: 'none',
    outline: 'none',
    background: 'none',
    color: '#fff',
    fontSize: '0.875rem',
    width: '100%',
    '&::placeholder': {
      color: '#64748b',
      opacity: 1,
    },
  },
  [theme.breakpoints.down('sm')]: {
    display: 'none',
  },
}));

const StyledBadge = styled(Badge)(({ theme }) => ({
  '& .MuiBadge-badge': {
    backgroundColor: '#ef4444',
    color: '#fff',
    minWidth: 18,
    height: 18,
    padding: '0 4px',
    fontSize: 11,
    fontWeight: 600,
    lineHeight: 1,
    boxShadow: `0 0 0 2px #0f1520`,
    '&::after': {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      borderRadius: '50%',
      animation: 'ripple 1.2s infinite ease-in-out',
      border: '1px solid #ef4444',
      content: '""',
    },
  },
  '@keyframes ripple': {
    '0%': {
      transform: 'scale(.8)',
      opacity: 1,
    },
    '100%': {
      transform: 'scale(2.4)',
      opacity: 0,
    },
  },
}));

const StyledAppBar = styled(AppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})<{ open?: boolean }>(({ theme, open }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#0f1520' : '#fff',
  borderBottom: `1px solid ${theme.palette.mode === 'dark' ? '#1a2234' : '#f3f4f6'}`,
  boxShadow: 'none',
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: 200,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
  }),
}));

const StyledDrawer = styled(Drawer, {
  shouldForwardProp: (prop) => prop !== 'open',
})<{ open?: boolean }>(({ theme, open }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: 'nowrap',
  boxSizing: 'border-box',
  '& .MuiDrawer-paper': {
    backgroundColor: theme.palette.mode === 'dark' ? '#0f1520' : '#fff',
    width: open ? drawerWidth : theme.spacing(7),
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: 200,
    }),
    overflowX: 'hidden',
    border: 'none',
    borderRight: `1px solid ${theme.palette.mode === 'dark' ? '#1a2234' : '#f3f4f6'}`,
    boxShadow: 'none',
    [theme.breakpoints.up('sm')]: {
      width: open ? drawerWidth : theme.spacing(9),
    },
  },
}));

const StyledListItemButton = styled(ListItemButton)(({ theme }) => ({
  minHeight: 48,
  padding: '8px 12px',
  margin: '2px 8px',
  borderRadius: 8,
  transition: 'all 200ms cubic-bezier(0.4, 0, 0.2, 1)',
  '&:hover': {
    backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#f3f4f6',
  },
  '&.Mui-selected': {
    backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#f3f4f6',
    '&:hover': {
      backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#f3f4f6',
    },
  },
}));

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const [open, setOpen] = useState(true);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuthStore();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  React.useEffect(() => {
    if (isMobile) {
      setOpen(false);
    }
  }, [isMobile]);

  const handleDrawerToggle = () => {
    setOpen(!open);
  };

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { text: 'Security Events', icon: <SecurityIcon />, path: '/events' },
    { text: 'Team', icon: <PeopleIcon />, path: '/team' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
  ];

  return (
    <Box sx={{ display: 'flex', bgcolor: theme.palette.mode === 'dark' ? '#0a0f18' : '#f9fafb', minHeight: '100vh' }}>
      <CssBaseline />
      
      <StyledAppBar position="fixed" open={open}>
        <Toolbar sx={{ minHeight: 64, px: 2 }}>
          <IconButton
            onClick={handleDrawerToggle}
            sx={{
              color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280',
              mr: 2,
              '&:hover': { backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#f3f4f6' },
            }}
          >
            {open ? <ChevronLeftIcon /> : <MenuIcon />}
          </IconButton>

          <SearchBox>
            <SearchIcon />
            <input placeholder="Search..." />
          </SearchBox>

          <Box sx={{ flexGrow: 1 }} />

          <IconButton
            sx={{
              color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280',
              '&:hover': { backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#f3f4f6' },
            }}
          >
            <StyledBadge badgeContent={3}>
              <NotificationsIcon />
            </StyledBadge>
          </IconButton>

          <Box
            onClick={handleMenu}
            sx={{
              ml: 2,
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              cursor: 'pointer',
              p: '6px 8px',
              borderRadius: 1,
              '&:hover': { backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#f3f4f6' },
            }}
          >
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
              {user?.full_name?.charAt(0) || 'U'}
            </Avatar>
            <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
              <Typography variant="subtitle2" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', fontWeight: 600 }}>
                {user?.full_name}
              </Typography>
              <Typography variant="caption" sx={{ color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280' }}>
                Administrator
              </Typography>
            </Box>
          </Box>
        </Toolbar>
      </StyledAppBar>

      <StyledDrawer variant="permanent" open={open}>
        <Toolbar sx={{ minHeight: 64, px: 2 }}>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
              transition: 'opacity 200ms',
              opacity: open ? 1 : 0,
            }}
          >
            <ShieldIcon sx={{ fontSize: 24, color: 'primary.main' }} />
            <Typography variant="h6" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', fontWeight: 600 }}>
              Cyber Defense
            </Typography>
          </Box>
        </Toolbar>

        <List sx={{ mt: 1, px: 0 }}>
          {menuItems.map((item) => (
            <StyledListItemButton
              key={item.text}
              selected={location.pathname === item.path}
              onClick={() => navigate(item.path)}
            >
              <ListItemIcon sx={{ 
                minWidth: 36,
                color: location.pathname === item.path ? 'primary.main' : theme.palette.mode === 'dark' ? '#64748b' : '#6b7280',
              }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.text}
                sx={{
                  m: 0,
                  opacity: open ? 1 : 0,
                  transition: 'opacity 200ms',
                  '& .MuiTypography-root': {
                    color: location.pathname === item.path ? 'primary.main' : theme.palette.mode === 'dark' ? '#fff' : '#111827',
                    fontSize: '0.875rem',
                    fontWeight: 500,
                  },
                }}
              />
            </StyledListItemButton>
          ))}
        </List>
      </StyledDrawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          minHeight: '100vh',
          backgroundColor: theme.palette.mode === 'dark' ? '#0a0f18' : '#f9fafb',
          transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: 200,
          }),
          marginLeft: 0,
          ...(open && {
            marginLeft: `${drawerWidth}px`,
          }),
          ...(!open && {
            marginLeft: {
              xs: theme.spacing(7),
              sm: theme.spacing(9),
            },
          }),
        }}
      >
        <Toolbar sx={{ minHeight: 64 }} />
        <Box
          sx={{
            flexGrow: 1,
            display: 'flex',
            width: '100%',
            py: { xs: 2, sm: 3 },
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  );
};

export default DashboardLayout; 