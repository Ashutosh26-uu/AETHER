import { useEffect, useState } from 'react';

const AutoBackendStarter = ({ onBackendReady }) => {
  const [backendStatus, setBackendStatus] = useState('checking');
  const [attempts, setAttempts] = useState(0);

  const checkBackend = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/dynamic/device-info', {
        method: 'GET',
        timeout: 5000
      });
      
      if (response.ok) {
        setBackendStatus('ready');
        onBackendReady(true);
        return true;
      }
    } catch (error) {
      console.log('Backend not ready, attempt:', attempts + 1);
    }
    return false;
  };

  const startBackend = async () => {
    try {
      // Try to start backend via API call to a startup endpoint
      await fetch('http://localhost:8000/startup', { method: 'POST' });
    } catch (error) {
      console.log('Could not auto-start backend');
    }
  };

  useEffect(() => {
    const initBackend = async () => {
      setBackendStatus('checking');
      
      // First check if backend is already running
      const isReady = await checkBackend();
      if (isReady) return;

      // Try to start backend
      setBackendStatus('starting');
      await startBackend();

      // Keep checking until backend is ready
      const maxAttempts = 30; // 30 seconds
      let currentAttempts = 0;

      const checkInterval = setInterval(async () => {
        currentAttempts++;
        setAttempts(currentAttempts);

        const ready = await checkBackend();
        if (ready) {
          clearInterval(checkInterval);
          return;
        }

        if (currentAttempts >= maxAttempts) {
          setBackendStatus('failed');
          clearInterval(checkInterval);
          onBackendReady(false);
        }
      }, 1000);
    };

    initBackend();
  }, []);

  if (backendStatus === 'ready') {
    return null; // Backend is ready, don't show anything
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      color: 'white',
      zIndex: 9999,
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{ 
        textAlign: 'center', 
        maxWidth: '600px', 
        padding: '30px',
        background: 'rgba(255,255,255,0.1)',
        borderRadius: '20px',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255,255,255,0.2)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
      }}>
        <h1 style={{ 
          fontSize: '3em', 
          marginBottom: '20px',
          textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
          background: 'linear-gradient(45deg, #fff, #e0e7ff)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>🌐 AETHER System</h1>
        
        {backendStatus === 'checking' && (
          <>
            <div style={{ 
              fontSize: '4em', 
              marginBottom: '20px',
              animation: 'pulse 2s infinite'
            }}>🔍</div>
            <h2 style={{ fontSize: '1.8em', marginBottom: '15px' }}>Checking Backend Status...</h2>
            <p style={{ fontSize: '1.1em', opacity: 0.9 }}>Verifying if the backend server is running</p>
            <div style={{
              marginTop: '20px',
              display: 'flex',
              justifyContent: 'center',
              gap: '5px'
            }}>
              {[0, 1, 2].map(i => (
                <div key={i} style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: '#fff',
                  animation: `pulse 1.5s infinite ${i * 0.2}s`
                }}></div>
              ))}
            </div>
          </>
        )}
        
        {backendStatus === 'starting' && (
          <>
            <div style={{ 
              fontSize: '4em', 
              marginBottom: '20px',
              animation: 'spin 2s linear infinite'
            }}>🚀</div>
            <h2 style={{ fontSize: '1.8em', marginBottom: '15px' }}>Starting Backend Server...</h2>
            <p style={{ fontSize: '1.1em', opacity: 0.9, marginBottom: '10px' }}>Initializing AETHER backend services</p>
            <p style={{ fontSize: '1em', opacity: 0.8, marginBottom: '20px' }}>Attempt: {attempts}/30</p>
            <div style={{
              width: '350px',
              height: '8px',
              backgroundColor: 'rgba(255,255,255,0.2)',
              borderRadius: '4px',
              margin: '20px auto',
              overflow: 'hidden',
              border: '1px solid rgba(255,255,255,0.1)'
            }}>
              <div style={{
                width: `${(attempts / 30) * 100}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #10B981, #059669)',
                borderRadius: '4px',
                transition: 'width 0.3s ease',
                boxShadow: '0 0 10px rgba(16, 185, 129, 0.5)'
              }}></div>
            </div>
            <div style={{
              fontSize: '0.9em',
              opacity: 0.7,
              marginTop: '15px'
            }}>
              {attempts < 10 ? '⚡ Initializing...' : 
               attempts < 20 ? '🔧 Configuring services...' : 
               '🔄 Finalizing setup...'}
            </div>
          </>
        )}
        
        {backendStatus === 'failed' && (
          <>
            <div style={{ 
              fontSize: '4em', 
              marginBottom: '20px',
              animation: 'pulse 2s infinite'
            }}>❌</div>
            <h2 style={{ fontSize: '1.8em', marginBottom: '15px', color: '#FCA5A5' }}>Backend Connection Failed</h2>
            <p style={{ fontSize: '1.1em', marginBottom: '10px' }}>Could not connect to the backend server.</p>
            <p style={{ fontSize: '1em', opacity: 0.9, marginBottom: '20px' }}>Please start the backend manually:</p>
            <div style={{
              background: 'rgba(0,0,0,0.3)',
              padding: '20px',
              borderRadius: '12px',
              marginTop: '20px',
              fontFamily: 'Consolas, monospace',
              fontSize: '1em',
              border: '1px solid rgba(255,255,255,0.2)',
              textAlign: 'left'
            }}>
              <div style={{ color: '#10B981', marginBottom: '5px' }}>$ cd backend</div>
              <div style={{ color: '#3B82F6' }}>$ python universal_backend.py</div>
            </div>
            <button
              onClick={() => window.location.reload()}
              style={{
                marginTop: '25px',
                padding: '12px 25px',
                background: 'linear-gradient(45deg, #3B82F6, #1D4ED8)',
                color: 'white',
                border: 'none',
                borderRadius: '25px',
                cursor: 'pointer',
                fontSize: '1.1em',
                fontWeight: 'bold',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(59, 130, 246, 0.3)'
              }}
              onMouseOver={(e) => {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 6px 20px rgba(59, 130, 246, 0.4)';
              }}
              onMouseOut={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 4px 15px rgba(59, 130, 246, 0.3)';
              }}
            >
              🔄 Retry Connection
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default AutoBackendStarter;