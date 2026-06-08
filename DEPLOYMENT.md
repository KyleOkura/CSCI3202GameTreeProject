# Deployment Guide - Mancala Solver Web Version

This guide will help you deploy the Mancala Solver as a live web application on your personal website.

## Table of Contents
- [Quick Start (Local)](#quick-start-local)
- [Deployment Options](#deployment-options)
- [Option 1: Heroku (Recommended - Free)](#option-1-heroku-recommended---free)
- [Option 2: PythonAnywhere](#option-2-pythonanywhere)
- [Option 3: Your Own Server](#option-3-your-own-server)
- [Production Considerations](#production-considerations)

## Quick Start (Local)

Before deploying, test the app locally:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Flask App
```bash
python app.py
```

### 3. Open in Browser
Navigate to: `http://localhost:5000`

## Deployment Options

### Option 1: Heroku (Recommended - Free)

Heroku allows you to deploy Python apps for free with easy setup and automatic updates.

#### Setup Steps:

1. **Create a Heroku Account**
   - Go to https://www.heroku.com
   - Sign up for a free account
   - Verify your email

2. **Install Heroku CLI**
   - Download from: https://devcenter.heroku.com/articles/heroku-cli
   - Install for your operating system

3. **Create Procfile**
   Create a file named `Procfile` (no extension) in your project root:
   ```
   web: gunicorn app:app
   ```

4. **Create Runtime File (Optional)**
   Create `runtime.txt` to specify Python version:
   ```
   python-3.11.4
   ```

5. **Update requirements.txt**
   Add gunicorn:
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

6. **Login to Heroku**
   ```bash
   heroku login
   ```

7. **Create Heroku App**
   ```bash
   heroku create your-mancala-app
   ```

8. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

9. **Open Your App**
   ```bash
   heroku open
   ```

Your app will be live at: `https://your-mancala-app.herokuapp.com`

#### Advantages:
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Automatic SSL/HTTPS
- ✅ Custom domain support
- ✅ Automatic restarts

#### Limitations:
- Free tier sleeps after 30 minutes of inactivity
- Limited to 550 compute hours/month
- 1GB RAM available

---

### Option 2: PythonAnywhere

PythonAnywhere is a Python-specific hosting platform.

#### Setup Steps:

1. **Create Account**
   - Go to https://www.pythonanywhere.com
   - Sign up (free tier available)

2. **Create Web App**
   - Click "Web" in the menu
   - Add new web app
   - Choose Python 3.11
   - Choose Flask framework
   - Use path: `/home/your_username/mancala`

3. **Upload Files**
   - Use the file browser to upload your files to `/home/your_username/`
   - Extract the zip if needed

4. **Configure WSGI**
   - Go to Web tab
   - Edit WSGI file at `/var/www/your_username_pythonanywhere_com_wsgi.py`
   - Replace with:
   ```python
   import sys
   path = '/home/your_username/mancala'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```

5. **Install Requirements**
   - Go to Web tab
   - Click "Add a new web app"
   - In the bash console:
   ```bash
   cd /home/your_username/mancala
   pip install -r requirements.txt
   ```

6. **Reload Your App**
   - Go to Web tab
   - Click "Reload"

Your app will be live at: `https://your_username.pythonanywhere.com`

#### Advantages:
- ✅ Beginner-friendly
- ✅ Always running (no sleep)
- ✅ Free tier available
- ✅ Easy file management

#### Limitations:
- Free tier has storage limits
- Limited CPU/bandwidth
- Fewer customization options

---

### Option 3: Your Own Server

Deploy on a server you control (AWS, DigitalOcean, Linode, etc.).

#### Using DigitalOcean (Example):

1. **Create Droplet**
   - Create a new Ubuntu 22.04 droplet ($5-6/month)
   - SSH into your droplet

2. **Install Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-venv git nginx
   ```

3. **Clone Your Project**
   ```bash
   git clone <your-repo-url> /var/www/mancala
   cd /var/www/mancala
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Configure Gunicorn**
   Create `/var/www/mancala/gunicorn_config.py`:
   ```python
   import multiprocessing
   bind = "127.0.0.1:8000"
   workers = multiprocessing.cpu_count() * 2 + 1
   worker_class = "sync"
   ```

6. **Create Systemd Service**
   Create `/etc/systemd/system/mancala.service`:
   ```ini
   [Unit]
   Description=Mancala Solver
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/mancala
   ExecStart=/var/www/mancala/venv/bin/gunicorn -c gunicorn_config.py app:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Enable Service**
   ```bash
   sudo systemctl enable mancala
   sudo systemctl start mancala
   ```

8. **Configure Nginx**
   Create `/etc/nginx/sites-available/mancala`:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /var/www/mancala/static;
       }
   }
   ```

9. **Enable Nginx**
   ```bash
   sudo ln -s /etc/nginx/sites-available/mancala /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. **Get SSL Certificate (Let's Encrypt)**
    ```bash
    sudo apt-get install certbot python3-certbot-nginx
    sudo certbot --nginx -d your_domain.com
    ```

#### Advantages:
- ✅ Full control
- ✅ No limitations
- ✅ Good performance
- ✅ Always running

#### Limitations:
- ❌ Monthly costs
- ❌ You maintain the server
- ❌ Need technical knowledge

---

## Embedding in Your Website

To embed the Mancala game in an existing website:

### Option A: Iframe Embed
```html
<iframe 
  src="https://your-mancala-app.herokuapp.com" 
  width="100%" 
  height="900"
  frameborder="0"
  style="border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
</iframe>
```

### Option B: Subdomain
Point a subdomain of your website to your Heroku/server app:
- Create DNS record: `mancala.yourwebsite.com` → `your-app.herokuapp.com`
- Users visit: `https://mancala.yourwebsite.com`

### Option C: Custom Domain (Recommended)
1. On Heroku: Add custom domain in app settings
2. On your domain registrar: Add CNAME record
3. Configure in Heroku to use your custom domain

---

## Production Considerations

### Security
1. **Change Secret Key**
   - Update `app.secret_key` in `app.py` to a random string
   - Generate with: `python -c "import os; print(os.urandom(24))"`

2. **Enable Debug Mode Only in Development**
   - Set `debug=False` in `app.py` for production
   - Current: `app.run(debug=True, host='0.0.0.0', port=5000)`
   - Should be: `app.run(debug=False)` when using gunicorn

3. **Use Environment Variables**
   ```python
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
   DEBUG = os.environ.get('DEBUG', 'False') == 'True'
   ```

### Performance
1. **Add Caching** (Optional)
   - For production, consider caching game states
   - Use Redis for better performance

2. **Optimize AI Depth**
   - Default depth 5 works well
   - Higher depth = slower response
   - Lower depth = faster but less intelligent

3. **Monitor Performance**
   - Use Heroku logs: `heroku logs --tail`
   - Monitor response times
   - Add error tracking (Sentry integration)

### Maintenance
1. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

2. **Monitor Uptime**
   - Use uptime monitoring services
   - Get alerts if app goes down

3. **Backup**
   - Regular backups of code on GitHub
   - Game state is temporary (no database needed currently)

---

## Troubleshooting

### App shows "Application Error" on Heroku
```bash
# Check logs
heroku logs --tail

# Restart app
heroku restart
```

### Port already in use locally
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### AI moves are very slow
- Reduce depth value in UI
- Current default (5) should be fast enough
- If response time > 10 seconds, reduce to depth 3-4

### Game state not saving
- This is expected (stateless design)
- Each game is independent
- Restart fresh by creating new game

---

## Cost Comparison

| Platform | Cost | Performance | Ease |
|----------|------|-------------|------|
| Heroku | Free/7/50$/mo | Good | ⭐⭐⭐⭐⭐ |
| PythonAnywhere | Free/5-15/mo | Good | ⭐⭐⭐⭐ |
| DigitalOcean | 5-12/mo | Excellent | ⭐⭐⭐ |
| AWS | Variable | Excellent | ⭐⭐ |

---

## Next Steps

1. Choose your deployment platform
2. Follow the specific setup guide above
3. Test the deployed app thoroughly
4. Share your live Mancala game with others!

For questions or issues, refer to the platform-specific documentation:
- [Heroku Docs](https://devcenter.heroku.com/)
- [PythonAnywhere Docs](https://help.pythonanywhere.com/)
- [DigitalOcean Docs](https://www.digitalocean.com/docs/)

Happy deploying! 🚀
