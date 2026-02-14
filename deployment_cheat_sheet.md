# Docker Deployment Commands for PhD Management System

## Prerequisites
Ensure you are in your `frappe_docker` directory:
```bash
cd ~/frappe_docker
```

## 1. Check Service Name
Run this to see your running containers:
```bash
docker compose ps
```
*Look for a service named `backend` (or sometimes `frappe-python` or `frappe`). The commands below assume `backend`. If yours is different, replace `backend` with your service name.*

## 2. Get the App
Download the app into your Docker container:
```bash
docker compose exec backend bench get-app phd_management https://github.com/Aravinda-05/phd-lifecycle-system
```

## 3. Install the App on Your Site
Install it on your specific site (replace `[your-site-name]`, e.g., `site1.local`):
```bash
docker compose exec backend bench --site [your-site-name] install-app phd_management
```

## 4. Verify Installation
Check if the app is listed:
```bash
docker compose exec backend bench --site [your-site-name] list-apps
```

## 5. View the App
Go to: [http://localhost:8000](http://localhost:8000)
