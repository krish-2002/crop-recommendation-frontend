import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ErrorBoundary from './components/ErrorBoundary';
import styled from 'styled-components';

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: #f5f5f5;
`;

const App = () => {
  return (
    <ErrorBoundary>
      <Router>
        <AppContainer>
          <Routes>
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </AppContainer>
      </Router>
    </ErrorBoundary>
  );
};

export default App; 