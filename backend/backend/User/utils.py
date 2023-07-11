from json import loads

def reactjs_request_unpack(req):
    post_data = req.POST.copy()

    if not "username" in post_data:
        keys = list(post_data)[0]
        post_data.clear()
        post_data.update(loads(keys))


    return post_data
