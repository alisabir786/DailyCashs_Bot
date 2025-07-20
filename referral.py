# referral.py

import config

def add_referral(new_user_id, referrer_id):
    if new_user_id == referrer_id:
        return  # Self-referral বাদ

    if referrer_id not in config.USERS:
        return  # রেফারার সিস্টেমে না থাকলে কিছু না করো

    if new_user_id in config.USERS[referrer_id]["referrals"]:
        return  # ডুপ্লিকেট রেফার না

    config.USERS[referrer_id]["referrals"].append(new_user_id)
    config.USERS[referrer_id]["coins"] += config.REFER_REWARD
