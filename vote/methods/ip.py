def get_client_ip(cls, request):
    if not request or not request.META:
        # METAが含まれていない場合は取得できない
        return None
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = None
    if xff:
        # 転送要素がある場合は転送経路の先頭を設定
        ip = xff.split(",")[0]
    else:
        # 通常のIPアドレス
        ip = request.META.get("REMOTE_ADDR")
    return ip