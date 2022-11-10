from utils.common import is_not_null_env

def is_mastodon_enabled():
    return not any(is_not_null_env(p) for p in ['MASTODON_BASE_URL', 'MASTODON_ACCESS_TOKEN'])
