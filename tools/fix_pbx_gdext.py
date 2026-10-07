#!/usr/bin/env python3
"""Fill the GDExtension-related template placeholders left unsubstituted by Godot's
headless iOS export ($additional_pbx_files etc.) with entries for the spine/fmod libs.

Without this the generated project.pbxproj is an invalid plist (literal `$` keys)
and xcodebuild reports "project is damaged ... parse error".
Usage: fix_pbx_gdext.py <path/to/project.pbxproj>
"""
import sys

p = sys.argv[1]
t = open(p, encoding="utf-8").read()

if "$additional_pbx_files" not in t:
    print("placeholders already substituted, nothing to do")
    sys.exit(0)

entries = """		F0DA00000000000000000001 /* libfmod_iphoneos.a in Frameworks */ = {isa = PBXBuildFile; fileRef = F0DA00000000000000000003; };
		F0DA00000000000000000002 /* libfmodstudio_iphoneos.a in Frameworks */ = {isa = PBXBuildFile; fileRef = F0DA00000000000000000004; };
		F0DA00000000000000000005 /* libspine_godot.ios.template_release.framework in Embed Frameworks */ = {isa = PBXBuildFile; fileRef = F0DA00000000000000000007; settings = {ATTRIBUTES = (CodeSignOnCopy, ); }; };
		F0DA00000000000000000006 /* libGodotFmod.ios.template_release.xcframework in Embed Frameworks */ = {isa = PBXBuildFile; fileRef = F0DA00000000000000000008; settings = {ATTRIBUTES = (CodeSignOnCopy, ); }; };
		F0DA00000000000000000003 /* libfmod_iphoneos.a */ = {isa = PBXFileReference; lastKnownFileType = archive.ar; name = libfmod_iphoneos.a; path = fmodlibs/libfmod_iphoneos.a; sourceTree = "<group>"; };
		F0DA00000000000000000004 /* libfmodstudio_iphoneos.a */ = {isa = PBXFileReference; lastKnownFileType = archive.ar; name = libfmodstudio_iphoneos.a; path = fmodlibs/libfmodstudio_iphoneos.a; sourceTree = "<group>"; };
		F0DA00000000000000000007 /* libspine_godot.ios.template_release.framework */ = {isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = libspine_godot.ios.template_release.framework; path = ../addons/spine/ios/libspine_godot.ios.template_release.framework; sourceTree = "<group>"; };
		F0DA00000000000000000008 /* libGodotFmod.ios.template_release.xcframework */ = {isa = PBXFileReference; lastKnownFileType = wrapper.xcframework; name = libGodotFmod.ios.template_release.xcframework; path = ../addons/fmod/libs/ios/libGodotFmod.ios.template_release.xcframework; sourceTree = "<group>"; };"""

repl = {
    "\t\t\t\t\t$pbx_embeded_frameworks":
        "\t\t\t\t\tF0DA00000000000000000005 /* libspine_godot.ios.template_release.framework in Embed Frameworks */,\n"
        "\t\t\t\t\tF0DA00000000000000000006 /* libGodotFmod.ios.template_release.xcframework in Embed Frameworks */",
    "\t\t$additional_pbx_files": entries,
    "\t\t\t\t$additional_pbx_frameworks_build":
        "\t\t\t\tF0DA00000000000000000001 /* libfmod_iphoneos.a in Frameworks */,\n"
        "\t\t\t\tF0DA00000000000000000002 /* libfmodstudio_iphoneos.a in Frameworks */",
    "\t\t\t\t$additional_pbx_frameworks_refs":
        "\t\t\t\tF0DA00000000000000000003 /* libfmod_iphoneos.a */,\n"
        "\t\t\t\tF0DA00000000000000000004 /* libfmodstudio_iphoneos.a */",
    "\t\t\t\t$additional_pbx_resources_build": "",
    "\t\t\t\t$additional_pbx_resources_refs": "",
}
for k, v in repl.items():
    if k in t:
        t = t.replace(k, v)
    else:
        print(f"warning: placeholder not found: {k!r}")

leftover = [ln for ln in t.splitlines() if "$additional_pbx" in ln or "$pbx_embeded" in ln]
if leftover:
    print("unsubstituted placeholders remain:", leftover)
    sys.exit(1)

open(p, "w", encoding="utf-8", newline="").write(t)
print("placeholders substituted OK")
