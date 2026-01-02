# Silicon Labs Wi-SUN FAN – Guidelines to Reduce Node Joining Time

This document summarizes **Silicon Labs–specific best practices** to minimize **Wi-SUN FAN node joining time** in private or internal deployments.

---

## 1. Limit the Allowed Channel List (Highest Impact)

Most join time is spent scanning channels.

**Guidelines**
- Restrict the **Allowed Channel List** to **4–8 channels**
- Keep **FHSS enabled** (required by Wi-SUN), but with fewer channels
- Select channels based on RF survey results

**Benefit**
- Reduces join time from minutes to seconds

---

## 2. Fix PHY Mode and Channel Plan

Avoid PHY auto-detection during join.

**Guidelines**
- Fix:
  - Regulatory Domain (ETSI / FCC / ARIB)
  - Channel Plan
  - PHY Mode (e.g. FSK 50 kbps)
- Disable PHY auto-selection

**Benefit**
- Prevents multiple discovery cycles

---

## 3. Fix the Wi-SUN Network Name (Recommended)

Instead of relying on PAN ID discovery:

**Guidelines**
- Configure a fixed **Network Name**
- Nodes join only PANs advertising this name

**Benefit**
- Fully Wi-SUN compliant
- Significantly reduces discovery time

---

## 4. Fix PAN ID (Optional)

For private, non-roaming deployments only.

**Guidelines**
- Configure a fixed PAN ID on both Border Router and nodes
- Nodes skip PAN selection entirely

**Warning**
- Not suitable for roaming or public networks

---

## 5. Border Router Join-Window Optimization

Tune the Border Router during commissioning.

**Guidelines**
- Increase PAN Advertisement rate
- Reduce advertisement jitter
- Avoid frequent BR restarts
- Use a dedicated commissioning mode if supported

**Benefit**
- Faster node discovery and association

---

## 6. Optimize Security Configuration

Authentication can dominate join time.

**Guidelines**
- Prefer **PSK-based authentication** if allowed
- If using certificates:
  - Pre-install trust anchors
  - Avoid runtime certificate downloads
  - Minimize EAP retry timers (within stack limits)

**Benefit**
- Saves several seconds per join

---

## 7. Enable Fast Rejoin (Critical for Reliability)

Allow nodes to reuse previous network information.

**Guidelines**
- Store:
  - Last PAN ID
  - Channel set
  - Border Router address
- Attempt direct rejoin before full discovery

**Benefit**
- Rejoin time < 2–3 seconds

---

## 8. RPL and Routing Optimization

Reduce time to become operational after join.

**Guidelines**
- Reduce initial RPL Trickle timers
- Enable parent caching
- Use leaf mode for non-routing nodes

---

## Recommended Minimal Configuration

Best balance of speed and compliance:

- Fixed Network Name
- Fixed PHY mode and channel plan
- 4–8 allowed channels
- PAN ID fixed only if strictly necessary

---

## Typical Results (Silicon Labs)

| Scenario      | Join Time |
|--------------|-----------|
| Cold join    | 5–10 s    |
| Fast rejoin  | 1–3 s     |

---

**Applies to:** Silicon Labs Wi-SUN FAN (EFR32 series)  
**Use case:** Private / internal Wi-SUN networks
