#!/usr/bin/env python3
"""
AWS Credentials Setup Script
Helps configure AWS credentials as environment variables
"""

import os
import sys
import subprocess
import getpass

def check_existing_credentials():
    """Check if AWS credentials are already configured"""
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_DEFAULT_REGION')
    
    if access_key and secret_key:
        print("✅ AWS credentials found in environment variables:")
        print(f"   Access Key: {access_key[:8]}...")
        print(f"   Secret Key: {'*' * 8}...")
        print(f"   Region: {region or 'Not set (will use eu-central-1)'}")
        return True
    
    return False

def setup_environment_variables():
    """Interactive setup of AWS credentials as environment variables"""
    print("\n🔧 Setting up AWS credentials as environment variables...")
    print("You can get these from: https://console.aws.amazon.com/iam/")
    print("Go to Users → Your User → Security credentials → Create access key")
    
    try:
        access_key = input("\nEnter AWS Access Key ID: ").strip()
        if not access_key:
            print("❌ Access Key ID is required")
            return False
        
        secret_key = getpass.getpass("Enter AWS Secret Access Key: ").strip()
        if not secret_key:
            print("❌ Secret Access Key is required")
            return False
        
        region = input("Enter AWS Region (default: eu-central-1): ").strip()
        if not region:
            region = 'eu-central-1'
        
        # Set environment variables for current session
        os.environ['AWS_ACCESS_KEY_ID'] = access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
        os.environ['AWS_DEFAULT_REGION'] = region
        
        print("\n✅ Environment variables set for current session")
        print("To make them permanent, add these to your system environment:")
        print(f"   AWS_ACCESS_KEY_ID={access_key}")
        print(f"   AWS_SECRET_ACCESS_KEY={secret_key}")
        print(f"   AWS_DEFAULT_REGION={region}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_credentials():
    """Test if the credentials work"""
    try:
        import boto3
        print("\n🧪 Testing AWS credentials...")
        
        sts = boto3.client('sts')
        response = sts.get_caller_identity()
        
        print("✅ Credentials are valid!")
        print(f"   Account: {response.get('Account', 'Unknown')}")
        print(f"   User ID: {response.get('UserId', 'Unknown')}")
        print(f"   ARN: {response.get('Arn', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Credential test failed: {e}")
        return False

def create_env_file():
    """Create a .env file for easy loading"""
    try:
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region = os.getenv('AWS_DEFAULT_REGION', 'eu-central-1')
        
        if not access_key or not secret_key:
            print("❌ No credentials found to save")
            return False
        
        env_content = f"""# AWS Credentials for Starshield Network Monitor
AWS_ACCESS_KEY_ID={access_key}
AWS_SECRET_ACCESS_KEY={secret_key}
AWS_DEFAULT_REGION={region}
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env file with your credentials")
        print("⚠️  Remember to add .env to your .gitignore file!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def main():
    """Main function"""
    print("🔐 AWS Credentials Setup for Starshield Network Monitor")
    print("=" * 60)
    
    # Check if credentials already exist
    if check_existing_credentials():
        choice = input("\nDo you want to update them? (y/N): ").strip().lower()
        if choice != 'y':
            print("Using existing credentials...")
            if test_credentials():
                print("\n✅ Ready to use AWS scripts!")
            return
    
    # Setup new credentials
    if setup_environment_variables():
        if test_credentials():
            print("\n🎉 AWS credentials are working!")
            
            # Ask if they want to create .env file
            choice = input("\nCreate .env file for easy loading? (y/N): ").strip().lower()
            if choice == 'y':
                create_env_file()
            
            print("\n✅ You can now run:")
            print("   python scripts/create_iperf3_server.py")
            print("   python scripts/cleanup_iperf3_server.py")
        else:
            print("\n❌ Credentials are not working. Please check your keys.")
    else:
        print("\n❌ Setup failed. Please try again.")

if __name__ == "__main__":
    main()
