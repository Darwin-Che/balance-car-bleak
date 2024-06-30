from bleak import BleakScanner, BleakClient
import asyncio
from pprint import pprint
import aioconsole

device = None

async def find_device():
    global device
    devices = await BleakScanner.discover(10, return_adv=True)
    for (d, adv) in devices.values():
        print(d)
        print(adv)
        if d.name == 'Balance-car':
            device = d

async def main():
    await find_device()
    pprint("==============")
    pprint("[Found Device]")
    pprint(device)

    if device == None:
        return

    pprint("==============")
    async with BleakClient(device) as client:
        for charac in client.services.characteristics.values():
            pprint(charac)
            pprint(charac.uuid)
            pprint(charac.description)

        def callback(sender, byte_array):
            val = int.from_bytes(byte_array, byteorder='little')
            print(f"{sender}: Tick = {val}")

        await client.start_notify(11, callback)

        line = await aioconsole.ainput('Is this your line? ')
    

asyncio.run(main())