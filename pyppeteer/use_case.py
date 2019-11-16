# coding:utf8
import re
import asyncio

from pyppeteer import launcher

# hook  禁用 防止监测webdriver
launcher.AUTOMATION_ARGS.remove("--enable-automation")

from pyppeteer import launch

from pyppeteer.network_manager import Request, Response
from pyppeteer.dialog import Dialog


launch_args = {
    "headless": False,
    "args": [
        "--start-maximized",
        "--no-sandbox",
        "--disable-infobars",
        "--ignore-certificate-errors",
        "--log-level=3",
        "--enable-extensions",
        "--window-size=1920,1080",
        "--proxy-server=http://localhost:1080",
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    ],
}


async def modify_url(request: Request):
    """
        # 启用拦截器
        await page.setRequestInterception(True)
        page.on("request", use_proxy_base)
    :param request:
    :return:
    """
    if request.url == "https://www.baidu.com/":
        await request.continue_({"url": "https://www.baidu.com/s?wd=ip&ie=utf-8"})
    else:
        await request.continue_()


async def get_content(response: Response):
    """
        # 注意这里不需要设置 page.setRequestInterception(True)
        page.on("response", get_content)
    :param response:
    :return:
    """
    if response.url == "https://www.baidu.com/":
        content = await response.text()
        title = re.search(b"<title>(.*?)</title>", content)
        print(title.group(1))


async def handle_dialog(dialog: Dialog):
    """
        page.on("dialog", get_content)
    :param dialog:
    :return:
    """
    await dialog.dismiss()


import aiohttp

aiohttp_session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

proxy = "http://127.0.0.1:1080"


async def use_proxy_base(request: Request):
    """
        # 启用拦截器
        await page.setRequestInterception(True)
        page.on("request", use_proxy_base)
    :param request:
    :return:
    """
    # 构造请求并添加代理
    req = {
        "headers": request.headers,
        "data": request.postData,
        "proxy": proxy,  # 使用全局变量 则可随意切换
        "timeout": 5,
        "ssl": False,
    }
    try:
        # 使用第三方库获取响应
        async with aiohttp_session.request(
            method=request.method, url=request.url, **req
        ) as response:
            body = await response.read()
    except Exception as e:
        await request.abort()
        return

    # 数据返回给浏览器
    resp = {"body": body, "headers": response.headers, "status": response.status}
    await request.respond(resp)
    return


# 静态资源缓存
static_cache = {}


async def use_proxy_and_cache(request: Request):
    """
        # 启用拦截器
        await page.setRequestInterception(True)
        page.on("request", use_proxy_base)
    :param request:
    :return:
    """
    global static_cache
    if request.url not in static_cache:
        # 构造请求并添加代理
        req = {
            "headers": request.headers,
            "data": request.postData,
            "proxy": proxy,  # 使用全局变量 则可随意切换
            "timeout": 5,
            "ssl": False,
        }
        try:
            # 使用第三方库获取响应
            async with aiohttp_session.request(
                method=request.method, url=request.url, **req
            ) as response:
                body = await response.read()
        except Exception as e:
            await request.abort()
            return

        # 数据返回给浏览器
        resp = {"body": body, "headers": response.headers, "status": response.status}
        # 判断数据类型 如果是静态文件则缓存起来
        content_type = response.headers.get("Content-Type")
        if content_type and ("javascript" in content_type or "/css" in content_type):
            static_cache[request.url] = resp
    else:
        resp = static_cache[request.url]

    await request.respond(resp)
    return


async def pass_webdriver(request: Request):
    """
        # 启用拦截器
        await page.setRequestInterception(True)
        page.on("request", use_proxy_base)
    :param request:
    :return:
    """
    # 构造请求并添加代理
    req = {
        "headers": request.headers,
        "data": request.postData,
        "proxy": proxy,  # 使用全局变量 则可随意切换
        "timeout": 5,
        "ssl": False,
    }
    try:
        # 使用第三方库获取响应
        async with aiohttp_session.request(
            method=request.method, url=request.url, **req
        ) as response:
            body = await response.read()
    except Exception as e:
        await request.abort()
        return

    if request.url == "https://www.baidu.com/":
        with open("pass_webdriver.js") as f:
            js = f.read()
        # 在html源码头部添加js代码 修改navigator属性
        body = body.replace(b"<title>", b"<script>%s</script><title>" % js.encode())

    # 数据返回给浏览器
    resp = {"body": body, "headers": response.headers, "status": response.status}
    await request.respond(resp)
    return


async def interception_test():
    # 启动浏览器
    browser = await launch(**launch_args)
    # 新建标签页
    page = await browser.newPage()
    # 设置页面打开超时时间
    page.setDefaultNavigationTimeout(10 * 1000)
    # 设置窗口大小
    await page.setViewport({"width": 1920, "height": 1040})

    # 设置拦截器
    # 1. 修改请求的url
    if 0:
        # 启用拦截器
        await page.setRequestInterception(True)
        page.on("request", modify_url)
    # 2. 获取响应内容
    if 0:
        # 注意这里不需要设置 page.setRequestInterception(True)
        page.on("response", get_content)
    # 3. 使用代理
    if 0:
        # 启用拦截器
        await page.setRequestInterception(True)
        # page.on("request", use_proxy_base)
        # page.on("request", use_proxy_and_cache)
        page.on("request", pass_webdriver)

    await page.goto("https://www.baidu.com")

    await asyncio.sleep(10)

    # 关闭浏览器
    await page.close()
    await browser.close()
    return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(interception_test())
