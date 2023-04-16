import asyncio
import json
import httpx
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import classonlymethod
from django.views import View
from django.core.cache import caches, cache


class Ping(View):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, *args, **kwargs):
        body_unicode = self.request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if 'url' in body:
            mem = cache.get(body['url'])
            if mem:
                return JsonResponse({"response": mem}, status=200)
            else:
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(body['url'])
                except httpx.RequestError as erro:
                    return JsonResponse({"error": f"An error occurred while requesting {erro.request.url!r}."}, status=400)
                cache.set(body['url'], response.text, 20)
        else:
            return JsonResponse({"error": "Please give url"}, status=400)
        return JsonResponse({"response": response.text}, status=200)
