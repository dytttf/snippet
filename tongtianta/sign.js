var encrypt;
var n_513;
var n_309;

!function () {
    var t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        , n = {
        rotl: function (e, t) {
            return e << t | e >>> 32 - t
        },
        rotr: function (e, t) {
            return e << 32 - t | e >>> t
        },
        endian: function (e) {
            if (e.constructor == Number)
                return 16711935 & n.rotl(e, 8) | 4278255360 & n.rotl(e, 24);
            for (var t = 0; t < e.length; t++)
                e[t] = n.endian(e[t]);
            return e
        },
        randomBytes: function (e) {
            for (var t = []; e > 0; e--)
                t.push(Math.floor(256 * Math.random()));
            return t
        },
        bytesToWords: function (e) {
            for (var t = [], n = 0, r = 0; n < e.length; n++,
                r += 8)
                t[r >>> 5] |= e[n] << 24 - r % 32;
            return t
        },
        wordsToBytes: function (e) {
            for (var t = [], n = 0; n < 32 * e.length; n += 8)
                t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
            return t
        },
        bytesToHex: function (e) {
            for (var t = [], n = 0; n < e.length; n++)
                t.push((e[n] >>> 4).toString(16)),
                    t.push((15 & e[n]).toString(16));
            return t.join("")
        },
        hexToBytes: function (e) {
            for (var t = [], n = 0; n < e.length; n += 2)
                t.push(parseInt(e.substr(n, 2), 16));
            return t
        },
        bytesToBase64: function (e) {
            for (var n = [], r = 0; r < e.length; r += 3)
                for (var o = e[r] << 16 | e[r + 1] << 8 | e[r + 2], a = 0; a < 4; a++)
                    8 * r + 6 * a <= 8 * e.length ? n.push(t.charAt(o >>> 6 * (3 - a) & 63)) : n.push("=");
            return n.join("")
        },
        base64ToBytes: function (e) {
            e = e.replace(/[^A-Z0-9+\/]/gi, "");
            for (var n = [], r = 0, o = 0; r < e.length; o = ++r % 4)
                0 != o && n.push((t.indexOf(e.charAt(r - 1)) & Math.pow(2, -2 * o + 8) - 1) << 2 * o | t.indexOf(e.charAt(r)) >>> 6 - 2 * o);
            return n
        }
    };
    n_513 = n
}()

var n = {
    utf8: {
        stringToBytes: function (e) {
            return n.bin.stringToBytes(unescape(encodeURIComponent(e)))
        },
        bytesToString: function (e) {
            return decodeURIComponent(escape(n.bin.bytesToString(e)))
        }
    },
    bin: {
        stringToBytes: function (e) {
            for (var t = [], n = 0; n < e.length; n++)
                t.push(255 & e.charCodeAt(n));
            return t
        },
        bytesToString: function (e) {
            for (var t = [], n = 0; n < e.length; n++)
                t.push(String.fromCharCode(e[n]));
            return t.join("")
        }
    }
};

n_309 = n;

n_310 = function (e) {
    function n(e) {
        return !!e.constructor && "function" == typeof e.constructor.isBuffer && e.constructor.isBuffer(e)
    };

    function r(e) {
        return "function" == typeof e.readFloatLE && "function" == typeof e.slice && n(e.slice(0, 0))
    };

    return null != e && (n(e) || r(e) || !!e._isBuffer)
};


!function () {
    var t = n_513
        , r = n_309.utf8
        , o = n_310
        , a = n_309.bin
        , i = function (e, n) {
        e.constructor == String ? e = n && "binary" === n.encoding ? a.stringToBytes(e) : r.stringToBytes(e) : o(e) ? e = Array.prototype.slice.call(e, 0) : Array.isArray(e) || (e = e.toString());
        for (var s = t.bytesToWords(e), u = 8 * e.length, l = 1732584193, c = -271733879, f = -1732584194, p = 271733878, d = 0; d < s.length; d++)
            s[d] = 16711935 & (s[d] << 8 | s[d] >>> 24) | 4278255360 & (s[d] << 24 | s[d] >>> 8);
        s[u >>> 5] |= 128 << u % 32,
            s[14 + (u + 64 >>> 9 << 4)] = u;
        for (var h = i._ff, m = i._gg, v = i._hh, y = i._ii, d = 0; d < s.length; d += 16) {
            var g = l
                , b = c
                , x = f
                , C = p;
            l = h(l, c, f, p, s[d + 0], 7, -680876936),
                p = h(p, l, c, f, s[d + 1], 12, -389564586),
                f = h(f, p, l, c, s[d + 2], 17, 606105819),
                c = h(c, f, p, l, s[d + 3], 22, -1044525330),
                l = h(l, c, f, p, s[d + 4], 7, -176418897),
                p = h(p, l, c, f, s[d + 5], 12, 1200080426),
                f = h(f, p, l, c, s[d + 6], 17, -1473231341),
                c = h(c, f, p, l, s[d + 7], 22, -45705983),
                l = h(l, c, f, p, s[d + 8], 7, 1770035416),
                p = h(p, l, c, f, s[d + 9], 12, -1958414417),
                f = h(f, p, l, c, s[d + 10], 17, -42063),
                c = h(c, f, p, l, s[d + 11], 22, -1990404162),
                l = h(l, c, f, p, s[d + 12], 7, 1804603682),
                p = h(p, l, c, f, s[d + 13], 12, -40341101),
                f = h(f, p, l, c, s[d + 14], 17, -1502002290),
                c = h(c, f, p, l, s[d + 15], 22, 1236535329),
                l = m(l, c, f, p, s[d + 1], 5, -165796510),
                p = m(p, l, c, f, s[d + 6], 9, -1069501632),
                f = m(f, p, l, c, s[d + 11], 14, 643717713),
                c = m(c, f, p, l, s[d + 0], 20, -373897302),
                l = m(l, c, f, p, s[d + 5], 5, -701558691),
                p = m(p, l, c, f, s[d + 10], 9, 38016083),
                f = m(f, p, l, c, s[d + 15], 14, -660478335),
                c = m(c, f, p, l, s[d + 4], 20, -405537848),
                l = m(l, c, f, p, s[d + 9], 5, 568446438),
                p = m(p, l, c, f, s[d + 14], 9, -1019803690),
                f = m(f, p, l, c, s[d + 3], 14, -187363961),
                c = m(c, f, p, l, s[d + 8], 20, 1163531501),
                l = m(l, c, f, p, s[d + 13], 5, -1444681467),
                p = m(p, l, c, f, s[d + 2], 9, -51403784),
                f = m(f, p, l, c, s[d + 7], 14, 1735328473),
                c = m(c, f, p, l, s[d + 12], 20, -1926607734),
                l = v(l, c, f, p, s[d + 5], 4, -378558),
                p = v(p, l, c, f, s[d + 8], 11, -2022574463),
                f = v(f, p, l, c, s[d + 11], 16, 1839030562),
                c = v(c, f, p, l, s[d + 14], 23, -35309556),
                l = v(l, c, f, p, s[d + 1], 4, -1530992060),
                p = v(p, l, c, f, s[d + 4], 11, 1272893353),
                f = v(f, p, l, c, s[d + 7], 16, -155497632),
                c = v(c, f, p, l, s[d + 10], 23, -1094730640),
                l = v(l, c, f, p, s[d + 13], 4, 681279174),
                p = v(p, l, c, f, s[d + 0], 11, -358537222),
                f = v(f, p, l, c, s[d + 3], 16, -722521979),
                c = v(c, f, p, l, s[d + 6], 23, 76029189),
                l = v(l, c, f, p, s[d + 9], 4, -640364487),
                p = v(p, l, c, f, s[d + 12], 11, -421815835),
                f = v(f, p, l, c, s[d + 15], 16, 530742520),
                c = v(c, f, p, l, s[d + 2], 23, -995338651),
                l = y(l, c, f, p, s[d + 0], 6, -198630844),
                p = y(p, l, c, f, s[d + 7], 10, 1126891415),
                f = y(f, p, l, c, s[d + 14], 15, -1416354905),
                c = y(c, f, p, l, s[d + 5], 21, -57434055),
                l = y(l, c, f, p, s[d + 12], 6, 1700485571),
                p = y(p, l, c, f, s[d + 3], 10, -1894986606),
                f = y(f, p, l, c, s[d + 10], 15, -1051523),
                c = y(c, f, p, l, s[d + 1], 21, -2054922799),
                l = y(l, c, f, p, s[d + 8], 6, 1873313359),
                p = y(p, l, c, f, s[d + 15], 10, -30611744),
                f = y(f, p, l, c, s[d + 6], 15, -1560198380),
                c = y(c, f, p, l, s[d + 13], 21, 1309151649),
                l = y(l, c, f, p, s[d + 4], 6, -145523070),
                p = y(p, l, c, f, s[d + 11], 10, -1120210379),
                f = y(f, p, l, c, s[d + 2], 15, 718787259),
                c = y(c, f, p, l, s[d + 9], 21, -343485551),
                l = l + g >>> 0,
                c = c + b >>> 0,
                f = f + x >>> 0,
                p = p + C >>> 0
        }
        return t.endian([l, c, f, p])
    };
    i._ff = function (e, t, n, r, o, a, i) {
        var s = e + (t & n | ~t & r) + (o >>> 0) + i;
        return (s << a | s >>> 32 - a) + t
    }
        ,
        i._gg = function (e, t, n, r, o, a, i) {
            var s = e + (t & r | n & ~r) + (o >>> 0) + i;
            return (s << a | s >>> 32 - a) + t
        }
        ,
        i._hh = function (e, t, n, r, o, a, i) {
            var s = e + (t ^ n ^ r) + (o >>> 0) + i;
            return (s << a | s >>> 32 - a) + t
        }
        ,
        i._ii = function (e, t, n, r, o, a, i) {
            var s = e + (n ^ (t | ~r)) + (o >>> 0) + i;
            return (s << a | s >>> 32 - a) + t
        }
        ,
        i._blocksize = 16,
        i._digestsize = 16,
        encrypt = function (e, n) {
            if (void 0 === e || null === e)
                throw new Error("Illegal argument " + e);
            var r = t.wordsToBytes(i(e, n));
            return n && n.asBytes ? r : n && n.asString ? a.bytesToString(r) : t.bytesToHex(r)
        }
}()


// console.log(encrypt("17720AxQ1z0YQobGltPnbL3vtVeFQikINC4paDVNG4BToxAC6qyQ1Uwhu3f1XCdJkn1PPsDVWXX79YsYBn9yqki"))