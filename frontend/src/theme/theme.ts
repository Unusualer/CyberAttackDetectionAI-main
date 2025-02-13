import { createTheme, alpha } from '@mui/material/styles';
import { PaletteMode } from '@mui/material';

declare module '@mui/material/styles' {
  interface BreakpointOverrides {
    xs: true;
    sm: true;
    md: true;
    lg: true;
    xl: true;
    '2xl': true;
  }
}

const getDesignTokens = (mode: PaletteMode) => ({
  breakpoints: {
    values: {
      xs: 0,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
      '2xl': 1536,
    },
  },
  palette: {
    mode,
    primary: {
      main: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#6366f1',
      light: '#818cf8',
      dark: '#4f46e5',
      contrastText: '#ffffff',
    },
    error: {
      main: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
      contrastText: '#ffffff',
    },
    warning: {
      main: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
      contrastText: '#ffffff',
    },
    info: {
      main: '#0ea5e9',
      light: '#38bdf8',
      dark: '#0284c7',
      contrastText: '#ffffff',
    },
    success: {
      main: '#10b981',
      light: '#34d399',
      dark: '#059669',
      contrastText: '#ffffff',
    },
    grey: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827',
    },
    ...(mode === 'light'
      ? {
          background: {
            default: '#f9fafb',
            paper: '#ffffff',
          },
          text: {
            primary: '#111827',
            secondary: '#4b5563',
            disabled: '#9ca3af',
          },
          divider: alpha('#000000', 0.12),
        }
      : {
          background: {
            default: '#0a0f18',
            paper: '#111827',
          },
          text: {
            primary: '#f9fafb',
            secondary: '#d1d5db',
            disabled: '#6b7280',
          },
          divider: alpha('#ffffff', 0.12),
        }),
  },
  typography: {
    fontFamily: '"Plus Jakarta Sans", sans-serif',
    fontWeightLight: 400,
    fontWeightRegular: 500,
    fontWeightMedium: 600,
    fontWeightBold: 700,
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.2,
    },
    h2: {
      fontWeight: 700,
      fontSize: '2rem',
      lineHeight: 1.2,
    },
    h3: {
      fontWeight: 700,
      fontSize: '1.75rem',
      lineHeight: 1.2,
    },
    h4: {
      fontWeight: 700,
      fontSize: '1.5rem',
      lineHeight: 1.2,
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.2,
    },
    h6: {
      fontWeight: 600,
      fontSize: '1rem',
      lineHeight: 1.2,
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 500,
      lineHeight: 1.5,
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: 1.57,
    },
    body1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: 1.5,
    },
    body2: {
      fontSize: '0.875rem',
      fontWeight: 400,
      lineHeight: 1.57,
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 600,
      lineHeight: 1.75,
      textTransform: 'none',
    },
    caption: {
      fontSize: '0.75rem',
      fontWeight: 400,
      lineHeight: 1.66,
    },
    overline: {
      fontSize: '0.75rem',
      fontWeight: 600,
      letterSpacing: '0.5px',
      lineHeight: 2.5,
      textTransform: 'uppercase',
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0px 1px 2px rgba(0, 0, 0, 0.06), 0px 1px 3px rgba(0, 0, 0, 0.1)',
    '0px 1px 5px rgba(0, 0, 0, 0.06), 0px 2px 4px rgba(0, 0, 0, 0.1)',
    '0px 2px 8px rgba(0, 0, 0, 0.06), 0px 4px 6px rgba(0, 0, 0, 0.1)',
    '0px 4px 12px rgba(0, 0, 0, 0.06), 0px 6px 8px rgba(0, 0, 0, 0.1)',
    '0px 6px 16px rgba(0, 0, 0, 0.06), 0px 8px 12px rgba(0, 0, 0, 0.1)',
    '0px 8px 24px rgba(0, 0, 0, 0.06), 0px 12px 16px rgba(0, 0, 0, 0.1)',
    '0px 12px 32px rgba(0, 0, 0, 0.06), 0px 16px 24px rgba(0, 0, 0, 0.1)',
    '0px 16px 48px rgba(0, 0, 0, 0.06), 0px 24px 32px rgba(0, 0, 0, 0.1)',
    '0px 24px 64px rgba(0, 0, 0, 0.06), 0px 32px 48px rgba(0, 0, 0, 0.1)',
  ],
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        '*': {
          boxSizing: 'border-box',
          margin: 0,
          padding: 0,
        },
        html: {
          MozOsxFontSmoothing: 'grayscale',
          WebkitFontSmoothing: 'antialiased',
          display: 'flex',
          flexDirection: 'column',
          minHeight: '100%',
          width: '100%',
        },
        body: {
          display: 'flex',
          flex: '1 1 auto',
          flexDirection: 'column',
          minHeight: '100%',
          width: '100%',
        },
        '#root': {
          display: 'flex',
          flex: '1 1 auto',
          flexDirection: 'column',
          height: '100%',
          width: '100%',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          '&:hover': {
            transform: 'translateY(-1px)',
            boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
          },
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: mode === 'dark'
            ? '0 0 24px rgba(0, 0, 0, 0.3)'
            : '0 2px 12px rgba(0, 0, 0, 0.04)',
          backgroundImage: 'none',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: mode === 'dark'
              ? '0 0 32px rgba(0, 0, 0, 0.4)'
              : '0 4px 16px rgba(0, 0, 0, 0.08)',
            transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
          },
        },
      },
    },
    MuiCardContent: {
      styleOverrides: {
        root: {
          padding: '32px 24px',
          '&:last-child': {
            paddingBottom: '32px',
          },
        },
      },
    },
    MuiCardHeader: {
      defaultProps: {
        titleTypographyProps: {
          variant: 'h6',
        },
        subheaderTypographyProps: {
          variant: 'body2',
        },
      },
      styleOverrides: {
        root: {
          padding: '32px 24px 16px',
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        input: {
          '&::placeholder': {
            opacity: 1,
            color: mode === 'dark' ? '#6b7280' : '#9ca3af',
          },
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          backgroundColor: mode === 'dark' ? alpha('#ffffff', 0.03) : '#ffffff',
          '&:hover': {
            backgroundColor: mode === 'dark' ? alpha('#ffffff', 0.05) : '#ffffff',
          },
          '&.Mui-focused': {
            backgroundColor: mode === 'dark' ? alpha('#ffffff', 0.05) : '#ffffff',
          },
        },
        notchedOutline: {
          borderColor: mode === 'dark' ? alpha('#ffffff', 0.12) : alpha('#000000', 0.12),
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: mode === 'dark' ? alpha('#ffffff', 0.03) : alpha('#000000', 0.02),
          '.MuiTableCell-root': {
            color: mode === 'dark' ? '#d1d5db' : '#4b5563',
            lineHeight: 1,
            fontSize: '0.75rem',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: 0.5,
          },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderBottom: `1px solid ${mode === 'dark' ? alpha('#ffffff', 0.12) : alpha('#000000', 0.12)}`,
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:last-child .MuiTableCell-root': {
            borderBottom: 0,
          },
          '&:hover': {
            backgroundColor: mode === 'dark' ? alpha('#ffffff', 0.02) : alpha('#000000', 0.01),
          },
        },
      },
    },
    MuiLink: {
      defaultProps: {
        underline: 'hover',
      },
    },
  },
});

export const darkTheme = createTheme(getDesignTokens('dark'));
export const lightTheme = createTheme(getDesignTokens('light')); 