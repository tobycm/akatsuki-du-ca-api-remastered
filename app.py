"""
Custom FastAPI app class
"""

from fastapi import FastAPI
from aiohttp import ClientSession

class CApp(FastAPI):
    """
    Custom App
    """

    http_sess: ClientSession
