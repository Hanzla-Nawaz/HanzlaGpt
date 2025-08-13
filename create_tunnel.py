#!/usr/bin/env python3
"""
Simple script to create ngrok tunnel for HanzlaGPT backend
"""

import time
from pyngrok import ngrok

def create_tunnel():
    print("🚀 Creating ngrok tunnel for HanzlaGPT backend...")
    print("=" * 50)
    
    try:
        # Create tunnel to localhost:8000
        tunnel = ngrok.connect(8000)
        
        print(f"✅ Tunnel created successfully!")
        print(f"🌐 Public URL: {tunnel.public_url}")
        print(f"🔗 Local URL: {tunnel.local_url}")
        print()
        print("📋 Next steps:")
        print("1. Copy the Public URL above")
        print("2. Go to Vercel Dashboard")
        print("3. Set BACKEND_URL = [Public URL]")
        print("4. Redeploy Vercel with cache clear")
        print()
        print("⚠️  Keep this script running to maintain the tunnel")
        print("Press Ctrl+C to stop the tunnel")
        print("=" * 50)
        
        # Keep tunnel alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping tunnel...")
        ngrok.kill()
        print("✅ Tunnel stopped")
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        print("💡 Make sure your backend is running on port 8000")

if __name__ == "__main__":
    create_tunnel()