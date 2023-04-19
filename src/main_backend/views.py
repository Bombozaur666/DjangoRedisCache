import asyncio
import json
import httpx
import redis.asyncio as redis
import os
from django.http import JsonResponse
from django.utils.decorators import classonlymethod
from django.views import View
from django.core.cache import cache
from concurrent.futures import ThreadPoolExecutor


class Ping(View):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, *args, **kwargs):
        domain = os.environ['DOMAIN']
        url = f'{domain}{self.request.path}'
        mem = await cache.aget(url)
        if mem:
            return JsonResponse({"response": mem}, status=200)
        else:
            re = await redis.Redis(host='cache', db=0)
            channels = await re.pubsub_channels()
            if url in channels:
                conn = await re.pubsub(ignore_subscribe_messages=True)
                await conn.subscribe(url)
                await conn.listen()
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
                await re.publish(url, 'START')
                return JsonResponse({"response": response.text}, status=200)
