# ▲ Deploy Frontend to Vercel

Deploy your Next.js frontend to Vercel with zero configuration.

---

## Prerequisites

- GitHub account with your code pushed
- [Vercel account](https://vercel.com/) (free tier available)
- Backend already deployed (Render/Railway)

---

## Step 1: Import Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New → Project**
3. Import your GitHub repository
4. Configure:

| Setting              | Value           |
| -------------------- | --------------- |
| **Framework Preset** | Next.js         |
| **Root Directory**   | `frontend`      |
| **Build Command**    | `npm run build` |
| **Output Directory** | `.next`         |

---

## Step 2: Set Environment Variables

Before deploying, add environment variables:

| Variable              | Value                                    |
| --------------------- | ---------------------------------------- |
| `NEXT_PUBLIC_API_URL` | `https://your-backend.onrender.com/api/` |

> Replace with your actual backend URL from Render/Railway

---

## Step 3: Deploy

1. Click **Deploy**
2. Wait for build to complete (~1-2 minutes)
3. Your app is live at `https://your-app.vercel.app`

---

## Step 4: Update Backend CORS

Add your Vercel domain to Django's allowed origins.

In `backend/chatbot_project/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-app.vercel.app",
]

# Or allow all Vercel preview deployments
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
]
```

Redeploy your backend after this change.

---

## Custom Domain (Optional)

1. Go to your project **Settings → Domains**
2. Add your custom domain
3. Configure DNS:
   - Add CNAME record pointing to `cname.vercel-dns.com`
   - Or use Vercel nameservers

---

## Automatic Deployments

Vercel automatically deploys when you:

- Push to `main` branch → Production deploy
- Open a PR → Preview deploy with unique URL

---

## Environment Variables per Environment

You can set different values for:

- **Production** - `main` branch
- **Preview** - PR deployments
- **Development** - Local only

In Vercel dashboard:

1. Go to **Settings → Environment Variables**
2. Select environment when adding variable

---

## Build Optimization

### Enable caching

Vercel caches `node_modules` automatically. For faster builds, add to `frontend/package.json`:

```json
{
  "scripts": {
    "build": "next build"
  }
}
```

### Ignore lint errors during build (if needed)

In `frontend/next.config.js`:

```javascript
module.exports = {
  eslint: {
    ignoreDuringBuilds: true,
  },
};
```

---

## Troubleshooting

### Build fails with "Module not found"

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
git add package-lock.json
git commit -m "Update lock file"
git push
```

### API calls failing (CORS)

1. Check backend is running
2. Verify `NEXT_PUBLIC_API_URL` is correct
3. Update Django `CORS_ALLOWED_ORIGINS`

### 404 on page refresh

Add to `frontend/next.config.js`:

```javascript
module.exports = {
  trailingSlash: true,
};
```

### Environment variables not working

- Must start with `NEXT_PUBLIC_` for client-side access
- Redeploy after changing variables

---

## Cost

| Resource             | Free Tier          |
| -------------------- | ------------------ |
| Bandwidth            | 100GB/month        |
| Builds               | 6000 minutes/month |
| Serverless Functions | 100GB-hours        |
| Deployments          | Unlimited          |

> 💡 Free tier is very generous for most projects!

---

## Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel
- [ ] Backend CORS includes Vercel domain
- [ ] Tested login/chat functionality
- [ ] Custom domain configured (optional)
