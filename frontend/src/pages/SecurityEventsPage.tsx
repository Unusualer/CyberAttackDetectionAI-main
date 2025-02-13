import React, { useState, useMemo } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  TextField,
  MenuItem,
  IconButton,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Search as SearchIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { format } from 'date-fns';
import api from '../services/api';

// Types
interface SecurityEvent {
  id: string;
  event_type: string;
  severity: 'low' | 'medium' | 'high';
  description: string;
  created_at: string;
  event_metadata: Record<string, any>;
}

interface EventsResponse {
  events: SecurityEvent[];
  total: number;
  page: number;
  per_page: number;
}

const severityColors = {
  low: 'success',
  medium: 'warning',
  high: 'error',
};

const SecurityEventsPage: React.FC = () => {
  // State for filters and pagination
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');
  const [selectedEventType, setSelectedEventType] = useState<string>('all');
  const [dateRange, setDateRange] = useState({
    start: '',
    end: '',
  });

  // Fetch events with filters
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['security-events', page, rowsPerPage, searchQuery, selectedSeverity, selectedEventType, dateRange],
    queryFn: async () => {
      const params = new URLSearchParams({
        page: (page + 1).toString(),
        per_page: rowsPerPage.toString(),
        ...(searchQuery && { search: searchQuery }),
        ...(selectedSeverity !== 'all' && { severity: selectedSeverity }),
        ...(selectedEventType !== 'all' && { event_type: selectedEventType }),
        ...(dateRange.start && { start_date: dateRange.start }),
        ...(dateRange.end && { end_date: dateRange.end }),
      });

      const response = await api.get<EventsResponse>(`/events?${params}`);
      return response.data;
    },
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  // Calculate statistics for the chart
  const chartData = useMemo(() => {
    if (!data?.events) return [];

    const stats = data.events.reduce((acc, event) => {
      const date = format(new Date(event.created_at), 'MM/dd');
      if (!acc[date]) {
        acc[date] = { date, low: 0, medium: 0, high: 0 };
      }
      acc[date][event.severity]++;
      return acc;
    }, {} as Record<string, any>);

    return Object.values(stats);
  }, [data?.events]);

  const handleChangePage = (_: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        Error loading security events: {(error as Error).message}
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Security Events</Typography>
        <IconButton onClick={() => refetch()}>
          <RefreshIcon />
        </IconButton>
      </Box>

      {/* Filters */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              label="Search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              InputProps={{
                endAdornment: <SearchIcon />,
              }}
            />
          </Grid>
          <Grid item xs={12} sm={2}>
            <TextField
              fullWidth
              select
              label="Severity"
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="low">Low</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="high">High</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} sm={2}>
            <TextField
              fullWidth
              select
              label="Event Type"
              value={selectedEventType}
              onChange={(e) => setSelectedEventType(e.target.value)}
            >
              <MenuItem value="all">All</MenuItem>
              {/* Add event types dynamically */}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={2}>
            <TextField
              fullWidth
              type="date"
              label="Start Date"
              value={dateRange.start}
              onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} sm={2}>
            <TextField
              fullWidth
              type="date"
              label="End Date"
              value={dateRange.end}
              onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} sm={1}>
            <IconButton onClick={() => refetch()}>
              <FilterIcon />
            </IconButton>
          </Grid>
        </Grid>
      </Paper>

      {/* Statistics Chart */}
      <Paper sx={{ p: 2, mb: 3, height: 300 }}>
        <Typography variant="h6" gutterBottom>
          Event Statistics
        </Typography>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="low" stackId="a" fill="#4caf50" name="Low" />
            <Bar dataKey="medium" stackId="a" fill="#ff9800" name="Medium" />
            <Bar dataKey="high" stackId="a" fill="#f44336" name="High" />
          </BarChart>
        </ResponsiveContainer>
      </Paper>

      {/* Events Table */}
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Time</TableCell>
                <TableCell>Event Type</TableCell>
                <TableCell>Severity</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Details</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={5} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : (
                data?.events.map((event) => (
                  <TableRow key={event.id}>
                    <TableCell>
                      {format(new Date(event.created_at), 'yyyy-MM-dd HH:mm:ss')}
                    </TableCell>
                    <TableCell>{event.event_type}</TableCell>
                    <TableCell>
                      <Chip
                        label={event.severity.toUpperCase()}
                        color={severityColors[event.severity]}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{event.description}</TableCell>
                    <TableCell>
                      <pre style={{ margin: 0, fontSize: '0.8em' }}>
                        {JSON.stringify(event.event_metadata, null, 2)}
                      </pre>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          component="div"
          count={data?.total || 0}
          page={page}
          onPageChange={handleChangePage}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          rowsPerPageOptions={[5, 10, 25, 50]}
        />
      </Paper>
    </Box>
  );
};

export default SecurityEventsPage; 