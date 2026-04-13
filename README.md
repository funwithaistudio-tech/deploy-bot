# deploy-bot
The most atomic GitOps deploy bot. One file, one job.

## What it does
Watches a GitHub repo branch. On successful push → deploys to Vercel.
No YAML configs. No CI/CD files. Just this one Python script.

## Setup
```bash
pip install requests ghapi
python deploy_bot.py --repo owner/repo --branch main
```

## How it works
The deploy-bot monitors GitHub repositories for successful workflow runs. When a push to a monitored branch completes successfully, it automatically triggers a deployment to Vercel.

Deployment behavior:
- Push to `main` branch → Production deployment
- Push to `preview/*` branches → Preview deployment
- Other branches → Preview deployment

The bot polls GitHub Actions API to detect successful workflow runs and triggers Vercel deployments accordingly.

## Real example
```bash
$ python deploy_bot.py --repo my-user/my-site --branch main
Watching my-user/my-site:main ...
✓ Push detected on main
✓ Waiting for Vercel deploy...
✓ Deployed: https://my-site-xyz.vercel.app
```

## Configuration

You can provide a Vercel token either via:
1. Command line argument: `--vercel-token YOUR_TOKEN`
2. Environment variable: `VERCEL_TOKEN=YOUR_TOKEN`

If no token is provided, the bot runs in demo mode.