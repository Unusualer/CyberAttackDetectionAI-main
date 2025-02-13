import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  Link,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import api from '../services/api';

const steps = ['Create Organization', 'Create Account'];

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register, isLoading } = useAuthStore();
  const [activeStep, setActiveStep] = useState(0);
  const [error, setError] = useState('');

  // Organization form state
  const [orgName, setOrgName] = useState('');
  
  // User form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [organizationId, setOrganizationId] = useState('');

  const handleCreateOrganization = async () => {
    try {
      const response = await api.post('/organizations/', {
        name: orgName,
        is_active: true,
      });
      setOrganizationId(response.data.id);
      setActiveStep(1);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create organization');
    }
  };

  const handleRegister = async () => {
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      await register({
        email,
        password,
        full_name: fullName,
        organization_id: organizationId,
      });
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to register');
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'background.default',
      }}
    >
      <Card sx={{ maxWidth: 600, width: '100%', mx: 2 }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Register
          </Typography>

          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {activeStep === 0 ? (
            // Organization Creation Form
            <Box>
              <TextField
                label="Organization Name"
                fullWidth
                margin="normal"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
                required
              />

              <Button
                variant="contained"
                fullWidth
                size="large"
                sx={{ mt: 3 }}
                onClick={handleCreateOrganization}
                disabled={!orgName || isLoading}
              >
                {isLoading ? 'Creating...' : 'Create Organization'}
              </Button>
            </Box>
          ) : (
            // User Registration Form
            <Box>
              <TextField
                label="Full Name"
                fullWidth
                margin="normal"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />

              <TextField
                label="Email"
                type="email"
                fullWidth
                margin="normal"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <TextField
                label="Password"
                type="password"
                fullWidth
                margin="normal"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />

              <TextField
                label="Confirm Password"
                type="password"
                fullWidth
                margin="normal"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />

              <Button
                variant="contained"
                fullWidth
                size="large"
                sx={{ mt: 3 }}
                onClick={handleRegister}
                disabled={isLoading}
              >
                {isLoading ? 'Registering...' : 'Complete Registration'}
              </Button>
            </Box>
          )}

          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2">
              Already have an account?{' '}
              <Link component={RouterLink} to="/login">
                Login here
              </Link>
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default RegisterPage; 