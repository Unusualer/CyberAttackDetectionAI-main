import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Tabs,
  Tab,
  TextField,
  Switch,
  FormControlLabel,
  Button,
  Divider,
  Alert,
  CircularProgress,
  Slider,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Grid,
} from '@mui/material';
import {
  Save as SaveIcon,
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import useAuthStore from '../store/authStore';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

interface OrganizationSettings {
  name: string;
  notification_email: string;
  alert_threshold: number;
  enable_notifications: boolean;
  notification_frequency: 'realtime' | 'hourly' | 'daily';
  security_level: 'low' | 'medium' | 'high';
  auto_block_threats: boolean;
  retention_days: number;
}

const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const { user } = useAuthStore();
  const queryClient = useQueryClient();

  // Fetch organization settings
  const { data: settings, isLoading } = useQuery({
    queryKey: ['organization-settings', user?.organization_id],
    queryFn: async () => {
      const response = await api.get<OrganizationSettings>(
        `/organizations/${user?.organization_id}/settings`
      );
      return response.data;
    },
  });

  // Update settings mutation
  const updateSettingsMutation = useMutation({
    mutationFn: (newSettings: Partial<OrganizationSettings>) =>
      api.put(`/organizations/${user?.organization_id}/settings`, newSettings),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['organization-settings'],
      });
    },
  });

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleSaveSettings = (
    sectionData: Partial<OrganizationSettings>
  ) => {
    updateSettingsMutation.mutate(sectionData);
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
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Paper sx={{ mt: 3 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          aria-label="settings tabs"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab
            icon={<BusinessIcon />}
            label="Organization"
            iconPosition="start"
          />
          <Tab
            icon={<SecurityIcon />}
            label="Security"
            iconPosition="start"
          />
          <Tab
            icon={<NotificationsIcon />}
            label="Notifications"
            iconPosition="start"
          />
        </Tabs>

        {/* Organization Settings */}
        <TabPanel value={activeTab} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Organization Name"
                value={settings?.name || ''}
                onChange={(e) =>
                  handleSaveSettings({ name: e.target.value })
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Primary Contact Email"
                type="email"
                value={settings?.notification_email || ''}
                onChange={(e) =>
                  handleSaveSettings({
                    notification_email: e.target.value,
                  })
                }
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Data Retention Period</InputLabel>
                <Select
                  value={settings?.retention_days || 30}
                  label="Data Retention Period"
                  onChange={(e) =>
                    handleSaveSettings({
                      retention_days: e.target.value as number,
                    })
                  }
                >
                  <MenuItem value={30}>30 days</MenuItem>
                  <MenuItem value={60}>60 days</MenuItem>
                  <MenuItem value={90}>90 days</MenuItem>
                  <MenuItem value={180}>180 days</MenuItem>
                  <MenuItem value={365}>1 year</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Security Settings */}
        <TabPanel value={activeTab} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Security Level</InputLabel>
                <Select
                  value={settings?.security_level || 'medium'}
                  label="Security Level"
                  onChange={(e) =>
                    handleSaveSettings({
                      security_level: e.target.value as 'low' | 'medium' | 'high',
                    })
                  }
                >
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <Typography gutterBottom>Alert Threshold</Typography>
              <Slider
                value={settings?.alert_threshold || 50}
                onChange={(_, value) =>
                  handleSaveSettings({ alert_threshold: value as number })
                }
                valueLabelDisplay="auto"
                step={10}
                marks
                min={0}
                max={100}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings?.auto_block_threats || false}
                    onChange={(e) =>
                      handleSaveSettings({
                        auto_block_threats: e.target.checked,
                      })
                    }
                  />
                }
                label="Automatically block detected threats"
              />
            </Grid>
          </Grid>
        </TabPanel>

        {/* Notification Settings */}
        <TabPanel value={activeTab} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings?.enable_notifications || false}
                    onChange={(e) =>
                      handleSaveSettings({
                        enable_notifications: e.target.checked,
                      })
                    }
                  />
                }
                label="Enable Notifications"
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Notification Frequency</InputLabel>
                <Select
                  value={settings?.notification_frequency || 'realtime'}
                  label="Notification Frequency"
                  onChange={(e) =>
                    handleSaveSettings({
                      notification_frequency: e.target.value as
                        | 'realtime'
                        | 'hourly'
                        | 'daily',
                    })
                  }
                >
                  <MenuItem value="realtime">Real-time</MenuItem>
                  <MenuItem value="hourly">Hourly Summary</MenuItem>
                  <MenuItem value="daily">Daily Digest</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>

      {/* Error Alert */}
      {updateSettingsMutation.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          Failed to update settings:{' '}
          {(updateSettingsMutation.error as Error).message}
        </Alert>
      )}

      {/* Success Alert */}
      {updateSettingsMutation.isSuccess && (
        <Alert severity="success" sx={{ mt: 2 }}>
          Settings updated successfully
        </Alert>
      )}
    </Box>
  );
};

export default SettingsPage; 