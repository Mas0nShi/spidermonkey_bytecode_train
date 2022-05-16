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

XDRClassKind = Enum(
    Int32ul,
    CK_BlockObject=0,
    CK_WithObject=1,
    CK_JSFunction=2,
    CK_JSObject=3,
)

ScriptBits = BitStruct(
    "NoScriptRval" / Flag,
    "SavedCallerFun" / Flag,
    "Strict" / Flag,
    "ContainsDynamicNameAccess" / Flag,
    "FunHasExtensibleScope" / Flag,
    "FunNeedsDeclEnvObject" / Flag,
    "FunHasAnyAliasedFormal" / Flag,
    "ArgumentsHasVarBinding" / Flag,
    "NeedsArgsObj" / Flag,
    "IsGeneratorExp" / Flag,
    "IsLegacyGenerator" / Flag,
    "IsStarGenerator" / Flag,
    "OwnSource" / Flag,
    "ExplicitUseStrict" / Flag,
    "SelfHosted" / Flag,
    "IsCompileAndGo" / Flag,
    "HasSingleton" / Flag,
    "TreatAsRunOnce" / Flag,
    "HasLazyScript" / Flag,
    Padding(13),  # 32 - 19
)

XDRAtom = Struct(
    "lengthAndEncoding" / Int32ul,
    "nogc" / IfThenElse(this.lengthAndEncoding & 1, Bytes(this.lengthAndEncoding >> 1), Bytes((this.lengthAndEncoding >> 1) * 2))
)

# TODO: not implemented.
XDRStaticBlockObject = Struct(
    "numVariables" / Int32ul,
    "localOffset" / Int32ul,
    "shapes" / Array(this.numVariables, Struct("atom" / XDRAtom, "isAliased" / Int32ul))
)

XDRStaticWithObject = None

FirstWordFlag = Enum(
    Int32ul,
    HasAtom=0x1,
    IsStarGenerator=0x2,
    IsLazy=0x4,
    HasSingletonType=0x8
)

DoublePun = Union(
    0,
    "d" / Double,
    "u" / Int64ul,
)

JSID_TYPE_STRING = 0x0
JSID_TYPE_INT = 0x1


# TODO: not implemented.
XDRLazyScript = Struct()
XDRScript = Struct()
XDRInterpretedFunction = Struct(
    "firstword" / Int32ul,
    "Atom" / If(this.firstword & FirstWordFlag.HasAtom, XDRAtom),
    "flagsword" / Int32ul,
    "Script" / IfThenElse(this.firstword & FirstWordFlag.IsLazy, XDRLazyScript, XDRScript),
)

# TODO: not implemented.
# TODO: XDRObjectLiteral and XDRScriptConst refer to each other.
XDRObjectLiteral = Struct(
    "isArray" / Int32ul,
    "length" / IfThenElse(this.isArray, Int32ul, AllocKind),
    "capacity" / Int32ul,  # Number of allocated slots.
    "initializedLength" / Int32ul,  # initialized: Number of initialized elements.
    # "tmpValue" / XDRScriptConst,  # Recursively copy dense elements.
    "nslot" / Int32ul,
    "slot" / Array(this.nslot, Struct(
        "idType" / Int32ul,
        "id" / Switch(this.idType, {
            JSID_TYPE_STRING: "atom" / XDRAtom,
            JSID_TYPE_INT: "indexVal" / Int32ul,
        }),
        # "tmpValue" / XDRScriptConst,
    ))
)
# TODO: not implemented.
XDRScriptConst = Struct(
    "tag" / ConstTag,
    "value" / Switch(
        this.tag,
        {
            ConstTag.SCRIPT_INT: Int32ul,
            ConstTag.SCRIPT_DOUBLE: DoublePun,
            ConstTag.SCRIPT_ATOM: XDRAtom,
            ConstTag.SCRIPT_TRUE: None,
            ConstTag.SCRIPT_FALSE: None,
            ConstTag.SCRIPT_NULL: None,
            ConstTag.SCRIPT_OBJECT: XDRObjectLiteral,
            ConstTag.SCRIPT_VOID: None,
            ConstTag.SCRIPT_HOLE: None,
        }
    )
)
