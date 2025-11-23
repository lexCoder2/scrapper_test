# 🔥 SOLUTION: Enable LAN Access to Product API

## ✅ Root Cause: Windows Firewall

The API is running correctly and listening on `0.0.0.0:3000`, but Windows Firewall is blocking incoming connections from other devices.

## 🚀 Quick Fix (Choose ONE method)

### Method 1: PowerShell as Administrator ⭐ RECOMMENDED

1. **Right-click on PowerShell** → **Run as Administrator**

2. **Copy and paste this command:**

```powershell
New-NetFirewallRule -DisplayName "Product API (Port 3000)" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow -Profile Private
```

3. **Test it works:**

```powershell
curl http://192.168.6.98:3000/health
```

---

### Method 2: Windows Firewall GUI (Easiest)

1. Press **Windows Key + R**
2. Type: `wf.msc` and press Enter
3. Click **"Inbound Rules"** (left sidebar)
4. Click **"New Rule..."** (right sidebar)
5. Choose **"Port"** → Click **Next**
6. Select **"TCP"** and type port: `3000` → Click **Next**
7. Select **"Allow the connection"** → Click **Next**
8. **Uncheck "Public"**, keep only **"Private"** and **"Domain"** checked → Click **Next**
9. Name: `Product API Port 3000` → Click **Finish**

---

### Method 3: Command Prompt as Administrator

1. **Right-click Command Prompt** → **Run as Administrator**
2. **Run:**

```cmd
netsh advfirewall firewall add rule name="Product API Port 3000" dir=in action=allow protocol=TCP localport=3000 profile=private
```

---

## 🧪 Testing from Another Device

After adding the firewall rule:

### From Mobile Phone or Another Computer:

1. **Connect to the same WiFi network**

2. **Open browser and test:**

   ```
   http://192.168.6.98:3000/health
   ```

   ✅ **Should see:** `{"status":"ok","timestamp":"2025-11-19T..."}`

3. **Test the scanner app:**

   ```
   https://192.168.6.98:8443
   ```

   ✅ **Should load** all 13,653 products automatically

---

## ✅ Verification

Run this on your server to confirm everything:

```powershell
# Check firewall rule exists
Get-NetFirewallRule -DisplayName "Product API*" | Select-Object DisplayName, Enabled, Direction, Action

# Check port is listening
netstat -an | findstr ":3000"

# Should see:
#   TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING

# Test from server
curl http://192.168.6.98:3000/health
```

---

## ⚠️ Troubleshooting

### If still not working:

1. **Verify firewall rule is enabled:**

   ```powershell
   Get-NetFirewallRule -DisplayName "Product API*" | Select-Object Enabled
   ```

   Should show: `Enabled : True`

2. **Check Docker container is running:**

   ```powershell
   docker ps | findstr product-api
   ```

3. **Try disabling firewall temporarily to test:**

   - Open Settings → Network & Internet → Windows Firewall
   - Turn off for Private networks (TEMPORARILY)
   - Test from another device
   - Turn firewall back ON
   - If it works, the firewall rule wasn't added correctly

4. **Restart network adapter:**
   ```powershell
   Restart-NetAdapter -Name "Ethernet"
   # or
   Restart-NetAdapter -Name "Wi-Fi"
   ```

---

## 📱 Final Test

From your mobile phone:

1. **Settings → WiFi** → Confirm connected to same network
2. **Browser** → `http://192.168.6.98:3000/health`
3. **If JSON appears** ✅ **SUCCESS!**
4. **Open scanner app** → `https://192.168.6.98:8443`
5. **Check console** → Should say: `✅ Successfully loaded 13653 products from API`

---

## 🎯 Summary

The API configuration is **perfect** - it's listening on `0.0.0.0:3000` which means all network interfaces.

The **only issue** is Windows Firewall blocking incoming connections.

**Adding the firewall rule will fix it immediately!**

Choose any method above and you'll be able to access the API from any device on your LAN. 🚀
