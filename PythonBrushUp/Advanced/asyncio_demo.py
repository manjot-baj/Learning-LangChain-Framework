import asyncio


async def fetch_data(
    id, sleep_time
):  # Every async function is a coroutine and returns coroutine object
    print(f"Coroutine {id} starting to fetch data.")
    await asyncio.sleep(sleep_time)
    return {"id": id, "data": f"Sample data from corotine {id}"}


# Coroutine Call
async def main1():
    # here the tasks are not concurrent
    task1 = await fetch_data(1, 3)  # to call coroutine u need await keyword
    print(task1)
    task2 = await fetch_data(2, 1)
    print(task2)
    task3 = await fetch_data(3, 2)
    print(task3)


# create_task function usage
async def main2():
    # task 1 and 2 are concurrent
    task1 = asyncio.create_task(fetch_data(1, 3))  # defining the task
    task2 = asyncio.create_task(fetch_data(2, 1))
    print(await task1)  # await keyword to call the task
    print(await task2)
    # task 3 is running after 1 and 2
    task3 = asyncio.create_task(fetch_data(3, 2))
    print(await task3)


# gather function usage
async def main3():
    # all tasks are concurrent, but gather is not good with exception
    results = await asyncio.gather(fetch_data(1, 3), fetch_data(2, 1), fetch_data(3, 2))
    for result in results:
        print(f"Received result: {result}")


# More Preferable way
# TaskGroup function usage, have built-in error handling
async def main3():
    tasks = []

    async with asyncio.TaskGroup() as tg:  # async with is a asyncronous context manager
        # if any task fails inside the taskGrp then cancel the other tasks
        # auto executes the tasks inside
        for i, sleep_time in enumerate([2, 1, 3], start=1):
            task = tg.create_task(fetch_data(i, sleep_time))
            tasks.append(task)

    results = [task.result() for task in tasks]

    for result in results:
        print(f"Received result: {result}")


# Future  used in lower level lib, not for normal usecase
async def set_future_result(future, value):
    await asyncio.sleep(2)
    # Set the result of the future
    future.set_result(value)
    print(f"Set the future,s result to: {value}")


async def main():
    # Create a future object
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    # Schedule setting the future's result
    asyncio.create_task(set_future_result(future, "Future result is ready"))

    # Wait for the future's result
    result = await future
    print(f"Received the future's result: {result}")


asyncio.run(main())  # Triggers a Event loop for main
