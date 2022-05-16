# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: jsc_parser.py
@Time: 2022/5/14 23:05
@Desc: It's all about getting better.
"""

from construct import *
from typedefs import JSVERSION, ScriptBits, XDRAtom


if __name__ == '__main__':
    jsc_bytecode = open("test/compile.js.jsc", "rb").read()
    # jsc_bytecode = open(r"\\wsl.localhost\Ubuntu-20.04\home\mas0n\cocos2d-jsc-decompiler\js\src\build-linux\js\src\decjsc\test\compile2.js.jsc", "rb").read()

    st = Struct(
        "spidermonkey version" / Hex(Int32ul),
        "numArgs" / Int16ul,
        "numBlockScoped" / Int16ul,
        "numVars" / Int32ul,
        "length" / Int32ul,  # length of code vector
        "prologLength" / Int32ul,  # offset of main entry point from code, after predef'ing prolog
        "js version" / JSVERSION,  # Run-time version
        "natoms" / Int32ul,  # length of atoms array
        "nsrcnotes" / Int32ul,
        "nconsts" / Int32ul,
        "nobjects" / Int32ul,
        "nregexps" / Int32ul,
        "ntrynotes" / Int32ul,
        "nblockscopes" / Int32ul,
        "nTypeSets" / Int32ul,
        "funLength" / Int32ul,
        "scriptBits" / ScriptBits,
        "hasSource" / Int8ul,
        "sourceRetrievable_" / Int8ul,
        "sourceLength" / Int32ul,  # length_
        "compressedLength" / Int32ul,
        "byteLen" / IfThenElse(this.compressedLength, Bytes(this.compressedLength), Bytes(this.sourceLength * 2 + 1)),

        "hasSourceMapURL" / Int8ul,
        "sourceMapURLLen" / If(this.hasSourceMapURL, Int32ul),
        "sourceMapURL_" / If(this.hasSourceMapURL, Bytes(this.sourceMapURLLen)),

        "haveDisplayURL" / Int8ul,
        "displayURLLen" / If(this.haveDisplayURL, Int32ul),
        "displayURL_" / If(this.haveDisplayURL, Bytes(this.displayURLLen)),

        "haveFilename" / Int8ul,
        "Filename" / If(this.haveFilename, CString('utf-8')),
        "sourceStart_" / Int32ul,
        "sourceEnd_" / Int32ul,
        "lineno" / Int32ul,
        "column" / Int32ul,
        "nslots" / Int32ul,
        "staticLevel" / Int32ul,
        "code" / Bytes(this.length),
        "code + length" / Bytes(this.nsrcnotes),
        "atoms" / Array(this.natoms, XDRAtom),
        # "vector" / Array(this.nconsts, XDRScriptConst)

    )

    print(st.parse(jsc_bytecode))
