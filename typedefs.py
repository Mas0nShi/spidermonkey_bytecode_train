# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: typedefs.py
@Time: 2022/5/14 23:20
@Desc: It's all about getting better.
"""
from construct import *

JSVERSION = Enum(
    Int32ul,
    JSVERSION_ECMA_3=148,
    JSVERSION_1_6=160,
    JSVERSION_1_7=170,
    JSVERSION_1_8=180,
    JSVERSION_ECMA_5=185,
    JSVERSION_DEFAULT=0,
    JSVERSION_UNKNOWN=-1,
    JSVERSION_LATEST=185
)

ConstTag = Enum(
    Int32ul,
    SCRIPT_INT=0,
    SCRIPT_DOUBLE=1,
    SCRIPT_ATOM=2,
    SCRIPT_TRUE=3,
    SCRIPT_FALSE=4,
    SCRIPT_NULL=5,
    SCRIPT_OBJECT=6,
    SCRIPT_VOID=7,
    SCRIPT_HOLE=8
)

# The GC allocation kinds.
AllocKind = Enum(
    Int32ul,
    FINALIZE_OBJECT0=0,
    FINALIZE_OBJECT0_BACKGROUND=1,
    FINALIZE_OBJECT2=2,
    FINALIZE_OBJECT2_BACKGROUND=3,
    FINALIZE_OBJECT4=4,
    FINALIZE_OBJECT4_BACKGROUND=5,
    FINALIZE_OBJECT8=6,
    FINALIZE_OBJECT8_BACKGROUND=7,
    FINALIZE_OBJECT12=8,
    FINALIZE_OBJECT12_BACKGROUND=9,
    FINALIZE_OBJECT16=10,
    FINALIZE_OBJECT16_BACKGROUND=11,
    FINALIZE_OBJECT_LAST=11,
    FINALIZE_SCRIPT=12,
    FINALIZE_LAZY_SCRIPT=13,
    FINALIZE_SHAPE=14,
    FINALIZE_BASE_SHAPE=15,
    FINALIZE_TYPE_OBJECT=16,
    FINALIZE_FAT_INLINE_STRING=17,
    FINALIZE_STRING=18,
    FINALIZE_EXTERNAL_STRING=19,
    FINALIZE_SYMBOL=20,
    FINALIZE_JITCODE=21,
    FINALIZE_LAST=21
)

ScriptBits = BitStruct(
    "NoScriptRval" / Bit,
    "SavedCallerFun" / Bit,
    "Strict" / Bit,
    "ContainsDynamicNameAccess" / Bit,
    "FunHasExtensibleScope" / Bit,
    "FunNeedsDeclEnvObject" / Bit,
    "FunHasAnyAliasedFormal" / Bit,
    "ArgumentsHasVarBinding" / Bit,
    "NeedsArgsObj" / Bit,
    "IsGeneratorExp" / Bit,
    "IsLegacyGenerator" / Bit,
    "IsStarGenerator" / Bit,
    "OwnSource" / Bit,
    "ExplicitUseStrict" / Bit,
    "SelfHosted" / Bit,
    "IsCompileAndGo" / Bit,
    "HasSingleton" / Bit,
    "TreatAsRunOnce" / Bit,
    "HasLazyScript" / Bit,
    Padding(13),  # 32 - 19
)

XDRAtom = Struct(
    "lengthAndEncoding" / Int32ul,
    "nogc" / IfThenElse(this.lengthAndEncoding & 1, Bytes(this.lengthAndEncoding >> 1), Bytes((this.lengthAndEncoding >> 1) * 2))
)

DoublePun = Union(None,
                  "d" / Double,
                  "u" / Int64ul,
                  )

JSID_TYPE_STRING = 0x0
JSID_TYPE_INT = 0x1


# XDRObjectLiteral = Struct(
#     "isArray" / Int32ul,
#     "length" / IfThenElse(this.isArray, Int32ul, AllocKind),
#     "capacity" / Int32ul,  # Number of allocated slots.
#     "initializedLength" / Int32ul,  # initialized: Number of initialized elements.
#     "tmpValue" / this.XDRScriptConst,  # Recursively copy dense elements.
#     "nslot" / Int32ul,
#     "slot" / Array(this.nslot, Struct(
#         "idType" / Int32ul,
#         "id" / Switch(this.idType, {
#             JSID_TYPE_STRING: "atom" / XDRAtom,
#             JSID_TYPE_INT: "indexVal" / Int32ul,
#         }),
#         "tmpValue" / this.XDRScriptConst,
#     ))
# )


#
# XDRScriptConst = Struct(
#     "tag" / ConstTag,
#     "value" / Switch(
#         this.tag,
#         {
#             "SCRIPT_INT": Int32ul,
#             "SCRIPT_DOUBLE": DoublePun,
#             "SCRIPT_ATOM": XDRAtom,
#             "SCRIPT_TRUE": None,
#             "SCRIPT_FALSE": None,
#             "SCRIPT_NULL": None,
#             "SCRIPT_OBJECT": Struct(
#                 "isArray" / Int32ul,
#                 "length" / IfThenElse(this.isArray, Int32ul, AllocKind),
#                 "capacity" / Int32ul,  # Number of allocated slots.
#                 "initializedLength" / Int32ul,  # initialized: Number of initialized elements.
#                 "tmpValue" / XDRScriptConst,  # Recursively copy dense elements.
#                 "nslot" / Int32ul,
#                 "slot" / Array(this.nslot, Struct(
#                     "idType" / Int32ul,
#                     "id" / Switch(this.idType, {
#                         JSID_TYPE_STRING: "atom" / XDRAtom,
#                         JSID_TYPE_INT: "indexVal" / Int32ul,
#                     }),
#                     "tmpValue" / this.XDRScriptConst,
#                 ))
#             ),
#             "SCRIPT_VOID": None,
#             "SCRIPT_HOLE": None,
#         }
#     )
#
# )
