var plugins = [
    {
        0: {
            "description": "Portable Document Format",
            "enabledPlugin": {},
            "suffixes": "pdf",
            "type": "application/x-google-chrome-pdf",
        },
        "description": "Portable Document Format",
        "filename": "internal-pdf-viewer",
        "length": 1,
        "name": "Chrome PDF Plugin",
    },
    {
        0: {
            "description": "",
            "enabledPlugin": {},
            "suffixes": "pdf",
            "type": "application/pdf",
        },
        "description": "",
        "filename": "mhjfbmdgcfjbbpaeojofohoefgiehjai",
        "length": 1,
        "name": "Chrome PDF Viewer",
    },
    {
        0: {
            "description": "Native Client Executable",
            "enabledPlugin": {},
            "suffixes": "",
            "type": "application/x-pnacl",
        },
        1: {
            "description": "Portable Native Client Executable",
            "enabledPlugin": {},
            "suffixes": "",
            "type": "application/x-nacl",
        },
        "description": "",
        "filename": "internal-nacl-plugin",
        "length": 2,
        "name": "Native Client",
    }
]


var dd = {
    "webdriver": undefined,
    "plugins": plugins,
    "languages": ['zh-CN', 'zh', 'en'],
    "language": "zh-CN",
    "platform": "Win32",
};

for (var name in window.navigator) {
    if (name in dd) {
        Object.defineProperty(window.navigator, name, {
            value: dd[name],
        })
    }
}