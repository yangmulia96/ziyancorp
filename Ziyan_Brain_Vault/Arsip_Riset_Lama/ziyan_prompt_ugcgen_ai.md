# Prompt: Build UGCGen AI (AI UGC Video Generator)

Act as a Senior Full-Stack Developer and SaaS Architect. Build a complete, production-ready AI UGC Video Generator web application called "UGCGen AI".

### Tech Stack:
- Frontend: Next.js (App Router), Tailwind CSS, Shadcn UI, Lucide Icons.
- Backend: Next.js Server Actions / API Routes.
- Database & Auth: Supabase (PostgreSQL + Auth).
- Payment/Credits: Integration placeholder for Midtrans/Stripe with a credit-based system.
- AI Video Generation: Placeholder API integration for AI Avatars (e.g., HeyGen API structure) and Text-to-Speech (ElevenLabs).

### Core Features & Requirements:
1. Landing Page:
   - Modern, high-converting SaaS landing page with Hero section, feature highlights, pricing plans (Free credits, Pro, Enterprise), and customer testimonials.

2. User Dashboard:
   - Sidebar navigation: Dashboard, Create Video, My Videos, Billing/Credits, Settings.
   - Credit counter widget at the top right.

3. Video Generation Wizard (Multi-step Form):
   - Step 1: Input Product URL or direct Script text.
   - Step 2: Select AI Avatar (grid of virtual human models with previews).
   - Step 3: Select Voice/Accent and Background music/style.
   - Step 4: Click "Generate" -> Triggers loading state ("Rendering your UGC video... This may take 2-3 minutes").

4. My Videos (Result Page):
   - Grid or table view of generated videos with status indicators (Processing, Completed, Failed).
   - Action buttons: Preview modal, Download MP4, Share link.

5. Database Schema Structure:
   - Users table (id, email, credits_balance, subscription_tier)
   - Videos table (id, user_id, script_text, avatar_id, status, video_url, created_at)

Write clean, modular code, implement robust error handling, and ensure the UI is fully responsive and modern.
