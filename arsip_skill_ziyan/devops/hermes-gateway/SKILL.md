---
name: hermes-gateway
description: Hermes Gateway config and troubleshooting for platforms.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, gateway, configuration, troubleshooting, provider, telegram, discord, setup]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [hermes-agent]
---

# Hermes Gateway: Configuration and Troubleshooting

Hermes Gateway is the core daemon that manages Hermes Agent's connections to messaging platforms (Telegram, Discord, etc.) and handles all inbound/outbound message routing. This skill covers common configuration issues, provider authentication problems, and practical troubleshooting workflows.

## Quick Reference

### Most Common Fixes

**Provider Authentication Failed → Switch to OpenRouter:**
```bash
# Change provider configuration
hermes config set model.provider openrouter
hermes config set model.base_url https://openrouter.ai/api/v1

# Restart gateway to apply changes
taskkill /f /im hermes_gateway.exe
hermes gateway start
```

**Telegram Integration Setup:**
```bash
# Ensure Telegram token exists in .env
echo "TELEGRAM_BOT_TOKEN=***" >> ~/.hermes/.env

# Configure allowed chats (user ID for DMs)
hermes config set --force telegram.allowed_chats 7349146540

# Restart gateway
hermes gateway restart
```

**Discord Integration Setup:**
```bash
# Configure Discord channel
hermes config set --force DISCORD_HOME_CHANNEL 1536996002463219802

# Restart gateway
hermes gateway restart
```

### Common Error Patterns & Solutions

**1. "Provider authentication failed. Check the configured credentials"
**Cause**: Gateway using invalid or missing provider configuration
**Solution**: Switch to OpenRouter with proper API key from `.env` file

**2. "Unauthorized user" on Telegram
**Cause**: User ID not in `telegram.allowed_chats` or pairing not approved
**Solution**: Add user ID to allowed chats and approve pairing code

**3. "No such table: tasks" in kanban dispatcher
**Cause**: Stale session database with missing schema
**Solution**: Delete problematic session IDs and restart gateway

**4. Gateway refuses restart from within Hermes
**Cause**: Security restrictions prevent gateway from stopping itself
**Solution**: Kill process from external terminal, then start again

## Configuration Commands

### Provider Management
```bash
# List current model configuration
hermes config get model

# Switch to OpenRouter (recommended)
hermes config set model.provider openrouter
hermes config set model.default "openrouter/deepseek/deepseek-chat"
hermes config set model.base_url "https://openrouter.ai/api/v1"

# Verify configuration
hermes config get model
```

### Platform Configuration
```bash
# Telegram
hermes config set --force telegram.allowed_chats "USER_ID"
hermes config set --force TELEGRAM_BOT_TOKEN "***"

# Discord
hermes config set --force DISCORD_HOME_CHANNEL "CHANNEL_ID"
hermes config set --force DISCORD_FREE_RESPONSE_CHANNELS "CHANNEL_ID"
```

### Gateway Operations
```bash
# Check status
hermes gateway status

# Restart (requires external terminal)
taskkill /f /im hermes_gateway.exe
hermes gateway start

# View logs
cat ~/.hermes/logs/gateway.log | tail -50
```

## Session Management

### Problematic Session IDs to Delete (when stuck)
```bash
# Delete specific problematic sessions
hermes sessions delete 20260807_185927_6b4e1271
hermes sessions delete 20260812_210545_fb4e9690

# List current sessions for reference
hermes sessions list
```

## Platform-Specific Setup

### Telegram Bot Setup
1. Start BotFather: `/start` in Telegram
2. Create bot: `/newbot` (name and username)
3. Get token: `/token` (botfather gives you the token)
4. Add token to `~/.hermes/.env`:
   ```
   TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
   ```

### Discord Bot Setup
1. Create bot in Discord Developer Portal
2. Enable Server Members Intent
3. Get bot token from Developer Portal
4. Add token to `~/.hermes/.env`:
   ```
   DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
   ```

## Troubleshooting Workflow

### Step 1: Check Gateway Status
```bash
hermes gateway status
# Look for "✓ telegram connected" and "✓ discord connected"
```

### Step 2: Review Recent Logs
```bash
cat ~/.hermes/logs/gateway.log | grep -E "(ERROR|Provider authentication|Unauthorized|connecting)" | tail -20
```

### Step 3: Common Fixes

**If seeing "Provider authentication failed":**
- Verify `OPENROUTER_API_KEY` exists in `.env`
- Check that `model.provider` is set to `openrouter`
- Ensure `model.base_url` is pointing to correct OpenRouter endpoint

**If seeing "Unauthorized user":**
- Add user ID to `telegram.allowed_chats`
- Approve pairing code if present
- Verify Telegram bot token is correct

**If seeing "no such table":**
- Delete old problematic sessions
- Restart gateway to rebuild database

### Step 4: Verify Fix
```bash
# After making changes, restart and verify
hermes gateway restart

# Test by sending a message to the bot
halo
```

## Provider-Specific Configuration

### OpenRouter Setup (Recommended)
```bash
# Set OpenRouter as default provider
hermes config set model.provider openrouter
hermes config set model.default "openrouter/deepseek/deepseek-chat"
hermes config set model.base_url "https://openrouter.ai/api/v1"

# Ensure API key exists in .env
echo "OPENROUTER_API_KEY=***" >> ~/.hermes/.env
```

### 9Router Setup (Legacy)
```bash
# 9Router is localhost-based service
hermes config set model.provider 9router
hermes config set model.base_url "http://localhost:20128/v1"

# Note: This requires local 9Router service running
```

## Emergency Recovery

### When Everything is Stuck
```bash
# Kill all Hermes processes
pkill -f hermes_gateway
pkill -f hermes.exe

# Clean up problematic sessions (if needed)
hermes sessions prune --older-than 7d

# Start fresh
hermes gateway start
```

### Verify Telegram Connectivity
```bash
# Check Telegram connection status
cat ~/.hermes/logs/gateway.log | grep "telegram connected"

# If not connected, restart
hermes gateway restart
```

## Configuration Best Practices

### .env File Structure
```
# Required variables
TELEGRAM_BOT_TOKEN=***
DISCORD_BOT_TOKEN=***
OPENROUTER_API_KEY=***
ROUTER_API_KEY=***

# Configuration
DEFAULT_MODEL=sub-agent
DISCORD_HOME_CHANNEL=CHANNEL_ID
TELEGRAM_ALLOWED_CHATS="USER_ID"
```

### config.yaml Structure
```yaml
model:
  default: "openrouter/deepseek/deepseek-chat"
  provider: "openrouter"
  base_url: "https://openrouter.ai/api/v1"

tg:
  allowed_chats: "USER_ID"

discord:
  home_channel: "CHANNEL_ID"
```

## Quick Diagnosis Commands

### Provider Issues
```bash
# Check current provider
hermes config get model

# Fix provider issues
hermes config set model.provider openrouter
hermes config set model.base_url "https://openrouter.ai/api/v1"
```

### Platform Connection Issues
```bash
# Check Telegram connection
cat ~/.hermes/logs/gateway.log | grep "telegram" | tail -10

# Check Discord connection  
cat ~/.hermes/logs/gateway.log | grep "discord" | tail -10
```

## Common Error Messages & Solutions

| Error Message | Cause | Solution |
|---|---|---|
| "Provider authentication failed" | Invalid provider config | Switch to OpenRouter |
| "Unauthorized user" | User ID not in allowed list | Add to telegram.allowed_chats |
| "No such table: tasks" | Corrupted session DB | Delete old sessions, restart gateway |
| "Connection timeout" | Port blocked/firewall | Check network, restart gateway |

## Next Steps

1. **Identify the specific error** from gateway logs
2. **Match to error pattern** in this guide
3. **Apply the corresponding fix**
4. **Restart gateway** to apply changes
5. **Test** by sending a message to the bot

Remember: Always restart the gateway after making configuration changes!

## Additional Resources

- [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs)
- [Provider Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/providers-and-models)
- [Troubleshooting Guide](https://hermes-agent.nousresearch.com/docs/user-guide/troubleshooting)