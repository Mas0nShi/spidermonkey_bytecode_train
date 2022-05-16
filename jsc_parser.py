# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: jsc_parser.py
@Time: 2022/5/14 23:05
@Desc: It's all about getting better.
"""

from construct import *
from typedefs import JSVERSION, ScriptBits, XDRAtom

MainStruct = Struct(
    "SpidermonkeyVersion" / Union(
        0,
        "magic" / Hex(Int32ul),
        "version" / Computed(0xb973c0de - this.magic),
    ),
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
    "hasSource" / Flag,
    "sourceRetrievable_" / Flag,
    "sourceLength" / Int32ul,  # length_
    "compressedLength" / Int32ul,
    "argumentsNotIncluded" / Flag,
    "Source" / IfThenElse(this.compressedLength, Bytes(this.compressedLength), Bytes(this.sourceLength * 2)),

    "hasSourceMapURL" / Flag,
    "sourceMapURLLen" / If(this.hasSourceMapURL, Int32ul),
    "sourceMapURL_" / If(this.hasSourceMapURL, Bytes(this.sourceMapURLLen)),

    "haveDisplayURL" / Flag,
    "displayURLLen" / If(this.haveDisplayURL, Int32ul),
    "displayURL_" / If(this.haveDisplayURL, Bytes(this.displayURLLen)),

    "haveFilename" / Flag,
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
    # TODO: not implemented.
    # "consts" / Array(this.nconsts, XDRScriptConst),
    # "objects" / Array(this.nobjects, ),
    # "regexps" / Array(this.nregexps, XDRScriptRegExpObject),
    # "trynotes" / Array(this.ntrynotes, JSTryNote),
    # "nblockscopes" / Array(this.nblockscopes, BlockScopeNote),
    # "LazyScript" / If(this.scriptBits.HasLazyScript, XDRRelazificationInfo)
)

if __name__ == '__main__':
    print(MainStruct.parse_file("test/compile.js.jsc"))
    # print(MainStruct.parse_file("test/compile2.js.jsc"))
