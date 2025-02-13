import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Chip,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PersonAdd as InviteIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import useAuthStore from '../store/authStore';

interface TeamMember {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  organization_id: string;
}

interface InviteData {
  email: string;
  role: 'admin' | 'user';
}

const TeamManagementPage: React.FC = () => {
  const { user } = useAuthStore();
  const queryClient = useQueryClient();
  const [inviteDialogOpen, setInviteDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<TeamMember | null>(null);
  const [inviteData, setInviteData] = useState<InviteData>({
    email: '',
    role: 'user',
  });

  // Fetch team members
  const { data: teamMembers, isLoading } = useQuery({
    queryKey: ['team-members'],
    queryFn: async () => {
      const response = await api.get<TeamMember[]>('/users/organization-members');
      return response.data;
    },
  });

  // Invite mutation
  const inviteMutation = useMutation({
    mutationFn: (data: InviteData) =>
      api.post('/users/invite', {
        ...data,
        organization_id: user?.organization_id,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['team-members'] });
      setInviteDialogOpen(false);
      setInviteData({ email: '', role: 'user' });
    },
  });

  // Update user mutation
  const updateUserMutation = useMutation({
    mutationFn: (data: Partial<TeamMember>) =>
      api.put(`/users/${data.id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['team-members'] });
      setEditDialogOpen(false);
      setSelectedUser(null);
    },
  });

  // Delete user mutation
  const deleteUserMutation = useMutation({
    mutationFn: (userId: string) => api.delete(`/users/${userId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['team-members'] });
    },
  });

  const handleInvite = () => {
    inviteMutation.mutate(inviteData);
  };

  const handleUpdateUser = (userData: Partial<TeamMember>) => {
    if (selectedUser) {
      updateUserMutation.mutate({ ...userData, id: selectedUser.id });
    }
  };

  const handleDeleteUser = (userId: string) => {
    if (window.confirm('Are you sure you want to remove this team member?')) {
      deleteUserMutation.mutate(userId);
    }
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Team Management</Typography>
        <Button
          variant="contained"
          startIcon={<InviteIcon />}
          onClick={() => setInviteDialogOpen(true)}
        >
          Invite Member
        </Button>
      </Box>

      {/* Team Members Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {teamMembers?.map((member) => (
              <TableRow key={member.id}>
                <TableCell>{member.full_name}</TableCell>
                <TableCell>{member.email}</TableCell>
                <TableCell>
                  <Chip
                    label={member.is_superuser ? 'Admin' : 'User'}
                    color={member.is_superuser ? 'primary' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={member.is_active ? 'Active' : 'Inactive'}
                    color={member.is_active ? 'success' : 'error'}
                    size="small"
                  />
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    onClick={() => {
                      setSelectedUser(member);
                      setEditDialogOpen(true);
                    }}
                  >
                    <EditIcon />
                  </IconButton>
                  {user?.id !== member.id && (
                    <IconButton
                      color="error"
                      onClick={() => handleDeleteUser(member.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Invite Dialog */}
      <Dialog
        open={inviteDialogOpen}
        onClose={() => setInviteDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Invite Team Member</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={inviteData.email}
              onChange={(e) =>
                setInviteData({ ...inviteData, email: e.target.value })
              }
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              select
              label="Role"
              value={inviteData.role}
              onChange={(e) =>
                setInviteData({
                  ...inviteData,
                  role: e.target.value as 'admin' | 'user',
                })
              }
            >
              <MenuItem value="user">User</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
            </TextField>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setInviteDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleInvite}
            disabled={inviteMutation.isPending}
          >
            {inviteMutation.isPending ? 'Sending...' : 'Send Invitation'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit User Dialog */}
      <Dialog
        open={editDialogOpen}
        onClose={() => setEditDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Edit Team Member</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Full Name"
              value={selectedUser?.full_name || ''}
              onChange={(e) =>
                setSelectedUser(
                  selectedUser
                    ? { ...selectedUser, full_name: e.target.value }
                    : null
                )
              }
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              select
              label="Role"
              value={selectedUser?.is_superuser ? 'admin' : 'user'}
              onChange={(e) =>
                setSelectedUser(
                  selectedUser
                    ? {
                        ...selectedUser,
                        is_superuser: e.target.value === 'admin',
                      }
                    : null
                )
              }
              sx={{ mb: 2 }}
            >
              <MenuItem value="user">User</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
            </TextField>
            <TextField
              fullWidth
              select
              label="Status"
              value={selectedUser?.is_active ? 'active' : 'inactive'}
              onChange={(e) =>
                setSelectedUser(
                  selectedUser
                    ? {
                        ...selectedUser,
                        is_active: e.target.value === 'active',
                      }
                    : null
                )
              }
            >
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="inactive">Inactive</MenuItem>
            </TextField>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => selectedUser && handleUpdateUser(selectedUser)}
            disabled={updateUserMutation.isPending}
          >
            {updateUserMutation.isPending ? 'Saving...' : 'Save Changes'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Error Alerts */}
      {inviteMutation.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          Failed to send invitation: {(inviteMutation.error as Error).message}
        </Alert>
      )}
      {updateUserMutation.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          Failed to update user: {(updateUserMutation.error as Error).message}
        </Alert>
      )}
      {deleteUserMutation.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          Failed to remove user: {(deleteUserMutation.error as Error).message}
        </Alert>
      )}
    </Box>
  );
};

export default TeamManagementPage; 