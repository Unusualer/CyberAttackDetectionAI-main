import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  TextField,
  InputAdornment,
  Stack,
  Button,
  Menu,
  MenuItem,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  MoreVert as MoreVertIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';

const mockEvents = [
  {
    id: 1,
    timestamp: '2024-01-20T14:30:00',
    type: 'Authentication',
    severity: 'high',
    source: '192.168.1.105',
    description: 'Multiple failed login attempts detected',
    status: 'open',
  },
  {
    id: 2,
    timestamp: '2024-01-20T14:25:00',
    type: 'Network',
    severity: 'medium',
    source: '192.168.1.210',
    description: 'Unusual outbound traffic pattern detected',
    status: 'investigating',
  },
  {
    id: 3,
    timestamp: '2024-01-20T14:20:00',
    type: 'System',
    severity: 'low',
    source: 'Server-01',
    description: 'System update completed successfully',
    status: 'resolved',
  },
  {
    id: 4,
    timestamp: '2024-01-20T14:15:00',
    type: 'Malware',
    severity: 'high',
    source: '192.168.1.150',
    description: 'Potential malware activity detected',
    status: 'open',
  },
  {
    id: 5,
    timestamp: '2024-01-20T14:10:00',
    type: 'Firewall',
    severity: 'medium',
    source: 'Firewall-01',
    description: 'Port scan attempt blocked',
    status: 'resolved',
  },
];

const EventsPage: React.FC = () => {
  const theme = useTheme();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedSeverity, setSelectedSeverity] = useState<string | null>(null);

  const handleFilterClick = (event: React.MouseEvent<HTMLElement>) => {
    setFilterAnchorEl(event.currentTarget);
  };

  const handleFilterClose = () => {
    setFilterAnchorEl(null);
  };

  const handleSeverityFilter = (severity: string | null) => {
    setSelectedSeverity(severity);
    handleFilterClose();
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return theme.palette.error;
      case 'medium':
        return theme.palette.warning;
      case 'low':
        return theme.palette.success;
      default:
        return theme.palette.info;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open':
        return theme.palette.error;
      case 'investigating':
        return theme.palette.warning;
      case 'resolved':
        return theme.palette.success;
      default:
        return theme.palette.info;
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return <ErrorIcon fontSize="small" />;
      case 'medium':
        return <WarningIcon fontSize="small" />;
      case 'low':
        return <InfoIcon fontSize="small" />;
      default:
        return <CheckCircleIcon fontSize="small" />;
    }
  };

  const filteredEvents = mockEvents.filter((event) => {
    const matchesSearch = Object.values(event).some((value) =>
      value.toString().toLowerCase().includes(searchTerm.toLowerCase())
    );
    const matchesSeverity = !selectedSeverity || event.severity === selectedSeverity;
    return matchesSearch && matchesSeverity;
  });

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 4 }}>
        Security Events
      </Typography>

      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Search events..."
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
                '& .MuiOutlinedInput-root': {
                  backgroundColor: alpha(theme.palette.primary.main, 0.02),
                },
              }}
            />
            <Button
              variant="outlined"
              startIcon={<FilterIcon />}
              onClick={handleFilterClick}
              sx={{
                borderColor: alpha(theme.palette.primary.main, 0.2),
                '&:hover': {
                  borderColor: theme.palette.primary.main,
                  backgroundColor: alpha(theme.palette.primary.main, 0.02),
                },
              }}
            >
              Filter
            </Button>
          </Box>

          <Menu
            anchorEl={filterAnchorEl}
            open={Boolean(filterAnchorEl)}
            onClose={handleFilterClose}
            PaperProps={{
              elevation: 2,
              sx: {
                minWidth: 180,
                borderRadius: 2,
                mt: 1,
              },
            }}
          >
            <MenuItem onClick={() => handleSeverityFilter(null)}>All Severities</MenuItem>
            <MenuItem onClick={() => handleSeverityFilter('high')}>High</MenuItem>
            <MenuItem onClick={() => handleSeverityFilter('medium')}>Medium</MenuItem>
            <MenuItem onClick={() => handleSeverityFilter('low')}>Low</MenuItem>
          </Menu>

          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Severity</TableCell>
                  <TableCell>Timestamp</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Source</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredEvents.map((event) => {
                  const severityColor = getSeverityColor(event.severity);
                  const statusColor = getStatusColor(event.status);

                  return (
                    <TableRow
                      key={event.id}
                      sx={{
                        '&:hover': {
                          backgroundColor: alpha(theme.palette.primary.main, 0.02),
                        },
                      }}
                    >
                      <TableCell>
                        <Stack direction="row" alignItems="center" spacing={1}>
                          <Box sx={{ color: severityColor.main }}>
                            {getSeverityIcon(event.severity)}
                          </Box>
                          <Typography
                            variant="body2"
                            sx={{
                              color: severityColor.main,
                              fontWeight: 600,
                              textTransform: 'capitalize',
                            }}
                          >
                            {event.severity}
                          </Typography>
                        </Stack>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {new Date(event.timestamp).toLocaleString()}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{event.type}</Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{event.source}</Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{event.description}</Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={event.status}
                          size="small"
                          sx={{
                            backgroundColor: alpha(statusColor.main, 0.1),
                            color: statusColor.main,
                            fontWeight: 600,
                            textTransform: 'capitalize',
                          }}
                        />
                      </TableCell>
                      <TableCell align="right">
                        <IconButton size="small">
                          <MoreVertIcon fontSize="small" />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default EventsPage; 