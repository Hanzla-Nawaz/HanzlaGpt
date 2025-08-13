// Simple test script to verify proxy function
// Run this after deployment to test the proxy

const testProxy = async () => {
  const baseUrl = 'https://hanzlagpt11.vercel.app'; // Replace with your actual domain
  
  try {
    console.log('Testing proxy function...');
    
    // Test health endpoint
    const healthResponse = await fetch(`${baseUrl}/api/chat/health`);
    console.log('Health check status:', healthResponse.status);
    
    if (healthResponse.ok) {
      const healthData = await healthResponse.json();
      console.log('Health data:', healthData);
    }
    
    // Test greeting endpoint
    const greetingResponse = await fetch(`${baseUrl}/api/chat/greeting`);
    console.log('Greeting status:', greetingResponse.status);
    
    if (greetingResponse.ok) {
      const greetingData = await greetingResponse.json();
      console.log('Greeting data:', greetingData);
    }
    
  } catch (error) {
    console.error('Test failed:', error);
  }
};

// Run test if this file is executed directly
if (typeof window === 'undefined') {
  // Node.js environment
  const fetch = require('node-fetch');
  testProxy();
} else {
  // Browser environment
  testProxy();
}
