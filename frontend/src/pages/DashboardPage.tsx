import React from 'react';
import {
  Box,
  Typography,
  Card,
  IconButton,
  Grid,
  LinearProgress,
  useTheme,
  alpha,
} from '@mui/material';
import {
  MoreVert as MoreVertIcon,
  Shield as ShieldIcon,
  Refresh as RefreshIcon,
  BugReport as BugIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from 'recharts';

const attackData = [
  { day: 'Mon', attempts: 4 },
  { day: 'Tue', attempts: 3 },
  { day: 'Wed', attempts: 7 },
  { day: 'Thu', attempts: 2 },
  { day: 'Fri', attempts: 5 },
  { day: 'Sat', attempts: 1 },
  { day: 'Sun', attempts: 3 },
];

const recentActivity = [
  {
    type: 'warning',
    message: 'Suspicious login attempt detected',
    time: '2 minutes ago',
    ip: 'IP: 192.168.1.105',
  },
  {
    type: 'success',
    message: 'System update completed successfully',
    time: '15 minutes ago',
  },
  {
    type: 'error',
    message: 'Multiple failed authentication attempts',
    time: '1 hour ago',
    ip: 'IP: 192.168.1.210',
  },
];

const DashboardPage = () => {
  const theme = useTheme();

  return (
    <Box sx={{ p: { xs: 2, sm: 3, md: 4 }, maxWidth: '100%' }}>
      <Typography
        variant="h4"
        sx={{
          mb: 4,
          fontWeight: 600,
          color: theme.palette.mode === 'dark' ? '#fff' : '#111827',
        }}
      >
        Dashboard Overview
      </Typography>

      <Grid container spacing={3}>
        {/* Security Score */}
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              p: 3,
              height: '100%',
              backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#fff',
              borderRadius: 2,
              position: 'relative',
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: theme.shadows[8],
              },
            }}
          >
            <IconButton
              size="small"
              sx={{
                position: 'absolute',
                top: 12,
                right: 12,
                color: theme.palette.mode === 'dark' ? '#64748b' : '#94a3b8',
              }}
            >
              <MoreVertIcon />
            </IconButton>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <ShieldIcon sx={{ color: theme.palette.primary.main, fontSize: 24, mr: 1 }} />
            </Box>
            <Typography variant="h3" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', mb: 0.5 }}>
              92%
            </Typography>
            <Typography variant="body2" sx={{ color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280' }}>
              Security Score
            </Typography>
          </Card>
        </Grid>

        {/* System Health */}
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              p: 3,
              height: '100%',
              backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#fff',
              borderRadius: 2,
              position: 'relative',
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: theme.shadows[8],
              },
            }}
          >
            <IconButton
              size="small"
              sx={{
                position: 'absolute',
                top: 12,
                right: 12,
                color: theme.palette.mode === 'dark' ? '#64748b' : '#94a3b8',
              }}
            >
              <MoreVertIcon />
            </IconButton>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <RefreshIcon sx={{ color: theme.palette.success.main, fontSize: 24, mr: 1 }} />
            </Box>
            <Typography variant="h3" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', mb: 0.5 }}>
              98%
            </Typography>
            <Typography variant="body2" sx={{ color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280' }}>
              System Health
            </Typography>
          </Card>
        </Grid>

        {/* Active Threats */}
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              p: 3,
              height: '100%',
              backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#fff',
              borderRadius: 2,
              position: 'relative',
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: theme.shadows[8],
              },
            }}
          >
            <IconButton
              size="small"
              sx={{
                position: 'absolute',
                top: 12,
                right: 12,
                color: theme.palette.mode === 'dark' ? '#64748b' : '#94a3b8',
              }}
            >
              <MoreVertIcon />
            </IconButton>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <BugIcon sx={{ color: theme.palette.error.main, fontSize: 24, mr: 1 }} />
            </Box>
            <Typography variant="h3" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', mb: 0.5 }}>
              3
            </Typography>
            <Typography variant="body2" sx={{ color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280' }}>
              Active Threats
            </Typography>
          </Card>
        </Grid>

        {/* Protected Assets */}
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              p: 3,
              height: '100%',
              backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#fff',
              borderRadius: 2,
              position: 'relative',
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: theme.shadows[8],
              },
            }}
          >
            <IconButton
              size="small"
              sx={{
                position: 'absolute',
                top: 12,
                right: 12,
                color: theme.palette.mode === 'dark' ? '#64748b' : '#94a3b8',
              }}
            >
              <MoreVertIcon />
            </IconButton>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <SecurityIcon sx={{ color: theme.palette.info.main, fontSize: 24, mr: 1 }} />
            </Box>
            <Typography variant="h3" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', mb: 0.5 }}>
              156
            </Typography>
            <Typography variant="body2" sx={{ color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280' }}>
              Protected Assets
            </Typography>
          </Card>
        </Grid>

        {/* Attack Attempts Chart */}
        <Grid item xs={12} md={8}>
          <Card
            sx={{
              p: 3,
              height: '100%',
              backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#fff',
              borderRadius: 2,
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: theme.shadows[8],
              },
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
              <Typography variant="h6" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', fontWeight: 600 }}>
                Attack Attempts
              </Typography>
              <Typography
                variant="body2"
                sx={{ color: theme.palette.primary.main, cursor: 'pointer' }}
              >
                Last 7 days
              </Typography>
            </Box>
            <Box sx={{ height: 300, width: '100%' }}>
              <ResponsiveContainer>
                <BarChart data={attackData}>
                  <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.mode === 'dark' ? '#2a3441' : '#e5e7eb'} />
                  <XAxis
                    dataKey="day"
                    stroke={theme.palette.mode === 'dark' ? '#64748b' : '#6b7280'}
                    fontSize={12}
                  />
                  <YAxis
                    stroke={theme.palette.mode === 'dark' ? '#64748b' : '#6b7280'}
                    fontSize={12}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#fff',
                      border: 'none',
                      borderRadius: 8,
                      boxShadow: theme.shadows[3],
                    }}
                  />
                  <Bar
                    dataKey="attempts"
                    fill={theme.palette.primary.main}
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </Card>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={4}>
          <Card
            sx={{
              p: 3,
              height: '100%',
              backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#fff',
              borderRadius: 2,
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: theme.shadows[8],
              },
            }}
          >
            <Typography variant="h6" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', fontWeight: 600, mb: 3 }}>
              Recent Activity
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {recentActivity.map((activity, index) => (
                <Box key={index} sx={{ display: 'flex', gap: 2 }}>
                  <Box
                    sx={{
                      width: 8,
                      height: 8,
                      borderRadius: '50%',
                      backgroundColor:
                        activity.type === 'warning'
                          ? theme.palette.warning.main
                          : activity.type === 'success'
                          ? theme.palette.success.main
                          : theme.palette.error.main,
                      mt: 1,
                    }}
                  />
                  <Box>
                    <Typography variant="body2" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', mb: 0.5 }}>
                      {activity.message}
                    </Typography>
                    <Typography variant="caption" sx={{ color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280', display: 'block' }}>
                      {activity.time}
                    </Typography>
                    {activity.ip && (
                      <Typography
                        variant="caption"
                        sx={{ color: theme.palette.primary.main, display: 'block', mt: 0.5 }}
                      >
                        {activity.ip}
                      </Typography>
                    )}
                  </Box>
                </Box>
              ))}
            </Box>
          </Card>
        </Grid>

        {/* System Performance */}
        <Grid item xs={12}>
          <Card
            sx={{
              p: 3,
              backgroundColor: theme.palette.mode === 'dark' ? '#1a2234' : '#fff',
              borderRadius: 2,
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: theme.shadows[8],
              },
            }}
          >
            <Typography variant="h6" sx={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827', fontWeight: 600, mb: 3 }}>
              System Performance
            </Typography>
            <Grid container spacing={4}>
              {[
                { label: 'CPU Usage', value: 45, color: theme.palette.primary.main },
                { label: 'Memory Usage', value: 72, color: theme.palette.warning.main },
                { label: 'Storage Usage', value: 28, color: theme.palette.success.main },
              ].map((metric) => (
                <Grid item xs={12} md={4} key={metric.label}>
                  <Box sx={{ mb: 1 }}>
                    <Typography
                      variant="body2"
                      sx={{
                        color: theme.palette.mode === 'dark' ? '#64748b' : '#6b7280',
                        display: 'flex',
                        justifyContent: 'space-between',
                        mb: 1,
                      }}
                    >
                      <span>{metric.label}</span>
                      <span style={{ color: theme.palette.mode === 'dark' ? '#fff' : '#111827' }}>{metric.value}%</span>
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={metric.value}
                      sx={{
                        height: 6,
                        borderRadius: 3,
                        backgroundColor: alpha(metric.color, 0.12),
                        '& .MuiLinearProgress-bar': {
                          borderRadius: 3,
                          backgroundColor: metric.color,
                        },
                      }}
                    />
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;