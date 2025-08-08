// Example of how to display provider information in your frontend
// Add this to your chat interface to show which provider is being used

function displayProviderInfo(response) {
    const provider = response.provider;
    const responseTime = response.response_time_ms;
    
    let providerInfo = "";
    
    if (provider.includes("OpenAI")) {
        providerInfo = "🤖 OpenAI API";
    } else if (provider.includes("HuggingFace")) {
        providerInfo = "🤗 HuggingFace API";
    } else if (provider.includes("Ollama")) {
        providerInfo = "🦙 Ollama Local";
    } else if (provider.includes("Intent-based")) {
        providerInfo = "📝 Pre-defined Response";
    } else {
        providerInfo = "❓ Unknown Provider";
    }
    
    // Display in your chat interface
    console.log(`Provider: ${providerInfo}`);
    console.log(`Response Time: ${responseTime}ms`);
    
    return providerInfo;
}

// Example usage in your chat function:
async function sendMessage(message) {
    try {
        const response = await fetch('/api/chat/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: 'web_user',
                session_id: 'web_session',
                query: message
            })
        });
        
        const data = await response.json();
        
        // Display the message
        displayMessage(data.response);
        
        // Display provider info
        const providerInfo = displayProviderInfo(data);
        displayProviderBadge(providerInfo, data.response_time_ms);
        
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayProviderBadge(provider, responseTime) {
    // Create a small badge showing the provider
    const badge = document.createElement('div');
    badge.className = 'provider-badge';
    badge.innerHTML = `
        <span class="provider-name">${provider}</span>
        <span class="response-time">${responseTime}ms</span>
    `;
    
    // Add to your chat interface
    document.querySelector('.chat-container').appendChild(badge);
}
