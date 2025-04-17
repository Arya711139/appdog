import asyncio

import appdog.petstore  # type: ignore


async def main() -> None:
    async with appdog.petstore.client as client:
        pets = await client.get_pet_find_by_status(status='available')
        print(pets)


if __name__ == '__main__':
    asyncio.run(main())
