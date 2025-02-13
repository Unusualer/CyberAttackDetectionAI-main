import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Avatar,
  IconButton,
  Button,
  TextField,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  MenuItem,
  Stack,
  Chip,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  MoreVert as MoreVertIcon,
  Mail as MailIcon,
  Phone as PhoneIcon,
  Shield as ShieldIcon,
  AdminPanelSettings as AdminIcon,
  Security as SecurityIcon,
  Person as PersonIcon,
} from '@mui/icons-material';

const mockTeamMembers = [
  {
    id: 1,
    name: 'John Smith',
    role: 'Administrator',
    email: 'john.smith@company.com',
    phone: '+1 (555) 123-4567',
    status: 'active',
    avatar: 'JS',
  },
  {
    id: 2,
    name: 'Sarah Johnson',
    role: 'Security Analyst',
    email: 'sarah.j@company.com',
    phone: '+1 (555) 234-5678',
    status: 'active',
    avatar: 'SJ',
  },
  {
    id: 3,
    name: 'Michael Chen',
    role: 'Security Engineer',
    email: 'michael.c@company.com',
    phone: '+1 (555) 345-6789',
    status: 'away',
    avatar: 'MC',
  },
  {
    id: 4,
    name: 'Emily Davis',
    role: 'Incident Responder',
    email: 'emily.d@company.com',
    phone: '+1 (555) 456-7890',
    status: 'active',
    avatar: 'ED',
  },
];

const roles = [
  'Administrator',
  'Security Analyst',
  'Security Engineer',
  'Incident Responder',
  'SOC Analyst',
];

const TeamPage: React.FC = () => {
  const theme = useTheme();
  const [searchTerm, setSearchTerm] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [newMember, setNewMember] = useState({
    name: '',
    role: '',
    email: '',
    phone: '',
  });

  const handleOpenDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setNewMember({
      name: '',
      role: '',
      email: '',
      phone: '',
    });
  };

  const getRoleIcon = (role: string) => {
    switch (role.toLowerCase()) {
      case 'administrator':
        return <AdminIcon />;
      case 'security analyst':
        return <SecurityIcon />;
      case 'security engineer':
        return <ShieldIcon />;
      default:
        return <PersonIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return theme.palette.success;
      case 'away':
        return theme.palette.warning;
      default:
        return theme.palette.error;
    }
  };

  const filteredMembers = mockTeamMembers.filter(
    (member) =>
      member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      member.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
      member.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4">Team Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleOpenDialog}
          sx={{
            borderRadius: 2,
            textTransform: 'none',
            px: 3,
          }}
        >
          Add Member
        </Button>
      </Box>

      <TextField
        fullWidth
        size="small"
        placeholder="Search team members..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon sx={{ color: 'text.secondary' }} />
            </InputAdornment>
          ),
        }}
        sx={{
          maxWidth: 300,
          mb: 4,
          '& .MuiOutlinedInput-root': {
            backgroundColor: alpha(theme.palette.primary.main, 0.02),
          },
        }}
      />

      <Grid container spacing={3}>
        {filteredMembers.map((member) => {
          const statusColor = getStatusColor(member.status);

          return (
            <Grid item xs={12} sm={6} md={4} key={member.id}>
              <Card
                sx={{
                  height: '100%',
                  position: 'relative',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: theme.shadows[8],
                  },
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Avatar
                      sx={{
                        width: 56,
                        height: 56,
                        backgroundColor: alpha(theme.palette.primary.main, 0.1),
                        color: theme.palette.primary.main,
                        fontSize: '1.2rem',
                        fontWeight: 600,
                      }}
                    >
                      {member.avatar}
                    </Avatar>
                    <Box>
                      <IconButton size="small">
                        <MoreVertIcon />
                      </IconButton>
                    </Box>
                  </Box>

                  <Stack spacing={1}>
                    <Box>
                      <Typography variant="h6" sx={{ mb: 0.5 }}>
                        {member.name}
                      </Typography>
                      <Stack direction="row" spacing={1} alignItems="center">
                        <Box sx={{ color: theme.palette.primary.main }}>
                          {getRoleIcon(member.role)}
                        </Box>
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          sx={{ fontWeight: 500 }}
                        >
                          {member.role}
                        </Typography>
                      </Stack>
                    </Box>

                    <Stack spacing={1}>
                      <Stack direction="row" spacing={1} alignItems="center">
                        <MailIcon sx={{ color: 'text.secondary', fontSize: '1rem' }} />
                        <Typography variant="body2" color="text.secondary">
                          {member.email}
                        </Typography>
                      </Stack>
                      <Stack direction="row" spacing={1} alignItems="center">
                        <PhoneIcon sx={{ color: 'text.secondary', fontSize: '1rem' }} />
                        <Typography variant="body2" color="text.secondary">
                          {member.phone}
                        </Typography>
                      </Stack>
                    </Stack>

                    <Box sx={{ mt: 1 }}>
                      <Chip
                        label={member.status}
                        size="small"
                        sx={{
                          backgroundColor: alpha(statusColor.main, 0.1),
                          color: statusColor.main,
                          fontWeight: 600,
                          textTransform: 'capitalize',
                        }}
                      />
                    </Box>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <Dialog
        open={openDialog}
        onClose={handleCloseDialog}
        maxWidth="sm"
        fullWidth
        PaperProps={{
          elevation: 2,
          sx: {
            borderRadius: 2,
          },
        }}
      >
        <DialogTitle>Add New Team Member</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Full Name"
              value={newMember.name}
              onChange={(e) => setNewMember({ ...newMember, name: e.target.value })}
            />
            <TextField
              fullWidth
              select
              label="Role"
              value={newMember.role}
              onChange={(e) => setNewMember({ ...newMember, role: e.target.value })}
            >
              {roles.map((role) => (
                <MenuItem key={role} value={role}>
                  {role}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={newMember.email}
              onChange={(e) => setNewMember({ ...newMember, email: e.target.value })}
            />
            <TextField
              fullWidth
              label="Phone"
              value={newMember.phone}
              onChange={(e) => setNewMember({ ...newMember, phone: e.target.value })}
            />
          </Stack>
        </DialogContent>
        <DialogActions sx={{ p: 2.5 }}>
          <Button onClick={handleCloseDialog} color="inherit">
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleCloseDialog}
            sx={{
              px: 3,
              borderRadius: 2,
              textTransform: 'none',
            }}
          >
            Add Member
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default TeamPage; 