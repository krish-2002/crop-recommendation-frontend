import { render, screen, waitFor } from '@testing-library/react';
import Dashboard from '../Dashboard';
import axios from 'axios';

// Mock axios
jest.mock('axios');

describe('Dashboard Component', () => {
  beforeEach(() => {
    // Mock successful API responses
    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:5000/api/sensor-data') {
        return Promise.resolve({
          data: [
            {
              temperature: 25.5,
              humidity: 60.0,
              moisture: 500,
              ph: 6.5,
              timestamp: '2024-03-15T12:00:00Z'
            }
          ]
        });
      }
      if (url === 'http://localhost:5000/api/system-status') {
        return Promise.resolve({
          data: {
            status: 'online',
            message: 'System is functioning normally',
            sensor_status: {
              temperature: 25.5,
              humidity: 60.0,
              moisture: 500,
              ph: 6.5
            }
          }
        });
      }
      return Promise.reject(new Error('Not found'));
    });
  });

  test('renders dashboard title', () => {
    render(<Dashboard />);
    expect(screen.getByText('Crop Recommendation System Dashboard')).toBeInTheDocument();
  });

  test('displays system status', async () => {
    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText('System Status')).toBeInTheDocument();
      expect(screen.getByText('Status: online')).toBeInTheDocument();
    });
  });

  test('displays farmer input form', () => {
    render(<Dashboard />);
    expect(screen.getByText('Enter Farm Details')).toBeInTheDocument();
    expect(screen.getByLabelText('Soil Type:')).toBeInTheDocument();
    expect(screen.getByLabelText('Weather Condition:')).toBeInTheDocument();
    expect(screen.getByLabelText('Region:')).toBeInTheDocument();
  });
}); 