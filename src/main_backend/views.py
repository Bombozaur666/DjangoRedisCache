import asyncio
import json
import httpx
import redis
import os
from django.http import JsonResponse
from django.utils.decorators import classonlymethod
from django.views import View
from django.core.cache import cache



class Ping(View):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, *args, **kwargs):
        if self.request.body.decode('utf-8'):
            body_unicode = self.request.body.decode('utf-8')
            body = json.loads(body_unicode)
            if 'url' in body:
                url = body['url']
                mem = await cache.aget(url)
                if mem:
                    return JsonResponse({"response": mem}, status=200)
                else:
                    re = redis.Redis(host='cache', db=0)
                    channels = re.pubsub_channels()
                    if url in channels:
                        conn = re.pubsub(ignore_subscribe_messages=True)
                        conn.subscribe(url)
                        conn.listen()
                        mem = await cache.aget(url)
                        return JsonResponse({"response": mem}, status=200)
                    else:
                        try:
                            async with httpx.AsyncClient() as client:
                                response = await client.get(url)
                        except httpx.RequestError as erro:
                            return JsonResponse({"error": f"An error occurred while requesting {erro.request.url!r}."},
                                                status=400)
                        await cache.aset(url, response.text, os.environ['CACHE_TTL'])
                        re.publish(url, 'START')
                        return JsonResponse({"response": response.text}, status=200)
        return JsonResponse({"error": "Please give url"}, status=400)
