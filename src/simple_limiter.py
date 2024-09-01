import asyncio
import time
from types import TracebackType
from typing import Self

import aiohttp


class Limiter:
    def __init__(
        self,
        max_requests_per_period: int,
        period: int
    ):
        self.max_requests_per_period = max_requests_per_period
        self.period = period

        self._last_time = time.time()
        self._requests_per_period = 0
        self._lock = asyncio.Lock()

    async def _try_to_acquire(self) -> bool:
        current_time = time.time()
        if current_time - self._last_time > self.period:
            self._last_time = current_time
            self._requests_per_period = 0

        if self._requests_per_period < self.max_requests_per_period:
            self._requests_per_period += 1
            return True

        return False

    async def __aenter__(self) -> Self:

        while True:
            async with self._lock:
                acquired = await self._try_to_acquire()

                if acquired:
                    return self

            await asyncio.sleep(0.5)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ):
        pass


async def send_request(limiter: Limiter, index: int) -> None:
    async with limiter:
        async with aiohttp.client.ClientSession() as session:
            async with session.get("https://google.com") as resp:
                print(resp.status, index)


async def main() -> None:
    limiter = Limiter(max_requests_per_period=10, period=10)

    tasks = [send_request(limiter, i) for i in range(30)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
