# Fix: API Not Accessible from LAN

## 🔍 Problem Identified

The Product API is running in Docker and bound correctly to `0.0.0.0:3000`, but **Windows Firewall** is blocking incoming connections from other devices on the LAN.

## ✅ Current Status

- ✅ Docker container running: `product-api`
- ✅ Port mapping: `0.0.0.0:3000->3000/tcp`
- ✅ API accessible locally: `http://localhost:3000`
- ✅ API accessible via host IP locally: `http://192.168.6.98:3000`
- ❌ API NOT accessible from other LAN devices

## 🔧 Solution: Create Firewall Rule

### Option 1: PowerShell (Run as Administrator)

1. **Right-click PowerShell** and select **"Run as Administrator"**

2. **Run this command:**

```powershell
New-NetFirewallRule -DisplayName "Product API (Port 3000)" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow -Profile Private,Domain
```

3. **Verify the rule:**

```powershell
Get-NetFirewallRule -DisplayName "Product API (Port 3000)"
```

### Option 2: Windows Firewall GUI

1. Press `Win + R` and type: `wf.msc`
2. Click **"Inbound Rules"** in left panel
3. Click **"New Rule..."** in right panel
4. Select **"Port"** → Next
5. Select **"TCP"** and enter port: `3000` → Next
6. Select **"Allow the connection"** → Next
7. Check **"Private"** and **"Domain"** → Next
8. Name: `Product API (Port 3000)` → Finish

### Option 3: Command Prompt (Run as Administrator)

```cmd
netsh advfirewall firewall add rule name="Product API (Port 3000)" dir=in action=allow protocol=TCP localport=3000 profile=private,domain
```

## 🧪 Testing After Firewall Rule

### From Another Device on LAN:

1. **Get your server IP:** `192.168.6.98`

2. **Test with browser:**

   - Open: `http://192.168.6.98:3000/health`
   - Should see: `{"status":"ok","timestamp":"..."}`

3. **Test with curl (if available):**

   ```bash
   curl http://192.168.6.98:3000/health
   ```

4. **Test scanner app:**
   - Open: `https://192.168.6.98:8443`
   - Check browser console for: `"Loaded 13653 products from API"`

### From Your Server (Verify it still works):

```powershell
# Test localhost
curl http://localhost:3000/health

# Test via IP
curl http://192.168.6.98:3000/health

# Test products endpoint
curl http://192.168.6.98:3000/api/stats
```

## 🔐 Security Considerations

### Recommended Firewall Profile Settings:

- ✅ **Private Network** (Home/Work): Allow
- ✅ **Domain Network** (Enterprise): Allow
- ❌ **Public Network** (Coffee shops, etc.): Block

This ensures the API is only accessible on trusted networks.

### Command with all profiles (less secure):

```powershell
New-NetFirewallRule -DisplayName "Product API (Port 3000)" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow -Profile Any
```

## 📋 Complete Firewall Rules Needed

For full functionality, ensure these ports are open:

| Port  | Service             | Rule Name                    | Required    |
| ----- | ------------------- | ---------------------------- | ----------- |
| 3000  | Product API         | "Product API (Port 3000)"    | ✅ YES      |
| 8443  | Scanner App (HTTPS) | May already exist            | Check       |
| 27017 | MongoDB             | Not needed (Docker internal) | ❌ NO       |
| 8081  | Mongo Express       | Optional for admin UI        | ⚠️ Optional |

## 🔍 Troubleshooting

### Check if firewall rule exists:

```powershell
Get-NetFirewallRule -DisplayName "Product API (Port 3000)"
```

### Check if port is listening:

```powershell
netstat -an | Select-String "3000"
```

Expected output:

```
TCP    0.0.0.0:3000          0.0.0.0:0              LISTENING
TCP    [::]:3000             [::]:0                 LISTENING
```

### Test from server to itself:

```powershell
Test-NetConnection -ComputerName 192.168.6.98 -Port 3000
```

Expected: `TcpTestSucceeded : True`

### Check Docker logs:

```powershell
docker logs product-api
```

### Restart Docker container (if needed):

```powershell
docker restart product-api
```

## 🚀 Quick Fix Commands (Run as Admin)

```powershell
# Add firewall rule
New-NetFirewallRule -DisplayName "Product API (Port 3000)" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow -Profile Private,Domain

# Verify rule
Get-NetFirewallRule -DisplayName "Product API (Port 3000)" | Select-Object DisplayName, Enabled, Direction, Action

# Test connection
Test-NetConnection -ComputerName 192.168.6.98 -Port 3000
```

## 📱 After Fixing: Test from Mobile

1. Connect mobile device to same WiFi
2. Open browser on mobile
3. Navigate to: `http://192.168.6.98:3000/health`
4. Should see JSON response with status "ok"
5. Open scanner app: `https://192.168.6.98:8443`
6. Check that products load (13,653 products)

## ⚠️ Common Issues

### Issue 1: Still can't connect from other devices

- **Solution**: Restart your computer to ensure firewall rules are applied
- **Or**: Disable/Enable firewall temporarily to test

### Issue 2: Works on some devices but not others

- **Solution**: Check if other devices are on the same network segment
- **Check**: Some routers have AP isolation enabled (guest networks)

### Issue 3: Connection refused

- **Solution**: Verify Docker container is running:
  ```powershell
  docker ps | Select-String product-api
  ```

### Issue 4: Timeout instead of refused

- **Solution**: This usually means firewall is blocking, apply the rule

## ✅ Verification Checklist

After creating the firewall rule:

- [ ] Firewall rule created and enabled
- [ ] Docker container running (`docker ps`)
- [ ] Port listening on 0.0.0.0:3000 (`netstat -an | Select-String 3000`)
- [ ] API accessible from server browser (`http://192.168.6.98:3000/health`)
- [ ] API accessible from another device on LAN
- [ ] Scanner app loads products from other device
- [ ] No errors in Docker logs (`docker logs product-api`)

## 🎯 Expected Results

Once firewall rule is added:

```
✅ From server:
   http://localhost:3000/health → 200 OK
   http://192.168.6.98:3000/health → 200 OK

✅ From other device on LAN:
   http://192.168.6.98:3000/health → 200 OK
   http://192.168.6.98:3000/api/stats → Shows 13,653 products

✅ Scanner app:
   https://192.168.6.98:8443 → Loads all products
   Console: "✅ Successfully loaded 13653 products from API"
```

## 📞 Next Steps

1. **Open PowerShell as Administrator**
2. **Run the firewall command**
3. **Test from another device**
4. **Report back if it works!**

If you still have issues after adding the firewall rule, we can check:

- Router settings (AP isolation)
- Network adapter settings
- Docker network configuration
- Alternative port (if 3000 conflicts)
