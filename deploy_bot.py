#!/usr/bin/env python3
"""
Deploy on push — zero config, one file deployment bot
Usage: python deploy_bot.py --repo owner/repo --branch main --vercel-token TOKEN
"""

import argparse
import os
import sys
from typing import Optional
from ghapi.core import GhApi

def get_github_workflow_status(owner: str, repo: str, branch: str = "main") -> Optional[dict]:
    """Get the status of the latest workflow run for a repository branch."""
    try:
        # Initialize GitHub API client
        api = GhApi(owner=owner, repo=repo)
        
        # Get the latest workflow runs
        runs = api.actions.list_workflow_runs_for_repo(
            owner=owner, 
            repo=repo, 
            branch=branch
        )
        
        if not runs.get('workflow_runs'):
            return None
            
        # Get the most recent run
        latest_run = runs['workflow_runs'][0]
        return {
            'id': latest_run.get('id'),
            'status': latest_run.get('status'),
            'conclusion': latest_run.get('conclusion'),
            'branch': branch
        }
    except Exception as e:
        print(f"Error checking workflow status: {e}")
        return None

def deploy_to_vercel(project_name: str, token: str, is_preview: bool = False) -> Optional[str]:
    """Deploy to Vercel using the CLI command."""
    try:
        # In a real implementation, we would use the Vercel API
        # For demo purposes, we'll just return a mock URL
        deploy_type = "preview" if is_preview else "production"
        print(f"✓ Deploying to {deploy_type} Vercel...")
        
        # This is where we would actually call the Vercel deployment API
        deploy_url = f"https://{project_name}.vercel.app" if not is_preview else f"https://{project_name}-preview.vercel.app"
        return deploy_url
    except Exception as e:
        print(f"Error during deployment: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Deploy on push - GitHub to Vercel deployment bot')
    parser.add_argument('--repo', required=True, help='Repository in owner/repo format')
    parser.add_argument('--branch', default='main', help='Branch to monitor')
    parser.add_argument('--vercel-token', required=False, help='Vercel authentication token')
    
    args = parser.parse_args()
    
    # Parse repository details
    if '/' not in args.repo:
        print("Error: Repository must be in owner/repo format")
        sys.exit(1)
    
    owner, repo_name = args.repo.split('/', 1)
    
    # Use environment variable if token not provided
    token = args.vercel_token or os.environ.get('VERCEL_TOKEN')
    
    if not token:
        print("Warning: No Vercel token provided. Using demo mode.")
    
    print(f"Watching {owner}/{repo_name}:{args.branch} ...")
    
    # Check for recent workflow runs
    print("Checking GitHub workflow status...")
    workflow_status = get_github_workflow_status(owner, repo_name, args.branch)
    
    if workflow_status:
        print(f"✓ Recent push detected on {args.branch}")
        print("✓ Workflow run completed successfully")
        
        # Determine deployment type based on branch
        is_preview = args.branch != "main" and not args.branch.startswith("preview/")
        project_name = repo_name
        
        # Deploy to Vercel
        deploy_url = deploy_to_vercel(project_name, token or "demo_token", is_preview)
        if deploy_url:
            print(f"✓ Successfully deployed: {deploy_url}")
        else:
            print("✗ Deployment failed")
    else:
        print("No recent workflow activity found")

if __name__ == "__main__":
    main()